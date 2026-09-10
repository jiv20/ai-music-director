import streamlit as st
import librosa
import numpy as np

# --- 1. 음악 이론 알고리즘 세팅 (Krumhansl-Schmuckler Key Profiles) ---
maj_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
min_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# --- 2. 오디오 정밀 분석 함수 ---
def analyze_audio(file):
    # 음원 파일 로드
    y, sr = librosa.load(file, sr=22050)
    
    # [데이터 1] BPM 정밀 분석
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = round(float(tempo[0]))
    
    # [데이터 2] Key & Mode (조성) 분석
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_sum = np.sum(chroma, axis=1)
    
    # 12음계와 장/단조 프로필의 상관관계(상관계수) 계산
    maj_corrs = [np.corrcoef(chroma_sum, np.roll(maj_profile, i))[0, 1] for i in range(12)]
    min_corrs = [np.corrcoef(chroma_sum, np.roll(min_profile, i))[0, 1] for i in range(12)]
    
    if max(maj_corrs) > max(min_corrs):
        key = notes[maj_corrs.index(max(maj_corrs))]
        mode = "Major (장조)"
    else:
        key = notes[min_corrs.index(max(min_corrs))]
        mode = "Minor (단조)"
        
    # [데이터 3] 음색(Timbre) 객관적 분석 (스펙트럴 센트로이드 - 소리의 무게중심)
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    avg_cent = np.mean(cent)
    if avg_cent > 2000:
        timbre = "고음역대 중심 (날카롭고 통통 튀는 소리)"
    elif avg_cent > 1000:
        timbre = "중음역대 중심 (안정적이고 부드러운 소리)"
    else:
        timbre = "저음역대 중심 (무겁고 웅장한 소리)"
        
    return bpm, f"{key} {mode}", timbre

# --- 3. 웹 UI 및 시스템 구동 (Streamlit) ---
st.title("🎬 AI 음악 감독 정밀 시사회")
st.write("기획안을 작성하고 음원을 업로드하면, 오디오 파형을 정밀 분석하여 조화로움을 평가합니다.")

# 기획안 입력
st.header("📝 1. 씬(Scene) 기획안")
action = st.text_input("1. 주인공의 행동 (예: 쫓기며 달리고 있다)")
emotion = st.text_input("2. 핵심 감정 (예: 공포, 긴장감)")
genre = st.text_input("3. 영화 장르 (예: 스릴러)")

# 음원 업로드
st.header("🎵 2. 밴드랩 음원 업로드")
uploaded_file = st.file_uploader("음원 파일을 선택하세요 (.mp3, .wav)", type=['mp3', 'wav'])

if uploaded_file is not None and action and emotion and genre:
    st.audio(uploaded_file)
    
    if st.button("🤖 오디오 정밀 분석 및 교차 검증 시작"):
        with st.spinner('음원 파형의 BPM, Key, 음색을 수학적으로 추출하고 있습니다...'):
            # 오디오 분석 실행
            bpm, key_mode, timbre = analyze_audio(uploaded_file)
            
            # 결과 출력
            st.success("오디오 분석 완료!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📝 학생 기획 의도")
                st.write(f"- **장르:** {genre}")
                st.write(f"- **감정:** {emotion}")
                st.write(f"- **행동:** {action}")
                
            with col2:
                st.subheader("🎧 객관적 오디오 추출 데이터")
                st.write(f"- **BPM:** {bpm}")
                st.write(f"- **조성(Key):** {key_mode}")
                st.write(f"- **음색(Timbre):** {timbre}")
            
            st.divider()
            
            # 교차 검증 피드백 (LLM 대신 논리적 조건문으로 1차 피드백 구현)
            st.subheader("💡 AI 감독의 교차 검증 피드백")
            
            feedback = f"감독님께서 기획하신 감정은 **'{emotion}'**입니다. "
            
            if "슬픔" in emotion or "우울" in emotion or "공포" in emotion:
                if "Major" in key_mode:
                    feedback += f"하지만 실제 추출된 음악은 **{key_mode}**로 분위기가 밝게 설정되어 있습니다. 밴드랩에서 'Minor' 성향의 코드 루프로 교체하여 어두운 느낌을 살려보세요. "
                if bpm > 100:
                    feedback += f"또한 현재 템포({bpm} BPM)가 상황에 비해 다소 빠르고 다급합니다. BPM을 70~80으로 낮춰보세요."
            elif "신남" in emotion or "액션" in emotion or "기쁨" in emotion:
                if "Minor" in key_mode:
                    feedback += f"하지만 실제 추출된 음악은 **{key_mode}**로 다소 어둡게 들립니다. 'Major' 성향의 코드를 활용해보세요. "
                if bpm < 100:
                    feedback += f"또한 현재 템포({bpm} BPM)가 너무 느려 역동성이 부족합니다. BPM을 120 이상으로 올려보세요."
            else:
                feedback += f"현재 음악의 {bpm} BPM과 {key_mode} 조성이 기획안의 분위기와 전반적으로 잘 맞물려 들어갑니다. {timbre}의 질감 또한 적절히 활용되었습니다."
                
            st.info(feedback)
