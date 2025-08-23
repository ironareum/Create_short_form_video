# 영상/이미지 선택 & 길이 맞춤
import os, random
from moviepy.editor import VideoFileClip, ImageClip


def pick_background(cfg, target_duration: float, seed=None):
    random.seed(seed)
    vdir = cfg["background"]["videos_dir"]
    idir = cfg["background"]["images_dir"]


    candidates = []
    if os.path.isdir(vdir):
        candidates += [os.path.join(vdir, f) for f in os.listdir(vdir) if f.lower().endswith('.mp4')]
    if os.path.isdir(idir):
        candidates += [os.path.join(idir, f) for f in os.listdir(idir) if f.lower().endswith(('.png','.jpg','.jpeg'))]


    assert candidates, "No background assets found"
    pick = random.choice(candidates)


    if pick.lower().endswith('.mp4'):
        clip = VideoFileClip(pick)
        if clip.duration >= target_duration:
            return clip.subclip(0, target_duration)
        else:
            # 단순 루프 (Phase 1)
            loops = int(target_duration // clip.duration) + 1
            return clip.loop(n=loops).subclip(0, target_duration)
    else:
        w, h = cfg["project"]["target_resolution"]
        img = ImageClip(pick).set_duration(target_duration).resize(newsize=(w, h)).margin(0)
        # 간단한 Ken Burns 효과(줌/패닝)는 다음 단계에서 추가
        return img