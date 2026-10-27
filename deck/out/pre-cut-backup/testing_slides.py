"""Section 3 (testing): one slide per test type. Facts checked against origin/dev 2390589."""
import json
from pathlib import Path

BADGES = {
    'gate': 'Every PR · blocks merge',
    'main': 'PRs to main · blocks merge',
    'manual': 'Run on demand',
    'deploy': 'Deploy · blocks upload',
    'report': 'Reports findings',
}


def badge(kind, text=None):
    return '<span class="badge ' + kind + '">' + (text or BADGES[kind]) + '</span>'


def ttype(count, countlabel, tool, runs, what, example_file, example_name, catches, quote=True):
    return ('<div class="tt"><div class="tt-left"><div class="tt-count">' + count + '</div>'
            '<div class="tt-countlabel">' + countlabel + '</div><div class="tt-tool">' + tool + '</div>'
            '<div class="tt-badges">' + runs + '</div></div>'
            '<div class="tt-right"><p class="tt-what">' + what + '</p>'
            '<div class="tt-example"><div class="tt-label">Example test</div><code>' + example_file + '</code>'
            '<p class="tt-name' + ('' if quote else ' plain') + '">' + ('“' + example_name + '”' if quote else example_name) + '</p>'
            '<p class="tt-catch"><b>Catches:</b> ' + catches + '</p></div></div></div>')


def add_overview(add, table):
    rows = [
        ['Static checks', 'Prettier · ESLint · tsc · layer rule', '4 checks', badge('gate')],
        ['Frontend unit and component', 'Jest · Testing Library', '1,674', badge('gate')],
        ['Server unit and API', 'node:test · HTTP · SQLite', '1,006', badge('gate')],
        ['Database', 'Same suite on PostgreSQL 17', '989', badge('gate')],
        ['Architecture and repository rules', 'node:test · Python', '131 + 13', badge('gate')],
        ['Deployment fixtures', 'Bash · injected failures', '11 fixtures', badge('gate')],
        ['Browser end-to-end', 'Playwright · Chromium', '41', badge('main')],
        ['Web export and PWA', 'expo export · check-pwa', '10 + 11', badge('main')],
        ['Accessibility', 'axe-core · keyboard', '6', badge('main')],
        ['Real-account journey', 'Playwright · Firefox · HTTPS', '1 long flow', badge('manual')],
        ['Security', 'Suites + six pipeline scans', '13 files + scans', badge('gate', 'Merge · deploy · report')],
        ['Performance and load', 'Node HTTP load runner', '5 stages', badge('manual')],
    ]
    add('s10', 3, 'TESTING', 'Twelve test types each catch a different failure',
        table(['Type', 'Tool', 'Tests', 'When it runs'], rows, 'matrix'),
        22, ['Fast suites block every merge; browser checks join for main; load and the real-account journey run on demand.'],
        'Start at the bottom: static checks.', ['B6'], '',
        'Here is the whole test map: twelve types, each catching a different kind of failure. '
        'The top six run on every pull request and block the merge. Browser, PWA and accessibility checks join for pull requests to main. '
        'The real-account journey and the load test run on demand. One slide on each.')

    add('T1', 3, 'TESTING', 'Static checks reject style, type and layering errors',
        ttype('4', 'checks in a parallel matrix', 'Prettier · ESLint · TypeScript · check-architecture', badge('gate'),
              'Formatting, lint rules and types are checked before any test runs. '
              'The layer rule keeps domain code free of framework imports and keeps device APIs out of routes. '
              '',
              'scripts/check-architecture.mjs',
              'npm run architecture:check · runs in CI and the pre-commit hook',
              'a domain module that imports React, or a route that imports expo-camera.', quote=False),
        10, ['Four static checks run in parallel and block the merge.'], 'Next, the frontend unit tests.', ['B6'], '',
        'Static checks come first: Prettier, ESLint, TypeScript and our own layer rule. '
        'Domain code may not import a framework, and routes may not touch device APIs. They block every merge.')

    add('T2', 3, 'TESTING', 'Component tests check screens and state without a device',
        ttype('1,674', 'Jest tests in 79 files', 'Jest (jest-expo) · React Native Testing Library', badge('gate'),
              'Screens, capture state, stores, the uploader, film playback and the auth client. '
              'Coverage is 89.6% of statements against an enforced 70% floor.',
              'tests/real-account-chat.test.tsx',
              'loads the selected group, sends replies and never adds session credentials to request URLs',
              'a change that leaks the session token into a chat request URL.'),
        14, ['1,674 Jest tests; 89.6% statement coverage against a 70% floor.'], 'Here is one of those tests in detail.', ['B6'], '',
        'The frontend has one thousand six hundred and seventy-four Jest tests. They render screens and drive state without a phone. '
        'Statement coverage is eighty-nine point six percent, with a seventy percent floor enforced in CI. '
        'This chat test fails if a session token ever appears in a request URL.')


