"""
동행복권 역대 당첨번호 수집 스크립트
- 1회 ~ 최신 회차까지 모든 당첨번호 수집
- lotto_history.json 저장 (개별 회차 데이터)
- lotto_stats.json  저장 (번호별 출현 빈도 + 메타)
"""

import requests
import json
import time
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")

BASE = "https://www.dhlottery.co.kr"
DELAY = 0.35  # 서버 부담 최소화


def build_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Referer": f"{BASE}/lt645/result",
        "X-Requested-With": "XMLHttpRequest",
    })
    s.verify = False
    # 세션 쿠키 획득
    try:
        s.get(f"{BASE}/", timeout=15)
    except Exception as e:
        print(f"[WARN] 홈페이지 세션 초기화 실패: {e}")
    return s


def get_latest_round(s):
    try:
        r = s.get(f"{BASE}/lt645/selectLt645History.do", timeout=15)
        return r.json()["data"]["lastLtEpsd"]
    except Exception as e:
        print(f"[WARN] 최신 회차 조회 실패: {e}")
        return None


def fetch_rounds_batch(s, center_epsd):
    """center_epsd 기준 10개 회차 당첨번호 반환"""
    try:
        r = s.get(
            f"{BASE}/lt645/selectPstLt645InfoNew.do",
            params={"srchLtEpsd": str(center_epsd)},
            timeout=20,
        )
        lst = r.json().get("data", {}).get("list", [])
        results = []
        for item in lst:
            results.append({
                "round":   item["ltEpsd"],
                "date":    item["ltRflYmd"],          # YYYYMMDD
                "numbers": sorted([
                    item["tm1WnNo"], item["tm2WnNo"], item["tm3WnNo"],
                    item["tm4WnNo"], item["tm5WnNo"], item["tm6WnNo"],
                ]),
                "bonus":   item["bnsWnNo"],
            })
        return results
    except Exception as e:
        print(f"[WARN] 배치 조회 실패 (center={center_epsd}): {e}")
        return []


def main():
    print("=" * 55)
    print("  동행복권 역대 당첨번호 수집기")
    print("=" * 55)

    s = build_session()

    # 최신 회차 확인
    latest = get_latest_round(s)
    if not latest:
        print("[ERROR] 최신 회차를 가져올 수 없습니다. 종료합니다.")
        return
    print(f"[INFO] 최신 회차: {latest}회")

    # 수집 전략: center_epsd를 10 단계로 순회
    # API가 center±5 범위(총 10개) 반환 → 1, 11, 21... 로 커버
    seen_rounds = set()
    all_data = {}

    centers = list(range(5, latest + 11, 10))
    # 첫 번째 센터를 1로 설정해 1~10 확실히 커버
    centers = [1] + [c for c in centers if c != 1]

    total = len(centers)
    print(f"[INFO] total {total} API calls (approx {total * DELAY:.0f}s)")
    print()

    for idx, center in enumerate(centers, 1):
        batch = fetch_rounds_batch(s, center)
        new_cnt = 0
        for item in batch:
            rn = item["round"]
            if rn not in seen_rounds and 1 <= rn <= latest:
                seen_rounds.add(rn)
                all_data[rn] = item
                new_cnt += 1

        if idx % 20 == 0 or idx == total:
            print(f"  [{idx:4d}/{total}] center={center:5d} | "
                  f"수집 완료: {len(all_data):4d}회")

        time.sleep(DELAY)

    print()

    # 누락 회차 체크 및 재수집
    missing = [r for r in range(1, latest + 1) if r not in seen_rounds]
    if missing:
        print(f"[INFO] 누락 회차 {len(missing)}개 재수집: {missing[:10]}...")
        for rn in missing:
            batch = fetch_rounds_batch(s, rn)
            for item in batch:
                if item["round"] not in seen_rounds and 1 <= item["round"] <= latest:
                    seen_rounds.add(item["round"])
                    all_data[item["round"]] = item
            time.sleep(DELAY)

    # 정렬 후 저장
    history = [all_data[r] for r in sorted(all_data.keys())]
    print(f"[INFO] 최종 수집 회차: {len(history)}개")

    with open("lotto_history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=None, separators=(",", ":"))
    print("[DONE] lotto_history.json 저장 완료")

    # ── 전체 번호별 출현 빈도 ──
    freq = {n: 0 for n in range(1, 46)}
    for item in history:
        for n in item["numbers"]:
            freq[n] += 1

    # ── 최근 100회 번호별 출현 빈도 ──
    recent100 = history[-100:]
    freq_recent100 = {n: 0 for n in range(1, 46)}
    for item in recent100:
        for n in item["numbers"]:
            freq_recent100[n] += 1

    stats = {
        "source": "동행복권 (dhlottery.co.kr)",
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_rounds": len(history),
        "latest_round": latest,
        "recent100_start": recent100[0]["round"],
        "recent100_end":   recent100[-1]["round"],
        "freq": freq,
        "freq_recent100": freq_recent100,
    }

    with open("lotto_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print("[DONE] lotto_stats.json 저장 완료")

    # ── 통계 요약 출력 ──
    print()
    print("[ 전체 번호별 출현 빈도 상위 10 ]")
    top10 = sorted(freq.items(), key=lambda x: -x[1])[:10]
    for num, cnt in top10:
        bar = "█" * (cnt // 5)
        print(f"  번호 {num:2d}: {cnt:3d}회  {bar}")
    print()
    print(f"[ 최근 100회({recent100[0]['round']}~{recent100[-1]['round']}회) 출현 빈도 상위 10 ]")
    top10r = sorted(freq_recent100.items(), key=lambda x: -x[1])[:10]
    for num, cnt in top10r:
        bar = "▓" * cnt
        print(f"  번호 {num:2d}: {cnt:2d}회  {bar}")


if __name__ == "__main__":
    main()
