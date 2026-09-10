<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎛️ AI 편곡 및 믹싱 진단기</title>
    <style>
        body { font-family: 'Pretendard', sans-serif; background-color: #f0f2f5; padding: 20px; display: flex; justify-content: center; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 800px; width: 100%; }
        h1 { color: #2c3e50; text-align: center; font-size: 24px; }
        .box { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 5px solid #3498db; }
        select, button { width: 100%; padding: 12px; margin-top: 10px; border-radius: 5px; border: 1px solid #ccc; font-size: 16px; }
        button { background: #27ae60; color: white; border: none; font-weight: bold; cursor: pointer; margin-top: 20px; }
        button:hover { background: #219a52; }
        .result { display: none; margin-top: 20px; padding: 20px; border-radius: 8px; background: #e8f6f3; border: 1px solid #a3e4d7; }
        .warning { color: #c0392b; font-weight: bold; }
        .good { color: #27ae60; font-weight: bold; }
    </style>
</head>
<body>

<div class="container">
    <h1>🎛️ AI 편곡 & 믹싱 진단기</h1>
    <p style="text-align:center; color:#7f8c8d;">현재 밴드랩에 추가한 트랙(악기)들을 입력하면, AI가 주파수 충돌과 밸런스를 분석합니다.</p>

    <div class="box">
        <h3>🎬 1. 장면(Scene)의 목표 감정</h3>
        <select id="emotion">
            <option value="none">감정을 선택하세요</option>
            <option value="긴장/공포">긴장감, 공포, 스릴러</option>
            <option value="슬픔/우울">슬픔, 우울, 회상</option>
            <option value="기쁨/활기">기쁨, 활기, 희망</option>
        </select>
    </div>

    <div class="box">
        <h3>🎧 2. 밴드랩 악기 구성 (최대 4개)</h3>
        <select id="track1"><option value="none">트랙 1 악기 선택</option><option value="low">킥 드럼 / 베이스 (저음역)</option><option value="mid">피아노 / 어쿠스틱 기타 / 패드 (중음역)</option><option value="high">하이햇 / 리드 신스 / 플룻 (고음역)</option></select>
        <select id="track2"><option value="none">트랙 2 악기 선택</option><option value="low">킥 드럼 / 베이스 (저음역)</option><option value="mid">피아노 / 어쿠스틱 기타 / 패드 (중음역)</option><option value="high">하이햇 / 리드 신스 / 플룻 (고음역)</option></select>
        <select id="track3"><option value="none">트랙 3 악기 선택</option><option value="low">킥 드럼 / 베이스 (저음역)</option><option value="mid">피아노 / 어쿠스틱 기타 / 패드 (중음역)</option><option value="high">하이햇 / 리드 신스 / 플룻 (고음역)</option></select>
        <select id="track4"><option value="none">트랙 4 악기 선택</option><option value="low">킥 드럼 / 베이스 (저음역)</option><option value="mid">피아노 / 어쿠스틱 기타 / 패드 (중음역)</option><option value="high">하이햇 / 리드 신스 / 플룻 (고음역)</option></select>
    </div>

    <button onclick="analyzeArrangement()">🤖 AI 주파수 및 밸런스 진단하기</button>

    <div id="resultBox" class="result">
        <h3 style="margin-top:0; color:#2c3e50;">💡 진단 결과 및 AI 감독의 조언</h3>
        <p id="analysisText"></p>
    </div>
</div>

<script>
    function analyzeArrangement() {
        const tracks = [
            document.getElementById('track1').value,
            document.getElementById('track2').value,
            document.getElementById('track3').value,
            document.getElementById('track4').value
        ].filter(t => t !== 'none');

        const emotion = document.getElementById('emotion').value;
        const resultBox = document.getElementById('resultBox');
        const analysisText = document.getElementById('analysisText');

        if (emotion === 'none' || tracks.length === 0) {
            alert("감정과 최소 1개 이상의 트랙을 선택해주세요!");
            return;
        }

        let low = 0, mid = 0, high = 0;
        tracks.forEach(t => {
            if (t === 'low') low++;
            if (t === 'mid') mid++;
            if (t === 'high') high++;
        });

        let feedback = "";

        // 1. 마스킹 현상 (주파수 충돌) 진단 - 복잡한 메타인지 요소
        if (mid >= 3) {
            feedback += "<span class='warning'>[⚠️ 주파수 충돌 경고]</span> 중음역대(피아노, 기타 등) 악기가 너무 많습니다. 소리가 뭉쳐서 지저분하게 들리는 <strong>'마스킹(Masking) 현상'</strong>이 발생합니다. 트랙 하나의 볼륨을 대폭 줄이거나 좌우 패닝(Pan)을 조절하여 공간을 분리하세요.<br><br>";
        } else if (low >= 2) {
            feedback += "<span class='warning'>[⚠️ 저음역 뭉침 경고]</span> 베이스와 킥 드럼이 부딪히고 있습니다. 소리가 먹먹해지니 베이스 루프를 다른 것으로 교체하거나 볼륨을 낮추세요.<br><br>";
        } else {
            feedback += "<span class='good'>[✅ 주파수 밸런스 양호]</span> 악기들이 서로의 영역을 침범하지 않고 깔끔하게 분리되어 있습니다.<br><br>";
        }

        // 2. 대역폭 결핍 진단
        if (low === 0) feedback += "<span class='warning'>[텅 빈 뼈대]</span> 저음역(베이스/킥)이 없어 음악이 허공에 뜬 것처럼 가볍습니다. 무게감을 잡아줄 베이스 트랙을 추가해보세요.<br><br>";
        if (high === 0 && tracks.length >= 2) feedback += "<span class='warning'>[답답한 소리]</span> 고음역(하이햇/리드)이 없어 소리가 답답합니다. 공간을 열어줄 높은 소리의 루프를 찾아보세요.<br><br>";

        // 3. 감정 매칭 진단
        if (emotion === '긴장/공포' && low === 0) {
            feedback += "<strong>[감정 매칭 조언]</strong> 공포와 긴장감은 '낮고 무거운 진동(저음)'에서 나옵니다. 심장 박동 같은 킥 드럼이나 무거운 베이스를 반드시 추가하세요.";
        } else if (emotion === '기쁨/활기' && high === 0) {
            feedback += "<strong>[감정 매칭 조언]</strong> 활기찬 분위기에는 찰랑거리는 고음역대(하이햇, 탬버린) 타악기가 필수입니다. 밴드랩에서 리듬 악기를 보강하세요.";
        }

        analysisText.innerHTML = feedback + "<hr><p>🔍 <strong>[나의 조절 계획]</strong> AI의 진단을 바탕으로 밴드랩에서 어떤 루프를 삭제/추가/볼륨 조절할지 고민해 보세요.</p>";
        resultBox.style.display = 'block';
    }
</script>

</body>
</html>
