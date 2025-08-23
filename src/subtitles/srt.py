# SRT 생성(문장 분리·타임코드 할당)
import math


def split_sentences_ko(text: str):
    # 매우 단순한 분할 (개선 여지: kss 등 라이브러리)
    parts = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
    return parts if parts else [text]




def build_srt(text: str, total_sec: float):
    parts = split_sentences_ko(text)
    total_chars = sum(len(p) for p in parts)
    cursor = 0.0
    items = []
    for idx, p in enumerate(parts, start=1):
        dur = total_sec * (len(p) / total_chars) if total_chars else total_sec / len(parts)
        start = cursor
        end = min(cursor + dur, total_sec)
        items.append({"index": idx, "start": start, "end": end, "text": p})
        cursor = end
    return items