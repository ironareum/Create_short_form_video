# 전체 파이프라인 순서 정의
from src.utils.cfg import load_cfg
from src.utils.logger import get_logger
from src.content.loader import load_texts
from src.content.selector import pick_one
from src.tts.base import TTSBackend
from src.tts.gtts_backend import GTTSBackend # 기본 예시
from src.media.background import pick_background
from src.subtitles.srt import build_srt
from src.media.overlay import render_with_overlay
from src.media.audio import mix_audio
from src.media.render import export_video




def run_pipeline(category, text_id, min_sec, max_sec, seed, dry_run=False):
    cfg = load_cfg()
    log = get_logger()


    log.info({"event": "start", "category": category, "text_id": text_id})


    texts = load_texts(cfg, category)
    choice = pick_one(texts, cfg, text_id=text_id, seed=seed)


    # 1) 보이스
    tts: TTSBackend = GTTSBackend(cfg)
    voice_path, voice_dur = tts.synthesize(choice["text"]) # returns (path, seconds)


    # 길이 제약 보정(예: speaking_rate 조정 또는 재선택)
    if not (min_sec <= voice_dur <= max_sec):
        log.warning({"event": "duration_out_of_range", "voice_dur": voice_dur})
        # TODO: 재선택/속도조정 로직


    # 2) 배경
    bg_clip = pick_background(cfg, target_duration=voice_dur, seed=seed)


    # 3) 자막
    srt_items = build_srt(choice["text"], total_sec=voice_dur)


    # 4) 오버레이 + 믹싱
    composed_clip = render_with_overlay(cfg, bg_clip, srt_items, choice)
    final_audio = mix_audio(cfg, voice_path, bgm_dir=cfg["bgm"]["dir"], duration=voice_dur, seed=seed)


    # 5) 렌더
    if not dry_run:
        out_path = export_video(cfg, composed_clip, final_audio, choice)
        log.info({"event": "done", "out": out_path})
    else:
        log.info({"event": "dry_run_done"})