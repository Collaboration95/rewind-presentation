exec(open('inspect_sources.py').read().split('sources=')[0])
jobs=[('08-reminder',list(range(180,220,2))+list(range(253,267))),('12-outsider',list(range(44,66)))]
def detail(item):
 name,times=item;args=['magick','montage','-font','/System/Library/Fonts/Supplemental/Arial.ttf','-pointsize','18']
 for t in times:
  p=QA/name/f'detail-{t}.jpg';run(['ffmpeg','-v','error','-ss',t,'-i',RAW/(name+'.mov'),'-frames:v','1','-vf','scale=300:-1','-y',p]);args+=['-label',f'{t}s',p]
 run(args+['-background','#f6efe5','-geometry','240x522+6+12','-tile','6x',QA/(name+'-detail.jpg')])
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(detail,jobs))
