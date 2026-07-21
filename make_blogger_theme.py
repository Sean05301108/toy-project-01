# -*- coding: utf-8 -*-
"""
out/ JSON  ->  블로그스팟 테마(theme.xml) + GitHub Pages용 data/ 폴더   [v2]

v2 변경점
  · 반응형: 모바일 1열 / 태블릿 2열 / 데스크톱 3열 + 상단 네비 + 상세 2단
  · 블로그스팟 '페이지'(개인정보처리방침 등)가 실제 주소로 열리도록 지원
  · 하단 푸터에 약관 링크 · 면책 문구

사용법:
  python3 build_data.py 로그.txt out
  python3 categorize.py out/index.json
  python3 make_blogger_theme.py out ./site
"""
import json, os, shutil, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else 'out'
DST = sys.argv[2] if len(sys.argv) > 2 else 'site'

# ★ 본인 GitHub Pages 주소 (끝에 /data 포함, 마지막 슬래시 없음)
DATA_BASE = 'https://sean05301108.github.io/toy-project-01/data'

# ★ 건의하기 메일 주소 (비워두면 링크가 표시되지 않습니다)
CONTACT = ''

# ── 1. GitHub Pages 데이터 폴더 ────────────────────────────────────
os.makedirs(f'{DST}/data', exist_ok=True)
if os.path.isdir(f'{DST}/data/item'):
    shutil.rmtree(f'{DST}/data/item')
shutil.copy(f'{SRC}/index.json', f'{DST}/data/index.json')
shutil.copytree(f'{SRC}/item', f'{DST}/data/item')
open(f'{DST}/.nojekyll', 'w').close()
n_items = len(json.load(open(f'{SRC}/index.json', encoding='utf-8'))['items'])

