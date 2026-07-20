# -*- coding: utf-8 -*-
"""아이템 이름 키워드 규칙 기반 카테고리 자동 분류"""
import re

RULES = [
    ('마스터리북', [r'^\[마스터리북\]']),
    ('주문서',     [r'주문서', r'^백의 주문서', r'혼돈의 주문서', r'^순백의']),
    ('소비',       [r'엘릭서', r'물약', r'포션', r'확성기', r'교환권', r'보따리', r'주스',
                    r'^하얀 물약', r'^빨간 물약', r'^파란 물약', r'회복제', r'^.*의 알$',
                    r'딸기|송편|만두|피자|햄버거|초콜릿|사탕|케이크|떡|과자|우유|아이스크림',
                    r'소환의 돌', r'^차원의', r'룬$', r'^황혼의 이슬$', r'^사막의 이슬$']),
    ('재료',       [r'원석$', r'파편', r'조각', r'결정', r'가루', r'광석', r'주괴', r'강철',
                    r'미스릴|오리하르콘|아다만티움|일렉트론|실버|골드|브론즈',
                    r'가죽|뼈|이빨|금니|눈동자|발도장|리본|머리|꼬리|날개|비늘|촉진제',
                    r'씨앗|나무|목재|천 조각|가공된', r'크리스탈$', r'수정$', r'항아리',
                    r'갓$|포자|뿔$|소울$|열매|버섯|껍질|심장|혓바닥|더듬이|점액|송곳니']),
    ('장비',       [r'투구|모자|헬멧', r'상의|하의|바지|갑옷|로브|슈트|메일', r'장갑|글러브',
                    r'신발|부츠|슈즈', r'망토|케이프', r'방패|실드', r'귀고리|이어링',
                    r'목걸이|펜던트', r'반지|링$', r'검$|도$|둔기|창$|폴암|단검|아대',
                    r'활$|석궁|보우', r'완드|스태프|지팡이', r'수리검|표창|건$|캐논']),
]

def categorize(name, is_gear=False):
    for cat, pats in RULES:
        for p in pats:
            if re.search(p, name):
                # 장비 규칙보다 옵션(실측) 신호가 우선
                if cat in ('재료', '소비') and is_gear:
                    return '장비'
                return cat
    return '장비' if is_gear else '기타'

if __name__ == '__main__':
    import json, collections, sys
    idx = json.load(open(sys.argv[1], encoding='utf-8'))
    c = collections.Counter()
    for it in idx['items']:
        it['cat'] = categorize(it['n'], bool(it['g']))
        c[it['cat']] += 1
    json.dump(idx, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(c.most_common())
    for cat in c:
        ex = [i['n'] for i in idx['items'] if i['cat'] == cat][:6]
        print(f'  {cat}: {ex}')
