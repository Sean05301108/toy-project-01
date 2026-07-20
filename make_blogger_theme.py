# -*- coding: utf-8 -*-
"""
out/ JSON  ->  블로그스팟 테마(theme.xml) + GitHub Pages용 data/ 폴더

사용법:
  python3 build_data.py 로그.txt out
  python3 categorize.py out/index.json
  python3 make_blogger_theme.py out ./site   <- 여기서 theme.xml 과 site/data/ 생성
"""
import json, os, shutil, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else 'out'
DST = sys.argv[2] if len(sys.argv) > 2 else 'site'

# ── 1. GitHub Pages 로 올릴 데이터 폴더 ─────────────────────────────
os.makedirs(f'{DST}/data', exist_ok=True)
if os.path.isdir(f'{DST}/data/item'):
    shutil.rmtree(f'{DST}/data/item')
shutil.copy(f'{SRC}/index.json', f'{DST}/data/index.json')
shutil.copytree(f'{SRC}/item', f'{DST}/data/item')
# GitHub Pages 가 Jekyll 처리를 건너뛰도록
open(f'{DST}/.nojekyll', 'w').close()

n_items = len(json.load(open(f'{SRC}/index.json', encoding='utf-8'))['items'])

# ── 2. CSS (프로토타입과 동일) ──────────────────────────────────────
CSS = open('prototype.html', encoding='utf-8').read().split('<style>')[1].split('</style>')[0]

