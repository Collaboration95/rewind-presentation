// Stress / breakpoint runner. Same request, mix, think time and timeout as
// scripts/load/hosted.mjs (origin/dev), read-only (CONFIRMATION_ONLY) mix,
// with extended VU stages, error classification and stop conditions.
// No credentials in results.
import { Buffer } from 'node:buffer';
import { randomBytes, randomUUID } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { setTimeout as sleep } from 'node:timers/promises';
import { performance, monitorEventLoopDelay } from 'node:perf_hooks';

const target = new URL(process.env.TARGET_URL || 'https://d2m6kz76y4kuvm.cloudfront.net');
const levels = (process.env.LEVELS || '100,150,200,300,500,750,1000').split(',').map(Number);
const steadySeconds = Number(process.env.STEADY_SECONDS || 60);
const rampSeconds = Number(process.env.RAMP_SECONDS || 15);
const deadline = Date.parse(process.env.DEADLINE || '2026-10-27T05:00:00Z'); // 13:00 SGT
const output = resolve(process.env.OUTPUT || 'stress/results.json');
const privateFixture = process.env.FIXTURE_FILE;
const fullMix = process.env.MIX === 'full'; // 1-100 VU headline mix: 5% chat-send
const maxVus = Math.max(...levels);
const samples = [];
const setup = [];
const health = [];
const client = [];
let interrupted = false;
let stopReason = null;
process.on('SIGTERM', () => { interrupted = true; stopReason ??= 'SIGTERM'; });
process.on('SIGINT', () => { interrupted = true; stopReason ??= 'SIGINT'; });
let current = null;
let originChecks = {};
const startedAt = new Date().toISOString();
const runId = `load-${Date.now()}`;

function classify(error) {
  if (!error) return 'unknown';
  if (error.name === 'TimeoutError' || error.name === 'AbortError') return 'timeout';
  const code = error.cause?.code || error.code;
  return code ? `socket:${code}` : `client:${error.name}`;
}

async function request(operation, path, actor, body, expected = [200], bucket = samples, contentType = 'application/json') {
  const start = performance.now();
  let status = 0, bytes = 0, data = null, valid = false, cache = null, kind = null;
  try {
    const response = await fetch(new URL(path, target), {
      method: body === undefined ? 'GET' : 'POST',
      headers: {
        ...(actor ? { Authorization: `Bearer ${actor.token}` } : {}),
        ...(body !== undefined ? { 'Content-Type': contentType } : {}),
      },
      body: body === undefined ? undefined : contentType === 'application/json' ? JSON.stringify(body) : body,
      signal: AbortSignal.timeout(15000),
      redirect: 'error',
    });
    status = response.status;
    cache = response.headers.get('x-cache');
    const text = await response.text();
    bytes = Buffer.byteLength(text);
    try { data = JSON.parse(text); } catch { /* Non-JSON responses fail below. */ }
    valid = expected.includes(status) && data !== null && !data.error;
    if (!valid) {
      if (status === 429) kind = `429:${typeof data?.error === 'string' ? data.error : 'unknown'}`;
      else if (status >= 500) kind = `5xx:${status}`;
      else if (expected.includes(status)) kind = 'invalid-body';
      else kind = `http:${status}`;
    }
  } catch (error) {
    kind = classify(error);
  }
  const sample = {
    operation, ms: performance.now() - start, status, ok: valid, bytes, cache, error: kind,
    stage: current?.vus ?? 0, phase: current?.phase ?? 'setup', at: new Date().toISOString(),
  };
  bucket.push(sample);
  return { ok: valid, status, data };
}
async function must(...args) {
  const result = await request(...args);
  if (!result.ok) throw new Error(`Setup failed: ${args[0]} HTTP ${result.status}`);
  return result.data;
}
function summarize(rows, seconds) {
  const times = rows.map((r) => r.ms).sort((a, b) => a - b);
  const percentile = (q) => (times.length ? times[Math.ceil(q * times.length) - 1] : null);
  const errors = rows.filter((r) => !r.ok).length;
  const errorTypes = {};
  for (const r of rows) if (!r.ok) errorTypes[r.error] = (errorTypes[r.error] || 0) + 1;
  const ok = rows.filter((r) => r.ok);
  return {
    requests: rows.length, errors, errorRate: rows.length ? errors / rows.length : null,
    throughputRps: rows.length / seconds, successRps: ok.length / seconds,
    meanMs: rows.length ? times.reduce((a, b) => a + b, 0) / rows.length : null,
    p50Ms: percentile(0.5), p95Ms: percentile(0.95), p99Ms: percentile(0.99), maxMs: times.at(-1) ?? null,
    errorTypes,
  };
}

