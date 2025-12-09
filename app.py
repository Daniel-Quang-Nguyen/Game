import streamlit as st
import random
import time
import pandas as pd
import requests
from streamlit_lottie import st_lottie

# --- CONFIGURATION ---
st.set_page_config(page_title="CYBER STRESS // AI CORE", page_icon="💠", layout="wide")

# --- ASSETS LOADING ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Robot Animation (Cyberpunk Bot)
lottie_robot = load_lottieurl("https://lottie.host/02028682-1246-4444-9694-4325a6984e72/yJ5Z1YqQ0H.json") 
# Fallback if URL fails
if not lottie_robot:
    lottie_robot = "https://assets5.lottiefiles.com/packages/lf20_sk5h1kfn.json"

# --- ADVANCED CSS (GLOWING BLUE & ANIMATIONS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');

    /* 1. CURSOR & GLOBAL FONT */
    .stApp {
        background-color: #02040a;
        background-image: 
            linear-gradient(rgba(0, 255, 194, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 194, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #00eaff;
        font-family: 'Share Tech Mono', monospace;
        cursor: crosshair; /* Crosshair cursor */
    }

    /* 2. GLOWING INPUT TEXT */
    /* Input Text Color & Glow */
    .stTextInput>div>div>input {
        background-color: rgba(10, 20, 30, 0.9);
        color: #00eaff; 
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 8px #00eaff; /* Glowing Effect */
        border: 1px solid #0055ff;
        border-radius: 0px;
        caret-color: #00eaff; /* Mouse cursor inside input */
    }
    .stTextInput>div>div>input:focus {
        border-color: #00eaff;
        box-shadow: 0 0 15px rgba(0, 234, 255, 0.3);
    }

    /* 3. HUD BOX & ROBOT AREA */
    .hud-box {
        border: 1px solid #0055ff;
        box-shadow: 0 0 10px rgba(0, 85, 255, 0.3), inset 0 0 20px rgba(0, 85, 255, 0.05);
        padding: 20px;
        background: rgba(5, 10, 15, 0.8);
        border-radius: 5px;
        text-align: center;
        margin-bottom: 20px;
        position: relative;
    }
    
    /* 4. HINT BUBBLE */
    .hint-bubble {
        background: #001122;
        border: 1px solid #ffcc00;
        color: #ffcc00;
        padding: 10px;
        border-radius: 10px;
        position: relative;
        animation: float 3s ease-in-out infinite;
        box-shadow: 0 0 10px #ffcc00;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }

    /* 5. BUTTONS */
    .stButton>button {
        background-color: #050a14;
        color: #00eaff;
        border: 1px solid #00eaff;
        font-family: 'Orbitron', sans-serif;
        transition: all 0.2s;
        text-shadow: 0 0 5px #00eaff;
    }
    .stButton>button:hover {
        background-color: #00eaff;
        color: #000;
        box-shadow: 0 0 20px #00eaff;
    }
    .stButton>button:disabled {
        border-color: #333;
        color: #555;
        text-shadow: none;
    }

    </style>
""", unsafe_allow_html=True)

# --- HUGE DATASET (ALL IMAGES) ---
word_data = {
    # --- Image 1 (-ary) ---
    "Infirmary": [2, "/ɪn'fɜ:.mə.ri/"], "Itinerary": [2, "/aɪ'tɪ.nə.rə.ri/"], "Luminary": [1, "/'lu:.mɪ.mə.ri/"],
    "Military": [1, "/'mɪ.lɪ.tə.ri/"], "Monetary": [1, "/'mʌ.nɪ.tə.ri/"], "Ordinary": [1, "/'ɔ:.dən.ri/"],
    "Secretary": [1, "/'se.krə.tri/"], "Temporary": [1, "/'tem.pə.rə.ri/"], "February": [1, "/'fe.brʊ.ə.ri/"],
    "Dietary": [1, "/'daɪ.ə.tə.ri/"], "Documentary": [3, "/ˌdɒk.ju'men.tri/"], "Contemporary": [2, "/kən'tem.pə.rə.ri/"],
    "Preliminary": [2, "/prɪ'lɪ.mɪ.nə.ri/"], "Anniversary": [3, "/ˌæ.nɪ'vɜ:.sə.ri/"], "Vocabulary": [2, "/və'kæ.bju.lə.ri/"],
    "Extraordinary": [2, "/ɪk'strɔ:.də.nə.ri/"], "Budgetary": [1, "/'bʌ.dʒɪ.tə.ri/"], "Sanitary": [1, "/'sæ.nɪ.tə.ri/"],
    
    # --- Image 2 (-ise/ize) ---
    "Advertise": [1, "/'æd.və.taɪz/"], "Analyse": [1, "/'æn.əl.aɪz/"], "Authorise": [1, "/'ɔ:.θə.raɪz/"], "Capitalise": [1, "/'kæp.ə.təl.aɪz/"],
    "Catalyse": [1, "/'kæt.əl.aɪz/"], "Centralise": [1, "/'sen.trə.laɪz/"], "Colonise": [1, "/'kɒ.lə.naɪz/"], "Compromise": [1, "/'kɒm.prə.maɪz/"],
    "Customise": [1, "/'kʌs.tə.maɪz/"], "Deputise": [1, "/'dep.ju.taɪz/"], "Enterprise": [1, "/'en.tə.praɪz/"], "Energise": [1, "/'en.ə.dʒaɪz/"],
    "Empathise": [1, "/'em.pə.θaɪz/"], "Moralise": [1, "/'mɔ:.rəl.aɪz/"], "Emphasize": [1, "/'em.fə.saɪz/"], "Equalise": [1, "/'i:.kwə.laɪz/"],
    "Exercise": [1, "/'ek.sə.saɪz/"], "Finalise": [1, "/'faɪ.nəl.aɪz/"], "Maximise": [1, "/'mæk.sə.maɪz/"], "Memorise": [1, "/'mem.ə.raɪz/"],

    # --- Image 3 (-y) ---
    "Bakery": [1, "/'beɪ.kə.ri/"], "Balcony": [1, "/'bæl.kə.ni/"], "Battery": [1, "/'bæ.tə.ri/"], "Blackberry": [1, "/'blæk.bə.ri/"],
    "Agency": [1, "/'eɪ.dʒən.si/"], "Century": [1, "/'sen.tʃə.ri/"], "Chemistry": [1, "/'ke.mɪ.stri/"], "Colony": [1, "/'kɒ.lə.ni/"],
    "Ancestry": [1, "/'æn.ses.tri/"], "Boundary": [1, "/'baʊn.dri/"], "Comedy": [1, "/'kɒ.mə.di/"], "Contrary": [1, "/'kɒn.trə.ri/"],
    "Atrophy": [1, "/'æ.trə.fi/"], "Bravery": [1, "/'breɪ.və.ri/"], "Currency": [1, "/'kʌ.rən.si/"], "Custody": [1, "/'kʌs.tə.di/"],
    "Bankruptcy": [1, "/'bæŋ.krʌpt.si/"], "Brewery": [1, "/'bru:.ə.ri/"], "Density": [1, "/'den.sə.ti/"], "Dentistry": [1, "/'den.tɪ.stri/"],

    # --- Image 4 (-ity) ---
    "Activity": [2, "/æk'tɪ.və.ti/"], "Capacity": [2, "/kə'pæ.sə.ti/"], "Fragility": [2, "/frə'dʒɪ.lə.ti/"], "Identity": [2, "/aɪ'den.tə.ti/"],
    "Authority": [2, "/ɔ:'θɒ.rə.ti/"], "Celebrity": [2, "/sə'le.brə.ti/"], "Finality": [2, "/faɪ'næ.lə.ti/"], "Impunity": [2, "/ɪm'pju:.nə.ti/"],
    "Civility": [2, "/sə'vɪ.lə.ti/"], "Facility": [2, "/fə'sɪ.lə.ti/"], "Faculty": [1, "/'fæk.əl.ti/"], "Inanity": [2, "/ɪ'næ.nə.ti/"],
    "Commodity": [2, "/kə'mɒ.də.ti/"], "Deputy": [1, "/'dep.ju.ti/"], "Indignity": [2, "/ɪn'dɪg.nə.ti/"], "Infinity": [2, "/ɪn'fɪ.nə.ti/"],
    "Community": [2, "/kə'mju:.nə.ti/"], "Complexity": [2, "/kəm'plek.sə.ti/"], "Extremity": [2, "/ɪk'stre.mə.ti/"], "Hospitality": [3, "/ˌhɒs.pɪ'tæ.lə.ti/"],

    # --- Image 5 (-ify) ---
    "Horrify": [1, "/'hɒ.rɪ.faɪ/"], "Notify": [1, "/'nəʊ.tɪ.faɪ/"], "Modify": [1, "/'mɒ.dɪ.faɪ/"], "Simplify": [1, "/'sɪm.plɪ.faɪ/"],
    "Identify": [2, "/aɪ'den.tɪ.faɪ/"], "Qualify": [1, "/'kwɒ.lɪ.faɪ/"], "Satisfy": [1, "/'sæ.tɪs.faɪ/"], "Quantify": [1, "/'kwɒn.tɪ.faɪ/"],
    "Intensify": [2, "/ɪn'ten.sɪ.faɪ/"], "Terrify": [1, "/'te.rɪ.faɪ/"], "Magnify": [1, "/'mæg.nɪ.faɪ/"], "Purify": [1, "/'pjʊə.rɪ.faɪ/"],
    "Electrify": [2, "/ɪ'lek.trɪ.faɪ/"], "Verify": [1, "/'ve.rɪ.faɪ/"], "Exemplify": [2, "/ɪg'zem.plɪ.faɪ/"], "Specify": [1, "/'spe.sɪ.faɪ/"],
    "Justify": [1, "/'dʒʌs.tɪ.faɪ/"], "Clarify": [1, "/'klæ.rə.faɪ/"], "Testify": [1, "/'tes.tɪ.faɪ/"], "Personify": [2, "/pə'sɒ.nɪ.faɪ/"]
}

sentence_data = [
    {"ipa": "/aɪ ə'k.nɒl.ɪdʒ maɪ 'prɪv.əl.ɪdʒ/", "text": "I acknowledge my privilege"},
    {"ipa": "/ðə 'fəʊ.təʊ ɪz ɪn ðə 'ɔː.fən.ɪdʒ/", "text": "The photo is in the orphanage"},
    {"ipa": "/hi 'sæ.tɪs.faɪd ðə 'ɔ:.di.əns/", "text": "He satisfied the audience"},
    {"ipa": "/ʃi wɒnts tu 'kæp.ə.təl.aɪz ɒn ɪt/", "text": "She wants to capitalise on it"},
    {"ipa": "/ðeɪ 'ɔ:.θə.raɪz ðə 'kɒn.trækt/", "text": "They authorise the contract"}
]

# --- STATE MANAGEMENT ---
# Dùng Dictionary để lưu điểm người chơi theo dạng: {'TenNguoiChoi': {'Mode1': 100, 'Mode2': 50, 'Mode3': 0}}
if 'user_db' not in st.session_state: st.session_state.user_db = {}
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_user' not in st.session_state: st.session_state.current_user = ""
if 'game_mode' not in st.session_state: st.session_state.game_mode = None
if 'score' not in st.session_state: st.session_state.score = 0
if 'q_index' not in st.session_state: st.session_state.q_index = 0
if 'start_time' not in st.session_state: st.session_state.start_time = 0
if 'shuffled_keys' not in st.session_state: st.session_state.shuffled_keys = []
if 'message' not in st.session_state: st.session_state.message = ""

# --- HELPER FUNCTIONS ---
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
        total = s1 + s2 + s3
        data.append({
            "CODENAME": user, 
            "MODE 1": s1 if scores['M1'] is not None else "-",
            "MODE 2": s2 if scores['M2'] is not None else "-", 
            "MODE 3": s3 if scores['M3'] is not None else "-", 
            "TOTAL": total
        })
    df = pd.DataFrame(data)
    if not df.empty:
        df = df.sort_values(by="TOTAL", ascending=False)
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
        st.session_state.message = f"✅ TARGET ACQUIRED! +{pts} PTS ({elapsed:.2f}s)"
    else:
        st.session_state.message = f"❌ MISS! CORRECT: {correct_val}"
    
    time.sleep(1)
    st.session_state.q_index += 1
    st.session_state.start_time = time.time()

# --- UI PAGES ---

# 1. WELCOME PAGE
if st.session_state.page == 'welcome':
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        # Robot waiting
        st_lottie(lottie_robot, height=250, key="robot_welcome")
        st.markdown("<h2 style='text-align:center; color:#00eaff'>A.I. SYSTEM READY</h2>", unsafe_allow_html=True)
        
    with col_right:
        st.markdown("<h1 style='color: #00eaff; font-size: 60px; text-shadow: 0 0 10px #00eaff;'>CYBER STRESS</h1>", unsafe_allow_html=True)
        st.markdown("IDENTIFY. DECODE. SURVIVE.")
        
        # Input Name
        username = st.text_input("ENTER CODENAME TO BEGIN:", placeholder="AGENT_NAME...")
        
        if username:
            st.session_state.current_user = username
            progress = get_user_progress(username)
            
            st.write(f"WELCOME BACK, AGENT **{username}**. SELECT MISSION:")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                played_m1 = progress['M1'] is not None
                if st.button("MODE 1\nSTRESS", disabled=played_m1, use_container_width=True):
                    start_game(1)
                    st.rerun()
                if played_m1: st.caption(f"DONE: {progress['M1']} PTS")
                    
            with c2:
                played_m2 = progress['M2'] is not None
                if st.button("MODE 2\nIPA QUIZ", disabled=played_m2, use_container_width=True):
                    start_game(2)
                    st.rerun()
                if played_m2: st.caption(f"DONE: {progress['M2']} PTS")

            with c3:
                played_m3 = progress['M3'] is not None
                if st.button("MODE 3\nDECODE", disabled=played_m3, use_container_width=True):
                    start_game(3)
                    st.rerun()
                if played_m3: st.caption(f"DONE: {progress['M3']} PTS")

    # Leaderboard
    st.markdown("---")
    st.markdown("### 🏆 GLOBAL LEADERBOARD")
    df_rank = calculate_leaderboard()
    if not df_rank.empty:
        st.dataframe(df_rank, hide_index=True, use_container_width=True)
    else:
        st.info("NO DATA AVAILABLE YET.")

# 2. PLAYING PAGE
elif st.session_state.page == 'playing':
    # --- HUD HEADER ---
    total_q = 10
    col_hud1, col_hud2, col_hud3 = st.columns([1, 3, 1])
    
    with col_hud1:
        # Robot Hint Logic
        time_elapsed = time.time() - st.session_state.start_time
        st_lottie(lottie_robot, height=100, key="robot_playing")
        if time_elapsed > 10:
             st.markdown(f"<div class='hint-bubble'>HURRY UP AGENT! <br>TIME IS TICKING!</div>", unsafe_allow_html=True)

    with col_hud2:
        st.progress(min(st.session_state.q_index / total_q, 1.0))
        if st.session_state.message:
            color = "#00eaff" if "✅" in st.session_state.message else "#ff0055"
            st.markdown(f"<div style='text-align:center; color:{color}; font-weight:bold; animation: float 1s;'>{st.session_state.message}</div>", unsafe_allow_html=True)

    with col_hud3:
         st.metric("CURRENT SCORE", st.session_state.score)

    # --- GAMEPLAY ---
    if st.session_state.q_index < total_q and st.session_state.q_index < len(st.session_state.shuffled_keys):
        
        # --- MODE 1 (STRESS) & 2 (IPA) ---
        if st.session_state.game_mode in [1, 2]:
            current_word = st.session_state.shuffled_keys[st.session_state.q_index]
            correct_stress = word_data[current_word][0]
            correct_ipa = word_data[current_word][1]

            st.markdown(f"""
            <div class="hud-box">
                <h1 style="font-size: 50px; margin:0; color: #fff;">{current_word}</h1>
                <p style="color: #888; font-size: 14px; letter-spacing: 2px;">IDENTIFY PATTERN</p>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.game_mode == 1:
                c1, c2, c3 = st.columns(3)
                with c1: 
                    if st.button("STRESS [1]", use_container_width=True): 
                        process_answer(correct_stress == 1, correct_stress)
                        st.rerun()
                with c2: 
                    if st.button("STRESS [2]", use_container_width=True): 
                        process_answer(correct_stress == 2, correct_stress)
                        st.rerun()
                with c3: 
                    if st.button("STRESS [3]", use_container_width=True): 
                        process_answer(correct_stress == 3, correct_stress)
                        st.rerun()

            elif st.session_state.game_mode == 2:
                # Tạo đáp án fake
                if 'current_options' not in st.session_state or st.session_state.get('last_q') != st.session_state.q_index:
                    options = [correct_ipa]
                    # Fake 1: Sai dấu trọng âm
                    fake1 = correct_ipa.replace("'", "", 1)
                    pos = random.randint(1, len(fake1)-2)
                    fake1 = fake1[:pos] + "'" + fake1[pos:]
                    options.append(fake1)
                    # Fake 2: Sai nguyên âm
                    fake2 = correct_ipa.replace("ə", "e").replace("ɪ", "i:")
                    options.append(fake2)
                    # Fake 3: Random khác
                    fake3 = correct_ipa.replace(":", "").replace("ʃ", "s")
                    options.append(fake3)
                    
                    random.shuffle(options)
                    st.session_state.current_options = options
                    st.session_state.last_q = st.session_state.q_index
                
                ops = st.session_state.current_options
                c1, c2 = st.columns(2)
                for i, op in enumerate(ops):
                    with (c1 if i%2==0 else c2):
                        if st.button(op, use_container_width=True):
                            process_answer(op == correct_ipa, correct_ipa)
                            st.rerun()

        # --- MODE 3 (DECODE) ---
        elif st.session_state.game_mode == 3:
            idx = st.session_state.shuffled_keys[st.session_state.q_index]
            current_item = sentence_data[idx]
            
            st.markdown(f"""
            <div class="hud-box">
                <p style="font-size: 28px; color: #ff0055; font-family: monospace;">{current_item['ipa']}</p>
                <p style="color: #888;">DECRYPT SIGNAL TO ENGLISH</p>
            </div>
            """, unsafe_allow_html=True)
            
            user_text = st.text_input("TYPE TRANSLATION:", key=f"input_{st.session_state.q_index}")
            
            if st.button("TRANSMIT", use_container_width=True):
                clean_user = user_text.strip().lower().rstrip('.')
                clean_target = current_item['text'].strip().lower().rstrip('.')
                process_answer(clean_user == clean_target, current_item['text'])
                st.rerun()

    else:
        # Game Finished
        save_score(st.session_state.current_user, st.session_state.game_mode, st.session_state.score)
        st.session_state.page = 'result'
        st.rerun()

# 3. RESULT PAGE
elif st.session_state.page == 'result':
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st_lottie(lottie_robot, height=300, key="robot_result")
    
    with col_r:
        st.markdown(f"<h1 style='font-size: 80px; color: #00eaff;'>{st.session_state.score}</h1>", unsafe_allow_html=True)
        st.markdown("### MISSION COMPLETE")
        st.markdown("DATA SAVED TO CORE.")
        
        if st.button("🔙 RETURN TO BASE (MAIN MENU)", use_container_width=True):
            st.session_state.page = 'welcome'
            st.rerun()