# ── 3. JS — 내장 데이터 대신 fetch 사용 ─────────────────────────────
JS = r'''
/* ============================================================
   여기만 본인 것으로 바꾸세요.
   GitHub 사용자명이 hong, 저장소가 lona-data 라면:
   https://hong.github.io/lona-data/data
   ============================================================ */
var DATA_BASE = 'https://GITHUB사용자명.github.io/저장소명/data';

var D = null, byId = {};
var cache = {};
var FAV = 'lona_fav';
function fav(){ try { return JSON.parse(localStorage.getItem(FAV) || '[]'); } catch(e){ return []; } }
var bust = '?v=' + new Date().toISOString().slice(0,10);

function get(path){
  if (cache[path]) return Promise.resolve(cache[path]);
  return fetch(DATA_BASE + path + bust).then(function(r){
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }).then(function(j){ cache[path] = j; return j; });
}

function money(n){
  if (n >= 100000000){ var v = n/100000000;
    return (v >= 10 ? Math.round(v) : v.toFixed(1).replace(/\.0$/,'')) + '억'; }
  if (n >= 10000) return Math.round(n/10000).toLocaleString() + '만';
  return n.toLocaleString();
}
function full(n){ return n.toLocaleString() + ' 메소'; }
function chgHtml(c){
  if (!c) return '<div class="chg flat">어제와 같아요</div>';
  var up = c > 0;
  return '<div class="chg ' + (up?'up':'down') + '">' + (up?'▲':'▼') + ' ' + Math.abs(c) + '%</div>';
}

var CHO = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'];
function cho(s){
  var o = '';
  for (var i = 0; i < s.length; i++){
    var c = s.charCodeAt(i) - 44032;
    o += (c >= 0 && c <= 11171) ? CHO[Math.floor(c/588)] : s[i];
  }
  return o;
}

var app = document.getElementById('app');
var state = { q:'', cat:'전체' };
function go(h){ location.hash = h; }

var CATS = ['전체','장비','주문서','소비','재료','마스터리북','기타'];
var foot = '<div class="foot">실제 거래 기록을 집계한 참고용 통계입니다.<br/>' +
           '극단적인 매물은 제외한 중앙값 기준이에요.</div>';

function tabs(on){
  var T = [['','홈','M3 10.5 12 3l9 7.5V21H3z'],
           ['/rank','랭킹','M4 20V10M10 20V4M16 20v-8M22 20h-20'],
           ['/fav','저장','M12 3l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.8 6.2 20.9l1.1-6.5L2.6 9.8l6.5-.9z']];
  return '<nav class="tabs">' + T.map(function(t){
    return '<button class="tab" ' + (on===t[0]?'data-on':'') + ' onclick="go(\'' + (t[0]||'/') + '\')">' +
      '<svg width="22" height="22" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="' + t[2] + '"/></svg>' + t[1] + '</button>';
  }).join('') + '</nav>';
}

function rowHtml(it, i){
  return '<button class="row" onclick="go(\'/item/' + it.id + '\')">' +
    (i != null ? '<span class="rank num">' + (i+1) + '</span>' : '') +
    '<span class="rname">' + it.n + '<div class="rsub">거래 ' + it.v.toLocaleString() + '건</div></span>' +
    '<span class="rprice num">' + money(it.p) + chgHtml(it.c) + '</span></button>';
}

function skeleton(){
  var r = '';
  for (var i = 0; i < 8; i++){
    r += '<div class="row"><div style="flex:1"><div class="sk" style="width:40%;height:17px"></div>' +
         '<div class="sk" style="width:22%;height:12px;margin-top:6px"></div></div>' +
         '<div class="sk" style="width:64px;height:17px"></div></div>';
  }
  return r;
}

/* ── 홈 ── */
function home(){
  app.innerHTML =
    '<div class="head"><h1 class="h1">로나 시세</h1>' +
      '<div class="date">' + (D ? D.updated.replace(/-/g,'.') + ' 기준' : '불러오는 중') + '</div></div>' +
    '<div class="search">' +
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round">' +
      '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>' +
      '<input id="q" placeholder="아이템 이름을 검색하세요" value="' + state.q + '" autocomplete="off"/></div>' +
    '<div class="chips">' + CATS.map(function(c){
      return '<button class="chip" ' + (state.cat===c?'data-on':'') +
             ' onclick="setCat(\'' + c + '\')">' + c + '</button>'; }).join('') + '</div>' +
    '<div id="list">' + (D ? '' : skeleton()) + '</div>' + foot + tabs('');
  var inp = document.getElementById('q');
  if (inp) inp.oninput = function(e){ state.q = e.target.value; list(); };
  if (D) list();
}
function setCat(c){ state.cat = c; home(); }

function list(){
  var q = state.q.trim().toLowerCase(), qc = cho(q).replace(/\s/g,'');
  var r = D.items.filter(function(i){ return state.cat === '전체' || i.cat === state.cat; });
  if (q) r = r.filter(function(i){
    return i.n.toLowerCase().indexOf(q) >= 0 || i._c.indexOf(qc) >= 0; });
  var el = document.getElementById('list');
  if (!el) return;
  if (!r.length){
    el.innerHTML = '<div class="empty"><div class="emptyT">검색 결과가 없어요</div>' +
                   '아직 거래된 적 없는 아이템일 수 있어요</div>';
    return;
  }
  el.innerHTML = '<div class="sec">' + (q ? '검색 결과 ' + r.length + '개' : '많이 거래된 아이템') + '</div>' +
    r.slice(0,60).map(function(i){ return rowHtml(i); }).join('');
}

/* ── 랭킹 ── */
var rmode = 'v';
function rank(){
  var L = [['v','거래량'],['up','상승'],['down','하락']];
  var r = D.items.slice();
  if (rmode === 'v') r.sort(function(a,b){ return b.v - a.v; });
  if (rmode === 'up') r = r.filter(function(i){ return i.v >= 20; }).sort(function(a,b){ return b.c - a.c; });
  if (rmode === 'down') r = r.filter(function(i){ return i.v >= 20; }).sort(function(a,b){ return a.c - b.c; });
  app.innerHTML =
    '<div class="head"><h1 class="h1">이번 주 랭킹</h1>' +
      '<div class="date">거래 20건 이상 아이템만 집계해요</div></div>' +
    '<div class="chips">' + L.map(function(k){
      return '<button class="chip" ' + (rmode===k[0]?'data-on':'') +
             ' onclick="setR(\'' + k[0] + '\')">' + k[1] + '</button>'; }).join('') + '</div>' +
    '<div class="sec">TOP 50</div>' +
    r.slice(0,50).map(function(i,n){ return rowHtml(i,n); }).join('') + foot + tabs('/rank');
}
function setR(k){ rmode = k; rank(); }

/* ── 저장 ── */
function favs(){
  var r = fav().map(function(id){ return byId[id]; }).filter(Boolean);
  app.innerHTML = '<div class="head"><h1 class="h1">저장한 아이템</h1></div>' +
    (r.length ? r.map(function(i){ return rowHtml(i); }).join('')
      : '<div class="empty"><div class="emptyT">저장한 아이템이 없어요</div>' +
        '아이템 화면에서 별표를 누르면 여기에 모여요</div>') + tabs('/fav');
}

/* ── 상세 ── */
function detail(id){
  var it = byId[id];
  if (!it){
    app.innerHTML = '<div class="empty"><div class="emptyT">아이템을 찾을 수 없어요</div>' +
      '<button class="chip" style="margin-top:14px" onclick="go(\'/\')">홈으로</button></div>';
    return;
  }
  var navBar = '<div class="nav"><button class="back" onclick="history.back()">' +
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" ' +
    'stroke-linecap="round" stroke-linejoin="round"><path d="m15 5-7 7 7 7"/></svg></button></div>';
  app.innerHTML = navBar + '<div class="detail"><h1 class="dname">' + it.n + '</h1>' +
    '<div class="sk" style="width:55%;height:32px"></div>' +
    '<div class="sk" style="width:100%;height:150px;margin-top:26px"></div></div>' + tabs('');

  get('/item/' + id + '.json').then(function(d){
    var s = d.series, last = s[s.length-1];
    var isFav = fav().indexOf(id) >= 0;
    var ps = s.map(function(x){ return x.p; });
    var allLo = Math.min.apply(null, ps), allHi = Math.max.apply(null, ps);
    app.innerHTML =
      '<div class="nav"><button class="back" onclick="history.back()">' +
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" ' +
        'stroke-linecap="round" stroke-linejoin="round"><path d="m15 5-7 7 7 7"/></svg></button>' +
      '<button class="fav" ' + (isFav?'data-on':'') + ' onclick="toggleFav(\'' + id + '\')">' +
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="' + (isFav?'currentColor':'none') + '" ' +
        'stroke="currentColor" stroke-width="2" stroke-linejoin="round">' +
        '<path d="M12 3l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.8 6.2 20.9l1.1-6.5L2.6 9.8l6.5-.9z"/></svg></button></div>' +
      '<div class="detail"><span class="dcat">' + it.cat + '</span>' +
      '<h1 class="dname">' + it.n + '</h1>' +
      '<div class="dprice num">' + money(last.p) + '<span class="dunit">메소</span></div>' +
      chgHtml(it.c) + chart(s) +
      '<div class="stats">' +
        '<div class="stat"><div class="slabel">최저</div><div class="sval num">' + money(allLo) + '</div></div>' +
        '<div class="stat"><div class="slabel">최고</div><div class="sval num">' + money(allHi) + '</div></div>' +
        '<div class="stat"><div class="slabel">거래</div><div class="sval num">' + it.v.toLocaleString() + '건</div></div>' +
      '</div>' +
      '<div class="sec" style="padding-left:0">최근 거래</div>' +
      d.recent.map(function(r){
        return '<div class="trade"><div><div class="ttime num">' +
          r.d.slice(5).replace('-','.') + ' ' + r.t.slice(0,5) + '</div>' +
          (r.o ? '<div class="topt">' + r.o + '</div>' : '') + '</div>' +
          '<div class="tprice num">' + full(r.u) +
          (r.q > 1 ? '<div class="tqty">' + r.q + '개 묶음 · 개당</div>' : '') + '</div></div>';
      }).join('') + foot + '</div>' + tabs('');
  }).catch(function(){
    app.innerHTML = navBar + '<div class="empty"><div class="emptyT">시세를 불러오지 못했어요</div>' +
      '잠시 후 다시 시도해 주세요' +
      '<div><button class="chip" style="margin-top:14px" onclick="detail(\'' + id + '\')">다시 시도</button></div></div>';
  });
}
function toggleFav(id){
  var f = fav(), i = f.indexOf(id);
  if (i < 0) f.push(id); else f.splice(i,1);
  localStorage.setItem(FAV, JSON.stringify(f));
  detail(id);
}

/* 시그니처: 그려지는 7일 시세선 */
function chart(s){
  var W = 100, H = 100, P = 8;
  var v = s.map(function(d){ return d.p; });
  var lo = Math.min.apply(null,v), hi = Math.max.apply(null,v), span = (hi - lo) || 1;
  var pts = v.map(function(y,i){
    return [ P + i * (W - P*2) / Math.max(v.length-1, 1),
             H - P - (y - lo) / span * (H - P*2) ];
  });
  var line = pts.map(function(p){ return p.join(','); }).join(' ');
  var end = pts[pts.length-1];
  return '<div class="chart"><svg viewBox="0 0 100 100" preserveAspectRatio="none">' +
    '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">' +
      '<stop offset="0%" stop-color="#3182F6" stop-opacity=".18"/>' +
      '<stop offset="100%" stop-color="#3182F6" stop-opacity="0"/></linearGradient></defs>' +
    '<polygon class="area" points="' + P + ',' + H + ' ' + line + ' ' + (W-P) + ',' + H + '"/>' +
    '<polyline class="line" points="' + line + '" style="--len:400" vector-effect="non-scaling-stroke"/>' +
    '<circle class="dot" cx="' + end[0] + '" cy="' + end[1] + '" r="1.6" vector-effect="non-scaling-stroke"/>' +
    '</svg><div class="xaxis">' + s.map(function(d){
      return '<span>' + d.d.slice(5).replace('-','/') + '</span>'; }).join('') + '</div></div>';
}

/* ── 라우팅 ── */
function render(){
  var h = location.hash.slice(1);
  if (h.indexOf('/item/') === 0) detail(h.slice(6));
  else if (h === '/rank') rank();
  else if (h === '/fav') favs();
  else home();
  window.scrollTo(0,0);
}
window.addEventListener('hashchange', render);

home();
get('/index.json').then(function(j){
  D = j;
  D.items.forEach(function(i){ i._c = cho(i.n).replace(/\s/g,''); byId[i.id] = i; });
  render();
}).catch(function(){
  app.innerHTML = '<div class="empty"><div class="emptyT">시세를 불러오지 못했어요</div>' +
    '네트워크 상태를 확인하고 새로고침해 주세요</div>';
});
'''

