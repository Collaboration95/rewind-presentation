"""Final presentation assembly; writes stay in the presentation-prep tree."""
import html
import json
import re
import subprocess


def finalise(slides, root, deck):
    by_id = {s['id']: s for s in slides}
    perf = json.loads((root / 'load-test/results/summary.json').read_text())

    by_id['s7']['script'] = (
        'A scheduler tick can repeat, and an old worker can finish after its lease expires. '
        'We compared polling alone, State or Command object hierarchies, and persisted state with a durable job. '
        'We chose the durable job with lease and generation checks: expensive rendering runs outside the transaction, '
        'then finalisation proves that this worker still owns the current claim. '
        'Storage creates a second design problem: duplicated backend branches would spread through the worker. '
        'Instead we inject the MediaStore Strategy. LocalMediaStore and PrivateS3MediaStore supply the implementations; '
        'the S3 transport Adapter translates the SDK operations. The pattern roles are labelled on the real design elements.'
    )
    by_id['s8']['script'] = (
        '[Show closure here; jump to #B16 for compilation, then #B17 for publication; return to #s9. '
        'All three views share this 57-second allocation.]\n\n'
        'The scheduler finds the ended cycle. One lifecycle transaction closes it, records the frozen inputs and durable film job, '
        'and opens its successor. The worker claims that job and renders outside the transaction. '
        'At finalisation it checks the current lease, generation and ordered input set. '
        'The alternatives explain the safety rule: a repeated tick reuses the retained job, and a stale worker cannot publish. '
        'Publication verifies the stored bytes before exposing the film. After the premiere, archiving verifies them again. '
        'The next schema shows which records preserve these decisions across a restart.'
    )
    by_id['B7']['script'] = (
        'The problem is duplicated storage-specific branches in compilation and media code. '
        'We compared branching in each caller with an injected storage contract. '
        'We chose the MediaStore Strategy so the worker uses one interface. '
        'LocalMediaStore and PrivateS3MediaStore implement that contract, and privateTransport adapts AWS SDK commands. '
        'Hosted runtime selects PrivateS3MediaStore; disk mode has its separate filesystem path.'
    )

    # The complete pipeline film occupies its own section. Supporting diagrams remain
    # addressable in backup instead of adding their old eight minutes to playback.
    for n in range(12, 18):
        s = by_id[f's{n}']
        s.update(id=f'B{n + 14}', kind='back', secs=0)
    for n in (1, 2):
        by_id[f'F{n}'].update(id=f'B{31+n}', kind='back', secs=0)

    pipeline = by_id['s18']
    poster = deck / 'assets/pipeline-poster.jpg'
    movie = deck / 'clips/ci-cd-40344230832.mp4'
    if movie.exists() and (not poster.exists() or poster.stat().st_mtime < movie.stat().st_mtime):
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-ss', '1', '-i', str(movie),
                        '-frames:v', '1', '-vf', 'scale=1280:-1', '-y', str(poster)], check=True)
    pipeline.update(
        secs=720, title='The pipeline connects protected source to a verified deployment',
        extra='pipeline-slide',
        body='<div class="clip pipeline-film" data-clip="clips/ci-cd-40344230832.mp4">'
             '<video muted playsinline preload="metadata"></video>'
             '<img class="poster" src="assets/pipeline-poster.jpg" alt="CI/CD activity view and recorded walkthrough">'
             '<div class="pb"><span class="tri"></span></div><div class="cb"></div></div>'
             '<div class="playback-strip"><span>Space / click · 11:26</span>'
             '<span>PR Quality 40343459119 → Deploy dev 40344230832</span><button data-action="commands">C · commands</button></div>',
        say=['Protected source, retained artifacts, seven security procedures and hosted dev in one recorded walkthrough.'],
        transition='Start the group journey with accounts ready.', refs=['B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B12'],
        source='Filmed PR Quality 40343459119 · Deploy dev 40344230832 · same-commit dev Quality 40344231052 · 26–27 Oct 2026',
    )
    # Turn the supplied shotlist into the word-for-word live narration. The stage
    # derivative omits the environment-settings shot; source-branch promotion stays.
    rows = []
    shift = 0
    for line in (root / 'videos/cicd/SHOTLIST.md').read_text().splitlines():
        if not re.match(r'\| \d\d ·', line):
            continue
        cols = [v.strip() for v in line.strip('|').split('|')]
        if cols[0].startswith('28 ·'):
            shift += 24
            continue
        a, b = cols[1].split('–')
        def seconds(v):
            m, s = v.split(':')
            return int(m)*60 + int(s)
        def clock(v):
            return f'{v//60:02d}:{v%60:02d}'
        rows.append(f'[{clock(seconds(a)-shift)}–{clock(seconds(b)-shift)} video · {cols[0]}]\n{cols[4]}')
    pipeline['script'] = (
        '[00:00–00:20 section clock: introduce the recording, then press Space. '
        'Narrate the following cues over the 11:26 film. Its clip clock starts at zero.]\n\n'
        'The recording starts with PR Quality 40343459119 at commit 38593b2. '
        'Deploy 40344230832 uses merged commit aea7478 and its separate dev Quality gate, 40344231052. '
        'Follow the actual artifacts and security findings; an advisory and FFmpeg pin explain why we verify built images.\n\n'
        + '\n\n'.join(rows) +
        '\n\n[11:46–12:00 section clock: pause on the final decision chain.]\n'
        'Quality controls integration, the exact-image scan controls upload, and candidate health controls activation. '
        'CodeQL, IaC, secrets and ZAP retain their findings for review. '
        'Those retained artifacts make the next internal change inspectable. Now follow the product journey.'
    )

    s = by_id['s19']
    s.update(title='A private-group journey runs from prompt to film',
             body='<div class="journey-map">'
                  '<div><em>01–02</em><h2>Create and invite</h2><p>Prompt · private membership</p></div>'
                  '<div><em>03–06</em><h2>Contribute</h2><p>Photo · video · chat · reminder</p></div>'
                  '<div><em>07–10</em><h2>Reveal and retain</h2><p>Ready · watch · save · access check</p></div>'
                  '</div><div class="rule">28-day product cycle · private groups · one feature per slide</div>',
             script='Our two members have their accounts ready. Start with the group and its shared prompt. '
                    'Then invite, contribute, chat and choose a reminder. Finally open the completed film, save it, '
                    'and test the outsider boundary. Each feature has its own controlled clip.',
             transition='Create the group and choose its shared prompt.')

    feature_names = ['Create a group', 'Invite and join', 'Seal a photo', 'Video and allowance', 'Group chat',
                     'Weekly reminder', 'Film ready', 'Watch the film', 'Archive and save', 'Outsider denied']
    lengths = [60, 60, 55, 65, 55, 50, 40, 80, 55, 50]
    device_manifest = deck / 'clips/device/manifest.json'
    device_data = json.loads(device_manifest.read_text())['clips'] if device_manifest.exists() else []
    hosted_manifest = deck / 'clips/hosted-device/manifest.json'
    hosted_data = json.loads(hosted_manifest.read_text())['clips'] if hosted_manifest.exists() else []
    for number in range(3, 13):
        s = by_id[f'F{number}']
        file = re.search(r'data-clip="([^"]+)"', s['body']).group(1).split('/')[-1]
        points = re.search(r'<div class="explain">(.*?)</div></div>$', s['body'], re.S)
        explanation = points.group(1).split('<div class="clip-hint">')[0] if points else ''
        hosted_meta = next((m for m in hosted_data if m['output'].endswith('/'+file)), None)
        folder = 'clips/hosted-device/' if hosted_meta else 'clips/device/'
        clip = folder + file
        poster = folder + file.replace('.mp4', '-poster.jpg')
        meta = next((m for m in device_data if m['output'].endswith('/'+file)), None)
        ratio = hosted_meta['width']/hosted_meta['height'] if hosted_meta else meta['crop']['width']/meta['crop']['height'] if meta else 416/776
        if number == 8:
            explanation = ('<p><b>Do.</b> Open settings and choose the weekly reminder.</p>'
                           '<p><b>Observe.</b> The switch and seven-day snooze keep the choice explicit.</p>'
                           '<p><b>Rule.</b> Sunday 19:00 in the group time zone; iPhone web push uses the Home Screen app.</p>')
            s['script'] = ('Open settings and choose the weekly reminder. The switch makes the preference explicit, '
                           'and snooze lasts seven days. The weekly schedule is Sunday at seven in the evening in the group’s time zone. '
                           'On iPhone, add Rewind to the Home Screen for web push. Pause on the saved preference, '
                           'then continue to a completed capsule and its premiere.')
        if number == 6:
            explanation = explanation.replace('Record with sound, trim and submit.', 'Record a video, review and submit.')
            s['script'] = s['script'].replace('Record a video with sound, review the trim and submit it.',
                                             'Record a video, review the trim and submit it.')
        s.update(secs=lengths[number-3]+9, extra='device-slide',
                 body='<div class="device-demo"><div class="device-column">'
                      '<div class="iphone-shell" style="--screen-aspect:'+str(ratio)+'"><span class="side-key volume"></span><span class="side-key power"></span>'
                      '<div class="device-status"><span>9:41</span><span class="island"></span><span>▮▮▮ ▰</span></div>'
                      '<div class="clip iphone-screen" data-clip="'+clip+'"><video muted playsinline preload="metadata"></video>'
                      '<img class="poster" src="'+poster+'" alt="'+html.escape(feature_names[number-3])+'">'
                      '<div class="pb"><span class="tri"></span></div><div class="cb"></div></div></div></div>'
                      '<div class="feature-notes"><div class="feature-number">'+f'{number-2:02d} / 10 · '+feature_names[number-3]+'</div>'
                      + explanation + '<div class="feature-control"><button data-action="play">Space / click · play or pause</button>'
                      '<button data-action="sound" aria-pressed="false">M · sound off</button>'
                      '<button data-action="restart">R · restart</button></div>'
                      '<p class="clip-state" aria-live="polite">Ready when you are</p></div></div>',
                 source=s['source'].split(' · ')[-1]+' · hosted dev · '+('27' if hosted_meta and number != 8 else '26')+' Oct 2026')
        if number == 4:
            s['script'] = s['script'].replace('The friend signs in and accepts it.', 'Our friend accepts it from the prepared account.')
        if number == 10:
            s['script'] = s['script'].replace('Let a short section play with sound, then pause at the end screen.',
                                           'Press M only if you want the film sound. Pause at the end screen.')
        if number == 12:
            s['script'] = s['script'].replace('The outsider signs in with a different account and tries',
                                           'From the outsider’s prepared account, try')
        if number == 9:
            s['script'] = s['script'].replace('Here is the completed capsule from Maya and Jun.',
                                             'Switch to The little things, a completed capsule from Maya and Jun.')
        s['script'] = ('[Press Space to start. Narrate over the clip; pause on the stated result. '
                       'Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]\n\n'
                       + s['script'])

    by_id['s20']['script'] = (
        '[00:00–00:35: point to the measured stages and acceptance rule.]\n'
        'The runner called hosted dev through CloudFront and the Node API backed by PostgreSQL. '
        'It stepped through one, ten, twenty-five, fifty and one hundred virtual users. Each stage had a fifteen-second ramp '
        'and three-minute steady window, with three-to-seven-second think time. The repeating mix was ninety-five percent reads '
        'and five percent chat writes, with three photo uploads. The gate is p95 below two seconds and fewer than one percent errors.\n\n'
        '[00:35–01:05: read the 100-user row and the all-stage totals.]\n'
        'All five stages passed, with six thousand and thirty-eight steady requests and zero errors. '
        'At one hundred users, p95 was one thousand three hundred and thirty-six milliseconds and throughput was seventeen point eight four requests per second. '
        'That leaves about two-thirds of a second below the latency target. The run finished at thirteen minutes past midnight Singapore time on twenty-seven October, on dev build 2390589.\n\n'
        '[01:05–01:45: follow the one-host and two-host projected curves.]\n'
        'The projected curves fit a closed-user model to the measured means at ten through one hundred users. '
        'The fitted serialized service demand is forty-five point three nine milliseconds, fixed delay is three hundred and seventy-eight milliseconds, '
        'and mean think time is five seconds. The one-host ceiling is about twenty-two requests per second, with a knee near one hundred and sixteen active users. '
        'At two hundred and fifty users, the projected mean is six point four three seconds on one host and one point zero seven seconds with two balanced hosts. '
        'These curves describe mean response time; the measured table describes p95.\n\n'
        '[01:45–02:35: explain the mechanism behind the scale-out choices.]\n'
        'The PostgreSQL adapter waits synchronously around one client, so part of the API path serializes. '
        'The media worker also shares host CPU with requests. Separate media processing first, then make persistence asynchronous with a bounded connection pool. '
        'A second API host also needs coordinated capability state, staged media and scheduler ownership. Sessions already live in PostgreSQL, and PostgreSQL and S3 stay shared. '
        'The shared writer lock means adding a host improves read concurrency without multiplying shared write throughput.\n\n'
        '[02:35–03:12: connect maintainability to the pipeline, then invite questions.]\n'
        'The pipeline we just followed checks those changes through behavioural tests, both database dialects, built-image verification, '
        'exact-image security, signed provenance and candidate health. That is the maintainability strategy: improve the internal mechanism while preserving the observed product behaviour. '
        'We have connected the group journey to its design, checks and delivery evidence. Thank you; I am ready for questions.'
    )
    by_id['B11']['script'] = (
        'The quiet-host run fits S = 45.39 milliseconds per request, L = 377.9 milliseconds, and Z = 5 seconds. '
        'The model solves U = lambda S, R = L + S/(1-U), and lambda = N/(Z+R) together. '
        'Projected one-host throughput approaches 22.0 requests per second; the 90-percent-utilisation knee is about 116 users. '
        'At 250, 500 and 1,000 users, projected one-host means are 6.43, 17.75 and 40.44 seconds. '
        'The two-balanced-host means are 1.07, 6.43 and 17.75 seconds. '
        'The measured 100-user mean is 615.4 milliseconds, and its p95 is 1,335.9 milliseconds.'
    )
    # Point every demonstration command to the bytes actually verified on film.
    for s in slides:
        for key in ('script', 'body'):
            s[key] = s[key].replace('gh attestation verify --repo Collaboration95/rewind-app rewind-release.tar',
                                    'gh attestation verify --repo Collaboration95/rewind-app release-manifest.json')
            s[key] = s[key].replace('on the downloaded bundle.', 'on the downloaded manifest.')
            s[key] = s[key].replace('the downloaded rewind-release.tar', 'the downloaded release-manifest.json')
    # Keep the complete pipeline supporting narrative readily usable in Q&A.
    by_id['B12']['script'] += (' The demonstrated verification checks release-manifest.json and exits zero. '
                               'The real IaC JSON is retained under pipeline-run-40344230832/iac/, '
                               'from same-commit Release security run 40344231046.')
    by_id['s14']['body'] = by_id['s14']['body'].replace('Exact exceptions and expiry checks', '15 findings · exact exceptions and expiry')
    by_id['s14']['script'] += (' The retained IaC JSON contains fifteen findings. '
                              'The successful scan workflow applies exact exceptions, with expiry on 31 October. '
                              'That workflow result and the individual findings remain separately inspectable.')
    by_id['B12']['body'] += ('<p class="artifact-links"><a href="../pipeline-run-40344230832/iac/iac-full.json" target="_blank">IaC JSON · 15 findings</a>'
                             '<a href="../pipeline-run-40344230832/security/release-manifest.json" target="_blank">Signed manifest JSON</a>'
                             '<a href="../pipeline-run-40344230832/zap/report_json.json" target="_blank">ZAP JSON</a></p>')
    for number, filename, title, script in [
        (34, 'latency-vs-vus.png', 'Every steady load stage stays below the latency target',
         'The measured p50, p95 and p99 curves cover one through one hundred virtual users. '
         'All p95 stages stay below two seconds; the 100-user p95 is 1,335.9 milliseconds.'),
        (35, 'throughput-vs-vus.png', 'Measured throughput rises with the active user count',
         'The measured 100-user throughput is 17.84 requests per second, with zero errors. '
         'Each point uses its own three-minute steady window.')]:
        slides.append(dict(id=f'B{number}', sec=5, tag='TESTING', title=title,
                           body='<figure class="figure chart"><figcaption>Performance view · measured hosted dev · 27 Oct 2026</figcaption>'
                                '<img src="assets/'+filename+'" alt="'+title+'"></figure>',
                           secs=0, say=[script], transition='Return to the measured table or capacity curve.', refs=['B11'],
                           source='load-test/results/summary.json · quiet-host run · dev 2390589', script=script,
                           kind='back', extra='chart-slide'))
    for s in slides:
        s['title'] = s['title'].rstrip('.')
        if s['id'] in ('B32', 'B33'):
            s['body'] = re.sub(r'<div class="ph">.*?</div>', '', s['body'])
            s['body'] = s['body'].replace('class="clip"', 'class="clip print-poster"')
    main = [s for s in slides if s['kind'] != 'back']
    backups = sorted((s for s in slides if s['kind'] == 'back'), key=lambda s: int(s['id'][1:]))
    slides[:] = main + backups


