import streamlit as st
import random
import time
import pandas as pd
import requests

# --- XỬ LÝ LỖI THƯ VIỆN & SETUP ---
try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

st.set_page_config(page_title="CYBER STRESS // OMEGA", page_icon="💠", layout="wide")

# --- ASSETS LOADING ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Robot mới (Giao diện AI Assistant - Cyberpunk)
lottie_url = "https://lottie.host/6a56e300-47a3-4a1c-99c5-6809e5192102/1sZ8ilG7hS.json" # Robot xịn hơn
lottie_robot = load_lottieurl(lottie_url) if LOTTIE_AVAILABLE else None

# --- CSS CAO CẤP (FULL SCREEN DASHBOARD) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Share+Tech+Mono&display=swap');

    /* 1. BACKGROUND & LAYOUT */
    .stApp {
        background-color: #050505;
        background-image: 
            linear-gradient(rgba(0, 255, 194, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 194, 0.05) 1px, transparent 1px);
        background-size: 40px 40px;
        color: #00eaff;
        font-family: 'Share Tech Mono', monospace;
    }

    /* 2. PANEL BOXES (Tạo khung cho từng khu vực) */
    .css-1r6slb0, .css-keje6w { /* Streamlit Column styling hack */
        background: rgba(10, 20, 30, 0.6);
        border: 1px solid #1f2937;
        padding: 15px;
        border-radius: 8px;
    }

    /* 3. NEON TEXT & HEADERS */
    h1, h2, h3 {
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        color: #fff;
        text-shadow: 0 0 10px rgba(0, 234, 255, 0.5);
    }
    
    /* 4. GLOWING BUTTONS */
    .stButton>button {
        background: #0a0a0a;
        border: 1px solid #00eaff;
        color: #00eaff;
        font-family: 'Rajdhani', sans-serif;
        font-size: 20px;
        font-weight: bold;
        transition: 0.3s;
        height: 60px;
        width: 100%;
    }
    .stButton>button:hover {
        background: #00eaff;
        color: #000;
        box-shadow: 0 0 25px #00eaff;
        transform: scale(1.02);
    }

    /* 5. HUD DISPLAY (Khung từ vựng) */
    .hud-display {
        background: rgba(0,0,0,0.8);
        border: 2px solid #ff0055; /* Red border for enemy/target */
        box-shadow: 0 0 20px rgba(255, 0, 85, 0.2);
        padding: 30px;
        text-align: center;
        margin-bottom: 20px;
        border-radius: 10px;
        position: relative;
    }
    .hud-word {
        font-size: 55px;
        color: #fff;
        font-weight: 700;
        letter-spacing: 3px;
    }
    
    /* 6. INPUT FIELD */
    .stTextInput input {
        background: #000;
        border: 1px solid #00eaff;
        color: #00eaff;
        text-align: center;
        font-size: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE (Đã gộp đầy đủ) ---
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
if 'current_user' not in st.session_state: st.session_state.current_user = ""
if 'game_mode' not in st.session_state: st.session_state.game_mode = None
if 'score' not in st.session_state: st.session_state.score = 0
if 'q_index' not in st.session_state: st.session_state.q_index = 0
if 'start_time' not in st.session_state: st.session_state.start_time = 0
if 'shuffled_keys' not in st.session_state: st.session_state.shuffled_keys = []
if 'message' not in st.session_state: st.session_state.message = ""

# --- LOGIC CỐT LÕI (FIX BUG TRÙNG ĐÁP ÁN) ---
def generate_robust_distractors(correct_ipa):
    """
    Tạo ra 4 đáp án KHÁC NHAU hoàn toàn.
    """
    options = set()
    options.add(correct_ipa)
    
    # Danh sách các thao tác làm sai
    def mutate(ipa):
        # 1. Bỏ dấu trọng âm
        if "'" in ipa: return ipa.replace("'", "")
        # 2. Dịch chuyển dấu trọng âm
        if "'" in ipa: 
            clean = ipa.replace("'", "")
            pos = random.randint(1, len(clean)-2)
            return clean[:pos] + "'" + clean[pos:]
        # 3. Đổi nguyên âm
        replacements = [("e", "ə"), ("i", "ai"), ("æ", "a:"), ("ou", "o"), ("ɪ", "e")]
        for old, new in replacements:
            if old in ipa: return ipa.replace(old, new, 1)
        # 4. Đổi phụ âm đuôi
        if ipa.endswith("/"): return ipa[:-2] + "s/"
        return ipa + ":"

    attempts = 0
    while len(options) < 4 and attempts < 20:
        fake = mutate(correct_ipa)
        # Randomize thêm nếu vẫn trùng
        if fake in options:
            fake = fake.replace("/", "") + ":" + "/" 
        options.add(fake)
        attempts += 1
    
    # Nếu vẫn không đủ 4 (do từ quá ngắn), thêm đại ký tự
    final_list = list(options)
    while len(final_list) < 4:
        final_list.append(f"/{'x'*len(final_list)}/")
        
    random.shuffle(final_list)
    return final_list

# --- CÁC HÀM HỖ TRỢ KHÁC ---
def get_user_progress(username):
    if username not in st.session_state.user_db:
        st.session_state.user_db[username] = {'M1': None, 'M2': None, 'M3': None}
    return st.session_state.user_db[username]

def save_score(username, mode, score):
    st.session_state.user_db[username][f'M{mode}'] = score

def calculate_leaderboard():
    data = []
    for user, scores in st.session_state.user_db.items():
        s1 = scores['M1'] if scores['M1'] is not None else 0
        s2 = scores['M2'] if scores['M2'] is not None else 0
        s3 = scores['M3'] if scores['M3'] is not None else 0
        data.append({"AGENT": user, "STRESS": s1, "IPA": s2, "DECODE": s3, "TOTAL": s1+s2+s3})
    df = pd.DataFrame(data)
    if not df.empty: df = df.sort_values(by="TOTAL", ascending=False)
    return df

def start_game(mode):
    st.session_state.game_mode = mode
    st.session_state.score = 0
    st.session_state.q_index = 0
    st.session_state.page = 'playing'
    st.session_state.message = ""
    
    if mode == 3:
        indices = list(range(len(sentence_data)))
        random.shuffle(indices)
        st.session_state.shuffled_keys = indices
    else:
        keys = list(word_data.keys())
        random.shuffle(keys)
        st.session_state.shuffled_keys = keys
    st.session_state.start_time = time.time()

def process_answer(is_correct, correct_val):
    elapsed = time.time() - st.session_state.start_time
    pts = max(10, 100 - int(elapsed * 2)) if is_correct else 0
    
    if is_correct:
        st.session_state.score += pts
        st.session_state.message = f"✅ TARGET HIT! +{pts} PTS"
    else:
        st.session_state.message = f"❌ MISS! ANS: {correct_val}"
    
    time.sleep(0.8)
    st.session_state.q_index += 1
    st.session_state.start_time = time.time()
    st.session_state.current_options = [] # Reset options cho Mode 2

# --- GIAO DIỆN CHÍNH (THE COCKPIT) ---

# HEADER
st.markdown("<h1>💠 CYBER STRESS // <span style='color:#ff0055'>OMEGA SYSTEM</span></h1>", unsafe_allow_html=True)

# LAYOUT 3 CỘT (ĐỂ LẤP ĐẦY MÀN HÌNH)
left_col, center_col, right_col = st.columns([1, 2, 1])

# --- 1. LEFT COLUMN: AI ASSISTANT ---
with left_col:
    st.markdown("### 🤖 AI CORE")
    if LOTTIE_AVAILABLE and lottie_robot:
        st_lottie(lottie_robot, height=200, key="robot_main")
    else:
        st.info("VISUAL CORE LOADING...")
    
    if st.session_state.page == 'playing':
        st.markdown("---")
        st.metric("SCORE", st.session_state.score)
        st.metric("LEVEL", f"{st.session_state.q_index + 1}/10")
        # Thanh máu ảo
        hp = max(0, 100 - (st.session_state.q_index * 10))
        st.write(f"ARMOR: {hp}%")
        st.progress(hp/100)

# --- 2. CENTER COLUMN: BATTLEFIELD ---
with center_col:
    if st.session_state.page == 'welcome':
        st.markdown("### >> IDENTIFICATION REQUIRED")
        username = st.text_input("ENTER CODENAME:", placeholder="AGENT_NAME...")
        
        if username:
            st.session_state.current_user = username
            progress = get_user_progress(username)
            st.success(f"ACCESS GRANTED: {username}")
            st.markdown("---")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                done = progress['M1'] is not None
                if st.button("MODE 1\nSTRESS", disabled=done):
                    start_game(1)
                    st.rerun()
            with c2:
                done = progress['M2'] is not None
                if st.button("MODE 2\nIPA", disabled=done):
                    start_game(2)
                    st.rerun()
            with c3:
                done = progress['M3'] is not None
                if st.button("MODE 3\nDECODE", disabled=done):
                    start_game(3)
                    st.rerun()

    elif st.session_state.page == 'playing':
        # HUD Message
        if st.session_state.message:
            color = "#00eaff" if "✅" in st.session_state.message else "#ff0055"
            st.markdown(f"<div style='text-align:center; color:{color}; font-weight:bold; font-size: 20px; margin-bottom:10px;'>{st.session_state.message}</div>", unsafe_allow_html=True)

        if st.session_state.q_index < 10 and st.session_state.q_index < len(st.session_state.shuffled_keys):
            
            # --- MODE 1 & 2 ---
            if st.session_state.game_mode in [1, 2]:
                current_word = st.session_state.shuffled_keys[st.session_state.q_index]
                correct_stress = word_data[current_word][0]
                correct_ipa = word_data[current_word][1]

                st.markdown(f"""
                <div class="hud-display">
                    <div style="font-size:12px; color:#ff0055; letter-spacing:2px;">TARGET LOCKED</div>
                    <div class="hud-word">{current_word}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.session_state.game_mode == 1:
                    b1, b2, b3 = st.columns(3)
                    with b1: 
                        if st.button("STRESS [1]"): 
                            process_answer(correct_stress == 1, correct_stress)
                            st.rerun()
                    with b2: 
                        if st.button("STRESS [2]"): 
                            process_answer(correct_stress == 2, correct_stress)
                            st.rerun()
                    with b3: 
                        if st.button("STRESS [3]"): 
                            process_answer(correct_stress == 3, correct_stress)
                            st.rerun()

                elif st.session_state.game_mode == 2:
                    # FIX BUG: Chỉ tạo đáp án nếu chưa có
                    if not st.session_state.get('current_options'):
                        st.session_state.current_options = generate_robust_distractors(correct_ipa)
                    
                    opts = st.session_state.current_options
                    
                    r1_col1, r1_col2 = st.columns(2)
                    r2_col1, r2_col2 = st.columns(2)
                    
                    with r1_col1:
                        if st.button(opts[0]): 
                            process_answer(opts[0] == correct_ipa, correct_ipa)
                            st.rerun()
                    with r1_col2:
                        if st.button(opts[1]): 
                            process_answer(opts[1] == correct_ipa, correct_ipa)
                            st.rerun()
                    with r2_col1:
                        if st.button(opts[2]): 
                            process_answer(opts[2] == correct_ipa, correct_ipa)
                            st.rerun()
                    with r2_col2:
                        if st.button(opts[3]): 
                            process_answer(opts[3] == correct_ipa, correct_ipa)
                            st.rerun()

            # --- MODE 3 ---
            elif st.session_state.game_mode == 3:
                idx = st.session_state.shuffled_keys[st.session_state.q_index]
                item = sentence_data[idx]
                
                st.markdown(f"""
                <div class="hud-display" style="border-color:#00eaff">
                    <div style="font-size:12px; color:#00eaff;">INCOMING SIGNAL</div>
                    <div style="font-size:30px; font-family:'Courier New'; color:#fff;">{item['ipa']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                inp = st.text_input("DECRYPT MESSAGE:", key=f"ans_{st.session_state.q_index}")
                if st.button("SEND TRANSMISSION"):
                    clean_u = inp.strip().lower().rstrip('.')
                    clean_t = item['text'].strip().lower().rstrip('.')
                    process_answer(clean_u == clean_t, item['text'])
                    st.rerun()
        else:
            save_score(st.session_state.current_user, st.session_state.game_mode, st.session_state.score)
            st.session_state.page = 'result'
            st.rerun()

    elif st.session_state.page == 'result':
        st.markdown(f"<h1 style='text-align:center; font-size:80px;'>{st.session_state.score}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>MISSION COMPLETE</h3>", unsafe_allow_html=True)
        if st.button("RETURN TO BASE"):
            st.session_state.page = 'welcome'
            st.rerun()

# --- 3. RIGHT COLUMN: LOGS ---
with right_col:
    st.markdown("### 📡 DATA LINK")
    df = calculate_leaderboard()
    if not df.empty:
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.caption("WAITING FOR DATA...")
    
    st.markdown("---")
    st.caption("SYSTEM STATUS: ONLINE")
    st.caption(f"CONNECTED: {st.session_state.current_user if st.session_state.current_user else 'GUEST'}")
