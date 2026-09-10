import streamlit as st
import librosa
import numpy as np

st.set_page_config(page_title="AI 믹싱 분석기", page_icon="🎧", layout="centered")

st.title("🎧 AI 음악 감독: 트랙 조화(Mixing) 분석기")
st.markdown("밴드랩에서 다운로드한 MP3/WAV 파일을 올리면, **트랙 간의 주파수 충돌(마스킹)과 볼륨 밸런스**를 정밀 진단합니다.")

uploaded_file = st.file_uploader("완성된 음원 파일을 업로드하세요.", type=['mp3', 'wav'])

if uploaded_file is not None:
    st.audio(uploaded_file)
    
    if st.button("🤖 AI 트랙 정밀 분석 시작"):
        with st.spinner("음원 파형의 주파수와 음압(RMS)을 분석 중입니다..."):
            # 1. 오디오 데이터 로드 (22050Hz 샘플링)
            y, sr = librosa.load(uploaded_file, sr=22050)
            
            # 2. 클리핑(Clipping) 및 다이내믹스 분석
            max_amplitude = np.max(np.abs(y))
            rms = librosa.feature.rms(y=y)[0]
            avg_rms = np.mean(rms)
            
            # 3. 주파수 대역별 에너지 분석 (트랙 충돌/마스킹 파악)
            # STFT(단기 푸리에 변환)를 통해 소리를 주파수 대역으로 분리
            S = np.abs(librosa.stft(y))
            freqs = librosa.fft_frequencies(sr=sr)
            
            # 대역폭 설정 (저음, 중음, 고음)
            low_idx = np.where(freqs < 250)[0]
            mid_idx = np.where((freqs >= 250) & (freqs < 4000))[0]
            high_idx = np.where(freqs >= 4000)[0]
            
            # 대역별 평균 에너지 계산
            low_energy = np.mean(S[low_idx, :])
            mid_energy = np.mean(S[mid_idx, :])
            high_energy = np.mean(S[high_idx, :])
            total_energy = low_energy + mid_energy + high_energy
            
            # 백분율 환산
            low_pct = (low_energy / total_energy) * 100
            mid_pct = (mid_energy / total_energy) * 100
            high_pct = (high_energy / total_energy) * 100

            st.success("분석이 완료되었습니다!")
            st.divider()

            # --- 진단 결과 출력 ---
            st.header("📊 AI 트랙 진단 결과")
            
            # [진단 1] 마스킹 현상 (주파수 충돌)
            st.subheader("1. 음역대 밸런스와 마스킹(Masking) 현상")
            st.write(f"- 저음역(베이스/킥): {low_pct:.1f}%")
            st.write(f"- 중음역(피아노/기타/신스): {mid_pct:.1f}%")
            st.write(f"- 고음역(하이햇/리드): {high_pct:.1f}%")
            
            if mid_pct > 65:
                st.error("⚠️ **[마스킹 경고]** 중음역대(피아노, 기타 등)에 악기가 너무 많이 뭉쳐 있습니다. 소리가 서로 잡아먹어 지저분하게 들립니다. 일부 트랙의 볼륨을 줄이거나 악기를 삭제하세요.")
            elif low_pct < 10:
                st.warning("⚠️ **[저음 부족]** 곡의 무게감을 잡아주는 저음(베이스/킥 드럼)이 너무 약합니다. 뼈대가 부실하게 들릴 수 있습니다.")
            elif high_pct < 5:
                st.warning("⚠️ **[고음 부족]** 찰랑거리는 고음역대가 부족하여 소리가 답답하게(먹먹하게) 들립니다. 하이햇이나 고음역 악기를 추가해보세요.")
            else:
                st.success("✅ **[밸런스 우수]** 저/중/고음역대가 고르게 분포되어 각 악기의 소리가 선명하게 분리되어 들립니다.")

            # [진단 2] 볼륨 및 클리핑
            st.subheader("2. 볼륨 밸런스 (다이내믹스)")
            if max_amplitude > 0.98:
                st.error("⚠️ **[클리핑 경고]** 전체 트랙의 볼륨이 너무 커서 소리가 찌그러지고(깨지고) 있습니다! 밴드랩에서 각 트랙의 페이더(볼륨)를 전체적으로 조금씩 내리세요.")
            elif avg_rms < 0.05:
                st.warning("⚠️ **[볼륨 미달]** 전체적인 소리가 너무 작습니다. 마스터 볼륨을 조금 올려주세요.")
            else:
                st.success("✅ **[볼륨 안정]** 소리가 깨지지 않고 안정적인 크기를 유지하고 있습니다.")
                
            st.divider()
            
            # [최종 성찰 가이드]
            st.info("💡 **[메타인지 조절 가이드]** 위 진단 결과와 짝꿍의 피드백을 종합해 보세요. 빨간색 경고가 떴다면 밴드랩으로 돌아가 해당 트랙을 수정한 뒤 다시 제출해야 합니다.")
