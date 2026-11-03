// Execute with the T3 preview and exec tools supplied by the host.
// Requires a fresh Day 1 at 1280x800 and no auto-state.json from an earlier run.
export async function run(tools, n = 14, text = console.log, image = () => {}) {
  return await (async (n) => {for(let i=0;i<n;i++){
const s=await tools.mcp__t3_code__preview_snapshot({save:true});let path;
for(const c of s.content??[])if(c.type==="text"){try{path=JSON.parse(c.text).screenshotPath||path}catch{}}
if(!path){text("No screenshot path");break;}
const r=await tools.exec_command({cmd:".venv/bin/python -m sushi_policy.auto '"+path+"'",max_output_tokens:400});
const d=JSON.parse(r.output);text({i,action:d.action,dish:d.dish,item:d.item});
for(const [x,y]of d.clicks||[]){await tools.mcp__t3_code__preview_act({action:"click",x,y});await new Promise(r=>setTimeout(r,d.action==="refill"?300:40));}
await new Promise(r=>setTimeout(r,d.action==="make"?1300:150));
}
const s=await tools.mcp__t3_code__preview_snapshot({includeImage:true});for(const c of s.content??[])if(c.type==="image")image(c);
})(n);
}
