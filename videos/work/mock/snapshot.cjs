const fs=require('fs'),path=require('path');
module.exports=async function(p,name,selector){
 const result=await p.evaluate(sel=>{
  const root=document.querySelector(sel),copy=root.cloneNode(true),a=[root,...root.querySelectorAll('*')],b=[copy,...copy.querySelectorAll('*')];
  for(let i=0;i<a.length;i++){
   const s=getComputedStyle(a[i]); let css='';
   for(const prop of s) css+=prop+':'+s.getPropertyValue(prop)+';';
   b[i].setAttribute('style',css);
   for(const attr of [...b[i].attributes])if(/^on/i.test(attr.name))b[i].removeAttribute(attr.name);
  }
  copy.style.position='absolute';copy.style.left='0';copy.style.top='0';copy.style.margin='0';copy.style.width='402px';copy.style.height='714px';copy.style.flex='none';
  const sheets=[...document.styleSheets].map(s=>{try{return [...s.cssRules].map(r=>r.cssText).join('\n')}catch{return ''}}).join('\n');
  return {html:copy.outerHTML,css:sheets,text:root.innerText};
 },selector);
 const html='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>'+result.css+'\nhtml,body{margin:0;padding:0;width:402px;height:714px;overflow:hidden;background:#120b08}</style></head><body>'+result.html+'</body></html>';
 fs.writeFileSync(path.join(__dirname,'source',name+'.html'),html);
 fs.writeFileSync(path.join(__dirname,'source',name+'.text.txt'),result.text);
 console.log('DOM snapshot',name,html.length);
 return result;
};