# ── 2. CSS ─────────────────────────────────────────────────────────
CSS = r'''
:root{
  --blue:#3182F6; --blueDark:#1B64DA; --blueBg:#EEF5FF;
  --up:#F04452; --down:#3182F6;
  --text:#191F28; --sub:#6B7684; --faint:#8B95A1;
  --line:#F2F4F6; --border:#E5E8EB; --bg:#fff;
  --r:16px;
  --font:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;padding:0}
body{font-family:var(--font);color:var(--text);background:#EDF0F3;
  font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}
.num{font-variant-numeric:tabular-nums}
button{font-family:inherit;border:0;background:none;cursor:pointer;color:inherit}
a{color:inherit}
:focus-visible{outline:3px solid var(--blue);outline-offset:2px;border-radius:8px}

#shell{max-width:520px;margin:0 auto;background:var(--bg);min-height:100vh;
  display:flex;flex-direction:column}
#app{padding-bottom:84px;flex:1}

.head{padding:28px 20px 8px}
.h1{font-size:26px;font-weight:700;letter-spacing:-.5px;margin:0}
.date{font-size:14px;color:var(--sub);margin-top:6px}

/* 검색 */
.search{margin:16px 20px 4px;display:flex;align-items:center;gap:10px;
  background:var(--line);border:2px solid transparent;border-radius:14px;padding:15px 16px}
.search:focus-within{border-color:var(--blue);background:var(--bg)}
.search input{border:0;background:none;outline:none;font-size:17px;font-weight:500;
  font-family:inherit;width:100%;color:var(--text)}
.search input::placeholder{color:var(--faint);font-weight:400}
.search svg{flex:0 0 20px;stroke:var(--sub)}
.clearq{flex:0 0 auto;color:var(--faint);font-size:20px;line-height:1;padding:4px}

.catlab{font-size:13px;font-weight:600;color:var(--faint);text-align:center;
  margin:18px 0 0;letter-spacing:.3px}
.chips{display:flex;gap:8px;padding:10px 20px 6px;overflow-x:auto;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.chip{white-space:nowrap;padding:11px 16px;border-radius:999px;background:var(--line);
  font-size:15px;font-weight:600;color:var(--sub);transition:.15s}
.chip[data-on]{background:var(--text);color:#fff}

.sec{font-size:14px;font-weight:700;color:var(--sub);padding:22px 20px 8px}
.rows{display:block}
.row{display:flex;align-items:center;gap:12px;padding:14px 20px;width:100%;
  min-height:72px;text-align:left;transition:background .12s}
.row{cursor:pointer}
.row:hover{background:#F2F6FD}
.row:hover .rname{color:var(--blue)}
.row:active{background:var(--line)}
.rank{width:22px;font-size:15px;font-weight:700;color:var(--faint);flex:0 0 22px}

/* 아이템 뱃지 (아이콘 자리) */
.ico{flex:0 0 44px;width:44px;height:44px;border-radius:12px;display:grid;place-items:center;
  font-size:15px;font-weight:700;color:#fff;letter-spacing:-.5px}
.c장비{background:#4E7FE8} .c주문서{background:#E8944E} .c소비{background:#3BA55C} .c재료{background:#8C6FE0} .c마스터리북{background:#D9538C}
.c기타{background:#7C8794}

.rmain{flex:1;min-width:0}
.rname{font-size:18px;font-weight:600;letter-spacing:-.3px;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rsub{font-size:13px;color:var(--sub);margin-top:3px}
.rprice{text-align:right;font-size:18px;font-weight:700;white-space:nowrap}
.chg{font-size:14px;font-weight:600;margin-top:3px}
.up{color:var(--up)} .down{color:var(--down)} .flat{color:var(--sub)}
.star{flex:0 0 auto;padding:10px;color:#D1D6DB;font-size:0}
.star[data-on]{color:#FFB800}

/* 상세 */
.nav{display:flex;align-items:center;height:60px;padding:0 12px;position:sticky;top:0;
  background:var(--bg);z-index:5;border-bottom:1px solid var(--line)}
.back,.iconbtn{width:44px;height:44px;display:grid;place-items:center;border-radius:12px;color:var(--sub)}
.back:hover,.iconbtn:hover{background:var(--line)}
.navsp{flex:1}
.fav[data-on]{color:#FFB800}
.detail{padding:16px 20px 0}
.dhead{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.dico{flex:0 0 52px;width:52px;height:52px;border-radius:14px;display:grid;place-items:center;
  font-size:17px;font-weight:700;color:#fff}
.dcat{display:inline-block;font-size:13px;font-weight:600;color:var(--blueDark);
  background:var(--blueBg);padding:4px 10px;border-radius:8px;margin-bottom:6px}
.dname{font-size:22px;font-weight:700;letter-spacing:-.5px;margin:0}

.pricebox{background:linear-gradient(180deg,#F9FBFF,#fff);border:1px solid var(--border);
  border-radius:var(--r);padding:20px;margin-bottom:8px}
.plabel{font-size:14px;color:var(--sub);font-weight:600}
.dprice{font-size:36px;font-weight:700;letter-spacing:-1.2px;line-height:1.15;margin-top:6px}
.dunit{font-size:20px;font-weight:600;color:var(--sub);margin-left:4px}
.dfull{font-size:14px;color:var(--sub);margin-top:4px}

/* 그래프 */
.chart{margin:22px 0 6px;height:180px;position:relative;padding-left:56px}
.chart svg{width:100%;height:100%;display:block}
.ygrid{position:absolute;left:56px;right:0;top:0;bottom:0;display:flex;
  flex-direction:column;justify-content:space-between;pointer-events:none}
.yline{border-top:1px solid var(--line);position:relative}
.yline span{position:absolute;left:-56px;top:-9px;width:48px;text-align:right;
  font-size:12px;color:var(--faint);font-variant-numeric:tabular-nums}
.plot{position:relative;height:100%}
.pt{position:absolute;width:9px;height:9px;margin:-4.5px 0 0 -4.5px;border-radius:50%;
  background:#fff;border:2px solid var(--blue);opacity:0;animation:fade .3s .5s forwards}
.grid{stroke:var(--line);stroke-width:1;vector-effect:non-scaling-stroke}
.line{fill:none;stroke:var(--blue);stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}
.plot svg{animation:reveal .6s cubic-bezier(.22,.61,.36,1) both}
@keyframes reveal{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
.area{fill:url(#g);opacity:0;animation:fade .5s .35s forwards}
.dot{fill:#fff;stroke:var(--blue);stroke-width:2;opacity:0;animation:fade .3s .5s forwards;
  vector-effect:non-scaling-stroke}
@keyframes fade{to{opacity:1}}
@media(prefers-reduced-motion:reduce){
  .line,.area,.pt,.plot svg{animation:none;opacity:1;clip-path:none}
}
.ylab{font-size:11px;fill:var(--faint)}
.xaxis{display:flex;justify-content:space-between;font-size:12px;color:var(--sub);
  padding:0 2px;margin-top:8px}

/* 기간 요약 카드 */
.stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:18px 0 4px}
.stat{background:var(--bg);border:1px solid var(--border);border-radius:14px;padding:16px 14px}
.slabel{font-size:13px;color:var(--sub);font-weight:600}
.sval{font-size:20px;font-weight:700;margin-top:6px;letter-spacing:-.5px}
.snote{font-size:12px;color:var(--faint);margin-top:3px}

/* 거래 기록 */
.tbar{display:flex;align-items:center;justify-content:space-between;gap:8px;
  padding:22px 0 10px}
.tbar .sec{padding:0}
.sortbtns{display:flex;gap:6px}
.optsearch{flex:1;min-width:130px;max-width:240px;margin:0 10px}
.optsearch input{width:100%;border:1.5px solid var(--border);border-radius:10px;
  padding:9px 12px;font-size:14px;font-family:inherit;outline:none;color:var(--text)}
.optsearch input:focus{border-color:var(--blue)}
.optbox{border:1px solid var(--border);border-radius:16px;padding:18px;margin:20px 0 4px}
.optgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:10px}
.optcell{background:var(--line);border-radius:12px;padding:12px}
.optk{font-size:12px;color:var(--sub);font-weight:600}
.optv{font-size:16px;font-weight:700;margin-top:4px}
.sortb{padding:8px 12px;border-radius:10px;background:var(--line);font-size:14px;
  font-weight:600;color:var(--sub)}
.sortb[data-on]{background:var(--text);color:#fff}
.trade{display:flex;align-items:center;gap:12px;
  padding:14px 0;border-bottom:1px solid var(--line);min-height:56px}
.trade:last-child{border:0}
.ttime{flex:0 0 96px;font-size:14px;color:var(--sub);line-height:1.4}
.tmid{flex:1;min-width:0}
.topt{font-size:13px;color:var(--sub);line-height:1.5;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tqtybadge{display:inline-block;font-size:12px;font-weight:600;color:var(--sub);
  background:var(--line);border-radius:7px;padding:3px 8px}
.tprice{flex:0 0 auto;font-size:16px;font-weight:700;text-align:right;white-space:nowrap}

/* 관련 아이템 */
.related{margin:26px 0 0;border-top:8px solid var(--line);
  margin-left:-20px;margin-right:-20px;padding:0 20px}

.hit{position:absolute;top:0;bottom:0;cursor:pointer}
.tip{position:absolute;background:var(--text);color:#fff;border-radius:12px;
  padding:11px 14px;font-size:13px;line-height:1.7;white-space:nowrap;pointer-events:none;
  opacity:0;transition:opacity .12s;transform:translate(-50%,-118%);z-index:15}
.tip[data-on]{opacity:1}
.tipd{font-weight:700;font-size:14px;margin-bottom:5px}
.tiprow{display:flex;justify-content:space-between;gap:18px}
.tipk{color:#B0B8C1}
.tipv{font-weight:600;font-variant-numeric:tabular-nums}
.range{display:flex;gap:6px;margin:20px 0 0}
.rangeb{padding:9px 16px;border-radius:10px;background:var(--line);font-size:14px;
  font-weight:600;color:var(--sub)}
.rangeb[data-on]{background:var(--text);color:#fff}
.pager{display:flex;align-items:center;justify-content:center;gap:6px;padding:22px 0 4px}
.pgb{min-width:40px;height:40px;padding:0 12px;border-radius:10px;font-size:15px;
  font-weight:600;color:var(--sub);background:var(--bg);border:1px solid var(--border)}
.pgb[data-on]{background:var(--text);color:#fff;border-color:var(--text)}
.pgb:disabled{opacity:.35;cursor:default}
.pgnote{text-align:center;font-size:13px;color:var(--faint);padding-bottom:8px}
.morewrap{padding:20px;text-align:center}
.more{padding:14px 28px;border-radius:12px;border:1px solid var(--border);
  font-size:15px;font-weight:600;color:var(--sub);background:var(--bg)}
.more:hover{border-color:var(--blue);color:var(--blue)}
.empty{text-align:center;padding:70px 20px;color:var(--sub);font-size:16px}
.emptyT{font-size:18px;font-weight:600;color:var(--text);margin-bottom:8px}
.sk{background:var(--line);border-radius:8px;animation:pulse 1.2s ease-in-out infinite}
@keyframes pulse{50%{opacity:.5}}

.tabs{position:fixed;bottom:0;left:0;right:0;max-width:520px;margin:0 auto;
  display:flex;background:rgba(255,255,255,.96);backdrop-filter:blur(12px);
  border-top:1px solid var(--border);padding-bottom:env(safe-area-inset-bottom);z-index:20}
.tab{flex:1;padding:12px 0 14px;font-size:12px;font-weight:600;color:var(--faint);
  display:flex;flex-direction:column;align-items:center;gap:4px;min-height:60px}
.tab[data-on]{color:var(--text)}
.tab svg{stroke:currentColor;fill:none;stroke-width:2}
.foot{text-align:center;font-size:13px;color:var(--sub);padding:30px 20px 8px;line-height:1.7}

/* 토스트 */
#toast{position:fixed;left:50%;bottom:96px;transform:translate(-50%,20px);
  background:var(--text);color:#fff;padding:13px 20px;border-radius:12px;
  font-size:15px;font-weight:600;opacity:0;pointer-events:none;transition:.25s;z-index:50}
#toast[data-on]{opacity:1;transform:translate(-50%,0)}

#sitefoot{border-top:1px solid var(--line);padding:28px 20px 100px;
  font-size:13px;color:var(--sub);line-height:1.8}
#sitefoot nav{display:flex;flex-wrap:wrap;gap:10px 20px;margin-bottom:16px}
#sitefoot nav a{font-weight:600;color:var(--text);text-decoration:none;font-size:14px}
#sitefoot nav a:hover{color:var(--blue)}
#sitefoot p{margin:0 0 6px}

.page{padding:8px 20px 40px;max-width:720px;margin:0 auto}
.ptitle{font-size:28px;font-weight:700;letter-spacing:-.5px;margin:24px 0 20px}
.pbody{font-size:16px;line-height:1.85;color:#333D4B;word-break:keep-all}
.pbody h2{font-size:19px;font-weight:700;color:var(--text);margin:34px 0 10px}
.pbody ul{padding-left:20px} .pbody li{margin:6px 0}
.pbody a{color:var(--blue)}
.homelink{display:inline-block;margin:8px 0 0;padding:12px 20px;border-radius:12px;
  background:var(--line);font-weight:600;font-size:15px;text-decoration:none}

.head.center{text-align:center}
.head.center + .search{margin-left:auto;margin-right:auto}
.head.center ~ .chips{justify-content:center}

/* ── 태블릿 ── */
@media(min-width:768px){
  #shell{max-width:768px}
  .tabs{max-width:768px}
  .rows{max-width:760px;margin:0 auto}
  .row{border-radius:12px}
  .stats{grid-template-columns:repeat(4,minmax(0,1fr))}
  .detail{padding:16px 28px 0}
  .related{margin-left:-28px;margin-right:-28px;padding:0 28px}
}

/* ── 데스크톱 ── */
@media(min-width:1080px){
  body{background:#F7F8FA}
  #shell{max-width:1120px;box-shadow:0 0 0 1px rgba(0,0,0,.04)}
  #app{padding-bottom:0}
  .tabs{position:sticky;top:0;bottom:auto;order:-1;max-width:none;width:100%;
    justify-content:flex-start;gap:4px;padding:0 20px;
    border-top:0;border-bottom:1px solid var(--border)}
  .tab{flex:0 0 auto;flex-direction:row;gap:8px;padding:18px 18px;font-size:16px;
    border-bottom:2px solid transparent;min-height:0}
  .tab[data-on]{border-bottom-color:var(--text)}
  .head{padding:34px 28px 8px}
  .h1{font-size:32px}
  .search{margin:20px auto 4px;max-width:760px}
  .chips{padding:16px 28px 6px}
  .sec{padding:24px 28px 8px}
  .rows{max-width:820px;margin:0 auto;padding:0 8px}
  .detail{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 44px;
    align-items:start;padding:20px 28px 40px}
  .detail{display:block;max-width:1040px;margin:0 auto}
  .trades{max-width:none}
  .chart{height:220px}
  .foot{grid-column:1 / -1}
  .related{margin-left:0;margin-right:0;padding:0;border-top:1px solid var(--border);padding-top:20px}
  #sitefoot{padding:32px 28px}
  #toast{bottom:40px}
}

/* 주문서 작 계산기 */
.simgrid{padding:8px 20px 0}
.simcol{min-width:0}
.step{display:flex;align-items:center;gap:10px;margin:28px 0 0}
.stepn{flex:0 0 26px;width:26px;height:26px;border-radius:50%;background:var(--text);
  color:#fff;font-size:14px;font-weight:700;display:grid;place-items:center}
.stepn[data-done]{background:var(--blue)}
.steptitle{font-size:17px;font-weight:700}
.fieldlab{font-size:13px;font-weight:600;color:var(--sub);margin:16px 0 8px}
.chips2{display:flex;flex-wrap:wrap;gap:8px}
.hint{font-size:13px;color:var(--sub);margin:10px 0 0;line-height:1.6}
.hint b{color:var(--text)}
.warn{font-size:13px;color:#A64B00;background:#FFF7ED;border-radius:10px;
  padding:12px 14px;margin:10px 0 0;line-height:1.6}
.warn b{color:#7A3800}
.linkb{font-size:13px;font-weight:600;color:var(--blue);text-decoration:underline}
.picked{display:flex;align-items:center;gap:12px;width:100%;text-align:left;
  border:1px solid var(--border);border-radius:14px;padding:14px;margin-top:12px}
.picked:hover{border-color:var(--blue)}
.change{font-size:14px;font-weight:600;color:var(--blue);flex:0 0 auto}
.rateb{font-size:13px;font-weight:700;color:var(--blueDark);background:var(--blueBg);
  padding:6px 10px;border-radius:9px;white-space:nowrap;flex:0 0 auto}

.picklist{display:flex;flex-direction:column;gap:2px;margin-top:4px;
  max-height:420px;overflow-y:auto}
.pickrow{display:flex;align-items:center;gap:12px;width:100%;text-align:left;
  padding:12px 10px;border-radius:12px;min-height:62px}
.pickrow{cursor:pointer}
.pickrow:hover{background:#F2F6FD}
.pkmain{flex:1;min-width:0}
.pkname{display:block;font-size:16px;font-weight:600;overflow:hidden;
  text-overflow:ellipsis;white-space:nowrap}
.pksub{display:block;font-size:13px;color:var(--sub);margin-top:2px}
.pkprice{font-size:15px;font-weight:700;white-space:nowrap;flex:0 0 auto}

.resbox{background:#F9FAFB;border-radius:16px;padding:20px;margin-top:12px}
.rescap{font-size:13px;font-weight:700;color:var(--sub);margin-bottom:14px;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bigrow{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
  padding:9px 0;font-size:15px;color:var(--sub)}
.bigrow b{font-size:19px;font-weight:700;color:var(--text);letter-spacing:-.4px}
.lucky{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:10px}
.lucky>div{border:1px solid var(--border);border-radius:14px;padding:14px}
.lucklab{font-size:12px;color:var(--sub);font-weight:600}
.luckval{font-size:19px;font-weight:700;margin-top:5px}
.dist{display:flex;flex-direction:column;gap:7px}
.distrow{display:flex;align-items:center;gap:10px}
.dk{flex:0 0 44px;font-size:14px;font-weight:600;color:var(--sub)}
.dbar{flex:1;height:22px;background:var(--line);border-radius:6px;overflow:hidden}
.dbar i{display:block;height:100%;background:var(--blue);border-radius:6px;
  animation:grow .5s cubic-bezier(.22,.61,.36,1) both}
@keyframes grow{from{width:0 !important}}
.dv{flex:0 0 54px;text-align:right;font-size:14px;font-weight:600}

.timing{border:1px solid var(--border);border-radius:16px;padding:18px;margin:20px 0 4px}
.timT{font-size:16px;font-weight:700;margin-bottom:12px}
.timrow{display:flex;align-items:flex-start;gap:10px;padding:8px 0;font-size:14px;
  color:#333D4B;line-height:1.6}
.timrow b{color:var(--text)}
.timico{flex:0 0 22px;font-size:16px;line-height:1.4}
.pos{display:block;margin-top:8px}
.posbar{display:block;height:10px;border-radius:5px;position:relative;
  background:linear-gradient(90deg,#3182F6,#8FBEF8 40%,#E5E8EB 55%,#F8A9B0 70%,#F04452)}
.posmark{position:absolute;top:-5px;width:4px;height:20px;border-radius:2px;
  background:var(--text);transform:translateX(-2px)}
.posscale{display:flex;justify-content:space-between;font-size:11px;color:var(--faint);margin-top:5px}
.posbar .posmark{display:block}

/* 직접 강화 */
.modetabs{display:flex;gap:8px;padding:16px 20px 0;max-width:760px;margin:0 auto}
.modeb{flex:1;padding:13px 0;border-radius:12px;background:var(--line);
  font-size:15px;font-weight:700;color:var(--sub)}
.modeb[data-on]{background:var(--text);color:#fff}
.ecard{border:1px solid var(--border);border-radius:16px;padding:24px 20px;
  text-align:center;margin-top:12px;position:relative;overflow:hidden}
.ename{font-size:18px;font-weight:700}
.estat{font-size:15px;color:var(--blueDark);font-weight:700;margin-top:6px}
.edots{display:flex;justify-content:center;gap:7px;margin:16px 0 12px;flex-wrap:wrap}
.edot{width:26px;height:26px;border-radius:50%;border:2px solid var(--border);
  display:grid;place-items:center;font-size:13px;font-weight:800}
.edot.ok{border-color:#12B76A;background:#E8F8F0;color:#0E9256}
.edot.no{border-color:#F04452;background:#FEECEE;color:#D42B3A}
.einfo{font-size:14px;color:var(--sub)}
.einfo b{color:var(--text)}
.eflash{margin-top:14px;padding:11px;border-radius:12px;font-size:16px;font-weight:800;
  animation:pop .35s cubic-bezier(.34,1.56,.64,1)}
.eflash.ok{background:#E8F8F0;color:#0E9256}
.eflash.no{background:#FEECEE;color:#D42B3A}
.eflash.wok{background:var(--blueBg);color:var(--blueDark);font-size:14px}
@keyframes pop{from{transform:scale(.7);opacity:0}}
.shake-ok{animation:bump .3s}
.shake-no{animation:shk .3s}
@keyframes bump{30%{transform:translateY(-5px)}}
@keyframes shk{25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
@media(prefers-reduced-motion:reduce){.eflash,.shake-ok,.shake-no{animation:none}}
.ebtn{display:block;width:100%;margin-top:14px;padding:16px;border-radius:14px;
  background:var(--blue);color:#fff;font-size:17px;font-weight:800;transition:.12s}
.ebtn:hover{background:var(--blueDark)}
.ebtn:active{transform:scale(.98)}
.ebtnsub{display:block;font-size:13px;font-weight:600;opacity:.85;margin-top:3px}
.ebtn.retry{background:var(--text)}
.ecost{margin-top:12px;text-align:center;font-size:14px;color:var(--sub)}
.ecost b{color:var(--text);font-size:16px}
.edone{border:1px solid var(--border);border-radius:16px;padding:20px;margin-top:14px;text-align:center}
.edoneT{font-size:19px;font-weight:800}
.edoneS{font-size:14px;color:var(--sub);margin-top:8px;line-height:1.6}
.edoneS b{color:var(--text)}
.elog{display:flex;flex-direction:column;gap:6px}
.elogrow{font-size:14px;color:var(--sub);padding:9px 12px;background:var(--line);border-radius:10px}

.reshold{border:1px dashed var(--border);border-radius:16px;padding:44px 24px;
  text-align:center;margin-top:12px}
.resicon{font-size:34px;margin-bottom:12px}
.resholdT{font-size:17px;font-weight:700;line-height:1.5}
.resholdS{font-size:14px;color:var(--sub);margin-top:8px;line-height:1.6}

@media(min-width:768px){ .simgrid{padding:8px 28px 0} }
@media(min-width:1080px){
  .simgrid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);
    gap:0 44px;align-items:start;padding:8px 28px 0}
  .simcol:last-child{position:sticky;top:84px}
  .step:first-child{margin-top:8px}
}
@media(min-width:1080px){
  .simwrap{padding:8px 28px 0;max-width:680px}
  .lucky{grid-template-columns:repeat(2,minmax(0,1fr))}
}

/* ══════════ v5: 와이드 레이아웃 · 광고 레일 ══════════ */
#shell{display:block}
body.static_page #app{display:none}
body.static_page .tabs{display:none}
#content{min-width:0}
#rail{display:none}

/* 데스크톱 상단 네비 정렬 (order 동작하도록 #app 을 flex 로) */
@media(min-width:1080px){
  #app{display:flex;flex-direction:column}
  .tabs{order:-1}
}

/* 와이드: 본문 + 광고 레일 */
@media(min-width:1400px){
  #shell{max-width:1560px;display:flex;flex-direction:row;align-items:flex-start}
  #content{flex:1 1 auto;min-width:0;border-right:1px solid var(--line);
    display:flex;flex-direction:column;align-items:center}
  #app,#sitefoot{width:100%;max-width:1120px}
  #rail{display:block;flex:0 0 320px;width:320px;position:sticky;top:0;padding:20px;
    max-height:100vh;overflow-y:auto;scrollbar-width:thin}
  .head{padding-left:32px;padding-right:32px}
  .sec{max-width:820px;margin:0 auto;padding-left:16px;padding-right:16px}
  .morewrap{max-width:820px;margin:0 auto}
}
@media(min-width:1700px){
  #shell{max-width:1680px}
  #rail{flex:0 0 336px;width:336px}
  #app,#sitefoot{max-width:1200px}
}

/* 레일 위젯 */
.railbox{border:1px solid var(--border);border-radius:14px;padding:16px;margin-bottom:16px}
.railtitle{font-size:14px;font-weight:700;margin-bottom:12px}
.railrow{display:flex;align-items:center;gap:10px;width:100%;text-align:left;
  padding:9px 0;border-bottom:1px solid var(--line)}
.railrow:last-child{border:0}
.railrank{flex:0 0 18px;font-size:13px;font-weight:700;color:var(--faint)}
.railname{flex:1;font-size:14px;font-weight:600;overflow:hidden;
  text-overflow:ellipsis;white-space:nowrap}
.railprice{font-size:13px;font-weight:700;white-space:nowrap}

/* 광고 슬롯 */
.adslot{margin:20px 0;text-align:center;overflow:hidden}
.adslot.inline{margin:24px 0}
.adlabel{font-size:11px;color:#B0B8C1;letter-spacing:.5px;margin-bottom:6px;text-align:left}
.addemo{border:1px dashed #D1D6DB;border-radius:12px;background:#FBFCFD;
  color:#B0B8C1;font-size:13px;font-weight:600;display:grid;place-items:center}

/* 적정가 판별기 */
.judge{border:1px solid var(--border);border-radius:16px;padding:18px;margin:20px 0 4px}
.judgetitle{font-size:16px;font-weight:700;margin-bottom:4px}
.judgesub{font-size:13px;color:var(--sub);margin-bottom:14px}
.judgein{display:flex;gap:8px}
.judgein input{flex:1;min-width:0;border:2px solid var(--border);border-radius:12px;
  padding:13px 14px;font-size:17px;font-family:inherit;font-weight:600;outline:none;
  color:var(--text);font-variant-numeric:tabular-nums}
.judgein input:focus{border-color:var(--blue)}
.judgebtn{flex:0 0 auto;padding:0 20px;border-radius:12px;background:var(--text);
  color:#fff;font-weight:700;font-size:15px}
.verdict{margin-top:14px;padding:16px;border-radius:12px;background:var(--line)}
.vhead{font-size:19px;font-weight:700;letter-spacing:-.4px}
.vsub{font-size:14px;color:var(--sub);margin-top:6px;line-height:1.6}
.vbar{height:10px;border-radius:5px;margin:14px 0 8px;position:relative;
  background:linear-gradient(90deg,#3182F6,#8FBEF8 35%,#E5E8EB 50%,#F8A9B0 65%,#F04452)}
.vmark{position:absolute;top:-5px;width:4px;height:20px;border-radius:2px;
  background:var(--text);transform:translateX(-2px);transition:left .35s cubic-bezier(.22,.61,.36,1)}
.vscale{display:flex;justify-content:space-between;font-size:11px;color:var(--faint)}
.vgood{color:var(--down)} .vbad{color:var(--up)}

/* 거래 시간대 */
.hours{display:flex;align-items:flex-end;gap:2px;height:70px;margin:14px 0 6px}
.hbar{flex:1;background:var(--line);border-radius:3px 3px 0 0;position:relative;
  min-height:3px;transition:background .15s}
.hbar[data-peak]{background:var(--blue)}
.hscale{display:flex;justify-content:space-between;font-size:11px;color:var(--faint)}
.peaknote{font-size:14px;color:var(--sub);margin-top:10px;line-height:1.6}
.peaknote b{color:var(--text)}

/* 저장 탭 요약 */
.favsum{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line);
  border-radius:14px;overflow:hidden;margin:16px 20px 4px}
.favcell{background:var(--bg);padding:15px 10px;text-align:center}
.favn{font-size:22px;font-weight:700;letter-spacing:-.5px}
.favl{font-size:12px;color:var(--sub);margin-top:3px}
.favtop{margin:14px 20px 0;padding:14px 16px;border-radius:12px;background:var(--blueBg);
  font-size:14px;color:#1B4B9E;line-height:1.6}
.favtop b{font-weight:700}
@media(min-width:1080px){ .favsum,.favtop{margin-left:28px;margin-right:28px} }
'''