// Client-side saturation monitor: event-loop delay and process CPU per 5 s.
const loop = monitorEventLoopDelay({ resolution: 10 });
loop.enable();
let lastCpu = process.cpuUsage();
let lastT = performance.now();
let inflight = 0;
const clientTimer = setInterval(() => {
  const cpu = process.cpuUsage(lastCpu);
  const now = performance.now();
  client.push({
    at: new Date().toISOString(), stage: current?.vus ?? 0, phase: current?.phase ?? 'setup',
    cpuPercent: ((cpu.user + cpu.system) / 1000 / (now - lastT)) * 100,
    loopP99Ms: loop.percentile(99) / 1e6, loopMaxMs: loop.max / 1e6, inflight,
    rssMb: process.memoryUsage().rss / 1048576,
  });
  lastCpu = process.cpuUsage(); lastT = now; loop.reset();
}, 5000);

// Health poller every 5 s on a separate bucket.
let healthFails = 0;
let healthStop = false;
async function healthLoop() {
  while (!healthStop) {
    const r = await request('health', '/api/health', null, undefined, [200], health);
    healthFails = r.ok ? 0 : healthFails + 1;
    await sleep(5000);
  }
}

let fixture;
const stages = [];
let workers = [];
let stopping = false;
try {
  originChecks = await must('health', '/api/health', null, undefined, [200], setup);
  if (privateFixture) {
    fixture = JSON.parse(await readFile(privateFixture, 'utf8'));
    if (fixture.target !== target.origin) throw new Error('Fixture origin mismatch');
  } else {
    const actors = [];
    for (let i = 0; i < 3; i++) {
      const username = `${runId}-${i}`;
      const password = randomBytes(24).toString('base64url');
      await must('register', '/api/auth/register', null, { username, password }, [201], setup);
      const login = await must('login', '/api/auth/login', null, { username, password, clientType: 'native' }, [200], setup);
      if (!login.token) throw new Error('Login did not return native session');
      actors.push({ token: login.token });
    }
    const group = await must('create-group', '/api/real/groups', actors[0],
      { name: `Scripted performance ${runId}`, prompt: 'Synthetic load-test moment', maxMembers: 5 }, [201], setup);
    const groupId = group.group.id;
    for (const actor of actors.slice(1)) {
      const invitation = await must('invite', `/api/real/groups/${groupId}/invites`, actors[0], {}, [201], setup);
      await must('join', '/api/real/invites/accept', actor, { code: invitation.invite.code }, [200], setup);
    }
    fixture = { target: target.origin, actors, groupId, cycle: group.cycle };
    if (process.env.SAVE_FIXTURE) await writeFile(process.env.SAVE_FIXTURE, JSON.stringify(fixture), { mode: 0o600 });
  }
  const { actors, groupId } = fixture;
  const mix = ['home','chat','groups','chat','home','archive','budget','chat','groups','capability','home','chat','archive','groups','budget','chat','home','archive','chat','send'];
  let capabilities = 0, capabilityEmpty = 0;
  async function operation(vu, index) {
    const actor = actors[vu % actors.length];
    let kind = mix[(index + vu) % mix.length];
    if (kind === 'send' && !fullMix) kind = 'chat'; // read-only profile (CONFIRMATION_ONLY)
    const groupPath = `/api/real/groups/${groupId}`;
    inflight++;
    try {
      if (kind === 'send')
        await request('chat-send', `/api/realtime/groups/${groupId}/messages`, actor,
          { body: `Synthetic performance ${runId}`, messageId: randomUUID() }, [201]);
      if (kind === 'home') await request('home', groupPath, actor);
      if (kind === 'groups') await request('groups', '/api/real/groups', actor);
      if (kind === 'chat') await request('chat-read', `/api/realtime/groups/${groupId}/messages?limit=30`, actor);
      if (kind === 'budget') await request('contributions', `/api/contributions?groupId=${groupId}&limit=5`, actor);
      if (kind === 'archive' || kind === 'capability') {
        const r = await request(kind === 'archive' ? 'archive' : 'media-capability', `/api/archive?groupId=${groupId}&limit=5`, actor);
        if (kind === 'capability' && r.ok) {
          const entries = [...(r.data.archive?.films || []), ...(r.data.archive?.clips || [])];
          if (entries[0]?.downloadPath) capabilities++; else capabilityEmpty++;
        }
      }
    } finally { inflight--; }
  }
  let active = 0, end = 0;
  async function vuLoop(vu) {
    let index = 0;
    while (!stopping) {
      if (vu < active && performance.now() < end) {
        await operation(vu, index++);
        await sleep(3000 + ((vu * 7919 + index * 1543) % 4001));
      } else await sleep(100);
    }
  }
  workers = Array.from({ length: maxVus }, (_, i) => vuLoop(i));
  const healthTask = healthLoop();
  let previous = 0;
  outer: for (const vus of levels) {
    for (const [phase, seconds] of [['ramp', rampSeconds], ['steady', steadySeconds]]) {
      current = { vus, phase };
      const start = performance.now();
      end = start + seconds * 1000;
      if (phase === 'steady') active = vus;
      let lastCheck = start;
      while (performance.now() < end && !interrupted) {
        if (phase === 'ramp')
          active = Math.max(1, Math.ceil(previous + ((vus - previous) * (performance.now() - start)) / (seconds * 1000)));
        if (Date.now() >= deadline) { stopReason = `deadline 13:00 SGT reached during ${vus} VU ${phase}`; interrupted = true; break; }
        if (healthFails >= 2) { stopReason = `health endpoint failing (2 consecutive) during ${vus} VU ${phase}`; interrupted = true; break; }
        // Rolling 15 s emergency check once per 5 s, after 15 s in the stage.
        const now = performance.now();
        if (now - lastCheck >= 5000 && now - start >= 15000) {
          lastCheck = now;
          const cutoff = Date.now() - 15000;
          const win = samples.filter((s) => s.stage === vus && Date.parse(s.at) >= cutoff);
          if (win.length >= 50) {
            const w = summarize(win, 15);
            if (w.errorRate > 0.1) { stopReason = `rolling error rate ${(w.errorRate * 100).toFixed(1)}% > 10% during ${vus} VU ${phase}`; interrupted = true; break; }
            if (w.p95Ms > 5000) { stopReason = `rolling p95 ${(w.p95Ms / 1000).toFixed(2)} s > 5 s during ${vus} VU ${phase}`; interrupted = true; break; }
          }
        }
        await sleep(100);
      }
      const elapsedSeconds = (performance.now() - start) / 1000;
      stages.push({ vus, phase, elapsedSeconds, complete: !interrupted });
      const s = summarize(samples.filter((r) => r.stage === vus && r.phase === phase), elapsedSeconds);
      console.log(JSON.stringify({ at: new Date().toISOString(), vus, phase, ...s }));
      if (interrupted) break outer;
      if (phase === 'steady') {
        if (s.errorRate > 0.1) { stopReason = `stage error rate ${(s.errorRate * 100).toFixed(1)}% > 10% at ${vus} VUs`; break outer; }
        if (s.p95Ms > 5000) { stopReason = `stage p95 ${(s.p95Ms / 1000).toFixed(2)} s > 5 s at ${vus} VUs`; break outer; }
      }
    }
    previous = vus;
  }
  stopReason ??= 'all stages completed';
  console.log(JSON.stringify({ stopReason }));
  active = 0;
  stopping = true;
  const drainStart = new Date().toISOString();
  current = { vus: -1, phase: 'drain' };
  await Promise.all(workers);
  console.log(JSON.stringify({ drained: true, drainStart, at: new Date().toISOString() }));
  healthStop = true;
  await healthTask;
  fixture = { ...fixture, actors: undefined, media: { uploadAttempts: 0, capabilitiesIssued: capabilities, capabilityEmpty } };
} catch (error) {
  console.error(error.message);
  stopReason ??= `error: ${error.message}`;
  stopping = true; healthStop = true;
  process.exitCode = 1;
} finally {
  clearInterval(clientTimer);
  const summaries = stages.map((stage) => ({
    ...stage, ...summarize(samples.filter((s) => s.stage === stage.vus && s.phase === stage.phase), stage.elapsedSeconds),
  }));
  const report = {
    schemaVersion: 1, kind: 'stress-breakpoint', runId, target: target.origin, startedAt,
    finishedAt: new Date().toISOString(), node: process.version, originChecks,
    profile: { confirmationOnly: !fullMix, mix: fullMix ? 'full (95% reads, 5% chat-send)' : 'read-only (chat-send slot reads chat)', levels, steadySeconds, rampSeconds, thinkTimeMs: [3000, 7000], timeoutMs: 15000,
      stopConditions: 'stage or rolling-15s errors > 10%, p95 > 5 s, 2 consecutive health failures, 13:00 SGT' },
    stopReason,
    fixture: fixture ? { groupId: fixture.groupId, cycle: fixture.cycle, media: fixture.media } : null,
    setup, stages: summaries, health, client, samples,
  };
  await mkdir(dirname(output), { recursive: true });
  await writeFile(output, JSON.stringify(report) + '\n');
  process.exit(process.exitCode ?? 0);
}
