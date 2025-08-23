import os
from moviepy import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips

"""
목표
output/video/morning_test.mp4 파일 하나 생성
배경 영상 + 보이스만 합쳐져 있음
실행해보면 "숲 영상"이 나오면서 gTTS 음성이 잘 들려야 함
"""

# 경로 설정
VIDEO_PATH = os.path.join("..", "assets", "videos", "forest.mp4")
VOICE_PATH = os.path.join("..", "output", "audio", "morning_voice.mp3")
OUTPUT_PATH = os.path.join("..", "output", "video", "morning_test.mp4")


# 보장: 출력 폴더 생성
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# 배경 영상 / 음성 로드
bg_video = VideoFileClip(VIDEO_PATH)
voice = AudioFileClip(VOICE_PATH)

if voice.duration > bg_video.duration:
    # 마지막 프레임 이미지 추출
    last_frame = bg_video.get_frame(bg_video.duration - 0.1)
    freeze_clip = ImageClip(last_frame).set_duration(voice.duration - bg_video.duration)

    # 원본 영상 + 정지 프레임 이어붙이기
    extended_video = concatenate_videoclips([bg_video, freeze_clip])
else:
    # 영상이 더 길면 보이스에 맞게 자르기
    extended_video = bg_video.subclipped(0, voice.duration)

# 음성 길이에 맞게 영상 잘라내기
final_clip = bg_video.with_audio(voice).subclipped(0, voice.duration)

# 결과 저장
final_clip.write_videofile(OUTPUT_PATH, fps=24)