# ── 3. JS ──────────────────────────────────────────────────────────
JS = r'''
var DATA_BASE = '__DATA_BASE__';
var CONTACT = '__CONTACT__';

var D = null, byId = {}, cache = {};
var FAV = 'lona_fav';
function fav(){ try { return JSON.parse(localStorage.getItem(FAV) || '[]'); } catch(e){ return []; } }
/* 목록(index.json)은 1분 단위로 새로 확인하고,
   아이템 파일은 데이터 갱신일이 바뀔 때만 새로 받습니다. */
function bustFor(path){
  if (path === '/index.json') return '?t=' + Math.floor(Date.now()/60000);
  return '?v=' + (D && D.updated ? D.updated : 'x');
}

function get(path){
  if (cache[path]) return Promise.resolve(cache[path]);
  return fetch(DATA_BASE + path + bustFor(path)).then(function(r){
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }).then(function(j){ cache[path] = j; return j; });
}

/* 숫자 */
function money(n){
  if (n >= 100000000){ var v = n/100000000;
    return (v >= 10 ? Math.round(v) : v.toFixed(1).replace(/\.0$/,'')) + '억'; }
  if (n >= 10000) return Math.round(n/10000).toLocaleString() + '만';
  return n.toLocaleString();
}
function full(n){ return n.toLocaleString() + ' 메소'; }
function chgHtml(c){
  if (!c) return '<div class="chg flat">어제와 같음</div>';
  var up = c > 0;
  return '<div class="chg ' + (up?'up':'down') + '">' + (up?'▲':'▼') + ' ' + Math.abs(c) + '%</div>';
}

/* 초성 검색 */
var CHO = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'];
function cho(s){
  var o = '';
  for (var i = 0; i < s.length; i++){
    var c = s.charCodeAt(i) - 44032;
    o += (c >= 0 && c <= 11171) ? CHO[Math.floor(c/588)] : s[i];
  }
  return o;
}

/* 아이콘 자리 뱃지 */
var SHORT = {'장비':'장','주문서':'주','소비':'소','재료':'재','마스터리북':'북','기타':'기'};
function ico(cat, cls){
  return '<span class="' + (cls||'ico') + ' c' + cat + '">' + (SHORT[cat]||'?') + '</span>';
}

var app = document.getElementById('app');
var state = { q:'', cat:'전체', limit:36 };
function go(h){ location.hash = h; }

function toast(msg){
  var t = document.getElementById('toast');
  if (!t){ t = document.createElement('div'); t.id = 'toast'; document.body.appendChild(t); }
  t.textContent = msg;
  t.setAttribute('data-on','');
  clearTimeout(t._x);
  t._x = setTimeout(function(){ t.removeAttribute('data-on'); }, 1800);
}

var CATS = ['전체','장비','주문서','소비','재료','마스터리북','기타'];
var foot = '<div class="foot">실제 거래 기록을 모아 계산한 참고용 시세입니다.<br/>' +
  '시세를 흔드는 극단적인 매물은 빼고 계산했어요.' +
  (CONTACT ? '<br/><a href="mailto:' + CONTACT + '" style="color:#3182F6;font-weight:600">건의하기</a>' : '') +
  '</div>';

function tabs(on){
  var T = [['','홈','M3 10.5 12 3l9 7.5V21H3z'],
           ['/search','시세 검색','M11 4a7 7 0 1 1 0 14 7 7 0 0 1 0-14zM20 20l-3.5-3.5'],
           ['/rank','랭킹','M4 20V10M10 20V4M16 20v-8M22 20h-20'],
           ['/sim','작 계산','M12 2v20M5 9l7-7 7 7M5 15l7 7 7-7'],
           ['/fav','저장','M12 3l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.8 6.2 20.9l1.1-6.5L2.6 9.8l6.5-.9z']];
  return '<nav class="tabs">' + T.map(function(t){
    return '<button class="tab" ' + (on===t[0]?'data-on':'') + ' onclick="go(\'' + (t[0]||'/') + '\')">' +
      '<svg width="24" height="24" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="' + t[2] + '"/></svg>' + t[1] + '</button>';
  }).join('') + '</nav>';
}

var STAR = 'M12 3l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.8 6.2 20.9l1.1-6.5L2.6 9.8l6.5-.9z';
function rowHtml(it, i){
  var on = fav().indexOf(it.id) >= 0;
  return '<div class="row">' +
    (i != null ? '<span class="rank num">' + (i+1) + '</span>' : '') +
    ico(it.cat) +
    '<button class="rmain" style="text-align:left" onclick="go(\'/item/' + it.id + '\')">' +
      '<div class="rname">' + it.n + '</div>' +
      '<div class="rsub">거래 ' + it.v.toLocaleString() + '건</div></button>' +
    '<button class="rprice num" onclick="go(\'/item/' + it.id + '\')">' +
      money(it.p) + chgHtml(it.c) + '</button>' +
    '<button class="star" ' + (on?'data-on':'') + ' aria-label="저장" onclick="quickFav(\'' + it.id + '\',this)">' +
      '<svg width="22" height="22" viewBox="0 0 24 24" fill="' + (on?'currentColor':'none') +
      '" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="' + STAR + '"/></svg>' +
    '</button></div>';
}
function quickFav(id, el){
  var f = fav(), i = f.indexOf(id), on = i < 0;
  if (on) f.push(id); else f.splice(i,1);
  localStorage.setItem(FAV, JSON.stringify(f));
  if (on) el.setAttribute('data-on',''); else el.removeAttribute('data-on');
  el.querySelector('svg').setAttribute('fill', on ? 'currentColor' : 'none');
  toast(on ? '저장했어요' : '저장을 해제했어요');
}

function skeleton(){
  var r = '';
  for (var i = 0; i < 8; i++){
    r += '<div class="row"><div class="sk" style="width:44px;height:44px;border-radius:12px"></div>' +
         '<div style="flex:1"><div class="sk" style="width:45%;height:18px"></div>' +
         '<div class="sk" style="width:25%;height:13px;margin-top:7px"></div></div>' +
         '<div class="sk" style="width:70px;height:18px"></div></div>';
  }
  return '<div class="rows">' + r + '</div>';
}

/* ── 홈 ── */
function home(){
  app.innerHTML =
    '<div class="head center"><h1 class="h1">로나 시세</h1>' +
      '<div class="date">' + (D ? D.updated.replace(/-/g,'.') + ' 기준 · 아이템 ' +
        D.items.length.toLocaleString() + '종' : '불러오는 중') + '</div></div>' +
    '<div class="search">' +
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round">' +
      '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>' +
      '<input id="q" placeholder="아이템 이름 검색 (예: 자쿰의 투구)" value="' + state.q + '" autocomplete="off"/>' +
      (state.q ? '<button class="clearq" onclick="clearQ()" aria-label="지우기">&#10005;</button>' : '') +
    '</div>' +
    '<div class="catlab">카테고리로 보기</div>' +
    '<div class="chips">' + CATS.map(function(c){
      return '<button class="chip" ' + (state.cat===c?'data-on':'') +
             ' onclick="setCat(\'' + c + '\')">' + c + '</button>'; }).join('') + '</div>' +
    ad('top') + '<div id="list">' + (D ? '' : skeleton()) + '</div>' +
    ad('foot') + foot + tabs('');
  var inp = document.getElementById('q');
  if (inp){
    inp.oninput = function(e){ state.q = e.target.value; state.limit = 36; list(); };
    if (state.q){ inp.focus(); inp.setSelectionRange(state.q.length, state.q.length); }
  }
  if (D) list();
}
function setCat(c){ state.cat = c; state.limit = 36; home(); }
function clearQ(){ state.q = ''; state.limit = 36; home(); }
function more(){ state.limit += 36; list(); }

function list(){
  var q = state.q.trim().toLowerCase(), qc = cho(q).replace(/\s/g,'');
  var r = D.items.filter(function(i){ return state.cat === '전체' || i.cat === state.cat; });
  if (q) r = r.filter(function(i){
    return i.n.toLowerCase().indexOf(q) >= 0 || i._c.indexOf(qc) >= 0; });
  var el = document.getElementById('list');
  if (!el) return;
  if (!r.length){
    el.innerHTML = '<div class="empty"><div class="emptyT">검색 결과가 없어요</div>' +
      '이름 일부만 입력해 보세요. 초성 검색도 됩니다 (예: ㅈㅋㅇㅌㄱ)</div>';
    return;
  }
  var shown = r.slice(0, state.limit);
  el.innerHTML = '<div class="sec">' + (q ? '검색 결과 ' + r.length + '개' : '많이 거래된 아이템') + '</div>' +
    '<div class="rows">' + shown.map(function(i, n){ return rowHtml(i, q ? null : n); }).join('') + '</div>' +
    (r.length > shown.length
      ? '<div class="morewrap"><button class="more" onclick="more()">' +
        (r.length - shown.length).toLocaleString() + '개 더 보기</button></div>' : '');
}

/* ── 시세 검색 ── */
function searchPage(){
  app.innerHTML =
    '<div class="head center"><h1 class="h1">시세 검색</h1>' +
      '<div class="date">아이템 이름이나 초성으로 찾아보세요 (예: ㅈㅋㅇㅌㄱ)</div></div>' +
    '<div class="search">' +
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round">' +
      '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>' +
      '<input id="q" placeholder="아이템 이름 검색" value="' + state.q + '" autocomplete="off"/>' +
      (state.q ? '<button class="clearq" onclick="clearQS()" aria-label="지우기">&#10005;</button>' : '') +
    '</div>' +
    '<div class="catlab">카테고리로 보기</div>' +
    '<div class="chips">' + CATS.map(function(c){
      return '<button class="chip" ' + (state.cat===c?'data-on':'') +
             ' onclick="setCatS(\'' + c + '\')">' + c + '</button>'; }).join('') + '</div>' +
    '<p class="hint" style="text-align:center;margin-top:4px">장비의 판매 옵션은 아이템 화면의 ' +
      '거래 기록에서 검색할 수 있어요.</p>' +
    '<div id="list">' + (D ? '' : skeleton()) + '</div>' + foot + tabs('/search');
  var inp = document.getElementById('q');
  if (inp){
    inp.oninput = function(e){ state.q = e.target.value; state.limit = 36; list(); };
    inp.focus();
  }
  if (D) list();
}
function setCatS(c){ state.cat = c; state.limit = 36; searchPage(); }
function clearQS(){ state.q = ''; state.limit = 36; searchPage(); }

/* ── 랭킹 ── */
var rmode = 'v';
function rank(){
  var L = [['v','거래 많은'],['up','가격 오른'],['down','가격 내린']];
  var r = D.items.slice();
  if (rmode === 'v') r.sort(function(a,b){ return b.v - a.v; });
  if (rmode === 'up') r = r.filter(function(i){ return i.v >= 100; }).sort(function(a,b){ return b.c - a.c; });
  if (rmode === 'down') r = r.filter(function(i){ return i.v >= 100; }).sort(function(a,b){ return a.c - b.c; });
  app.innerHTML =
    '<div class="head"><h1 class="h1">이번 주 랭킹</h1>' +
      '<div class="date">반짝 팔린 아이템은 빼고, 거래 100건 이상만 순위에 넣었어요</div></div>' +
    '<div class="chips">' + L.map(function(k){
      return '<button class="chip" ' + (rmode===k[0]?'data-on':'') +
             ' onclick="setR(\'' + k[0] + '\')">' + k[1] + '</button>'; }).join('') + '</div>' +
    '<div class="sec">TOP 30</div>' +
    '<div class="rows">' + r.slice(0,30).map(function(i,n){ return rowHtml(i,n); }).join('') + '</div>' +
    foot + tabs('/rank');
}
function setR(k){ rmode = k; rank(); }

/* ── 저장 ── */
function favSummary(r){
  var up = r.filter(function(i){ return i.c > 0; });
  var dn = r.filter(function(i){ return i.c < 0; });
  var top = r.slice().sort(function(a,b){ return Math.abs(b.c) - Math.abs(a.c); })[0];
  var h = '<div class="favsum">' +
    '<div class="favcell"><div class="favn up">' + up.length + '</div><div class="favl">올랐어요</div></div>' +
    '<div class="favcell"><div class="favn down">' + dn.length + '</div><div class="favl">내렸어요</div></div>' +
    '<div class="favcell"><div class="favn">' + (r.length - up.length - dn.length) + '</div>' +
      '<div class="favl">그대로예요</div></div></div>';
  if (top && top.c){
    h += '<div class="favtop"><b>' + top.n + '</b>이(가) 가장 크게 ' +
      (top.c > 0 ? '올랐어요' : '내렸어요') + '. ' +
      (top.c > 0 ? '+' : '') + top.c + '% · 지금 ' + money(top.p) + ' 메소</div>';
  }
  return h;
}
function favs(){
  var r = fav().map(function(id){ return byId[id]; }).filter(Boolean);
  app.innerHTML = '<div class="head"><h1 class="h1">저장한 아이템</h1>' +
    (r.length ? '<div class="date">' + r.length + '개를 지켜보고 있어요</div>' : '') + '</div>' +
    (r.length ? favSummary(r) : '') +
    (r.length ? '<div class="rows">' + r.map(function(i){ return rowHtml(i); }).join('') + '</div>'
      : '<div class="empty"><div class="emptyT">저장한 아이템이 없어요</div>' +
        '목록에서 별표(☆)를 누르면 여기에 모입니다</div>') + tabs('/fav');
}

/* ── 기간 요약 ── */
function periodAvg(series, days){
  var s = series.slice(-days);
  if (!s.length) return null;
  var w = 0, sum = 0;
  s.forEach(function(d){ sum += d.p * d.n; w += d.n; });
  return w ? Math.round(sum / w) : null;
}
function statCards(series, it){
  var span = series.length;
  var defs = [[7,'최근 7일'],[14,'최근 2주'],[30,'최근 1달'],[90,'최근 3달']];
  var cards = '<div class="stat"><div class="slabel">전체 거래</div>' +
    '<div class="sval num">' + it.v.toLocaleString() + '건</div>' +
    '<div class="snote">' + span + '일간</div></div>';
  var shown = 0;
  defs.forEach(function(d){
    if (span < d[0] || shown >= 3) return;
    var v = periodAvg(series, d[0]);
    if (v == null) return;
    shown++;
    cards += '<div class="stat"><div class="slabel">' + d[1] + '</div>' +
      '<div class="sval num">' + money(v) + '</div>' +
      '<div class="snote">보통 이 가격</div></div>';
  });
  if (!shown){
    var v = periodAvg(series, span);
    cards += '<div class="stat"><div class="slabel">' + span + '일 평균</div>' +
      '<div class="sval num">' + money(v) + '</div><div class="snote">보통 이 가격</div></div>';
  }
  var ps = series.map(function(x){ return x.p; });
  cards += '<div class="stat"><div class="slabel">기간 내 최저 · 최고</div>' +
    '<div class="sval num">' + money(Math.min.apply(null,ps)) + ' ~ ' + money(Math.max.apply(null,ps)) + '</div>' +
    '<div class="snote">하루 대표가 기준</div></div>';
  return '<div class="stats">' + cards + '</div>';
}

/* ── 상세 ── */
var tsort = 'new', tpage = 0, TPP = 20, tquery = '';
var chartRange = 30;
var curItem = null, curData = null;
function setRange(d){ chartRange = d; if (curItem) detail(curItem.id); }
function backBtn(){
  return '<button class="back" onclick="history.back()" aria-label="뒤로">' +
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" ' +
    'stroke-linecap="round" stroke-linejoin="round"><path d="m15 5-7 7 7 7"/></svg></button>';
}
function share(){
  var url = location.href;
  if (navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(url).then(function(){ toast('링크를 복사했어요'); },
      function(){ toast('복사에 실패했어요'); });
  } else { toast('주소창을 길게 눌러 복사해 주세요'); }
}
function setTsort(k){ tsort = k; tpage = 0; renderTrades(); }

function sortedTrades(){
  var r = curData.recent.slice();
  if (tquery){
    var q = tquery.toLowerCase();
    r = r.filter(function(t){ return (t.o || '').toLowerCase().indexOf(q) >= 0; });
  }
  if (tsort === 'high') r.sort(function(a,b){ return b.u - a.u; });
  if (tsort === 'low') r.sort(function(a,b){ return a.u - b.u; });
  return r;
}
function pager(total){
  var pages = Math.ceil(total / TPP);
  if (pages <= 1) return '';
  var b = '<div class="pager">' +
    '<button class="pgb" onclick="setPage(' + (tpage-1) + ')"' +
      (tpage === 0 ? ' disabled' : '') + '>&#8249;</button>';
  for (var i = 0; i < pages; i++){
    b += '<button class="pgb" ' + (i === tpage ? 'data-on' : '') +
         ' onclick="setPage(' + i + ')">' + (i+1) + '</button>';
  }
  b += '<button class="pgb" onclick="setPage(' + (tpage+1) + ')"' +
       (tpage >= pages-1 ? ' disabled' : '') + '>&#8250;</button></div>' +
    '<div class="pgnote">' + (tquery ? '옵션 검색 결과 ' : '전체 ') + total.toLocaleString() + '건 중 ' +
      (tpage*TPP+1) + '~' + Math.min(total, (tpage+1)*TPP) + '번째</div>';
  return b;
}
function setPage(i){
  var total = sortedTrades().length, pages = Math.ceil(total / TPP);
  if (i < 0 || i >= pages) return;
  tpage = i; renderTrades();
}
function tradeRows(){
  var all = sortedTrades();
  if (tquery && !all.length){
    return '<div class="empty" style="padding:36px 0"><div class="emptyT">옵션 검색 결과가 없어요</div>' +
      '다른 검색어를 넣어보세요 (예: 공격력, STR)</div>';
  }
  var r = all.slice(tpage*TPP, (tpage+1)*TPP);
  return '<div class="trades">' + r.map(function(t){
    var mid = '';
    if (t.q > 1) mid += '<span class="tqtybadge num">' + t.q.toLocaleString() + '개 · 개당가</span>';
    if (t.o) mid += (mid ? ' ' : '') + '<span class="topt">' + t.o + '</span>';
    return '<div class="trade">' +
      '<div class="ttime num">' + t.d.slice(5).replace('-','.') + '<br/>' + t.t.slice(0,5) + '</div>' +
      '<div class="tmid">' + mid + '</div>' +
      '<div class="tprice num">' + full(t.u) + '</div></div>';
  }).join('') + '</div>' + pager(all.length);
}
function renderTrades(){
  var box = document.getElementById('tradesbox');
  if (box) box.innerHTML = tradeRows();
  var ti = document.getElementById('tq');
  if (ti && ti !== document.activeElement) ti.value = tquery;
  ['new','high','low'].forEach(function(k){
    var b = document.getElementById('sb-' + k);
    if (b){ if (k === tsort) b.setAttribute('data-on',''); else b.removeAttribute('data-on'); }
  });
}

function relatedHtml(it){
  var r = D.items.filter(function(x){
    return x.cat === it.cat && x.id !== it.id && x.v >= 10;
  }).sort(function(a,b){
    return Math.abs(Math.log(a.p/it.p)) - Math.abs(Math.log(b.p/it.p));
  }).slice(0,5);
  if (!r.length) return '';
  return '<div class="related"><div class="sec" style="padding-left:0">비슷한 가격대의 ' + it.cat + '</div>' +
    '<div class="rows">' + r.map(function(i){ return rowHtml(i); }).join('') + '</div></div>';
}

function detail(id){
  var it = byId[id];
  if (!it){
    app.innerHTML = '<div class="empty"><div class="emptyT">아이템을 찾을 수 없어요</div>' +
      '<button class="chip" style="margin-top:14px" onclick="go(\'/\')">홈으로 가기</button></div>' + tabs('');
    return;
  }
  curItem = it; tsort = 'new'; tpage = 0; tquery = '';
  app.innerHTML = '<div class="nav">' + backBtn() + '</div>' +
    '<div class="detail"><div class="dhead">' + ico(it.cat,'dico') +
    '<div><span class="dcat">' + it.cat + '</span><h1 class="dname">' + it.n + '</h1></div></div>' +
    '<div class="sk" style="width:100%;height:120px;border-radius:16px"></div>' +
    '<div class="sk" style="width:100%;height:180px;margin-top:22px"></div></div>' + tabs('');

  get('/item/' + id + '.json').then(function(d){
    curData = d;
    var s = d.series, last = s[s.length-1];
    var isFav = fav().indexOf(id) >= 0;
    app.innerHTML =
      '<div class="nav">' + backBtn() + '<div class="navsp"></div>' +
      '<button class="iconbtn" onclick="share()" aria-label="링크 복사">' +
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
        'stroke-linecap="round"><path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/>' +
        '<path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></svg></button>' +
      '<button class="iconbtn fav" ' + (isFav?'data-on':'') + ' onclick="toggleFav(\'' + id + '\')" aria-label="저장">' +
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="' + (isFav?'currentColor':'none') + '" ' +
        'stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="' + STAR + '"/></svg></button></div>' +

      '<div class="detail">' +
      '<div class="dhead">' + ico(it.cat,'dico') +
        '<div><span class="dcat">' + it.cat + '</span><h1 class="dname">' + it.n + '</h1></div></div>' +

      (function(){
        var wk = periodAvg(s, 7) || last.p;
        var prev = s.length >= 14 ? periodAvg(s.slice(0, s.length-7), 7) : null;
        var wc = prev ? Math.round((wk/prev - 1) * 1000) / 10 : 0;
        var wchg = !prev || !wc ? '<div class="chg flat">지난주와 비슷해요</div>'
          : '<div class="chg ' + (wc>0?'up':'down') + '">' + (wc>0?'▲':'▼') + ' ' +
            Math.abs(wc) + '% 지난주보다</div>';
        return '<div class="pricebox"><div class="plabel">마지막 일주일 보통 거래가</div>' +
          '<div class="dprice num">' + money(wk) + '<span class="dunit">메소</span></div>' +
          '<div class="dfull num">' + full(wk) + ' · ' + D.updated.replace(/-/g,'.') + ' 집계</div>' +
          wchg + '</div>';
      })() +

      rangeChips(s.length) + chart(s.slice(-chartRange)) + statCards(s, it) +
      judgeBox() + timingBox(d, it) + optSummary(d) + hoursBox(d.hours || []) +

      '<div class="tbar"><div class="sec">최근 거래 기록</div>' +
        (d.recent.some(function(r){ return r.o; })
          ? '<div class="optsearch"><input id="tq" placeholder="옵션 검색 (예: 공격력)" ' +
            'value="' + tquery + '" autocomplete="off"/></div>' : '') +
        '<div class="sortbtns">' +
          '<button class="sortb" id="sb-new" data-on onclick="setTsort(\'new\')">최신순</button>' +
          '<button class="sortb" id="sb-high" onclick="setTsort(\'high\')">비싼순</button>' +
          '<button class="sortb" id="sb-low" onclick="setTsort(\'low\')">싼순</button>' +
        '</div></div><div id="tradesbox">' + tradeRows() + '</div>' +

      ad('detail') + relatedHtml(it) + foot + '</div>' + tabs('');
    var ti = document.getElementById('tq');
    if (ti) ti.oninput = function(e){ tquery = e.target.value.trim(); tpage = 0; renderTrades(); };
  }).catch(function(){
    app.innerHTML = '<div class="nav">' + backBtn() + '</div>' +
      '<div class="empty"><div class="emptyT">시세를 불러오지 못했어요</div>잠시 후 다시 시도해 주세요' +
      '<div><button class="chip" style="margin-top:14px" onclick="detail(\'' + id + '\')">다시 시도</button></div></div>' +
      tabs('');
  });
}
function toggleFav(id){
  var f = fav(), i = f.indexOf(id), on = i < 0;
  if (on) f.push(id); else f.splice(i,1);
  localStorage.setItem(FAV, JSON.stringify(f));
  toast(on ? '저장했어요' : '저장을 해제했어요');
  detail(id);
}

function rangeChips(span){
  var opts = [[7,'1주'],[30,'1개월'],[90,'3개월'],[9999,'전체']];
  var use = opts.filter(function(o){ return o[0] <= span || o[0] === 9999; });
  if (use.length <= 1) return '';
  return '<div class="range">' + use.map(function(o){
    return '<button class="rangeb" ' + (chartRange === o[0] ? 'data-on' : '') +
      ' onclick="setRange(' + o[0] + ')">' + o[1] + '</button>';
  }).join('') + '</div>';
}

/* ── 그래프 ── */
function chart(s){
  var v = s.map(function(d){ return d.p; });
  var lo = Math.min.apply(null,v), hi = Math.max.apply(null,v);
  if (hi === lo){ hi = lo * 1.08 + 1; lo = Math.max(0, lo * 0.92 - 1); }
  var pad = (hi - lo) * 0.14; lo = Math.max(0, lo - pad); hi = hi + pad;
  var n = Math.max(v.length - 1, 1);
  function px(i){ return i / n * 100; }
  function py(y){ return (1 - (y - lo)/(hi - lo)) * 100; }

  var line = v.map(function(y,i){ return px(i).toFixed(2) + ',' + py(y).toFixed(2); }).join(' ');
  var dots = v.map(function(y,i){
    return '<i class="pt" style="left:' + px(i).toFixed(2) + '%;top:' + py(y).toFixed(2) + '%"></i>';
  }).join('');
  var hw = 100 / v.length;
  var hits = v.map(function(y,i){
    return '<i class="hit" style="left:' + Math.max(0, px(i) - hw/2).toFixed(2) + '%;width:' +
      hw.toFixed(2) + '%" onmouseenter="tip(' + i + ',' + px(i).toFixed(2) + ',' + py(y).toFixed(2) +
      ')" onmouseleave="tipOff()" onclick="tip(' + i + ',' + px(i).toFixed(2) + ',' + py(y).toFixed(2) + ')"></i>';
  }).join('');
  var ylabs = [hi, (hi+lo)/2, lo].map(function(t){
    return '<div class="yline"><span>' + money(Math.round(t)) + '</span></div>';
  }).join('');

  var xs, last = s.length - 1;
  if (s.length <= 8) xs = s.map(function(d){ return d.d.slice(5).replace('-','/'); });
  else xs = [s[0], s[Math.round(last/2)], s[last]].map(function(d){ return d.d.slice(5).replace('-','/'); });

  return '<div class="chart">' +
    '<div class="ygrid">' + ylabs + '</div>' +
    '<div class="plot">' +
      '<svg viewBox="0 0 100 100" preserveAspectRatio="none">' +
        '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">' +
          '<stop offset="0%" stop-color="#3182F6" stop-opacity=".16"/>' +
          '<stop offset="100%" stop-color="#3182F6" stop-opacity="0"/></linearGradient></defs>' +
        '<polygon class="area" points="0,100 ' + line + ' 100,100"/>' +
        '<polyline class="line" points="' + line + '" vector-effect="non-scaling-stroke"/>' +
      '</svg>' + dots + hits + '<div class="tip" id="ctip"></div>' +
    '</div></div>' +
    '<div class="xaxis" style="padding-left:56px">' +
      xs.map(function(x){ return '<span>' + x + '</span>'; }).join('') + '</div>';
}

/* ══════════════ 주문서 작 계산기 v2 ══════════════ */
var SC = { item:null, slot:null, slots:7, scroll:null, white:'none', trials:5000, pick:'item' };
var simMode = 'play';
var ENH = null;
function enhReset(){
  ENH = { left:SC.slots, succ:0, fail:0, saved:0, cost:0, log:[], flash:'', done:false };
}
function setMode(m){ simMode = m; if (m === 'play') enhReset(); redrawSim(); }
var RATE = /(\d+)%$/;
var GAIN = { '100':1, '70':1, '60':2, '30':3, '10':5 };

var SLOTS = ['투구','상의','하의','전신 갑옷','신발','장갑','망토','방패','귀 장식','반지','벨트',
  '뱃지','펫장비','악세서리','한손검','두손검','한손도끼','두손도끼','한손둔기','두손둔기',
  '창','폴암','단검','스태프','완드','활','석궁','너클','아대','건','블레이드'];

var SLOT_RULES = [
  ['두손검',['두손검']], ['한손도끼',['도끼']], ['두손둔기',['해머']], ['한손둔기',['둔기','메이스']],
  ['폴암',['폴암']], ['창',['장창','스피어']], ['단검',['단검','크리스','대거']],
  ['스태프',['스태프','지팡이']], ['완드',['완드']], ['활',['보우']], ['석궁',['석궁','크로스보우']],
  ['너클',['너클']], ['아대',['아대']], ['건',['캐논','리볼버']],
  ['한손검',['검','소드','블레이드']],
  ['투구',['투구','모자','헬멧','캡']], ['상의',['상의','셔츠','자켓']],
  ['하의',['하의','바지','칠부','스커트']],
  ['전신 갑옷',['갑옷','로브','슈트','메일','드레스','아머']],
  ['신발',['신발','부츠','슈즈','샌들']], ['장갑',['장갑','글러브']],
  ['망토',['망토','케이프']], ['방패',['방패','실드']],
  ['귀 장식',['이어링','귀고리','귀걸이']], ['반지',['반지']], ['벨트',['벨트','복대']],
  ['뱃지',['뱃지','배지']], ['펫장비',['펫']], ['악세서리',['목걸이','펜던트','안경','고글']]
];
var SLOT_EXCL = ['표창','수리검','부메랑','화살'];

function slotOf(name){
  for (var e = 0; e < SLOT_EXCL.length; e++) if (name.indexOf(SLOT_EXCL[e]) >= 0) return null;
  for (var i = 0; i < SLOT_RULES.length; i++){
    var keys = SLOT_RULES[i][1];
    for (var k = 0; k < keys.length; k++) if (name.indexOf(keys[k]) >= 0) return SLOT_RULES[i][0];
  }
  return null;
}
function maxUpOf(d){
  var mx = null;
  (d.recent || []).forEach(function(r){
    var m = (r.o || '').match(/업그레이드 가능 횟수 : (\d+)/);
    if (m){ var v = parseInt(m[1],10); if (mx === null || v > mx) mx = v; }
  });
  return mx;
}
function scrollRate(name){ var m = name.match(RATE); return m ? parseInt(m[1],10) : null; }
function isWhite(n){ return n.indexOf('백의 주문서') === 0; }
function whiteList(){
  return D.items.filter(function(i){ return isWhite(i.n); })
    .sort(function(a,b){ return scrollRate(a.n) - scrollRate(b.n); });
}
function scrollsFor(slot, q){
  var qc = cho(q || '').replace(/\s/g,'');
  return D.items.filter(function(i){
    if (i.cat !== '주문서' || scrollRate(i.n) == null || isWhite(i.n)) return false;
    if (slot && i.n.indexOf(slot) !== 0) return false;
    if (!q) return true;
    return i.n.toLowerCase().indexOf(q.toLowerCase()) >= 0 || i._c.indexOf(qc) >= 0;
  }).sort(function(a,b){ return b.v - a.v; });
}

function binom(n, p){
  var r = [], c = 1;
  for (var k = 0; k <= n; k++){
    r.push(c * Math.pow(p,k) * Math.pow(1-p, n-k));
    c = c * (n-k) / (k+1);
  }
  return r;
}
function simulate(n, p, wp, price, wprice, trials){
  var costs = [], succ = [], scrolls = [], whites = [];
  for (var t = 0; t < trials; t++){
    var left = n, s = 0, sc = 0, wc = 0;
    while (left > 0 && sc < 300){
      sc++; left--;
      if (Math.random() < p) s++;
      else if (wp > 0){ wc++; if (Math.random() < wp) left++; }
    }
    succ.push(s); scrolls.push(sc); whites.push(wc);
    costs.push(sc*price + wc*wprice);
  }
  costs.sort(function(a,b){ return a-b; });
  var avg = function(a){ return a.reduce(function(x,y){return x+y;},0)/a.length; };
  return { succAvg:avg(succ), scrollAvg:avg(scrolls), whiteAvg:avg(whites),
    costMid:costs[Math.floor(trials*0.5)], costLucky:costs[Math.floor(trials*0.1)],
    costUnlucky:costs[Math.floor(trials*0.9)], succ:succ };
}

/* ── 화면 ── */
function sim(){
  app.innerHTML =
    '<div class="head"><h1 class="h1">주문서 작 계산기</h1>' +
      '<div class="date">실제 거래 시세로 총비용과 성공 확률을 계산해요</div></div>' +
    '<div class="modetabs">' +
      '<button class="modeb" ' + (simMode==='play'?'data-on':'') +
        ' onclick="setMode(\'play\')">직접 강화해보기</button>' +
      '<button class="modeb" ' + (simMode==='calc'?'data-on':'') +
        ' onclick="setMode(\'calc\')">확률·비용 계산</button>' +
    '</div>' +
    '<div class="simgrid">' +
      '<div class="simcol" id="simsteps">' + simSteps() + '</div>' +
      '<div class="simcol" id="simres">' +
        (simMode === 'play' ? enhView() : simResult()) + '</div>' +
    '</div>' + ad('foot') + foot + tabs('/sim');
  bindSimSearch();
}
function redrawSim(){
  var a = document.getElementById('simsteps'), b = document.getElementById('simres');
  if (!a) return sim();
  a.innerHTML = simSteps();
  b.innerHTML = (simMode === 'play' ? enhView() : simResult());
  bindSimSearch();
}
function bindSimSearch(){
  var g = document.getElementById('gq');
  if (g){ g.oninput = function(e){ gearList(e.target.value); }; gearList(''); }
  var s = document.getElementById('sq');
  if (s){ s.oninput = function(e){ scrollListUI(e.target.value); }; scrollListUI(''); }
}

function stepHead(n, t, done){
  return '<div class="step"><div class="stepn" ' + (done?'data-done':'') + '>' +
    (done ? '&#10003;' : n) + '</div><div class="steptitle">' + t + '</div></div>';
}

function simSteps(){
  var h = '';

  /* 1. 아이템 */
  h += stepHead(1, '어떤 장비에 바르나요', !!SC.item);
  if (SC.item){
    h += '<button class="picked" onclick="clearItem()">' + ico('장비') +
      '<div class="rmain"><div class="rname">' + SC.item.n + '</div>' +
      '<div class="rsub">업그레이드 ' + SC.slots + '회 · ' +
        (SC.slot || '부위 미지정') + '</div></div>' +
      '<span class="change">변경</span></button>';
  } else if (SC.pick === 'item'){
    h += '<div class="search" style="margin:12px 0 4px">' +
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round">' +
      '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>' +
      '<input id="gq" placeholder="장비 이름 검색 (예: 드래곤 크리스)" autocomplete="off"/></div>' +
      '<div id="gearlist"></div>' +
      '<p class="hint"><button class="linkb" onclick="skipItem()">장비 없이 주문서만 고를게요</button></p>';
    return h;
  } else {
    h += '<p class="hint">장비를 건너뛰었어요. ' +
      '<button class="linkb" onclick="backToItem()">장비부터 고르기</button></p>';
  }

  /* 2. 부위 + 횟수 */
  h += stepHead(2, '부위와 업그레이드 횟수', true);
  h += '<div class="fieldlab">부위</div><div class="chips2">' +
    SLOTS.map(function(s){
      return '<button class="chip" ' + (SC.slot === s ? 'data-on' : '') +
        ' onclick="setSlot(\'' + s + '\')">' + s + '</button>';
    }).join('') + '</div>';
  h += '<div class="fieldlab">업그레이드 가능 횟수</div><div class="chips2">' +
    [1,2,3,5,7,10].map(function(k){
      return '<button class="chip" ' + (SC.slots === k ? 'data-on' : '') +
        ' onclick="setSlots(' + k + ')">' + k + '회</button>';
    }).join('') + '</div>' +
    '<p class="hint">아이템 정보창에 적힌 숫자예요.' +
      (SC.item ? ' 실제 매물에서 확인한 값으로 채웠어요.' : '') + '</p>';

  /* 3. 주문서 */
  h += stepHead(3, '주문서 고르기', !!SC.scroll);
  if (SC.scroll){
    h += '<button class="picked" onclick="clearScroll()">' + ico('주문서') +
      '<div class="rmain"><div class="rname">' + SC.scroll.n + '</div>' +
      '<div class="rsub">개당 ' + full(SC.scroll.p) + ' · 성공률 ' +
        scrollRate(SC.scroll.n) + '%</div></div>' +
      '<span class="change">변경</span></button>';
  } else {
    h += '<div class="search" style="margin:12px 0 4px">' +
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round">' +
      '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>' +
      '<input id="sq" placeholder="주문서 검색" autocomplete="off"/></div>' +
      '<div id="scrolllist"></div>';
    return h;
  }

  /* 4. 백의 */
  h += stepHead(4, '백의 주문서 사용', true);
  h += '<div class="chips2">' +
    '<button class="chip" ' + (SC.white==='none'?'data-on':'') + ' onclick="setWhite(\'none\')">안 씀</button>' +
    whiteList().map(function(x){
      return '<button class="chip" ' + (SC.white===x.id?'data-on':'') +
        ' onclick="setWhite(\'' + x.id + '\')">' + x.n.replace('주문서 ','') +
        ' · ' + money(x.p) + '</button>';
    }).join('') + '</div>' +
    '<p class="hint">실패해도 업그레이드 횟수를 되살리는 주문서예요.</p>';
  return h;
}

function gearList(q){
  var el = document.getElementById('gearlist');
  if (!el) return;
  var qc = cho(q||'').replace(/\s/g,'');
  var r = D.items.filter(function(i){
    if (i.cat !== '장비') return false;
    if (!q) return true;
    return i.n.toLowerCase().indexOf(q.toLowerCase()) >= 0 || i._c.indexOf(qc) >= 0;
  }).sort(function(a,b){ return b.v - a.v; }).slice(0, 24);
  if (!r.length){ el.innerHTML = '<div class="empty">찾는 장비가 없어요</div>'; return; }
  el.innerHTML = '<div class="picklist">' + r.map(function(i){
    var s = slotOf(i.n);
    return '<button class="pickrow" onclick="pickItem(\'' + i.id + '\')">' + ico('장비') +
      '<span class="pkmain"><span class="pkname">' + i.n + '</span>' +
      '<span class="pksub">' + (s ? s + ' · ' : '') + '거래 ' + i.v.toLocaleString() + '건</span></span>' +
      '<span class="pkprice num">' + money(i.p) + '</span></button>';
  }).join('') + '</div>';
}
function scrollListUI(q){
  var el = document.getElementById('scrolllist');
  if (!el) return;
  var r = scrollsFor(q ? null : SC.slot, q);
  if (!r.length && SC.slot) r = scrollsFor(null, q);
  r = r.slice(0, 24);
  if (!r.length){ el.innerHTML = '<div class="empty">찾는 주문서가 없어요</div>'; return; }
  el.innerHTML = '<div class="picklist">' + r.map(function(i){
    return '<button class="pickrow" onclick="pickScroll(\'' + i.id + '\')">' + ico('주문서') +
      '<span class="pkmain"><span class="pkname">' + i.n + '</span>' +
      '<span class="pksub">개당 ' + money(i.p) + ' 메소</span></span>' +
      '<span class="rateb">' + scrollRate(i.n) + '%</span></button>';
  }).join('') + '</div>';
}

function pickItem(id){
  var it = byId[id];
  SC.item = it; SC.slot = slotOf(it.n); SC.scroll = null;
  redrawSim();
  get('/item/' + id + '.json').then(function(d){
    var mu = maxUpOf(d);
    if (mu != null && mu > 0){ SC.slots = mu; redrawSim(); }
  }).catch(function(){});
}
function clearItem(){ SC.item = null; SC.scroll = null; SC.pick = 'item'; redrawSim(); }
function skipItem(){ SC.pick = 'scroll'; redrawSim(); }
function backToItem(){ SC.pick = 'item'; redrawSim(); }
function setSlot(s){ SC.slot = (SC.slot === s ? null : s); SC.scroll = null; redrawSim(); }
function setSlots(n){ SC.slots = n; enhReset(); redrawSim(); }
function pickScroll(id){ SC.scroll = byId[id]; enhReset(); redrawSim(); }
function clearScroll(){ SC.scroll = null; redrawSim(); }
function setWhite(v){ SC.white = v; enhReset(); redrawSim(); }


/* ── 직접 강화 모드 ── */
function enhView(){
  if (!SC.scroll){
    return '<div class="reshold"><div class="resicon">&#9889;</div>' +
      '<div class="resholdT">주문서를 고르면<br/>바로 강화를 시작할 수 있어요</div>' +
      '<div class="resholdS">실패해도 진짜 메소는 안 나가요.<br/>마음껏 연습해 보세요.</div></div>';
  }
  if (!ENH) enhReset();
  var it = SC.scroll;
  var p = scrollRate(it.n), gain = GAIN[String(p)] || 1;
  var w = SC.white === 'none' ? null : byId[SC.white];
  var name = SC.item ? SC.item.n : (SC.slot || '장비');

  /* 슬롯 도트 */
  var dots = '';
  for (var i = 0; i < ENH.succ; i++) dots += '<span class="edot ok">&#10003;</span>';
  for (var j = 0; j < ENH.fail; j++) dots += '<span class="edot no">&#10005;</span>';
  for (var k = 0; k < ENH.left; k++) dots += '<span class="edot"></span>';

  var flash = ENH.flash === 'ok' ? '<div class="eflash ok">성공! +' + gain + '</div>'
    : ENH.flash === 'no' ? '<div class="eflash no">실패...</div>'
    : ENH.flash === 'wok' ? '<div class="eflash wok">백의 주문서로 횟수를 되살렸어요!</div>'
    : ENH.flash === 'wno' ? '<div class="eflash no">백의 주문서도 실패했어요</div>'
    : '';

  var h = '<div class="ecard' + (ENH.flash === 'ok' ? ' shake-ok' : ENH.flash && ENH.flash !== 'wok' ? ' shake-no' : '') + '">' +
    '<div class="ename">' + name + '</div>' +
    '<div class="estat num">' + (ENH.succ ? '강화 수치 +' + (ENH.succ * gain) : '아직 강화 전이에요') + '</div>' +
    '<div class="edots">' + dots + '</div>' +
    '<div class="einfo">남은 횟수 <b class="num">' + ENH.left + '회</b> · 성공 <b class="num up">' +
      ENH.succ + '</b> · 실패 <b class="num down">' + ENH.fail + '</b>' +
      (ENH.saved ? ' · 되살림 <b class="num">' + ENH.saved + '</b>' : '') + '</div>' +
    flash + '</div>';

  if (!ENH.done && ENH.left > 0){
    h += '<button class="ebtn" onclick="enhHit()">' + it.n.replace(/ \d+%$/, '') +
      ' 바르기<span class="ebtnsub num">' + p + '% · ' + money(it.p) + ' 메소</span></button>';
  } else {
    ENH.done = true;
    var exp = SC.slots * p / 100;
    var verdict = ENH.succ > exp + 0.5 ? '평균(' + exp.toFixed(1) + '회)보다 <b>잘 나왔어요!</b>'
      : ENH.succ < exp - 0.5 ? '평균(' + exp.toFixed(1) + '회)보다 <b>아쉬웠어요.</b>'
      : '딱 <b>평균</b>(' + exp.toFixed(1) + '회) 수준이에요.';
    h += '<div class="edone"><div class="edoneT">강화 끝!</div>' +
      '<div class="edoneS">' + ENH.succ + '번 성공해서 <b>+' + (ENH.succ * gain) + '</b> · ' + verdict + '</div>' +
      '<div class="edoneS">쓴 메소: <b class="num">' + full(ENH.cost) + '</b></div>' +
      '<button class="ebtn retry" onclick="enhReset();redrawSim()">같은 조건으로 다시</button></div>';
  }

  h += '<div class="ecost">지금까지 쓴 메소 <b class="num">' + full(ENH.cost) + '</b></div>';

  if (ENH.log.length){
    h += '<div class="sec" style="padding:18px 0 8px">강화 기록</div><div class="elog">' +
      ENH.log.slice(0, 10).map(function(l){ return '<div class="elogrow">' + l + '</div>'; }).join('') +
      '</div>';
  }
  h += '<p class="hint">가상 강화예요. 주문서 시세(' + money(it.p) +
    ')는 실제 거래 기록 기준이고, 성공 1회당 +' + gain + '로 계산해요.</p>';
  return h;
}

function enhHit(){
  if (!ENH || ENH.left <= 0 || ENH.done) return;
  var it = SC.scroll;
  var p = scrollRate(it.n) / 100, gain = GAIN[String(scrollRate(it.n))] || 1;
  var w = SC.white === 'none' ? null : byId[SC.white];
  ENH.left--; ENH.cost += it.p;
  var n = ENH.succ + ENH.fail + 1;
  if (Math.random() < p){
    ENH.succ++; ENH.flash = 'ok';
    ENH.log.unshift(n + '번째 · <b class="up">성공</b> +' + gain);
  } else {
    ENH.fail++;
    if (w){
      ENH.cost += w.p;
      if (Math.random() < scrollRate(w.n) / 100){
        ENH.left++; ENH.fail--; ENH.saved++;
        ENH.flash = 'wok';
        ENH.log.unshift(n + '번째 · 실패 &#8594; <b>백의 주문서로 되살림</b>');
      } else {
        ENH.flash = 'wno';
        ENH.log.unshift(n + '번째 · <b class="down">실패</b> (백의도 실패)');
      }
    } else {
      ENH.flash = 'no';
      ENH.log.unshift(n + '번째 · <b class="down">실패</b>');
    }
  }
  var b = document.getElementById('simres');
  if (b) b.innerHTML = enhView();
}

function simResult(){
  if (!SC.scroll){
    return '<div class="reshold"><div class="resicon">&#128176;</div>' +
      '<div class="resholdT">주문서를 고르면<br/>비용이 계산돼요</div>' +
      '<div class="resholdS">실제 거래된 시세를 기준으로<br/>총비용과 성공 확률을 알려드려요</div></div>';
  }
  var it = SC.scroll;
  var p = scrollRate(it.n) / 100, n = SC.slots;
  var w = SC.white === 'none' ? null : byId[SC.white];
  var wp = w ? scrollRate(w.n)/100 : 0, wprice = w ? w.p : 0;
  var gain = GAIN[String(scrollRate(it.n))] || 1;
  var title = SC.item ? SC.item.n : '장비';

  var h = '<div class="resbox"><div class="rescap">' + title + ' · ' + it.n + '</div>';
  var dist, note = '';

  if (!w){
    var pmf = binom(n, p), cost = n * it.p, expS = n * p;
    h += '<div class="bigrow"><span>주문서 필요 개수</span><b class="num">' + n + '개</b></div>' +
      '<div class="bigrow"><span>총 비용</span><b class="num">' + full(cost) + '</b></div>' +
      '<div class="bigrow"><span>평균 성공 횟수</span><b class="num">' + expS.toFixed(1) + '회</b></div>' +
      '<div class="bigrow"><span>예상 상승치</span><b class="num">약 +' + Math.round(expS*gain) + '</b></div>' +
      '</div>';
    var mx = Math.max.apply(null, pmf);
    dist = pmf.map(function(v,k){ return [k, v, v/mx]; });
    note = '<p class="hint">' + n + '개를 다 발라도 <b>' + ((1-pmf[0])*100).toFixed(1) +
      '%</b> 확률로 1회 이상 성공해요.</p>';
  } else {
    var r = simulate(n, p, wp, it.p, wprice, SC.trials);
    h += '<div class="bigrow"><span>주문서</span><b class="num">평균 ' + r.scrollAvg.toFixed(1) + '개</b></div>' +
      '<div class="bigrow"><span>백의 주문서</span><b class="num">평균 ' + r.whiteAvg.toFixed(1) + '개</b></div>' +
      '<div class="bigrow"><span>총 비용</span><b class="num">' + full(Math.round(r.costMid)) + '</b></div>' +
      '<div class="bigrow"><span>평균 성공 횟수</span><b class="num">' + r.succAvg.toFixed(1) + '회</b></div>' +
      '<div class="bigrow"><span>예상 상승치</span><b class="num">약 +' +
        Math.round(r.succAvg*gain) + '</b></div></div>' +
      '<div class="lucky">' +
        '<div><div class="lucklab">운이 좋으면 (상위 10%)</div>' +
          '<div class="luckval num down">' + money(Math.round(r.costLucky)) + '</div></div>' +
        '<div><div class="lucklab">운이 나쁘면 (하위 10%)</div>' +
          '<div class="luckval num up">' + money(Math.round(r.costUnlucky)) + '</div></div></div>';
    var cnt = {};
    r.succ.forEach(function(s){ cnt[s] = (cnt[s]||0)+1; });
    var keys = Object.keys(cnt).map(Number).sort(function(a,b){ return a-b; });
    var mxc = Math.max.apply(null, keys.map(function(k){ return cnt[k]; }));
    dist = keys.map(function(k){ return [k, cnt[k]/SC.trials, cnt[k]/mxc]; });
    note = '<p class="hint">' + SC.trials.toLocaleString() + '회 모의실험 결과예요.</p>';
    /* 백의 효율 안내 */
    var plain = n * it.p;
    if (r.costMid > plain * 1.5 && r.succAvg < n * p + 0.3){
      note += '<p class="warn">백의 주문서를 안 쓰면 <b>' + money(plain) +
        '</b>인데, 성공 횟수는 거의 같아요. 복구 확률이 낮아 비용만 늘어납니다.</p>';
    }
  }

  h += '<div class="sec" style="padding:22px 0 10px">몇 번 성공할까요</div><div class="dist">' +
    dist.map(function(d){
      return '<div class="distrow"><span class="dk num">' + d[0] + '회</span>' +
        '<span class="dbar"><i style="width:' + (d[2]*100).toFixed(1) + '%"></i></span>' +
        '<span class="dv num">' + (d[1]*100).toFixed(1) + '%</span></div>';
    }).join('') + '</div>' + note +
    '<p class="hint">성공 1회당 +' + gain + ' 기준입니다. 실제 수치가 다르면 알려주세요.</p>';
  return h;
}

/* ══════════════ 광고 슬롯 ══════════════ */
/* 애드센스/쿠팡 코드를 아래 4곳에 붙여넣으면 자동으로 표시됩니다.
   비워두면 아무것도 표시되지 않습니다. */
var ADS = {
  top:    '',   /* 홈 목록 위 (가로형) */
  detail: '',   /* 아이템 상세 하단 (가로형) */
  rail:   '',   /* 우측 레일 (1400px 이상에서만, 세로형) */
  foot:   ''    /* 푸터 위 (가로형) */
};
var AD_DEMO = __AD_DEMO__;
var AD_SIZE = { top:'90px', detail:'250px', rail:'600px', foot:'90px' };

function ad(slot){
  var code = ADS[slot];
  if (code) return '<div class="adslot"><div class="adlabel">광고</div>' + code + '</div>';
  if (!AD_DEMO) return '';
  return '<div class="adslot"><div class="adlabel">광고</div>' +
    '<div class="addemo" style="height:' + AD_SIZE[slot] + '">광고 자리 (' + slot + ')</div></div>';
}

/* ══════════════ 우측 레일 ══════════════ */
function renderRail(){
  var el = document.getElementById('rail');
  if (!el || !D) return;
  var top = D.items.slice().sort(function(a,b){ return b.v - a.v; }).slice(0,10);
  el.innerHTML = ad('rail') +
    '<div class="railbox"><div class="railtitle">거래 많은 아이템</div>' +
    top.map(function(i,n){
      return '<button class="railrow" onclick="go(\'/item/' + i.id + '\')">' +
        '<span class="railrank num">' + (n+1) + '</span>' +
        '<span class="railname">' + i.n + '</span>' +
        '<span class="railprice num">' + money(i.p) + '</span></button>';
    }).join('') + '</div>' +
    '<div class="railbox"><div class="railtitle">이번 주 많이 오른</div>' +
    D.items.filter(function(i){ return i.v >= 100; })
      .sort(function(a,b){ return b.c - a.c; }).slice(0,5).map(function(i){
      return '<button class="railrow" onclick="go(\'/item/' + i.id + '\')">' +
        '<span class="railname">' + i.n + '</span>' +
        '<span class="railprice num up">+' + i.c + '%</span></button>';
    }).join('') + '</div>';
}

/* ══════════════ 적정가 판별기 ══════════════ */
function pctOf(x, q){
  /* q = [p10,p25,p50,p75,p90] */
  var xs = [0.10,0.25,0.50,0.75,0.90];
  if (x <= q[0]) return Math.max(1, 10 * x / (q[0]||1));
  if (x >= q[4]) return Math.min(99, 90 + 9 * (x - q[4]) / (q[4]||1));
  for (var i = 0; i < 4; i++){
    if (x <= q[i+1]){
      var t = (x - q[i]) / ((q[i+1] - q[i]) || 1);
      return (xs[i] + t * (xs[i+1] - xs[i])) * 100;
    }
  }
  return 50;
}
function judge(){
  var inp = document.getElementById('jprice');
  var out = document.getElementById('jout');
  if (!inp || !out || !curData) return;
  var raw = (inp.value || '').replace(/[^0-9]/g,'');
  if (!raw){ out.innerHTML = ''; return; }
  var x = parseInt(raw,10);
  inp.value = x.toLocaleString();
  var p = pctOf(x, curData.pct);
  var head, sub, cls;
  if (p <= 10){ head = '아주 싼 편이에요'; cls = 'vgood';
    sub = '최근 거래 중 가장 싼 축에 듭니다. 좋은 기회로 보여요.'; }
  else if (p <= 25){ head = '싼 편이에요'; cls = 'vgood';
    sub = '평소 시세보다 저렴합니다.'; }
  else if (p <= 75){ head = '보통 시세예요'; cls = '';
    sub = '평소 거래되던 가격대입니다.'; }
  else if (p <= 90){ head = '비싼 편이에요'; cls = 'vbad';
    sub = '평소보다 높은 가격입니다. 급하지 않다면 조금 기다려 보세요.'; }
  else { head = '아주 비싼 편이에요'; cls = 'vbad';
    sub = '최근 거래 중 가장 비싼 축에 듭니다.'; }

  out.innerHTML =
    '<div class="verdict"><div class="vhead ' + cls + '">' + head + '</div>' +
    '<div class="vsub">' + sub + ' 최근 거래 중 <b>상위 ' + Math.round(100-p) + '%</b> 수준이에요.</div>' +
    '<div class="vbar"><span class="vmark" style="left:' + p.toFixed(1) + '%"></span></div>' +
    '<div class="vscale"><span>싼 가격 ' + money(curData.pct[0]) + '</span>' +
    '<span>보통 ' + money(curData.pct[2]) + '</span>' +
    '<span>비싼 가격 ' + money(curData.pct[4]) + '</span></div></div>';
}
function judgeBox(){
  return '<div class="judge"><div class="judgetitle">이 가격, 사도 될까요?</div>' +
    '<div class="judgesub">사려는 개당 가격을 넣어보세요. 실제 거래 기록과 비교해 드려요.</div>' +
    '<div class="judgein"><input id="jprice" inputmode="numeric" placeholder="예: 620000"/>' +
    '<button class="judgebtn" onclick="judge()">확인</button></div>' +
    '<div id="jout"></div></div>';
}

/* ══════════════ 거래 시간대 ══════════════ */
function hoursBox(h){
  var total = h.reduce(function(a,b){ return a+b; }, 0);
  if (!total) return '';
  var mx = Math.max.apply(null, h);
  /* 연속 3시간 합이 가장 큰 구간 */
  var best = 0, bi = 0;
  for (var i = 0; i < 24; i++){
    var s = h[i] + h[(i+1)%24] + h[(i+2)%24];
    if (s > best){ best = s; bi = i; }
  }
  var peak = [bi, (bi+1)%24, (bi+2)%24];
  var bars = h.map(function(v,i){
    return '<div class="hbar" ' + (peak.indexOf(i)>=0 ? 'data-peak' : '') +
      ' style="height:' + Math.max(3, v/mx*100) + '%" title="' + i + '시 ' + v + '건"></div>';
  }).join('');
  return '<div class="sec" style="padding-left:0">거래가 몰리는 시간</div>' +
    '<div class="hours">' + bars + '</div>' +
    '<div class="hscale"><span>0시</span><span>6시</span><span>12시</span><span>18시</span><span>23시</span></div>' +
    '<div class="peaknote"><b>' + bi + '시 ~ ' + ((bi+3)%24) + '시</b>에 가장 많이 거래돼요' +
    ' (전체의 ' + Math.round(best/total*100) + '%). 이 시간대에 올리면 더 빨리 팔립니다.</div>';
}

function tip(i, x, y){
  var el = document.getElementById('ctip');
  if (!el || !curData) return;
  var d = curData.series[i];
  if (!d) return;
  function row(k, val){
    return '<div class="tiprow"><span class="tipk">' + k + '</span>' +
           '<span class="tipv">' + val + '</span></div>';
  }
  el.innerHTML = '<div class="tipd">' + d.d.slice(5).replace('-','월 ') + '일</div>' +
    row('거래', d.n.toLocaleString() + '건') +
    row('평균가', money(d.a != null ? d.a : d.p)) +
    row('최고가', money(d.hi)) +
    row('최저가', money(d.lo));
  el.style.left = x + '%';
  el.style.top  = y + '%';
  el.setAttribute('data-on','');
}
function tipOff(){
  var el = document.getElementById('ctip');
  if (el) el.removeAttribute('data-on');
}

/* 장비: 판매된 옵션 요약 (스탯별 최소~최대) */
function optSummary(d){
  var stats = {};
  var cnt = 0;
  (d.recent || []).forEach(function(r){
    if (!r.o) return;
    cnt++;
    r.o.split(',').forEach(function(part){
      var kv = part.split(':');
      if (kv.length < 2) return;
      var k = kv[0].trim(), v = parseInt(kv[kv.length-1].trim(), 10);
      if (isNaN(v) || k === '업그레이드 가능 횟수') return;
      if (!stats[k]) stats[k] = [v, v];
      else { if (v < stats[k][0]) stats[k][0] = v; if (v > stats[k][1]) stats[k][1] = v; }
    });
  });
  var keys = Object.keys(stats);
  if (cnt < 5 || !keys.length) return '';
  return '<div class="optbox"><div class="timT">최근 판매된 옵션 범위</div>' +
    '<div class="optgrid">' + keys.map(function(k){
      var s = stats[k];
      return '<div class="optcell"><div class="optk">' + k + '</div>' +
        '<div class="optv num">' + (s[0] === s[1] ? s[0] : s[0] + ' ~ ' + s[1]) + '</div></div>';
    }).join('') + '</div>' +
    '<p class="hint">최근 거래 ' + cnt + '건에서 관측된 값이에요. 옵션에 따라 가격 차이가 큽니다.</p></div>';
}

var WDL = ['월','화','수','목','금','토','일'];
var HBL = ['새벽 0~4시','새벽 4~8시','오전 8~12시','낮 12~16시','저녁 16~20시','밤 20~24시'];
function timingBox(d, it){
  var rows = '';
  /* 요일 효과: 최고/최저 요일 차이가 2% 이상일 때만 */
  var w = d.wmed || [];
  var wv = [];
  for (var i = 0; i < 7; i++) if (w[i] != null) wv.push([i, w[i]]);
  if (wv.length >= 5){
    var wmax = wv[0], wmin = wv[0];
    wv.forEach(function(x){ if (x[1] > wmax[1]) wmax = x; if (x[1] < wmin[1]) wmin = x; });
    if (wmin[1] > 0 && (wmax[1]/wmin[1] - 1) >= 0.02){
      rows += '<div class="timrow"><span class="timico">&#128197;</span><span>' +
        '<b>' + WDL[wmax[0]] + '요일</b>에 가장 비싸게(' + money(wmax[1]) + '), ' +
        '<b>' + WDL[wmin[0]] + '요일</b>에 가장 싸게(' + money(wmin[1]) + ') 거래됐어요. ' +
        WDL[wmin[0]] + '요일에 사서 ' + WDL[wmax[0]] + '요일에 파는 게 유리해요.</span></div>';
    }
  }
  /* 시간대 효과: 4시간 구간 차이 2% 이상일 때만 */
  var hm = d.hmed || [];
  var hv = [];
  for (var j = 0; j < 6; j++) if (hm[j] != null) hv.push([j, hm[j]]);
  if (hv.length >= 4){
    var hmax = hv[0], hmin = hv[0];
    hv.forEach(function(x){ if (x[1] > hmax[1]) hmax = x; if (x[1] < hmin[1]) hmin = x; });
    if (hmin[1] > 0 && (hmax[1]/hmin[1] - 1) >= 0.02){
      rows += '<div class="timrow"><span class="timico">&#9200;</span><span>' +
        '하루 중에는 <b>' + HBL[hmax[0]] + '</b>에 비싸고 <b>' + HBL[hmin[0]] + '</b>에 쌌어요. ' +
        '팔 거라면 ' + HBL[hmax[0]] + ' 등록이 유리해요.</span></div>';
    }
  }
  /* 기간 내 현재가 위치 */
  var s = d.series, ps = s.map(function(x){ return x.p; });
  var lo = Math.min.apply(null, ps), hi = Math.max.apply(null, ps);
  if (hi > lo && s.length >= 14){
    var cur = periodAvg(s, 7) || ps[ps.length-1];
    var pos = Math.max(0, Math.min(100, (cur - lo) / (hi - lo) * 100));
    var msg = pos <= 30 ? '마지막 일주일 시세는 이 기간에서 <b>싼 편</b>이었어요.'
            : pos >= 70 ? '마지막 일주일 시세는 이 기간에서 <b>비싼 편</b>이었어요.'
            : '마지막 일주일 시세는 이 기간의 <b>중간 수준</b>이었어요.';
    rows += '<div class="timrow"><span class="timico">&#128200;</span><span>' + msg +
      '<span class="pos"><span class="posbar"><span class="posmark" style="left:' +
      pos.toFixed(1) + '%"></span></span>' +
      '<span class="posscale"><span>기간 최저 ' + money(lo) + '</span><span>기간 최고 ' +
      money(hi) + '</span></span></span></span></div>';
  }
  if (!rows) return '';
  return '<div class="timing"><div class="timT">언제 사고팔면 좋을까요</div>' + rows +
    '<p class="hint" style="margin-top:10px">최근 ' + s.length +
    '일 거래 기록으로 계산했어요. 참고용이에요.</p></div>';
}

function render(){
  var h = location.hash.slice(1);
  if (h.indexOf('/item/') === 0) detail(h.slice(6));
  else if (h === '/search') searchPage();
  else if (h === '/rank') rank();
  else if (h === '/sim') sim();
  else if (h === '/fav') favs();
  else home();
  window.scrollTo(0,0);
}

var isPage = (document.body.className || '').indexOf('static_page') >= 0;
if (app && !isPage){
  window.addEventListener('hashchange', render);
  home();
  get('/index.json').then(function(j){
    D = j;
    D.items.forEach(function(i){ i._c = cho(i.n).replace(/\s/g,''); byId[i.id] = i; });
    render(); renderRail();
  }).catch(function(){
    app.innerHTML = '<div class="empty"><div class="emptyT">시세를 불러오지 못했어요</div>' +
      '인터넷 연결을 확인하고 새로고침해 주세요</div>' + tabs('');
  });
}
'''.replace('__DATA_BASE__', DATA_BASE).replace('__CONTACT__', CONTACT)

