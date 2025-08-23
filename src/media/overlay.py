# 텍스트 오버레이(자막·스타일)
from moviepy.editor import CompositeVideoClip, TextClip




def render_with_overlay(cfg, bg_clip, srt_items, meta):
    w, h = cfg["project"]["target_resolution"]
    font = cfg["overlay"]["font_path"]
    fontsize = cfg["overlay"]["font_size"]
    margin = cfg["overlay"]["margin_px"]


    layers = [bg_clip.resize(newsize=(w, h))]


    for it in srt_items:
        # 중앙 정렬 캡션 (캡션 줄바꿈 자동)
        txt = TextClip(
            it["text"], fontsize=fontsize, font=font, color="white", method="caption",
            size=(int(w * cfg["overlay"]["text_box_width_ratio"]), None), align="center"
        ).set_start(it["start"]).set_end(it["end"]).set_position(("center", h//2))


        # if cfg["overlay"]