def latency_svg(perf):
    st = perf['steadyStagesMeasured']
    X0, X1, Y0, Y1, top = 60, 505, 330, 40, 2.2
    def y(v): return Y0 - (v / top) * (Y0 - Y1)
    def x(i): return X0 + i * (X1 - X0) / (len(st) - 1)
    out = ['<svg viewBox="0 0 580 400" role="img" aria-label="Latency by stage: p50, p95 and p99 against the 2 second target">']
    for v in (0, 0.5, 1.0, 1.5, 2.0):
        out.append(f'<path d="M{X0} {y(v):.1f}H{X1}" stroke="#E1EBE3"/><text x="{X0-10}" y="{y(v)+6:.1f}" text-anchor="end">{v:g}</text>')
    out.append(f'<path d="M{X0} {y(2):.1f}H{X1}" stroke="#A5481B" stroke-width="2.5" stroke-dasharray="8 6"/>'
               f'<text x="{X1}" y="{y(2)-10:.1f}" text-anchor="end" fill="#A5481B" style="fill:#A5481B;font-weight:700">2 s target</text>')
    for key, colour, label in (('p99Ms', '#8FB9A2', 'p99'), ('p95Ms', '#1F6B55', 'p95'), ('p50Ms', '#2B5C86', 'p50')):
        pts = ' '.join(f'{x(i):.1f},{y(r[key]/1000):.1f}' for i, r in enumerate(st))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="{4 if key == "p95Ms" else 3}"/>')
        for i, r in enumerate(st):
            out.append(f'<circle cx="{x(i):.1f}" cy="{y(r[key]/1000):.1f}" r="5" fill="{colour}"/>')
        out.append(f'<text x="{X1+8}" y="{y(st[-1][key]/1000)+6:.1f}" style="fill:{colour};font-weight:700">{label}</text>')
    for i, r in enumerate(st):
        out.append(f'<text x="{x(i):.1f}" y="{Y0+30}" text-anchor="middle">{r["vus"]}</text>')
    out.append(f'<text x="{(X0+X1)/2}" y="{Y0+62}" text-anchor="middle">concurrent users</text></svg>')
    return ''.join(out)


