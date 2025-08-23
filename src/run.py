# 오케스트레이터 (CLI)
import argparse
from pipeline.orchestrator import run_pipeline
"""
--category {morning,bedtime,breathing}
--text-id <id>: 특정 텍스트 강제 사용
--min-sec/--max-sec: 길이 범위 제약
--seed: 배경/음원 랜덤 고정
--dry-run: 렌더 없이 파이프라인 시뮬레이션
"""

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--category", default="morning")
    p.add_argument("--text-id", default=None)
    p.add_argument("--min-sec", type=int, default=45)
    p.add_argument("--max-sec", type=int, default=58)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    run_pipeline(
        category=args.category,
        text_id=args.text_id,
        min_sec=args.min_sec,
        max_sec=args.max_sec,
        seed=args.seed,
        dry_run=args.dry_run,
    )