/* OX derivative of yichahucha/surge @ 06d6e36771880959c008d3c59c192068f00ddd51; GPL-3.0.
Modifications: synchronous failures pass through; Netflix requires own OMDb preference key, shared key pool removed. */
(function () { try {
/*
README：https://github.com/yichahucha/surge/tree/master
 */

const path1 = "/interface/sdk/sdkad.php";
const path2 = "/wbapplua/wbpullad.lua";

const url = $request.url;
var body = $response.body;

if (url.indexOf(path1) != -1) {
    let re = /\{.*\}/;
    body = body.match(re);
    var obj = JSON.parse(body);
    if (obj.background_delay_display_time) obj.background_delay_display_time = 60*60*24*365;
    if (obj.show_push_splash_ad) obj.show_push_splash_ad = false;
    if (obj.ads) obj.ads = [];
    body = JSON.stringify(obj) + 'OK';
}

if (url.indexOf(path2) != -1) {
    var obj = JSON.parse(body);
    if (obj.cached_ad && obj.cached_ad.ads) obj.cached_ad.ads = [];
    body = JSON.stringify(obj);
}

$done({body});

} catch (error) { $done({}); } })();
