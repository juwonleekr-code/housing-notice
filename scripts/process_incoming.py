import json
import os
import glob
from datetime import date


def simplify_party(text):
    """법인명·괄호·직책 제거해서 짧게"""
    if not text:
        return text
    return text.split('(')[0].split('·')[0].strip()


def extract_index_entry(site):
    balcony_all = site.get('balcony', {}).get('all', '')
    balcony_str = f"전타입 {balcony_all}" if balcony_all else None

    return {
        "id":                  site.get('id'),
        "name":                site.get('name'),
        "sido":                site.get('location', {}).get('sido'),
        "sigungu":             site.get('location', {}).get('sigungu'),
        "district":            site.get('location', {}).get('district'),
        "units":               site.get('building', {}).get('totalUnits'),
        "moveIn":              site.get('building', {}).get('moveIn'),
        "avgPyeong":           site.get('pricing', {}).get('avgPyeongPrice'),
        "kookmin84Ratio":      site.get('pricing', {}).get('kookmin84Ratio'),
        "balcony":             balcony_str,
        "loanType":            site.get('loan', {}).get('type'),
        "loanRatio":           site.get('loan', {}).get('ratio'),
        "downPaymentGrade":    site.get('downPayment', {}).get('grade'),
        "essentialOptionRatio":site.get('options', {}).get('essentialRatio'),
        "fullOptionRatio":     site.get('options', {}).get('fullRatio'),
        "developer":           simplify_party(site.get('parties', {}).get('developer', '')),
        "trust":               simplify_party(site.get('parties', {}).get('trust', '')),
        "constructor":         simplify_party(site.get('parties', {}).get('constructor', '')),
        "regulated":           site.get('building', {}).get('regulated', False),
        "resaleRestriction":   site.get('building', {}).get('resaleRestriction', False),
        "totalRevenueEok":     site.get('pricing', {}).get('totalRevenueEok'),
    }


def main():
    incoming_files = glob.glob('incoming/*.json')

    if not incoming_files:
        print("incoming/ 폴더에 처리할 파일이 없습니다.")
        return

    index_path = 'data/index.json'
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)

    os.makedirs('data/sites', exist_ok=True)

    for filepath in incoming_files:
        print(f"\n처리 중: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            site = json.load(f)

        site_id = site.get('id')
        if not site_id:
            print(f"  오류: 'id' 필드 없음 → 건너뜀")
            continue

        # data/sites/{id}.json 저장
        site_path = f'data/sites/{site_id}.json'
        with open(site_path, 'w', encoding='utf-8') as f:
            json.dump(site, f, ensure_ascii=False, indent=2)
        print(f"  저장: {site_path}")

        # index.json 업데이트
        entry = extract_index_entry(site)
        ids = [s['id'] for s in index['sites']]
        if site_id in ids:
            index['sites'][ids.index(site_id)] = entry
            print(f"  index 갱신: {site_id}")
        else:
            index['sites'].append(entry)
            print(f"  index 추가: {site_id}")

        # incoming에서 삭제
        os.remove(filepath)
        print(f"  삭제: {filepath}")

    index['updated'] = date.today().isoformat()
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"\nindex.json 업데이트 완료: {index_path}")


if __name__ == '__main__':
    main()
