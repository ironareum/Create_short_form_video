# YouTube Shorts 자동화 - 전체 아키텍처 설계 (버전 0.1)

목적: 잔잔하고 따뜻한 위로/지혜/명상 숏폼(≤ 60초)을 완전 자동화로 생성·내보내기·업로드까지 확장 가능한 구조 설계.  
이 문서는 구조(골격)에 집중하며, 개별 라이브러리/버전은 추후 지속적으로 업데이트 예정입니다.  

---

## 1) 목표 기능 (MVP → 확장)

### MVP
- 텍스트 소스(명언·확언·명상 가이드) 선택
- TTS로 보이스오버 생성 (기본: gTTS 백엔드, 선택: OpenAI 등 플러그형)
- 배경(자연 영상/이미지) + BGM 합성
- 텍스트 오버레이(자막) 동기화
- 세로 1080×1920, 30fps, ≤ 58초 렌더링

### 확장 (Phase 2)
- 썸네일 자동 생성
- SRT 생성 및 외부자막 업로드 옵션
- YouTube Data API 업로드 자동화
- 스케줄러 실행 (Windows Task Scheduler / cron)
- A/B 테스트 (문구·배경·BGM 조합)

---

## 2) 디렉터리 구조 (제안)

shorts/  
├─ README.md  
├─ pyproject.toml # 또는 requirements.txt (버전 핀 고정)  
├─ .env.example # API 키, 기본 환경값 샘플  
├─ config/  
│ └─ settings.yaml # 전역 설정  
├─ data/  
│ └─ quotes/  
│ ├─ morning.csv # 아침 명언·확언  
│ ├─ bedtime.csv # 자기 전 확언  
│ └─ breathing.csv # 호흡 명상 스크립트  
├─ assets/  
│ ├─ videos/ # 자연 풍경 mp4 (저작권 클린)  
│ ├─ images/ # 일러스트/스틸 이미지  
│ ├─ bgm/ # BGM mp3/wav (루프 가능 음원)  
│ └─ fonts/ # 예: NotoSansKR-Regular.otf  
├─ outputs/  
│ ├─ videos/ # 최종 mp4  
│ └─ captions/ # srt/vtt  
├─ logs/  
├─ src/  
│ ├─ run.py # 오케스트레이터 (CLI)  
│ ├─ pipeline/  
│ │ ├─ orchestrator.py # 전체 파이프라인 순서 정의  
│ │ └─ steps.py # 개별 스텝 모음  
│ ├─ content/  
│ │ ├─ loader.py # CSV/JSON/프롬프트 로더  
│ │ └─ selector.py # 카테고리/길이 제약 고려 선택  
│ ├─ tts/  
│ │ ├─ base.py # TTS 백엔드 인터페이스  
│ │ └─ gtts_backend.py # 기본 구현 (옵션)  
│ ├─ media/  
│ │ ├─ background.py # 영상/이미지 선택 & 길이 맞춤  
│ │ ├─ overlay.py # 텍스트 오버레이 (자막·스타일)  
│ │ ├─ audio.py # 보이스+배경음 믹싱  
│ │ └─ render.py # 최종 렌더 (moviepy)  
│ ├─ subtitles/  
│ │ └─ srt.py # SRT 생성 (문장 분리·타임코드 할당)  
│ └─ utils/  
│ ├─ cfg.py # YAML/ENV 로딩  
│ ├─ logger.py # 구조적 로깅  
│ └─ timing.py # 길이/세이프티 마진 계산  
└─ tests/  
└─ test_selector.py  

---

## 3) 설정파일 스펙 (`config/settings.yaml`)


### project:
- out_dir: "outputs/videos"
- caption_dir: "outputs/captions"
- max_duration_sec: 58
- target_resolution: [1080, 1920] # width, height (세로)
- fps: 30

### content:
- default_category: "morning" # morning | bedtime | breathing
- csv_dir: "data/quotes"
- filters:
--   min_chars: 30
--   max_chars: 300 # TTS 속도에 따라 조정

### voice:
- backend: "gtts"   # gtts | openai | edge-tts
- lang: "ko"
- speaking_rate: 1.0
- out_format: "mp3"

### bgm:
- dir: "assets/bgm"
- target_lufs: -23
- ducking_db: -10

### background:
- videos_dir: "assets/videos"
- images_dir: "assets/images"
- pick_mode: "random" # random | by-tag

### overlay:
- font_path: "assets/fonts/NotoSansKR-Regular.otf"
- font_size: 60
- margin_px: 96
- text_box_width_ratio: 0.85
- position: "center" # center | bottom | custom(x,y)
- shadow: true

### export:
- codec: "libx264"
- audio_codec: "aac"
- crf: 18
- preset: "medium"
- audio_bitrate: "192k"

---

## 4) 데이터 스키마 (CSV)
### CSV 컬럼 : id, category, text, attribution, tags
- id: 고유키 (uuid 등)
- category: morning|bedtime|breathing
- text: 전체 본문 (줄바꿈 허용)
- attribution: 출처/저자(명언일 경우)
- tags: "forest, sky, warm" 같이 배경 선택 도움 태그

### 예시 (morning.csv): id,category,text,attribution,tags
- 1,morning,"아침은 새로운 시작입니다. 오늘도 천천히, 그러나 분명하게 나아가세요.",,forest,light
- 2,morning,"당신은 이미 충분합니다. 오늘의 해가 당신을 비출 거예요.",,sky,warm

---

## 5) 파이프라인 플로우 (시퀀스)
- 구성 로드: YAML + ENV → 런타임 파라미터 병합
- 콘텐츠 선택: 카테고리/길이/태그 제약 반영하여 1건 선택
- TTS: 보이스 생성(mp3/wav) → 길이 측정 → 58초 이하 보장 (과하면 텍스트 교체/속도 조정)
- 배경 선택: 태그/랜덤 → 영상 길이 맞춤(트림·루프) 또는 이미지(줌·패닝 효과)
- 자막/오버레이: 문장 분리→SRT 생성→ 렌더 시 오버레이(그림자/여백 포함)
- 오디오 믹싱: 보이스 + BGM(덕킹) → 페이드인/아웃
- 렌더: 1080×1920, 30fps, ≤ 58초 mp4 저장
- 결과물: outputs/videos/yyyymmdd_hhmm_topic.mp4 + outputs/captions/*.srt
- (옵션) 업로드: YouTube API 호출(제목·설명·태그·썸네일)

---

## 6) CLI 사용 시나리오 (예정 인터페이스)
### 예: 아침 명언 1개 생성
- python -m src.run --category morning --seed 42 --dry-run false 

### 자기 전 확언, 특정 텍스트 id 지정
- python -m src.run --category bedtime --text-id 2 

### 호흡 명상, 길이 목표 50~55초
- python -m src.run --category breathing --min-sec 50 --max-sec 55
주요 옵션(제안)  
-- category {morning,bedtime,breathing}  
-- text-id <id>: 특정 텍스트 강제 사용  
-- min-sec/--max-sec: 길이 범위 제약  
-- seed: 배경/음원 랜덤 고정  
-- dry-run: 렌더 없이 파이프라인 시뮬레이션  

---

## 7) 코드 스텁 (핵심 파일 초안)
- src/run.py  

---

## 8) 모듈 설치 (version)
- Name: gTTS, Version: 2.5.4  
- Name: pandas, Version: 2.3.2  
- Name: moviepy, Version: 2.2.1  