FINAL_CSS = r'''
.device-slide,.pipeline-slide{padding:0}
.device-slide>.kicker,.device-slide>.section-progress,.device-slide>.foot,
.pipeline-slide>.kicker,.pipeline-slide>.section-progress,.pipeline-slide>.foot{display:none!important}
.device-slide>h1,.pipeline-slide>h1{position:absolute;top:9px;left:24px;right:24px;font-size:22px;line-height:28px;min-height:0;height:28px;margin:0;letter-spacing:-.35px}
.device-slide>.body{position:absolute;inset:44px 24px 12px;margin:0;height:auto;display:block}
.device-demo{display:grid;grid-template-columns:390px 1fr;gap:45px;height:100%;align-items:center}
.device-column{height:100%;display:flex;align-items:center;justify-content:center}
.iphone-shell{box-sizing:border-box;height:642px;width:calc(576px * var(--screen-aspect) + 18px);position:relative;padding:36px 7px 26px;border:2px solid #777979;border-radius:47px;background:#f4ede3;box-shadow:inset 0 0 0 6px #151719,0 14px 25px #14202b24,0 0 0 1px #111}
.iphone-shell:after{content:'';position:absolute;bottom:13px;left:50%;transform:translateX(-50%);height:4px;width:78px;background:#161819;border-radius:4px}
.device-status{position:absolute;top:11px;left:23px;right:22px;display:flex;align-items:center;justify-content:space-between;font:600 14px Arial,sans-serif;height:18px;color:#111}
.device-status .island{width:82px;height:21px;background:#050505;border-radius:20px}
.iphone-screen.clip{width:100%;height:100%;border-radius:4px;background:#f4ede3;position:relative}
.iphone-screen video{object-fit:contain}
.iphone-screen .poster{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;display:block;opacity:1;pointer-events:none}
.iphone-screen.ready .poster,.pipeline-film.ready .poster{opacity:0}
.iphone-screen .pb{width:70px;height:70px;margin:-35px 0 0 -35px;background:#14202bba}
.iphone-screen .pb .tri{border-left-width:22px;border-top-width:14px;border-bottom-width:14px}
.side-key{position:absolute;width:4px;background:#6b7072;border-radius:3px;left:-5px;top:132px;height:48px}
.side-key.power{left:auto;right:-5px;top:178px;height:65px}
.feature-number{font:600 17px Menlo,monospace;color:#367348;margin-bottom:26px}
.feature-notes>p{font-size:28px;line-height:1.45;margin:0 0 28px;max-width:680px}
.feature-notes>p b{display:block;font-size:18px;text-transform:uppercase;letter-spacing:1.2px;color:#50606a;margin-bottom:5px}
.feature-control{display:flex;flex-wrap:wrap;gap:12px;margin-top:35px}
.feature-control button{font-size:17px;padding:11px 15px;background:#fff;border:1px solid #bfc8bd;border-radius:8px;cursor:pointer}
.feature-notes .clip-state{font-size:16px;margin-top:15px;color:#50606a}
.pipeline-slide>.body{position:absolute;inset:45px 18px 0;margin:0;height:auto;display:block}
.pipeline-film.clip{width:1244px;height:calc(1244px * 9 / 16);max-height:635px;background:#fff;border-radius:8px}
.pipeline-film video,.pipeline-film .poster{width:100%;height:100%;object-fit:contain;background:#f5f2e9}
.pipeline-film .poster{position:absolute;inset:0;opacity:1;pointer-events:none}
.playback-strip{position:absolute;bottom:3px;left:0;right:0;display:flex;align-items:center;justify-content:space-between;font-size:16px;background:#f5f2e9;padding:5px 12px}
.playback-strip button{font-size:15px;padding:5px 12px}
.artifact-links{display:flex;gap:22px;font-size:17px}
.artifact-links a{color:#247b72}
#s20 .confirmation{font-size:18px;line-height:1.3}
#s20 .perf-method{font-size:18px;line-height:1.35;margin:8px 0}
.clip.print-poster .poster{opacity:1;pointer-events:none}
.clip.print-poster.ready .poster{opacity:0}
#notes .spoken p{margin:10px 0;font-size:19px;line-height:1.45;white-space:pre-line}
@media print{
.device-slide>.body,.pipeline-slide>.body{position:absolute!important;display:block!important}
.iphone-screen .poster,.pipeline-film .poster{opacity:1!important;display:block!important}
.feature-control,.clip-state,.playback-strip{display:none!important}
.iphone-shell{break-inside:avoid}
}
'''


