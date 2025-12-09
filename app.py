import streamlit as st
import random
import time
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="CYBER STRESS // REBOOT", page_icon="💠", layout="centered")

# --- ADVANCED CSS (CYBERPUNK HUD STYLE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');

    /* 1. GLOBAL SETTINGS */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(#112233 1px, transparent 1px);
        background-size: 20px 20px;
        color: #00FFC2;
        font-family: 'Share Tech Mono', monospace;
    }

    /* 2. HUD CONTAINER (THE BOX) */
    .hud-box {
        border: 2px solid #00FFC2;
        box-shadow: 0 0 15px #00FFC2, inset 0 0 20px rgba(0, 255, 194, 0.1);
        padding: 30px;
        border-radius: 10px;
        background: rgba(10, 20, 30, 0.8);
        text-align: center;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }

    /* 3. SCANLINE ANIMATION */
    .scanline {
        width: 100%;
        height: 5px;
        background: rgba(0, 255, 194, 0.3);
        position: absolute;
        top: 0;
        left: 0;
        animation: scan 3s linear infinite;
        opacity: 0.5;
    }
    @keyframes scan {
        0% { top: 0%; }
        100% { top: 100%; }
    }

    /* 4. TYPOGRAPHY */
    .word-display {
        font-family: 'Orbitron', sans-serif;
        font-size: 60px;
        font-weight: 700;
        color: #FFFFFF;
        text-shadow: 0 0 10px #00FFC2;
        margin: 0;
        padding: 0;
        letter-spacing: 2px;
    }
    .sub-text {
        color: #8899A6;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-top: 10px;
    }
    .ipa-text {
        font-size: 24px;
        color: #FF0055;
        font-family: 'Courier New', monospace;
        margin-bottom: 15px;
        text-shadow: 0 0 5px #FF0055;
    }

    /* 5. BUTTONS */
    .stButton>button {
        background-color: #0E1117;
        color: #00FFC2;
        border: 1px solid #00FFC2;
        font-family: 'Orbitron', sans-serif;
        font-size: 18px;
        height: 60px;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 0 5px rgba(0, 255, 194, 0.2);
    }
    .stButton>button:hover {
        background-color: #00FFC2;
        color: #000000;
        box-shadow: 0 0 20px #00FFC2;
        transform: scale(1.02);
        border: 1px solid #FFFFFF;
    }

    /* 6. PROGRESS BAR & METRICS */
    div[data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-family: 'Orbitron', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATASET (Đã gộp -o và -age) ---
word_data = {
    # --- Nhóm đuôi -O ---
    "Also": [1, "/'ɔ:l.sou/"], "Apollo": [2, "/ə'pɑ:.lou/"], "Auto": [1, "/'ɔ:.tou/"],
    "Bingo": [1, "/'biŋ.gou/"], "Bolero": [2, "/bə'ler.ou/"], "Photo": [1, "/'fou.tou/"],
    "Picasso": [2, "/pi'kæ.sou/"], "Potato": [2, "/pə'tei.tou/"], "Inferno": [2, "/in'fз:.nou/"],
    "Morocco": [2, "/mə'rɑ:.kou/"], "Psycho": [1, "/'sai.kou/"], "Toronto": [2, "/tə'rɑ:n.tou/"],
    "Disco": [1, "/'dis.kou/"], "Intro": [1, "/'in.trou/"], "Mosquito": [2, "/mə'ski:.tou/"],
    "Motto": [1, "/'mɑ:.tou/"], "Casino": [2, "/kə'si:.nou/"], "Commando": [2, "/kə'mæn.dou/"],
    "Flamingo": [2, "/flə'miŋ.gou/"], "Manifesto": [3, "/,mæn.ə'fes.tou/"],
    # --- Nhóm đuôi -AGE ---
    "Curtilage": [1, "/'kɜː.təl.ɪdʒ/"], "Baronage": [1, "/'bær.ə.nɪdʒ/"], "Patronage": [1, "/'peɪ.trə.nɪdʒ/"],
    "Pilgrimage": [1, "/'pɪl.grɪ.mɪdʒ/"], "Leverage": [1, "/'lev.ər.ɪdʒ/"], "Orphanage": [1, "/'ɔː.fən.ɪdʒ/"],
    "Parsonage": [1, "/'pɑː.sən.ɪdʒ/"], "Vassalage": [1, "/'væs.ə.lɪdʒ/"], "Acknowledge": [2, "/ək'nɒl.ɪdʒ/"],
    "Advantage": [2, "/əd'vɑːn.tɪdʒ/"], "Appendage": [2, "/ə'pen.dɪdʒ/"], "Assemblage": [2, "/ə'sem.blɪdʒ/"],
    "Beverage": [1, "/'bev.ər.ɪdʒ/"], "Brokerage": [1, "/'brəʊ.kər.ɪdʒ/"], "Coverage": [1, "/'kʌv.ər.ɪdʒ/"],
    "Percentage": [2, "/pə'sen.tɪdʒ/"], "Haemorrhage": [1, "/'hem.ər.ɪdʒ/"], "Hermitage": [1, "/'hɜː.mɪ.tɪdʒ/"],
    "Privilege": [1, "/'prɪv.əl.ɪdʒ/"], "Porterage": [1, "/'pɔː.tər.ɪdʒ/"], "Encourage": [2, "/ɪn'kʌr.ɪdʒ/"],
    "Parentage": [1, "/'per.ən.tɪdʒ/"]
}

sentence_data = [
    {"ipa": "/aɪ ə'k.nɒl.ɪdʒ maɪ 'prɪv.əl.ɪdʒ/", "text": "I acknowledge my privilege"},
    {"ipa": "/ðə 'fəʊ.təʊ ɪz ɪn ðə 'ɔː.fən.ɪdʒ/", "text": "The photo is in the orphanage"},
    {"ipa": "/ðæt 'pə.tei.tou iz 'ɔ:.səm/", "text": "That potato is awesome"},
    {"ipa": "/hi lɒst hɪz 'mʌ.ni ɪn ə kə'si:.nou/", "text": "He lost his money in a casino"}
]

# --- STATE MANAGEMENT ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'score' not in st.session_state: st.session_state.score = 0
if 'user_name' not in st.session_state: st.session_state.user_name = "AGENT_001"
if 'game_mode' not in st.session_state: st.session_state.game_mode = None
if 'q_index' not in st.session_state: st.session_state.q_index = 0
if 'start_time' not in st.session_state: st.session_state.start_time = 0
if 'leaderboard' not in st.session_state: 
    st.session_state.leaderboard = pd.DataFrame(columns=["CODENAME", "SCORE", "MODE", "TIME"])
if 'shuffled_keys' not in st.session_state: st.session_state.shuffled_keys = []
if 'message' not in st.session_state: st.session_state.message = ""

# --- LOGIC FUNCTIONS ---
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
        st.session_state.message = f"❌ ERROR! CORRECT TARGET: {correct_val}"
    
    time.sleep(1) # Delay nhỏ để tạo cảm giác xử lý
    st.session_state.q_index += 1
    st.session_state.start_time = time.time()

def generate_ipa_distractors(correct_ipa):
    # (Giữ nguyên logic tạo đáp án nhiễu)
    options = [correct_ipa]
    fake1 = correct_ipa.replace("'", "", 1)
    insert_pos = random.randint(1, len(fake1)-2)
    fake1 = fake1[:insert_pos] + "'" + fake1[insert_pos:]
    options.append(fake1)
    fake2 = correct_ipa.replace("ei", "e").replace("ou", "o").replace("i", "ai")
    if fake2 == correct_ipa: fake2 = correct_ipa.replace("ə", "e")
    options.append(fake2)
    fake3 = correct_ipa.replace("dʒ", "g").replace("ʃ", "s")
    if fake3 == correct_ipa: fake3 = correct_ipa + ":"
    options.append(fake3)
    random.shuffle(options)
    return options

# --- UI PAGES ---

# 1. WELCOME PAGE
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align: center; color: #00FFC2; text-shadow: 0 0 10px #00FFC2;'>💠 CYBER STRESS 💠</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; letter-spacing: 5px; color: #fff;'>SYSTEM INITIALIZED</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.session_state.user_name = st.text_input("ENTER CODENAME:", value=st.session_state.user_name)
        
        st.markdown("---")
        if st.button("🚀 MODE 1: STRESS TARGET", use_container_width=True):
            start_game(1)
            st.rerun()
            
        if st.button("🧩 MODE 2: IPA DECODER", use_container_width=True):
            start_game(2)
            st.rerun()
            
        if st.button("📡 MODE 3: SIGNAL REWRITE", use_container_width=True):
            start_game(3)
            st.rerun()
    
    # Show Leaderboard
    if not st.session_state.leaderboard.empty:
        st.markdown("### 🏆 HALL OF FAME")
        st.dataframe(st.session_state.leaderboard.sort_values("SCORE", ascending=False).head(5), hide_index=True, use_container_width=True)

# 2. PLAYING PAGE
elif st.session_state.page == 'playing':
    # Top Bar: Score & Progress
    total_q = 10
    col_hud1, col_hud2 = st.columns([3, 1])
    with col_hud1:
        st.progress(min(st.session_state.q_index / total_q, 1.0))
    with col_hud2:
        st.markdown(f"<div style='text-align:right; color:#FFD700; font-weight:bold;'>SCORE: {st.session_state.score}</div>", unsafe_allow_html=True)
    
    # Message Log
    if st.session_state.message:
        if "✅" in st.session_state.message:
            st.markdown(f"<div style='background: rgba(0,255,194,0.1); border-left: 5px solid #00FFC2; padding: 10px; margin-bottom: 20px;'>{st.session_state.message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background: rgba(255,0,85,0.1); border-left: 5px solid #FF0055; padding: 10px; margin-bottom: 20px;'>{st.session_state.message}</div>", unsafe_allow_html=True)

    # Main Game Logic
    if st.session_state.q_index < total_q and st.session_state.q_index < len(st.session_state.shuffled_keys):
        
        # --- MODE 1 & 2 ---
        if st.session_state.game_mode in [1, 2]:
            current_word = st.session_state.shuffled_keys[st.session_state.q_index]
            correct_stress = word_data[current_word][0]
            correct_ipa = word_data[current_word][1]

            # HUD VISUAL
            st.markdown(f"""
            <div class="hud-box">
                <div class="scanline"></div>
                <p class="word-display">{current_word}</p>
                <p class="sub-text">IDENTIFY PATTERN</p>
            </div>
            """, unsafe_allow_html=True)

            # BUTTONS AREA
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
                # Tạo đáp án 1 lần
                if 'current_options' not in st.session_state or st.session_state.get('last_q') != st.session_state.q_index:
                    st.session_state.current_options = generate_ipa_distractors(correct_ipa)
                    st.session_state.last_q = st.session_state.q_index
                
                options = st.session_state.current_options
                
                c1, c2 = st.columns(2)
                for i, opt in enumerate(options):
                    with (c1 if i % 2 == 0 else c2):
                        if st.button(opt, use_container_width=True):
                            process_answer(opt == correct_ipa, correct_ipa)
                            st.rerun()

        # --- MODE 3 ---
        elif st.session_state.game_mode == 3:
            idx = st.session_state.shuffled_keys[st.session_state.q_index]
            current_item = sentence_data[idx]
            
            st.markdown(f"""
            <div class="hud-box">
                <div class="scanline"></div>
                <p class="ipa-text">{current_item['ipa']}</p>
                <p class="sub-text">DECRYPT SIGNAL TO ENGLISH</p>
            </div>
            """, unsafe_allow_html=True)
            
            user_text = st.text_input("INPUT DECODED MESSAGE:", key=f"input_{st.session_state.q_index}")
            
            if st.button("TRANSMIT ANSWER", use_container_width=True):
                clean_user = user_text.strip().lower().rstrip('.')
                clean_target = current_item['text'].strip().lower().rstrip('.')
                process_answer(clean_user == clean_target, current_item['text'])
                st.rerun()

    else:
        # Game Over
        st.session_state.page = 'result'
        st.rerun()

# 3. RESULT PAGE
elif st.session_state.page == 'result':
    st.markdown("""
    <div style="text-align: center; margin-top: 50px;">
        <h1 style="color: #00FFC2; font-size: 50px;">MISSION COMPLETE</h1>
        <p style="color: #8899A6;">TRANSMISSION ENDED</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="hud-box">
        <h2 style="font-size: 80px; margin: 0; color: #fff;">{st.session_state.score}</h2>
        <p>TOTAL SCORE</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Save Score
    new_entry = pd.DataFrame([{
        "CODENAME": st.session_state.user_name,
        "SCORE": st.session_state.score,
        "MODE": f"MODE {st.session_state.game_mode}",
        "TIME": time.strftime("%H:%M")
    }])
    
    # Avoid dups logic
    if st.session_state.leaderboard.empty or \
       (not st.session_state.leaderboard.empty and \
        st.session_state.score != st.session_state.leaderboard.iloc[-1]['SCORE']):
         st.session_state.leaderboard = pd.concat([st.session_state.leaderboard, new_entry], ignore_index=True)

    if st.button("🔄 REBOOT SYSTEM", use_container_width=True):
        st.session_state.page = 'welcome'
        st.rerun()
