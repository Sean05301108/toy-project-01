# -*- coding: utf-8 -*-
"""로나월드 옥션 로그 -> 정적 사이트용 JSON 빌더"""
import re, os, json, hashlib, statistics, collections, sys

REC = re.compile(r'^(\d{4})\.(\d{1,2})\.(\d{1,2})/(\d{1,2}):(\d{1,2}):(\d{1,2}) \[(.+?)\] ([\d,]+)개 총합 ([\d,]+) 메소$')

def num(s): return int(s.replace(',', ''))

def item_id(name):
    return hashlib.md5(name.encode('utf-8')).hexdigest()[:10]

def parse(paths):
    for p in paths:
        with open(p, encoding='utf-8') as f:
            lines = f.read().split('\n')
        for i, line in enumerate(lines):
            m = REC.match(line.strip())
            if not m: continue
            y, mo, d, h, mi, se, name, qty, total = m.groups()
            opt = lines[i+1].strip() if i+1 < len(lines) else ''
            if REC.match(opt): opt = ''
            q, t = num(qty), num(total)
            yield {
                'date': f'{y}-{int(mo):02d}-{int(d):02d}',
                'ts': f'{int(h):02d}:{int(mi):02d}:{int(se):02d}',
                'name': name, 'qty': q, 'total': t,
                'unit': t // q if q else t,
                'opt': opt,
            }

def trimmed(vals, p=0.1):
    """상하위 10% 잘라낸 대표가 (500M 피로회복제 같은 이상치 제거)"""
    v = sorted(vals)
    if len(v) < 5: return statistics.median(v)
    k = int(len(v) * p)
    core = v[k:len(v)-k] or v
    return int(statistics.median(core))

def build(paths, outdir):
    by_item = collections.defaultdict(list)
    for r in parse(paths):
        by_item[r['name']].append(r)

    os.makedirs(f'{outdir}/item', exist_ok=True)
    index = []
    for name, rows in by_item.items():
        iid = item_id(name)
        is_gear = sum(1 for r in rows if r['opt']) > len(rows) * 0.5  # 옵션 있으면 장비류
        daily = collections.defaultdict(list)
        for r in rows: daily[r['date']].append(r)

        series = []
        for date in sorted(daily):
            units = [r['unit'] for r in daily[date]]
            series.append({
                'd': date,
                'p': trimmed(units),                    # 대표가(중앙값)
                'a': sum(units) // len(units),          # 단순 평균 (툴팁용)
                'lo': min(units), 'hi': max(units),
                'n': len(daily[date]),                  # 거래 건수
                'q': sum(r['qty'] for r in daily[date]) # 거래 수량
            })
        # 거래 시간대 (24칸: 건수) + 시간대별 중앙단가 (6칸: 4시간 구간)
        hours = [0]*24
        hbins = [[] for _ in range(6)]
        for r in rows:
            h = int(r['ts'][:2])
            hours[h] += 1
            hbins[h//4].append(r['unit'])
        hmed = [int(statistics.median(b)) if len(b) >= 30 else None for b in hbins]

        # 요일별 중앙단가 (월=0)
        import datetime as _dt
        wbins = [[] for _ in range(7)]
        for r in rows:
            y, mo, dd = map(int, r['date'].split('-'))
            wbins[_dt.date(y, mo, dd).weekday()].append(r['unit'])
        wmed = [int(statistics.median(b)) if len(b) >= 30 else None for b in wbins]

        # 가격 분위수 (적정가 판별용) - 전체 거래 기준
        units = sorted(r['unit'] for r in rows)
        def qt(f):
            return units[min(len(units)-1, int(len(units)*f))]
        pct = [qt(.1), qt(.25), qt(.5), qt(.75), qt(.9)]

        # 오래된 구간은 주별로 압축 (최근 90일은 일별 유지)
        if len(series) > 90:
            old, keep = series[:-90], series[-90:]
            import datetime as _d2
            weeks = {}
            for s in old:
                y, mo, dd = map(int, s['d'].split('-'))
                dt = _d2.date(y, mo, dd)
                wk = dt - _d2.timedelta(days=dt.weekday())
                weeks.setdefault(wk.isoformat(), []).append(s)
            comp = []
            for wd in sorted(weeks):
                grp = weeks[wd]
                ps = sorted(x['p'] for x in grp)
                tot_n = sum(x['n'] for x in grp)
                comp.append({
                    'd': wd, 'w': 1, 'dd': len(grp),
                    'p': ps[len(ps)//2],
                    'a': sum(x['a'] * x['n'] for x in grp) // max(tot_n, 1),
                    'lo': min(x['lo'] for x in grp),
                    'hi': max(x['hi'] for x in grp),
                    'n': tot_n, 'q': sum(x['q'] for x in grp),
                })
            for s in keep: s['dd'] = 1
            series = comp + keep
        else:
            for s in series: s['dd'] = 1

        recent = sorted(rows, key=lambda r: (r['date'], r['ts']))[-100:]
        last = series[-1]
        prev = series[-2] if len(series) > 1 else last
        chg = round((last['p'] - prev['p']) / prev['p'] * 100, 1) if prev['p'] else 0.0

        json.dump({
            'id': iid, 'name': name, 'gear': is_gear,
            'hours': hours, 'pct': pct, 'hmed': hmed, 'wmed': wmed,
            'series': series,
            'recent': [{'d': r['date'], 't': r['ts'], 'q': r['qty'],
                        'u': r['unit'], 'o': r['opt']} for r in reversed(recent)]
        }, open(f'{outdir}/item/{iid}.json', 'w', encoding='utf-8'),
           ensure_ascii=False, separators=(',', ':'))

        index.append({'id': iid, 'n': name, 'p': last['p'],
                      'c': chg, 'v': sum(s['n'] for s in series), 'g': int(is_gear)})

    index.sort(key=lambda x: -x['v'])
    all_dates = max(max(s['d'] for s in json.load(open(f'{outdir}/item/{it["id"]}.json', encoding='utf-8'))['series']) for it in index[:50])
    json.dump({'updated': all_dates, 'items': index},
              open(f'{outdir}/index.json', 'w', encoding='utf-8'),
              ensure_ascii=False, separators=(',', ':'))
    return index

if __name__ == '__main__':
    idx = build(sys.argv[1:-1], sys.argv[-1])
    print(f'아이템 {len(idx)}종 생성 완료')
