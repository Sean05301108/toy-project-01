# -*- coding: utf-8 -*-
"""
주간 시세 리포트 생성 -> 블로거 '글'에 붙여넣을 HTML

사용법:  python3 make_report.py out ./site
결과:    site/report_YYYY-MM-DD.html  (블로거 새 글 > HTML 보기 에 붙여넣기)

목적은 체류시간이 아니라 검색 유입입니다.
지금 사이트는 색인 가능한 페이지가 홈 하나뿐이라 구글에 노출될 창구가 없습니다.
매주 이 글을 발행하면 '로나월드 시세', '아이템명 시세' 검색에 잡히기 시작합니다.
"""
import json, os, sys, datetime

SRC = sys.argv[1] if len(sys.argv) > 1 else 'out'
DST = sys.argv[2] if len(sys.argv) > 2 else 'site'
SITE = 'https://ronaworld-auction.blogspot.com/'

idx = json.load(open(f'{SRC}/index.json', encoding='utf-8'))
items = idx['items']
updated = idx['updated']

def money(n):
    if n >= 100000000:
        v = n / 100000000
        return (f'{round(v)}' if v >= 10 else f'{v:.1f}'.rstrip('0').rstrip('.')) + '억'
    if n >= 10000:
        return f'{round(n/10000):,}만'
    return f'{n:,}'

def link(it):
    return f'<a href="{SITE}#/item/{it["id"]}">{it["n"]}</a>'

live = [i for i in items if i['v'] >= 20]
up   = sorted(live, key=lambda x: -x['c'])[:10]
down = sorted(live, key=lambda x:  x['c'])[:10]
vol  = sorted(items, key=lambda x: -x['v'])[:10]
expensive = sorted([i for i in items if i['v'] >= 5], key=lambda x: -x['p'])[:10]

d = datetime.date.fromisoformat(updated)
week = (d.day - 1) // 7 + 1
title = f'{d.year}년 {d.month}월 {week}주차 로나월드 옥션 시세 리포트'

def table(rows, head, fmt):
    h = '<table style="width:100%;border-collapse:collapse;font-size:15px"><thead><tr>' + \
        ''.join(f'<th style="text-align:{a};padding:10px 8px;border-bottom:2px solid #191F28;'
                f'font-size:14px">{t}</th>' for t, a in head) + '</tr></thead><tbody>'
    for n, it in enumerate(rows, 1):
        h += '<tr>' + ''.join(
            f'<td style="text-align:{a};padding:11px 8px;border-bottom:1px solid #F2F4F6">{v}</td>'
            for v, a in fmt(n, it)) + '</tr>'
    return h + '</tbody></table>'

def chg(c):
    if c > 0:  return f'<b style="color:#F04452">+{c}%</b>'
    if c < 0:  return f'<b style="color:#3182F6">{c}%</b>'
    return '<span style="color:#8B95A1">변동 없음</span>'

parts = []
parts.append(
  f'<p>메이플스토리 월드 로나월드 옥션의 <b>{updated.replace("-", ".")} 기준</b> 시세를 정리했습니다. '
  f'이번 주 집계 대상은 아이템 <b>{len(items):,}종</b>입니다.</p>'
  f'<p>모든 가격은 <b>개당 가격</b>이며, 시세를 왜곡하는 극단적인 매물을 제외한 중앙값입니다. '
  f'묶음 매물은 총액을 수량으로 나눠 환산했습니다.</p>')

parts.append('<h2>가격이 오른 아이템 TOP 10</h2>')
parts.append('<p>거래 20건 이상인 아이템만 집계했습니다.</p>')
parts.append(table(up, [('순위','center'),('아이템','left'),('시세','right'),('변동','right')],
    lambda n, it: [(n,'center'), (link(it),'left'), (money(it['p'])+' 메소','right'), (chg(it['c']),'right')]))

parts.append('<h2>가격이 내린 아이템 TOP 10</h2>')
parts.append(table(down, [('순위','center'),('아이템','left'),('시세','right'),('변동','right')],
    lambda n, it: [(n,'center'), (link(it),'left'), (money(it['p'])+' 메소','right'), (chg(it['c']),'right')]))

parts.append('<h2>거래가 가장 많았던 아이템 TOP 10</h2>')
parts.append('<p>거래량이 많을수록 시세가 안정적이고, 사고팔기도 쉽습니다.</p>')
parts.append(table(vol, [('순위','center'),('아이템','left'),('거래','right'),('시세','right')],
    lambda n, it: [(n,'center'), (link(it),'left'), (f"{it['v']:,}건",'right'), (money(it['p'])+' 메소','right')]))

parts.append('<h2>가장 비싼 아이템 TOP 10</h2>')
parts.append(table(expensive, [('순위','center'),('아이템','left'),('시세','right'),('거래','right')],
    lambda n, it: [(n,'center'), (link(it),'left'), (money(it['p'])+' 메소','right'), (f"{it['v']:,}건",'right')]))

top_up, top_down = up[0], down[0]
parts.append('<h2>이번 주 요약</h2><ul>')
parts.append(f'<li>가장 많이 오른 아이템은 <b>{top_up["n"]}</b>({chg(top_up["c"])})으로, 현재 {money(top_up["p"])} 메소에 거래되고 있습니다.</li>')
parts.append(f'<li>가장 많이 내린 아이템은 <b>{top_down["n"]}</b>({chg(top_down["c"])})입니다.</li>')
parts.append(f'<li>거래가 가장 활발한 아이템은 <b>{vol[0]["n"]}</b>({vol[0]["v"]:,}건)입니다.</li>')
parts.append('</ul>')

parts.append(
  f'<h2>실시간 시세 확인</h2>'
  f'<p>아이템별 상세 시세, 가격 추이 그래프, 최근 거래 기록은 '
  f'<a href="{SITE}"><b>로나월드 옥션 시세 조회</b></a>에서 확인하실 수 있습니다. '
  f'아이템 이름 초성으로도 검색됩니다.</p>'
  f'<p>주문서 작에 드는 비용이 궁금하시면 '
  f'<a href="{SITE}#/sim"><b>주문서 작 계산기</b></a>를 이용해 보세요. '
  f'실제 거래 시세를 기준으로 총비용과 성공 확률을 계산해 드립니다.</p>'
  f'<p style="color:#8B95A1;font-size:13px;margin-top:24px">'
  f'본 자료는 실제 거래 기록을 집계한 참고용 통계이며, 거래 결과를 보장하지 않습니다. '
  f'본 사이트는 넥슨 및 로나월드 제작자와 무관한 비공식 팬 사이트입니다.</p>')

body = '\n'.join(parts)
out = f'{DST}/report_{updated}.html'
open(out, 'w', encoding='utf-8').write(body)

print(f'{out}')
print(f'  글 제목: {title}')
print(f'  검색어 태그: 로나월드 시세, 로나월드 옥션, 메이플스토리 월드, {top_up["n"]} 시세')
