import streamlit as st
import random
import time
import pandas as pd
import requests

# --- SETUP CƠ BẢN ---
try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

st.set_page_config(page_title="CYBER STRESS: OVERDRIVE", page_icon="☣️", layout="wide")

# --- CSS: GLITCH EFFECT & BLUR (Dành cho Robot phá đám) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Share+Tech+Mono&display=swap');

    /* 1. NỀN & FONT */
    .stApp {
        background-color: #02040a;
        background-image: radial-gradient(circle at 50% 50%, #0a1128 0%, #000000 100%);
        color: #00eaff;
        font-family: 'Share Tech Mono', monospace;
    }

    /* 2. HIỆU ỨNG ROBOT PHÁ ĐÁM (GLITCH) */
    @keyframes glitch-anim {
        0% { transform: translate(0) }
        20% { transform: translate(-2px, 2px) }
        40% { transform: translate(-2px, -2px) }
        60% { transform: translate(2px, 2px) }
        80% { transform: translate(2px, -2px) }
        100% { transform: translate(0) }
    }
    .glitch-mode {
        animation: glitch-anim 0.3s infinite;
        filter: blur(1px);
        color: #ff0055 !important;
        border-color: #ff0055 !important;
    }
    
    /* 3. HIỆU ỨNG ROBOT GIÚP ĐỠ (HINT) */
    .hint-box {
        border: 1px dashed #00ff00;
        background: rgba(0, 255, 0, 0.1);
        color: #00ff00;
        padding: 10px;
        text-align: center;
        animation: float 2s infinite;
    }

    /* 4. THANH ARMOR (SHIELD) */
    .armor-bar {
        height: 10px;
        background-color: #333;
        border-radius: 5px;
        overflow: hidden;
        margin-bottom: 10px;
    }
    .armor-fill {
        height: 100%;
        background: linear-gradient(90deg, #00eaff, #0055ff);
        transition: width 0.5s linear;
    }

    /* 5. GIAO DIỆN CHÍNH */
    .hud-display {
        background: rgba(10, 20, 30, 0.8);
        border: 2px solid #0055ff;
        box-shadow: 0 0 15px rgba(0, 85, 255, 0.2);
        padding: 30px;
        text-align: center;
        border-radius: 10px;
    }
    .stButton>button {
        background: #050a14;
        border: 1px solid #00eaff;
        color: #00eaff;
        font-family: 'Rajdhani', sans-serif;
        font-size: 18px;
        height: 55px;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background: #00eaff;
        color: #000;
        box-shadow: 0 0 20px #00eaff;
    }
    </style>
""", unsafe_allow_html=True)

# --- DỮ LIỆU TỪ VỰNG ---
word_data = {
    # Image 1 (-ary)
    "Infirmary": [2, "/ɪn'fɜ:.mə.ri/"], "Itinerary": [2, "/aɪ'tɪ.nə.rə.ri/"], "Luminary": [1, "/'lu:.mɪ.mə.ri/"],
    "Military": [1, "/'mɪ.lɪ.tə.ri/"], "Monetary": [1, "/'mʌ.nɪ.tə.ri/"], "Ordinary": [1, "/'ɔ:.dən.ri/"],
    "Secretary": [1, "/'se.krə.tri/"], "Temporary": [1, "/'tem.pə.rə.ri/"], "February": [1, "/'fe.brʊ.ə.ri/"],
    "Dietary": [1, "/'daɪ.ə.tə.ri/"], "Documentary": [3, "/ˌdɒk.ju'men.tri/"], "Contemporary": [2, "/kən'tem.pə.rə.ri/"],
    "Preliminary": [2, "/prɪ'lɪ.mɪ.nə.ri/"], "Anniversary": [3, "/ˌæ.nɪ'vɜ:.sə.ri/"], "Vocabulary": [2, "/və'kæ.bju.lə.ri/"],
    "Extraordinary": [2, "/ɪk'strɔ:.də.nə.ri/"], "Budgetary": [1, "/'bʌ.dʒɪ.tə.ri/"], "Sanitary": [1, "/'sæ.nɪ.tə.ri/"],
    # Image 2 (-ise/ize)
    "Advertise": [1, "/'æd.və.taɪz/"], "Analyse": [1, "/'æn.əl.aɪz/"], "Authorise": [1, "/'ɔ:.θə.raɪz/"], "Capitalise": [1, "/'kæp.ə.təl.aɪz/"],
    "Catalyse": [1, "/'kæt.əl.aɪz/"], "Centralise": [1, "/'sen.trə.laɪz/"], "Colonise": [1, "/'kɒ.lə.naɪz/"], "Compromise": [1, "/'kɒm.prə.maɪz/"],
    "Customise": [1, "/'kʌs.tə.maɪz/"], "Deputise": [1, "/'dep.ju.taɪz/"], "Enterprise": [1, "/'en.tə.praɪz/"], "Energise": [1, "/'en.ə.dʒaɪz/"],
    "Empathise": [1, "/'em.pə.θaɪz/"], "Moralise": [1, "/'mɔ:.rəl.aɪz/"], "Emphasize": [1, "/'em.fə.saɪz/"], "Equalise": [1, "/'i:.kwə.laɪz/"],
    "Exercise": [1, "/'ek.sə.saɪz/"], "Finalise": [1, "/'faɪ.nəl.aɪz/"], "Maximise": [1, "/'mæk.sə.maɪz/"], "Memorise": [1, "/'mem.ə.raɪz/"],
    # Image 3 (-y)
    "Bakery": [1, "/'beɪ.kə.ri/"], "Balcony": [1, "/'bæl.kə.ni/"], "Battery": [1, "/'bæ.tə.ri/"], "Blackberry": [1, "/'blæk.bə.ri/"],
    "Agency": [1, "/'eɪ.dʒən.si/"], "Century": [1, "/'sen.tʃə.ri/"], "Chemistry": [1, "/'ke.mɪ.stri/"], "Colony": [1, "/'kɒ.lə.ni/"],
    "Ancestry": [1, "/'æn.ses.tri/"], "Boundary": [1, "/'baʊn.dri/"], "Comedy": [1, "/'kɒ.mə.di/"], "Contrary": [1, "/'kɒn.trə.ri/"],
    "Atrophy": [1, "/'æ.trə.fi/"], "Bravery": [1, "/'breɪ.və.ri/"], "Currency": [1, "/'kʌ.rən.si/"], "Custody": [1, "/'kʌs.tə.di/"],
    "Bankruptcy": [1, "/'bæŋ.krʌpt.si/"], "Brewery": [1, "/'bru:.ə.ri/"], "Density": [1, "/'den.sə.ti/"], "Dentistry": [1, "/'den.tɪ.stri/"],
    # Image 4 (-ity)
    "Activity": [2, "/æk'tɪ.və.ti/"], "Capacity": [2, "/kə'pæ.sə.ti/"], "Fragility": [2, "/frə'dʒɪ.lə.ti/"], "Identity": [2, "/aɪ'den.tə.ti/"],
    "Authority": [2, "/ɔ:'θɒ.rə.ti/"], "Celebrity": [2, "/sə'le.brə.ti/"], "Finality": [2, "/faɪ'næ.lə.ti/"], "Impunity": [2, "/ɪm'pju:.nə.ti/"],
    "Civility": [2, "/sə'vɪ.lə.ti/"], "Facility": [2, "/fə'sɪ.lə.ti/"], "Faculty": [1, "/'fæk.əl.ti/"], "Inanity": [2, "/ɪ'næ.nə.ti/"],
    "Commodity": [2, "/kə'mɒ.də.ti/"], "Deputy": [1, "/'dep.ju.ti/"], "Indignity": [2, "/ɪn'dɪg.nə.ti/"], "Infinity": [2, "/ɪn'fɪ.nə.ti/"],
    "Community": [2, "/kə'mju:.nə.ti/"], "Complexity": [2, "/kəm'plek.sə.ti/"], "Extremity": [2, "/ɪk'stre.mə.ti/"], "Hospitality": [3, "/ˌhɒs.pɪ'tæ.lə.ti/"],
    # Image 5 (-ify)
    "Horrify": [1, "/'hɒ.rɪ.faɪ/"], "Notify": [1, "/'nəʊ.tɪ.faɪ/"], "Modify": [1, "/'mɒ.dɪ.faɪ/"], "Simplify": [1, "/'sɪm.plɪ.faɪ/"],
    "Identify": [2, "/aɪ'den.tɪ.faɪ/"], "Qualify": [1, "/'kwɒ.lɪ.faɪ/"], "Satisfy": [1, "/'sæ.tɪs.faɪ/"], "Quantify": [1, "/'kwɒn.tɪ.faɪ/"],
    "Intensify": [2, "/ɪn'ten.sɪ.faɪ/"], "Terrify": [1, "/'te.rɪ.faɪ/"], "Magnify": [1, "/'mæg.nɪ.faɪ/"], "Purify": [1, "/'pjʊə.rɪ.faɪ/"],
    "Electrify": [2, "/ɪ'lek.trɪ.faɪ/"], "Verify": [1, "/'ve.rɪ.faɪ/"], "Exemplify": [2, "/ɪg'zem.plɪ.faɪ/"], "Specify": [1, "/'spe.sɪ.faɪ/"],
    "Justify": [1, "/'dʒʌs.tɪ.faɪ/"], "Clarify": [1, "/'klæ.rə.faɪ/"], "Testify": [1, "/'tes.tɪ.faɪ/"], "Personify": [2, "/pə'sɒ.nɪ.faɪ/"],
    # Original (-o/-age)
    "Inferno": [2, "/in'fз:.nou/"], "Mosquito": [2, "/mə'ski:.tou/"], "Manifesto": [3, "/,mæn.ə'fes.tou/"], "Casino": [2, "/kə'si:.nou/"],
    "Advantage": [2, "/əd'vɑːn.tɪdʒ/"], "Encourage": [2, "/ɪn'kʌr.ɪdʒ/"]
}

sentence_data = [
    {"ipa": "/aɪ ə'k.nɒl.ɪdʒ maɪ 'prɪv.əl.ɪdʒ/", "text": "I acknowledge my privilege"},
    {"ipa": "/ðə 'fəʊ.təʊ ɪz ɪn ðə 'ɔː.fən.ɪdʒ/", "text": "The photo is in the orphanage"},
    {"ipa": "/hi 'sæ.tɪs.faɪd ðə 'ɔ:.di.əns/", "text": "He satisfied the audience"},
    {"ipa": "/ʃi wɒnts tu 'kæp.ə.təl.aɪz ɒn ɪt/", "text": "She wants to capitalise on it"},
    {"ipa": "/ðeɪ 'ɔ:.θə.raɪz ðə 'kɒn.trækt/", "text": "They authorise the contract"}
]

# --- STATE MANAGEMENT ---
if 'user_db' not in st.session_state: st.session_state.user_db = {}
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'score' not in st.session_state: st.session_state.score = 0
if 'start_time' not in st.session_state: st.session_state.start_time = 0
if 'glitch_active' not in st.session_state: st.session_state.glitch_active = False

# --- LOGIC THÔNG MINH (MODE 2 STRATEGY) ---
def strategic_distractors(correct_ipa):
    """Tạo đáp án nhiễu dựa trên lỗi sai phát âm thực tế."""
    distractors = set()
    distractors.add(correct_ipa)
    
    # 1. CHIẾN THUẬT: Vowel Confusion (Nhầm lẫn nguyên âm)
    # Thay thế các nguyên âm na ná nhau
    vowel_map = {
        "eɪ": "e",  # /ei/ -> /e/ (make -> mek)
        "aɪ": "i",  # /ai/ -> /i/ (like -> lick)
        "i:": "ɪ",  # /i:/ -> /i/ (heat -> hit)
        "æ": "e",   # /ae/ -> /e/ (man -> men)
        "ə": "ʌ",   # schwa -> /u/
        "oʊ": "ɒ"   # /ou/ -> /o/
    }
    
    # 2. CHIẾN THUẬT: Stress Shift (Dịch chuyển trọng âm)
    # Đây là lỗi phổ biến nhất
    def shift_stress(ipa):
        if "'" in ipa:
            clean = ipa.replace("'", "")
            # Tìm vị trí nguyên âm để đặt dấu trọng âm sai
            vowels = [i for i, char in enumerate(clean) if char in "aeiouəʌɒɔɪʊ"]
            if len(vowels) > 1:
                # Chọn random một vị trí nguyên âm khác
                idx = random.choice(vowels)
                return clean[:idx] + "'" + clean[idx:]
        return ipa

    # Tạo 3 đáp án sai
    attempts = 0
    while len(distractors) < 4 and attempts < 30:
        fake = correct_ipa
        strategy = random.choice(["vowel", "stress", "consonant"])
        
        if strategy == "vowel":
            for k, v in vowel_map.items():
                if k in fake:
                    fake = fake.replace(k, v, 1)
                    break
        elif strategy == "stress":
            fake = shift_stress(fake)
        elif strategy == "consonant":
            # Thay đổi phụ âm cuối s/z, t/d
            if "s" in fake: fake = fake.replace("s", "z")
            elif "z" in fake: fake = fake.replace("z", "s")
            elif "t" in fake: fake = fake.replace("t", "d")
        
        # Nếu fake giống hệt cái đúng (do không tìm thấy gì để thay), thêm dấu :
        if fake == correct_ipa:
            fake = fake.replace("/", "") + ":/"

        distractors.add(fake)
        attempts += 1
        
    return list(distractors)

def load_lottieurl(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_robot = load_lottieurl("https://lottie.host/6a56e300-47a3-4a1c-99c5-6809e5192102/1sZ8ilG7hS.json")

def start_game(mode):
    st.session_state.game_mode = mode
    st.session_state.score = 0
    st.session_state.q_index = 0
    st.session_state.page = 'playing'
    st.session_state.message = ""
    st.session_state.glitch_active = False
    
    if mode == 3:
        idx = list(range(len(sentence_data)))
        random.shuffle(idx)
        st.session_state.shuffled_keys = idx
    else:
        keys = list(word_data.keys())
        random.shuffle(keys)
        st.session_state.shuffled_keys = keys
    st.session_state.start_time = time.time()

def process_answer(is_correct, correct_val, armor_val):
    elapsed = time.time() - st.session_state.start_time
    
    # ROBOT PHẢN ỨNG: Nếu trả lời quá nhanh (< 2s) -> Kích hoạt Glitch
    st.session_state.glitch_active = True if elapsed < 2.0 else False

    base_points = 100
    if is_correct:
        # Nếu Armor còn > 50% -> Nhân đôi điểm
        multiplier = 2 if armor_val > 50 else 1
        points = base_points * multiplier
        st.session_state.score += points
        msg = f"✅ CRITICAL HIT! +{points} PTS" if multiplier > 1 else f"✅ TARGET HIT! +{points} PTS"
        st.session_state.message = msg
    else:
        st.session_state.message = f"❌ SYSTEM FAIL! ANS: {correct_val}"
    
    time.sleep(1)
    st.session_state.q_index += 1
    st.session_state.start_time = time.time()
    st.session_state.current_options = [] 
    st.rerun()

# --- GIAO DIỆN ---
left, mid, right = st.columns([1, 2, 1])

# --- CỘT TRÁI: AI & ARMOR ---
with left:
    st.markdown("### 🤖 AI SECURITY")
    if LOTTIE_AVAILABLE and lottie_robot:
        st_lottie(lottie_robot, height=180, key="bot")
    
    if st.session_state.page == 'playing':
        # Tính toán Armor (Shield) dựa trên thời gian
        # Giả sử mỗi câu có 15 giây để suy nghĩ. Armor giảm dần về 0.
        elapsed = time.time() - st.session_state.start_time
        max_time = 15.0 
        armor_pct = max(0, int(100 - (elapsed / max_time * 100)))
        
        st.markdown(f"**🛡️ SHIELD INTEGRITY: {armor_pct}%**")
        
        # Thanh Armor đổi màu
        color = "#00eaff" if armor_pct > 50 else "#ff0055"
        st.markdown(f"""
        <div class="armor-bar">
            <div class="armor-fill" style="width:{armor_pct}%; background:{color};"></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("WARNING: SHIELD < 50% = NO CRIT BONUS")
        
        # ROBOT HINT (Nếu suy nghĩ quá lâu > 8s)
        if elapsed > 8:
            st.markdown(f"<div class='hint-box'>⚠️ AI HINT: DETECTED LATENCY.<br>STAY FOCUSED AGENT!</div>", unsafe_allow_html=True)

# --- CỘT GIỮA: CHIẾN TRƯỜNG ---
with mid:
    st.markdown("<h1 style='text-align:center'>CYBER STRESS</h1>", unsafe_allow_html=True)
    
    if st.session_state.page == 'welcome':
        user = st.text_input("AGENT LOGIN:", placeholder="CODENAME")
        if user:
            st.session_state.current_user = user
            st.success("ACCESS GRANTED")
            c1, c2, c3 = st.columns(3)
            if c1.button("MODE 1\nSTRESS"): start_game(1); st.rerun()
            if c2.button("MODE 2\nIPA"): start_game(2); st.rerun()
            if c3.button("MODE 3\nDECODE"): start_game(3); st.rerun()

    elif st.session_state.page == 'playing':
        # Nếu Armor về 0 -> Tự động thua câu này
        if armor_pct == 0:
            st.error("SHIELD BREACHED! TURN LOST.")
            process_answer(False, "TIME OUT", 0)

        # Xử lý Glitch (Nếu câu trước trả lời quá nhanh)
        glitch_class = "glitch-mode" if st.session_state.glitch_active else ""
        if st.session_state.glitch_active:
             st.toast("⚠️ SPEED ANOMALY DETECTED! SYSTEM UNSTABLE!", icon="👾")

        if st.session_state.q_index < 10 and st.session_state.q_index < len(st.session_state.shuffled_keys):
            
            # --- GAME LOGIC ---
            if st.session_state.game_mode in [1, 2]:
                word = st.session_state.shuffled_keys[st.session_state.q_index]
                correct_stress = word_data[word][0]
                correct_ipa = word_data[word][1]

                # Hiển thị từ vựng (Có thể bị Glitch làm mờ)
                st.markdown(f"""
                <div class="hud-display {glitch_class}">
                    <h1 style='margin:0; font-size:50px; color:#fff'>{word}</h1>
                </div>
                """, unsafe_allow_html=True)

                if st.session_state.game_mode == 1:
                    c1, c2, c3 = st.columns(3)
                    with c1: 
                        if st.button("STRESS [1]"): process_answer(correct_stress==1, 1, armor_pct)
                    with c2: 
                        if st.button("STRESS [2]"): process_answer(correct_stress==2, 2, armor_pct)
                    with c3: 
                        if st.button("STRESS [3]"): process_answer(correct_stress==3, 3, armor_pct)
                
                elif st.session_state.game_mode == 2:
                    # Tạo đáp án thông minh 1 lần
                    if not st.session_state.get('current_options'):
                        st.session_state.current_options = strategic_distractors(correct_ipa)
                    
                    opts = st.session_state.current_options
                    
                    # Nút bấm cũng bị Glitch nếu cần
                    col_a, col_b = st.columns(2)
                    for i, op in enumerate(opts):
                        with (col_a if i%2==0 else col_b):
                            # Nút bấm có hiệu ứng glitch class thông qua CSS
                            if st.button(op): process_answer(op==correct_ipa, correct_ipa, armor_pct)

            elif st.session_state.game_mode == 3:
                # Mode 3 logic (Giữ nguyên)
                idx = st.session_state.shuffled_keys[st.session_state.q_index]
                item = sentence_data[idx]
                st.markdown(f"<div class='hud-display'><h3>{item['ipa']}</h3></div>", unsafe_allow_html=True)
                ans = st.text_input("DECODE:")
                if st.button("SUBMIT"):
                    clean_u = ans.strip().lower().rstrip('.')
                    clean_t = item['text'].strip().lower().rstrip('.')
                    process_answer(clean_u == clean_t, item['text'], armor_pct)

        else:
            # End Game
            st.session_state.user_db[st.session_state.current_user] = st.session_state.score
            st.session_state.page = 'result'
            st.rerun()

    elif st.session_state.page == 'result':
        st.markdown(f"<h1 style='text-align:center; font-size:80px'>{st.session_state.score}</h1>", unsafe_allow_html=True)
        if st.button("MAIN MENU"): st.session_state.page = 'welcome'; st.rerun()

# --- CỘT PHẢI: LOGS ---
with right:
    st.markdown("### 📡 DATA LINK")
    if st.session_state.user_db:
        df = pd.DataFrame(list(st.session_state.user_db.items()), columns=['AGENT', 'SCORE'])
        st.dataframe(df.sort_values('SCORE', ascending=False), hide_index=True)
    st.metric("CURRENT SCORE", st.session_state.score)