def final_javascript(js):
    js = js.replace("s.dataset.num+' · feature / 12'", "(Number(s.id.slice(1))-2)+' / 10 · feature'")
    js = js.replace("v.preload='auto';v.src=c.dataset.clip;", "v.muted=true;v.defaultMuted=true;v.preload='auto';v.src=c.dataset.clip;")
    js = js.replace("function toggleClip(){var c=cur>=0&&clipOf(cur);if(!c||!c.classList.contains('ready'))return;var v=c.querySelector('video');if(v.paused)v.play();else v.pause()}",
                    "function toggleClip(){var c=cur>=0&&clipOf(cur);if(!c)return;var v=c.querySelector('video');if(v.paused)v.play().catch(function(){clipStatus(c,'Press Space again to start')});else v.pause()}")
    js = js.replace("v.addEventListener('ended',function(){c.classList.remove('playing')});",
                    "v.addEventListener('ended',function(){c.classList.remove('playing');clipStatus(c,'Finished · R to replay')});")
    js = js.replace("v.addEventListener('play',function(){c.classList.add('playing')});",
                    "v.addEventListener('play',function(){c.classList.add('playing');clipStatus(c,'Playing · Space to pause')});")
    js = js.replace("v.addEventListener('pause',function(){c.classList.remove('playing')});",
                    "v.addEventListener('pause',function(){c.classList.remove('playing');clipStatus(c,'Paused · Space to continue')});")
    js = js.replace("if(blk.classList.contains('on')&&k.toLowerCase()!=='b')return;",
                    "if(blk.classList.contains('on')&&k.toLowerCase()!=='b')return;"
                    "if(k===' '){e.preventDefault();if(!ov.classList.contains('on'))toggleClip();return;}"
                    "if(k==='m'||k==='M'){toggleSound();return;}"
                    "if(k==='r'||k==='R'){var c=clipOf(cur);if(c){c.querySelector('video').pause();c.querySelector('video').currentTime=0;}return;}")
    js = js.replace("var cur=-1,buf='',hudT=0;", "var cur=-1,buf='',hudT=0;" + r'''
function clipStatus(c,text){var s=c.closest('.slide');var el=s&&s.querySelector('.clip-state');if(el)el.textContent=text}
function toggleSound(){var c=clipOf(cur);if(!c)return;var v=c.querySelector('video');v.muted=!v.muted;var b=slides[cur].querySelector('[data-action=sound]');if(b){b.textContent=v.muted?'M · sound off':'M · sound on';b.setAttribute('aria-pressed',String(!v.muted))}}
document.addEventListener('click',function(e){var b=e.target.closest('button[data-action]');if(!b)return;if(b.dataset.action==='play'){e.stopPropagation();toggleClip()}if(b.dataset.action==='sound')toggleSound();if(b.dataset.action==='restart'){var c=clipOf(cur);if(c){var v=c.querySelector('video');v.pause();v.currentTime=0;clipStatus(c,'Ready when you are')}}});
''')
    # The commands card verifies the retained manifest, matching the filmed result.
    return js.replace('gh attestation verify --repo Collaboration95/rewind-app rewind-release.tar',
                      'gh attestation verify --repo Collaboration95/rewind-app release-manifest.json')