def add_rest(add, table, root):
    add('T3', 3, 'TESTING', 'API tests call real routes on a running server',
        ttype('1,006', 'server tests in 66 files', 'node:test · real HTTP server · SQLite', badge('gate'),
              'Each test starts the server, signs in and calls the real routes: route contracts, sessions, '
              'membership, media integrity, the cycle engine and reminders. Server line coverage is 85.7%.',
              'server/tests/cross-group-access.test.mjs',
              'every exposed protected category denies a member of another group without content',
              'a missing membership check. Another group’s member must get 403 and no content for contributions, clips and Archive.'),
        14, ['1,006 server tests drive real HTTP routes, including privacy denials.'], 'The same suite then runs on PostgreSQL.', ['B6'], '',
        'The server suite has one thousand and six tests. Each starts the real HTTP server and calls real routes. '
        'This privacy test signs in as a member of another group and expects a 403 with no content for every protected resource.')

    add('T4', 3, 'TESTING', 'The server suite runs again on PostgreSQL 17',
        ttype('989', 'pass on PostgreSQL · 17 SQLite-only tests skip', 'node:test · postgres:17-alpine service container', badge('gate'),
              'Local runs use SQLite; hosted dev uses PostgreSQL. Running the same suite on both catches dialect differences. '
              'Migration tests check that a fresh schema equals the upgraded one.',
              'server/tests/migration-baseline.test.mjs',
              'a fresh database gets exactly the schema of the retired chain',
              'schema drift between a new install and an upgraded database.'),
        10, ['The same suite passes 989 tests on PostgreSQL 17.'], 'Repository rules guard the architecture itself.', ['B9'], '',
        'The same suite runs again on PostgreSQL seventeen in a throwaway container: nine hundred and eighty-nine pass. '
        'That catches SQL that works on SQLite but not on the hosted database.')

    add('T5', 3, 'TESTING', 'Repository tests stop the architecture and policies drifting',
        ttype('131', 'root tests · plus 13 Python gate tests', 'node:test · Python unittest', badge('gate'),
              'The layer guard, service-worker cache rules, the change-scope classifier, deployment policy '
              'and Terraform policy are all tested like code.',
              'tests/architecture.test.mjs',
              'architecture guard rejects framework imports in domain and device imports in routes',
              'a broken layer guard. The test plants a bad import in each layer and expects both to be reported.'),
        10, ['Architecture, PWA, classifier and Terraform policies are tested like code.'], 'Deployment scripts get the same treatment.', ['B6'], '',
        'Repository tests check our own rules. The architecture guard is itself tested: we plant a bad import in each layer and expect two violations. '
        'Terraform and deploy policy, such as only deploying a commit that passed Quality, are tested the same way.')

    add('T6', 3, 'TESTING', 'Deployment scripts are tested offline with injected failures',
        ttype('11', 'shell fixtures · no cloud access', 'Bash fixtures · fake tar, chown and health check', badge('gate'),
              'Backup, restore, release bundle and host lifecycle run against fake commands. '
              'Failures are injected at plan, apply, transfer, restore and health.',
              'tests/deploy/restore-atomic.test.sh',
              'Cases: corrupt media · checksum · extraction · permissions · readiness',
              'a restore that half-applies a broken backup. Every case must leave the previous state in place.', quote=False),
        10, ['Eleven cloud-free fixtures inject deployment failures.'], 'Now the browser tests.', ['B5'], '',
        'Deployment scripts are tested offline. Eleven fixtures replace tar, chown and the health check with fakes, then inject failures. '
        'A failed restore must leave the previous state intact.')

    add('T7', 3, 'TESTING', 'Playwright drives the exported app in a real browser',
        ttype('41', 'Playwright tests in 9 specs', 'Playwright · Chromium · iPhone-size viewports', badge('main') + badge('manual', 'Real-account journey · on demand'),
              'Phone-size layout, capture with an injected camera stream, video fallback, film playback and the chat keyboard. '
              'A separate Firefox journey runs owner, invited member and outsider over local HTTPS.',
              'tests/e2e-real-account/real-account.spec.mjs',
              'real owner, invited member, outsider, strict local HTTPS, and automatic next cycle',
              'an outsider who can open the owner’s group. The journey expects a 404.'),
        14, ['41 browser tests join for main; one real-account journey runs on demand.'], 'The exported PWA is checked as installed.', ['B3'], '',
        'Playwright drives the exported web app in Chromium at iPhone sizes: forty-one tests, required for pull requests to main. '
        'A longer Firefox journey uses real accounts: owner, invited member and outsider, through to the next cycle.')

    add('T8', 3, 'TESTING', 'The PWA build is checked the way it will be installed',
        ttype('10 + 11', 'routing tests · service-worker rule tests', 'expo export · check-pwa · Playwright', badge('main') + badge('gate', 'Service-worker rules · every PR'),
              'After export, check-pwa verifies the manifest, service worker, offline page, Apple Home Screen metadata and icons. '
              'Routing tests reload deep routes offline and check cache headers.',
              'tests/pwa.test.mjs',
              'private API/media, invite query navigations and writes never enter the shell cache',
              'a service worker that would cache private media or API answers on a shared phone.'),
        10, ['The exported PWA build, offline shell and cache rules are tested.'], 'Accessibility uses the same browser run.', ['B5'], '',
        'The exported PWA is tested as it will be installed: manifest, service worker, offline page and icons. '
        'A service-worker rule test makes sure private media and API answers never enter the cache.')

    add('T9', 3, 'TESTING', 'Axe and keyboard tests check the main screens for WCAG 2.1 AA',
        ttype('6', 'tests · 4 Axe scans and 2 keyboard tests', '@axe-core/playwright · WCAG 2.0 and 2.1, A and AA', badge('main'),
              'Welcome, sign-in, registration, Home, Settings, Camera, Chat, Archive, the sign-out dialog and the loading state. '
              'Any serious or critical violation fails the test.',
              'tests/responsive/accessibility.spec.ts',
              'sign-out dialog keeps keyboard focus inside, restores its trigger, and has no serious or critical violations',
              'a dialog that lets keyboard focus escape behind it.'),
        10, ['Axe scans and keyboard tests fail on serious or critical violations.'], 'Security is tested at two levels.', ['B6'], '',
        'Accessibility runs in the same browser job. Axe scans the main screens against WCAG 2.1 A and AA, and two keyboard tests check focus. '
        'Serious or critical violations fail the build.')

    sec_left = ('<div class="sec-col"><h2>In the test suites</h2>'
                '<p><b>Access and privacy.</b> 13 server files: cross-group reads, media tokens, Cognito callback failures, account safety.</p>'
                '<p><b>Rate limits.</b> <code>safety-rate-limits.test.mjs</code>: thirty chat messages pass, the next is refused.</p>'
                '<p><b>Patched dependencies.</b> braces and node-forge: the original <code>node-forge</code> accepts a forged signature; our fork rejects it.</p>'
                '<p><b>Scan gates.</b> 13 Python tests prove the IaC and image gates reject expired, wrong or incomplete scans.</p>'
                + badge('gate') + '</div>')
    sec_right = ('<div class="sec-col"><h2>In the pipeline · Section 4</h2>' + table(['Scan', 'Tool', 'Decision'], [
        ['SAST', 'CodeQL', badge('report', 'Reports')],
        ['SCA', 'npm audit', badge('gate', 'Blocks merge')],
        ['Secrets', 'Gitleaks', badge('report', 'Fails its job')],
        ['IaC', 'Trivy config', badge('report', 'Fails its job')],
        ['Images', 'Trivy', badge('deploy', 'Blocks upload')],
        ['DAST', 'ZAP baseline', badge('report', 'Reports')]], 'secscan') + '</div>')
    add('T10', 3, 'TESTING', 'Security is tested in the suites and scanned in the pipeline',
        '<div class="sec-grid">' + sec_left + sec_right + '</div>',
        12, ['Security tests run in the merge gate; six scans run in the pipeline.'], 'Last, performance under load.', ['B12'], '',
        'Security is tested at two levels. Inside the suites: privacy denials, rate limits, our patched dependencies and the scan gates themselves. '
        'In the pipeline: SAST, SCA, secrets, IaC, image and DAST scans. I will show those in the CI/CD section.')

    # Performance methodology and results, from load-test/METHODOLOGY.md and RESULTS.md.
    stages = ''.join(
        f'<rect x="{30+i*104}" y="{200-h}" width="92" height="{h}" rx="4" fill="#1F6B55" opacity="{0.45+i*0.13:.2f}"/>'
        f'<text x="{76+i*104}" y="{190-h}" text-anchor="middle" font-weight="700">{v}</text>'
        for i, (v, h) in enumerate([(1, 12), (10, 40), (25, 72), (50, 112), (100, 160)]))
    stage_svg = ('<svg viewBox="0 0 560 250" role="img" aria-label="Load stages: 1, 10, 25, 50, 100 virtual users">'
                 + stages + '<path d="M22 200H552" stroke="#9DB5A6"/>'
                 '<text x="287" y="236" text-anchor="middle">virtual users · 15 s ramp + 180 s steady each</text></svg>')
    mix = table(['Action', 'Share'], [['Read chat', '30%'], ['Open Home', '20%'], ['List groups · open Archive', '15% each'],
                                      ['Budget · media links', '10% · 5%'], ['Send chat', '5%']], 'mix')
    add('T11', 3, 'TESTING', 'A scripted load test drives the hosted API in five stages',
        '<div class="perf-grid"><div>' + '<div class="figure"><div class="figuretitle">Ramp · 1 → 100 concurrent users</div>' + stage_svg + '</div>'
        + '<p class="perf-rule"><b>Pass rule:</b> every stage p95 &lt; 2 s and errors &lt; 1%.</p></div><div>'
        + '<p class="perf-p"><b>Target.</b> Hosted dev: CloudFront → Node API → PostgreSQL.</p>'
        + '<p class="perf-p"><b>Runner.</b> Node HTTP closed loop, <code>scripts/load/hosted.mjs</code>; manual <code>performance.yml</code> workflow.</p>'
        + '<p class="perf-p"><b>Users.</b> Each virtual user acts, then waits 3–7 s.</p>'
        + mix + '</div></div>',
        14, ['Five stages from 1 to 100 users; pass rule p95 under 2 seconds and under 1% errors.'], 'Here are the results.', ['B11'], '',
        'Performance has its own test. A Node runner drives the hosted API through CloudFront in five stages, from one to one hundred concurrent users. '
        'Each user acts, then waits three to seven seconds. The mix is ninety-five percent reads. Every stage must keep p95 under two seconds and errors under one percent.')

    perf = json.loads((root / 'load-test/results/summary.json').read_text())
    rows = [[str(r['vus']), f"{r['p95Ms']:,.0f}", f"{r['throughputRps']:.2f}", f"{r['errorRate']*100:.0f}%", '<b class="pass">PASS</b>']
            for r in perf['steadyStagesMeasured']]
    add('T12', 3, 'TESTING', '100 concurrent users stay under the 2-second target, error-free',
        '<div class="perf-grid results"><div>' + table(['Users', 'p95 ms', 'req/s', 'Errors', 'Stage'], rows, 'perfres')
        + '<div class="perf-stats"><div><strong>6,038</strong><span>steady requests</span></div><div><strong>0</strong><span>errors</span></div>'
          '<div><strong>1.34 s</strong><span>p95 at 100 users</span></div></div></div>'
        + '<div class="figure"><div class="figuretitle">Latency by stage · seconds</div>' + latency_svg(perf) + '</div></div>',
        12, ['All five stages pass: 6,038 requests, zero errors, p95 1.34 s at 100 users.'], 'Now the pipeline that runs these tests.', ['B11', 'B34', 'B35'], '',
        'All five stages passed: six thousand and thirty-eight requests, zero errors. At one hundred users p95 was one point three four seconds, '
        'with seventeen point eight requests per second. I return to capacity in the system demo. Now, the pipeline that runs all of these tests.')