# ── 4. 블로그스팟 테마 XML 조립 ─────────────────────────────────────
THEME = """<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html>
<html b:version='2' class='v2' expr:dir='data:blog.languageDirection'
      xmlns='http://www.w3.org/1999/xhtml'
      xmlns:b='http://www.google.com/2005/gml/b'
      xmlns:data='http://www.google.com/2005/gml/data'
      xmlns:expr='http://www.google.com/2005/gml/expr'>
<head>
<meta charset='UTF-8'/>
<meta content='width=device-width,initial-scale=1,viewport-fit=cover' name='viewport'/>
<meta content='메이플스토리 월드 로나월드 옥션 시세를 한눈에.' name='description'/>
<title><data:blog.pageTitle/></title>
<link href='https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css'
      rel='stylesheet'/>
<b:skin><![CDATA[
__CSS__
]]></b:skin>
</head>
<body>

<div id='app'></div>

<!-- 블로그스팟이 요구하는 필수 위젯. 내용은 비워서 화면에 아무것도 그리지 않음 -->
<b:section id='main' showaddelement='no'>
  <b:widget id='Blog1' locked='true' type='Blog' version='2'>
    <b:includable id='main'></b:includable>
  </b:widget>
</b:section>

<script type='text/javascript'>
//<![CDATA[
__JS__
//]]>
</script>

</body>
</html>
"""

theme = THEME.replace('__CSS__', CSS).replace('__JS__', JS)
open(f'{DST}/theme.xml', 'w', encoding='utf-8').write(theme)

# ── 5. 검증: 블로그스팟은 XML 파서라 well-formed 가 아니면 저장 자체가 거부됨 ──
import xml.dom.minidom
try:
    xml.dom.minidom.parseString(theme.encode('utf-8'))
    ok = 'XML 검증 통과'
except Exception as e:
    ok = f'XML 오류: {e}'

size = os.path.getsize(f'{DST}/theme.xml') / 1024
print(f'{DST}/theme.xml  {size:.0f}KB  |  {ok}')
print(f'{DST}/data/      아이템 {n_items}종')