def write_guides(slides, deck):
    def mm(n):
        return f'{n//60:02d}:{n%60:02d}'
    lines = ['# Rewind · final presentation outline', '',
             '27 October 2026 · 14:30 SGT · Team 14 · Gopal Guruprasath', '',
             '38:00 planned delivery + 2:00 interruptions = 40:00 presentation slot. Q&A follows for 5:00.', '',
             '| Section | Clock | Budget |', '|---|---|---:|',
             '| Intro and PM | 00:00–03:30 | 3:30 |',
             '| Analysis, design and patterns | 03:30–08:30 | 5:00 |',
             '| Testing | 08:30–11:30 | 3:00 |',
             '| CI/CD demonstration | 11:30–23:30 | 12:00 |',
             '| System demo and quality attributes | 23:30–38:00 | 14:30 |', '',
             '## Presentation sequence', '',
             '14 narrative frames and 10 feature inserts. Feature playback totals 9:30, with 1:30 for introductions and pauses. '
             'The CI/CD stage edit is 11:26, with 0:34 for introduction and closing.', '',
             '| Physical page | Anchor | Section | Clock | Content |', '|---:|---|---:|---|---|']
    for i, s in enumerate(slides, 1):
        if s['kind'] != 'back':
            lines.append(f"| {i} | {s['id']} | {s['sec']} | {mm(s['clock'])}–{mm(s['clock']+s['secs'])} | {s['title']} |")
    lines += ['', 'The CU-B sequence uses s8 → B16 → B17 → s9 within the same 0:57 allocation. '
              'Installation and sign-in are B32/B33. Accounts are ready before the main demo. '
              'The reveal transition opens the completed capsule The little things.', '', '## Q&A backups', '',
              '| Anchor | Question / view |', '|---|---|']
    lines += [f"| {s['id']} | {s['title']} |" for s in slides if s['kind'] == 'back']
    lines += ['', '## Playback and source files', '',
              '- deck.html: every slide and full speaker notes; images and posters are embedded.',
              '- SCRIPT.md: word-for-word delivery and clip-clock cues.',
              '- clips/ci-cd-40344230832.mp4: 11:26 stage edit; ../videos/cicd/cicd-demo.mp4 is the 11:50 source backup.',
              '- clips/device/ and clips/hosted-device/: portrait feature derivatives; ../videos/demo.mp4 is the complete system backup.',
              '- ../load-test/results/summary.json: hosted run; 100 VUs, p95 1,336 ms, 17.84 req/s, 6,038 steady requests and zero errors.',
              '- ../pipeline-run-40344230832/: manifest, SBOM, Trivy, ZAP and same-commit IaC JSON.',
              '- ../records/: five named members, agreed effort, agile records and all four sprint charts.', '']
    (deck / 'OUTLINE.md').write_text('\n'.join(lines))
