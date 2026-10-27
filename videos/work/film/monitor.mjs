import {spawn} from 'node:child_process';
import fs from 'node:fs';
import {dir} from './hosted.mjs';
async function step(){return new Promise(resolve=>{const p=spawn(process.execPath,[dir+'poll.mjs'],{stdio:'inherit'});p.on('exit',resolve);});}
for(;;){await step();const n=JSON.parse(fs.readFileSync(dir+'production-notes.json'));if(n.film){console.log('DOWNLOAD_COMPLETE');break;}await new Promise(resolve=>setTimeout(resolve,55000));}