# ── 4. 테마 XML ────────────────────────────────────────────────────
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
<meta content='메이플스토리 월드 로나월드 옥션 실거래 시세를 아이템별로 확인하세요.' name='description'/>
<title><data:blog.pageTitle/></title>
<link href='https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css'
      rel='stylesheet'/>
<b:skin><![CDATA[]]></b:skin>
<style type='text/css'>/*<![CDATA[*/
__CSS__
/*]]>*/</style>
</head>
<body expr:class='data:blog.pageType'>

<div id='shell'>
 <div id='content'>

  <div id='app'></div>

  <b:section id='main' showaddelement='no'>
    <b:widget id='Blog1' locked='true' type='Blog' version='2'>
      <b:includable id='main'>
        <b:if cond='data:blog.pageType == &quot;static_page&quot;'>
          <div class='page'>
            <b:loop values='data:posts' var='post'>
              <h1 class='ptitle'><data:post.title/></h1>
              <div class='pbody'><data:post.body/></div>
            </b:loop>
            <p><a class='homelink' expr:href='data:blog.homepageUrl'>&#8592; 시세 보러 가기</a></p>
          </div>
        </b:if>
      </b:includable>
    </b:widget>
  </b:section>

  <footer id='sitefoot'>
    <b:section id='footlinks' showaddelement='no'>
      <b:widget id='PageList1' locked='true' title='' type='PageList' version='2'>
        <b:includable id='main'>
          <nav>
            <a expr:href='data:blog.homepageUrl'>홈</a>
            <b:loop values='data:links' var='link'>
              <a expr:href='data:link.href'><data:link.title/></a>
            </b:loop>
          </nav>
        </b:includable>
      </b:widget>
    </b:section>
    <p>본 사이트는 메이플스토리 월드 &#8216;로나월드&#8217;의 옥션 거래 기록을 집계해 제공하는 비공식 팬 사이트입니다.</p>
    <p>넥슨(NEXON) 및 로나월드 제작자와 제휴 관계가 없으며, 게임 내 모든 상표와 저작물의 권리는 각 권리자에게 있습니다.</p>
    <p>제공되는 시세는 참고용 통계이며, 실제 거래 결과를 보장하지 않습니다.</p>
    <p style='margin-top:12px'>&#169; <data:blog.title/></p>
  </footer>

 </div>
 <aside id='rail'></aside>
