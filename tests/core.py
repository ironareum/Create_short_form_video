import random
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip


quote = ""
bg_video = ""
bgm = ""
voice = ""
final_audio = ""
txt  = ""

def create_quote():
    # 1. 문구 선택
    quotes = [
        "아침은 새로운 시작입니다. 오늘도 빛나길 바랍니다.",
        "당신은 충분히 소중하고, 오늘도 잘 해낼 수 있어요.",
        "숨을 고르고, 마음의 평화를 느껴보세요."
    ]
    quote = random.choice(quotes)

def generate_tts():
    # 2. 음성 생성
    tts = gTTS(text=quote, lang="ko")
    tts.save("voice.mp3")


def search_source(): #video_audio
    # 3. 배경 영상 + 배경 음악 로드
    bg_video = VideoFileClip("videos/forest.mp4").subclip(0, 60)  # 1분 이내
    bgm = AudioFileClip("bgm/soft.mp3").volumex(0.2)
    voice = AudioFileClip("voice.mp3")

    # 오디오 믹싱 (보이스 + 배경음)
    final_audio = voice.set_duration(bg_video.duration).fx(lambda a: a.volumex(1.0)).audio_fadeout(1).overlay(bgm)

def search_source():
    # 4. 텍스트 오버레이
    txt = TextClip(quote, fontsize=50, color="white", font="NanumGothic", method="caption", size=bg_video.size)
    txt = txt.set_position("center").set_duration(bg_video.duration)

    # 5. 최종 합성
    final = CompositeVideoClip([bg_video, txt])
    final = final.set_audio(final_audio)

    # 6. 결과 저장
    final.write_videofile("shorts_output.mp4", fps=24)


# 메인 실행
def unit_run():


if __name__ == "__main__":
    unit_run()