// Execute only synthetic fixtures in an isolated VM, no network APIs exposed.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');
const base = path.join(__dirname, '../modules/scripts');
function run(name, url, body, extra={}) {
  let calls=[];
  const ctx = {$request:{url},$response:{body},$done:v=>calls.push(v),...extra};
  vm.runInNewContext(fs.readFileSync(path.join(base,name),'utf8'), ctx, {timeout:1000});
  assert.equal(calls.length,1, name+' must complete exactly once');
  return calls[0];
}
let x=run('wb_launch.js','https://sdkapp.uve.weibo.com/interface/sdk/sdkad.php',JSON.stringify({ads:[1],show_push_splash_ad:true}));
assert.equal(JSON.parse(x.body.slice(0,-2)).ads.length,0);
x=run('wb_launch.js','https://wbapp.uve.weibo.com/wbapplua/wbpullad.lua',JSON.stringify({cached_ad:{ads:[1]},keep:true}));
assert.equal(JSON.parse(x.body).cached_ad.ads.length,0);
assert.equal(JSON.parse(x.body).keep,true);
x=run('wb_ad.js','https://api.weibo.cn/2/statuses/unread',JSON.stringify({statuses:[],advertises:[1],keep:42}));
assert.equal(JSON.parse(x.body).advertises.length,0);
assert.equal(JSON.parse(x.body).keep,42);
for (const name of ['wb_launch.js','wb_ad.js']) {
  const url=name==='wb_launch.js'?'https://sdkapp.uve.weibo.com/interface/sdk/sdkad.php':'https://api.weibo.cn/2/statuses/unread';
  assert.equal(Object.keys(run(name,url,'not-json')).length,0);
  assert.equal(run(name,'https://example.invalid/untouched','original').body,'original');
}
const extra={$task:{fetch:()=>{throw Error('Unexpected network');}},$prefs:{valueForKey:()=>null,setValueForKey:()=>true},$notify:()=>{}};
assert.equal(Object.keys(run('nf_rating.js','https://ios.prod.ftl.netflix.com/iosui/user/x','{}',extra)).length,0);
console.log('PASS: 8 synthetic script cases: expected fields, passthrough, invalid JSON, missing API key; zero network access. App endpoints not tested.');
