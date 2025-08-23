import argparse
import os
import random
import pandas as pd
from gtts import gTTS

# 경로 설정 (프로젝트 루트 기준 상대 경로)
DATA_DIR = os.path.join("..", "data", "quotes")
OUTPUT_DIR = os.path.join("..", "output", "audio")

# 보장: 출력 폴더 없으면 생성
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_quote(mode: str) -> str:
    """CSV에서 랜덤 문구 하나 로드"""
    csv_path = os.path.join(DATA_DIR, f"{mode}.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    if "text" not in df.columns:
        raise ValueError("CSV must contain a 'text' column")

    row = df.sample().iloc[0]
    return row["text"]


def text_to_speech(text: str, filename: str):
    """텍스트를 음성(mp3)으로 변환"""
    tts = gTTS(text=text, lang="ko")
    out_path = os.path.join(OUTPUT_DIR, filename)
    tts.save(out_path)
    print(f"### Saved: {out_path}")


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--mode", choices=["morning", "bedtime", "breathing"], required=True, help="콘텐츠 모드 선택")
    parser.add_argument("--mode", choices=["morning", "bedtime", "breathing"], help="콘텐츠 모드 선택")
    args = parser.parse_args()
    print(f"args: {args}")

    # 디버깅 모드 기본값
    args.mode = "morning"

    # 1) 문구 불러오기
    quote = load_quote(args.mode)
    print(f"### 선택된 문구: {quote}")

    # 2) 음성 파일 생성
    text_to_speech(quote, f"{args.mode}_voice.mp3")


if __name__ == "__main__":
    main()