</div>

<script type='text/javascript'>
//<![CDATA[
__JS__
//]]>
</script>

</body>
</html>
"""

theme = THEME.replace('__CSS__', CSS).replace('__JS__', JS.replace('__AD_DEMO__','false'))
open(f'{DST}/theme.xml', 'w', encoding='utf-8').write(theme)

import xml.dom.minidom
try:
    xml.dom.minidom.parseString(theme.encode('utf-8'))
    ok = 'XML 검증 통과'
except Exception as e:
    ok = f'XML 오류: {e}'

print(f"{DST}/theme.xml  {os.path.getsize(f'{DST}/theme.xml')/1024:.0f}KB  |  {ok}")
print(f'{DST}/data/      아이템 {n_items}종')
print(f'DATA_BASE = {DATA_BASE}')

# ── 5. 로컬 미리보기 HTML (블로그스팟 올리기 전 확인용) ─────────────
PREVIEW = ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
  '<meta name="viewport" content="width=device-width,initial-scale=1">'
  '<title>미리보기 · 로나 시세</title>'
  '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard'
  '@v1.3.9/dist/web/static/pretendard.min.css">'
  '<style>' + CSS + '</style></head><body>'
  '<div id="shell"><div id="content"><div id="app"></div>'
  '<footer id="sitefoot"><nav><a href="#/">홈</a><a href="#">사이트 소개</a>'
  '<a href="#">개인정보처리방침</a><a href="#">이용약관</a><a href="#">문의하기</a></nav>'
  '<p>본 사이트는 메이플스토리 월드 로나월드의 옥션 거래 기록을 집계해 제공하는 비공식 팬 사이트입니다.</p>'
  '<p>넥슨(NEXON) 및 로나월드 제작자와 제휴 관계가 없습니다.</p>'
  '<p>제공되는 시세는 참고용 통계이며, 실제 거래 결과를 보장하지 않습니다.</p></footer></div>'
  '<aside id="rail"></aside></div>'
  '<script>' + JS.replace('__AD_DEMO__','true') + '</script></body></html>')
open(f'{DST}/preview.html', 'w', encoding='utf-8').write(PREVIEW)
print(f'{DST}/preview.html  로컬 확인용')
