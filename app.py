import streamlit as st
import random
import time
import pandas as pd
import requests
import re

# ==========================================
# 1. SYSTEM CONFIGURATION & ASSET LOADING
# ==========================================

st.set_page_config(
    page_title="CYBER STRESS: NEURAL LINK",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Asset Loader (Safe Mode) ---
def load_lottie_safe(url):
    try:
        r = requests.get(url, timeout=2)
        if r.status_code != 200: return None
        return r.json()
    except:
        return None

# Load the AI Assistant (Floating Robot)
LOTTIE_ROBOT = load_lottie_safe("https://lottie.host/6a56e300-47a3-4a1c-99c5-6809e5192102/1sZ8ilG7hS.json")

# ==========================================
# 2. ADVANCED CSS ENGINE (VISUALS)
# ==========================================

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

    /* --- RESET & BACKGROUND --- */
    .stApp {
        background-color: #050505;
        background-image: 
            linear-gradient(rgba(0, 255, 194, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 194, 0.03) 1px, transparent 1px),
            radial-gradient(circle at 50% 50%, #0a101f 0%, #000000 90%);
        background-size: 50px 50px, 50px 50px, 100% 100%;
        color: #e0fbfc;
        font-family: 'Share Tech Mono', monospace;
        overflow-x: hidden;
    }

    /* --- CRT SCANLINE & FLICKER EFFECT (The "Old Version" Vibe) --- */
    .stApp::before {
        content: " ";
        display: block;
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        z-index: 999;
        background-size: 100% 2px, 3px 100%;
        pointer-events: none;
    }
    
    @keyframes flicker {
        0% { opacity: 0.97; }
        5% { opacity: 0.95; }
        10% { opacity: 0.9; }
        15% { opacity: 0.95; }
        20% { opacity: 0.99; }
        25% { opacity: 0.95; }
        30% { opacity: 0.9; }
        35% { opacity: 0.96; }
        40% { opacity: 0.98; }
        45% { opacity: 0.95; }
        50% { opacity: 0.99; }
        55% { opacity: 0.93; }
        60% { opacity: 0.9; }
        65% { opacity: 0.96; }
        70% { opacity: 1; }
        75% { opacity: 0.97; }
        80% { opacity: 0.95; }
        85% { opacity: 0.92; }
        90% { opacity: 0.97; }
        95% { opacity: 0.99; }
        100% { opacity: 0.94; }
    }
    .main-container {
        animation: flicker 0.15s infinite;
        padding-top: 5rem; /* Push content down */
    }

    /* --- LAYOUT CONTAINERS --- */
    div.block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }

    /* --- DISRUPTION EFFECTS (Glitch & Shake) --- */
    @keyframes shake {
        0% { transform: translate(1px, 1px) rotate(0deg); }
        10% { transform: translate(-1px, -2px) rotate(-1deg); }
        20% { transform: translate(-3px, 0px) rotate(1deg); }
        30% { transform: translate(3px, 2px) rotate(0deg); }
        40% { transform: translate(1px, -1px) rotate(1deg); }
        50% { transform: translate(-1px, 2px) rotate(-1deg); }
        60% { transform: translate(-3px, 1px) rotate(0deg); }
        70% { transform: translate(3px, 1px) rotate(-1deg); }
        80% { transform: translate(-1px, -1px) rotate(1deg); }
        90% { transform: translate(1px, 2px) rotate(0deg); }
        100% { transform: translate(1px, -2px) rotate(-1deg); }
    }
    .system-malfunction {
        animation: shake 0.5s; 
        filter: blur(1.5px) contrast(1.2);
        border: 2px solid red !important;
        box-shadow: 0 0 20px red;
    }

    /* --- HUD ELEMENTS --- */
    .hud-box {
        background: rgba(10, 15, 20, 0.85);
        border: 1px solid #00eaff;
        box-shadow: 0 0 15px rgba(0, 234, 255, 0.1), inset 0 0 30px rgba(0, 234, 255, 0.05);
        border-radius: 4px;
        padding: 25px;
        text-align: center;
        backdrop-filter: blur(5px);
        margin-bottom: 20px;
        position: relative;
    }
    
    .hud-title {
        color: #8899a6;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 10px;
        border-bottom: 1px solid #333;
        padding-bottom: 5px;
    }

    /* --- TYPOGRAPHY --- */
    .word-display {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: -webkit-linear-gradient(#fff, #00eaff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 234, 255, 0.4);
    }

    /* --- BUTTONS (Sci-Fi Style) --- */
    .stButton>button {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
        border: 1px solid #30363d;
        color: #00eaff;
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 15px 0;
        font-size: 1.1rem;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .stButton>button::after {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0,255,194,0.2), transparent);
        transition: 0.5s;
    }
    .stButton>button:hover {
        border-color: #00eaff;
        box-shadow: 0 0 15px rgba(0, 234, 255, 0.4);
        transform: translateY(-2px);
        color: #fff;
    }
    .stButton>button:hover::after {
        left: 100%;
    }
    
    /* --- INPUT FIELDS --- */
    .stTextInput>div>div>input {
        background-color: #050505;
        color: #00eaff;
        border: 1px solid #333;
        font-family: 'Share Tech Mono', monospace;
        text-align: center;
        font-size: 1.2rem;
        caret-color: #ff0055;
    }
    .stTextInput>div>div>input:focus {
        border-color: #00eaff;
        box-shadow: 0 0 15px rgba(0, 234, 255, 0.2);
    }

    /* --- ARMOR BAR --- */
    .armor-container {
        width: 100%;
        height: 8px;
        background: #111;
        border-radius: 4px;
        overflow: hidden;
        margin-top: 10px;
        border: 1px solid #333;
    }
    .armor-fill {
        height: 100%;
        background: linear-gradient(90deg, #ff0055, #ffcc00, #00eaff);
        width: 100%;
        transition: width 0.1s linear;
        box-shadow: 0 0 10px rgba(0, 234, 255, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. COMPREHENSIVE DATASET
# ==========================================

# Merging all requested word lists into a master dictionary
WORD_DB = {
    # --- Group -o / -age ---
    "Inferno": [2, "/in'fз:.nou/"], "Mosquito": [2, "/mə'ski:.tou/"], "Manifesto": [3, "/,mæn.ə'fes.tou/"], 
    "Casino": [2, "/kə'si:.nou/"], "Advantage": [2, "/əd'vɑːn.tɪdʒ/"], "Encourage": [2, "/ɪn'kʌr.ɪdʒ/"],
    "Potato": [2, "/pə'tei.tou/"], "Flamingo": [2, "/flə'miŋ.gou/"], "Orphanage": [1, "/'ɔː.fən.ɪdʒ/"],
    "Heritage": [1, "/'her.ɪ.tɪdʒ/"], "Percentage": [2, "/pə'sen.tɪdʒ/"], "Torpedo": [2, "/tɔː'piː.dəʊ/"],
    
    # --- Group -ary ---
    "Military": [1, "/'mɪ.lɪ.tə.ri/"], "Secretary": [1, "/'se.krə.tri/"], "Necessary": [1, "/'ne.sə.sə.ri/"],
    "Imaginary": [2, "/ɪ'mæ.dʒɪ.nə.ri/"], "Vocabulary": [2, "/və'kæ.bju.lə.ri/"], "Revolutionary": [3, "/ˌre.və'lu:.ʃən.ri/"],
    "Documentary": [3, "/ˌdɒk.ju'men.tri/"], "Contemporary": [2, "/kən'tem.pə.rə.ri/"], "Anniversary": [3, "/ˌæ.nɪ'vɜ:.sə.ri/"],

    # --- Group -ize / -ise ---
    "Apologize": [2, "/ə'pɒ.lə.dʒaɪz/"], "Recognize": [1, "/'re.kəg.naɪz/"], "Organize": [1, "/'ɔ:.gə.naɪz/"],
    "Economize": [2, "/ɪ'kɒ.nə.maɪz/"], "Monopolize": [2, "/mə'nɒ.pə.laɪz/"], "Characterize": [1, "/'kæ.rək.tə.raɪz/"],
    
    # --- Group -y ---
    "Economy": [2, "/ɪ'kɒ.nə.mi/"], "Photography": [2, "/fə'tɒ.grə.fi/"], "Biology": [2, "/baɪ'ɒ.lə.dʒi/"],
    "Geography": [2, "/dʒi'ɒ.grə.fi/"], "Ability": [2, "/ə'bɪ.lə.ti/"], "Personality": [3, "/ˌpɜ:.sə'næ.lə.ti/"],
    "Responsibility": [4, "/rɪˌspɒn.sə'bɪ.lə.ti/"], "University": [3, "/ˌju:.nɪ'vɜ:.sə.ti/"],
    
    # --- Group -ify ---
    "Identify": [2, "/aɪ'den.tɪ.faɪ/"], "Solidify": [2, "/sə'lɪ.dɪ.faɪ/"], "Classify": [1, "/'klæ.sɪ.faɪ/"],
    "Personify": [2, "/pə'sɒ.nɪ.faɪ/"], "Electrify": [2, "/ɪ'lek.trɪ.faɪ/"], "Exemplify": [2, "/ɪg'zem.plɪ.faɪ/"]
}

SENTENCE_DB = [
    {"ipa": "/ðə 'fəʊ.təʊ ɪz ɪn ðə 'ɔː.fən.ɪdʒ/", "text": "The photo is in the orphanage"},
    {"ipa": "/aɪ ə'k.nɒl.ɪdʒ maɪ 'prɪv.əl.ɪdʒ/", "text": "I acknowledge my privilege"},
    {"ipa": "/hi 'sæ.tɪs.faɪd ðə 'ɔ:.di.əns/", "text": "He satisfied the audience"},
    {"ipa": "/ʃi wɒnts tu 'kæp.ə.təl.aɪz ɒn ɪt/", "text": "She wants to capitalise on it"},
    {"ipa": "/ðeɪ 'ɔ:.θə.raɪz ðə 'kɒn.trækt/", "text": "They authorise the contract"},
    {"ipa": "/ɪt wɒz ə 'ne.sə.sə.ri 'sæ.krɪ.faɪs/", "text": "It was a necessary sacrifice"},
    {"ipa": "/ðə vju: ɪz ɪk'strɔ:.də.nə.ri/", "text": "The view is extraordinary"}
]

# ==========================================
# 4. INTELLIGENT LOGIC ENGINES
# ==========================================

def generate_smart_distractors(correct_ipa):
    """
    ENGINE: MODE 2
    Uses phonetic mapping to swap sounds with similar/confusing ones.
    Never deletes the slashes.
    """
    distractors = set()
    distractors.add(correct_ipa)
    
    # Phonetic Swap Map (Confusing pairs)
    swap_map = {
        "eɪ": "e",    # say -> se
        "aɪ": "ɔɪ",   # my -> moy (confusing)
        "i:": "ɪ",    # heat -> hit
        "u:": "ʊ",    # boot -> book
        "θ": "ð",     # think -> this
        "ð": "θ",     # this -> think
        "ʃ": "s",     # she -> see
        "tʃ": "ʃ",    # chip -> ship
        "dʒ": "ʒ",    # joy -> vision
        "æ": "e",     # bat -> bet
        "ə": "ʌ",     # schwa -> up
        "ŋ": "n",     # sing -> sin
        "s": "z",     # house -> houze
        "z": "s"      # rise -> rice
    }

    def shift_stress(ipa_str):
        """Move the stress mark ' to a wrong position"""
        if "'" not in ipa_str: return ipa_str
        clean = ipa_str.replace("'", "")
        # Find all vowels
        vowel_indices = [m.start() for m in re.finditer(r"[aeiouəʌɒɔɪʊ]", clean)]
        if len(vowel_indices) > 1:
            # Pick a spot that ISN'T the original stress position
            # This is simplified; real stress logic is hard, but random placement works for distractors
            new_pos = random.choice(vowel_indices)
            return clean[:new_pos] + "'" + clean[new_pos:]
        return ipa_str

    attempts = 0
    while len(distractors) < 4 and attempts < 50:
        fake = correct_ipa
        
        # Strategy 1: Sound Swap
        keys = list(swap_map.keys())
        random.shuffle(keys)
        swapped = False
        for k in keys:
            if k in fake:
                fake = fake.replace(k, swap_map[k], 1)
                swapped = True
                break
        
        # Strategy 2: Stress Shift (if swap didn't happen or 50% chance)
        if not swapped or random.random() > 0.5:
            fake = shift_stress(fake)

        # Safety: Ensure slashes remain
        if not fake.startswith("/"): fake = "/" + fake
        if not fake.endswith("/"): fake = fake + "/"
        
        # Safety: Ensure it's not the correct answer
        if fake != correct_ipa:
            distractors.add(fake)
        
        attempts += 1
        
    # Fallback if specific swaps failed (rare)
    final_list = list(distractors)
    while len(final_list) < 4:
        # Emergency dummy answer
        final_list.append(correct_ipa.replace("/", "") + ":/")
        
    random.shuffle(final_list)
    return final_list

# ==========================================
# 5. STATE MANAGEMENT
# ==========================================

if 'user_data' not in st.session_state: st.session_state.user_data = {}
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_user' not in st.session_state: st.session_state.current_user = "GUEST"
if 'shuffled_keys' not in st.session_state: st.session_state.shuffled_keys = []
if 'q_index' not in st.session_state: st.session_state.q_index = 0
if 'start_time' not in st.session_state: st.session_state.start_time = 0
if 'distractors' not in st.session_state: st.session_state.distractors = []
if 'malfunction' not in st.session_state: st.session_state.malfunction = False # For glitch
if 'feedback_msg' not in st.session_state: st.session_state.feedback_msg = ""
if 'armor_val' not in st.session_state: st.session_state.armor_val = 100

def init_game(mode):
    st.session_state.game_mode = mode
    st.session_state.score = 0
    st.session_state.q_index = 0
    st.session_state.malfunction = False
    st.session_state.feedback_msg = ""
    
    if mode == 3:
        idxs = list(range(len(SENTENCE_DB)))
        random.shuffle(idxs)
        st.session_state.shuffled_keys = idxs
    else:
        keys = list(WORD_DB.keys())
        random.shuffle(keys)
        st.session_state.shuffled_keys = keys
    
    st.session_state.page = 'playing'
    st.session_state.start_time = time.time()
    st.session_state.distractors = [] # Reset for Mode 2

def handle_answer(correct, correct_val):
    elapsed = time.time() - st.session_state.start_time
    
    # --- DISRUPTION LOGIC ---
    # If answered too fast (<1.5s), trigger malfunction for next round
    if elapsed < 1.5:
        st.session_state.malfunction = True
    else:
        st.session_state.malfunction = False

    # --- SCORE CALCULATION ---
    # Armor is calculated at render time, but let's calc points here
    time_limit = 15.0
    remaining_pct = max(0, (time_limit - elapsed) / time_limit)
    
    if correct:
        base = 100
        bonus = int(base * remaining_pct) # Faster = Higher Bonus
        total = base + bonus
        st.session_state.score += total
        st.session_state.feedback_msg = f"✅ TARGET ACQUIRED! +{total} PTS"
    else:
        st.session_state.feedback_msg = f"❌ SYSTEM ERROR. CORRECT: {correct_val}"

    # Transition
    st.session_state.q_index += 1
    st.session_state.start_time = time.time()
    st.session_state.distractors = [] # Clear cached options
    st.rerun()

# ==========================================
# 6. UI COMPONENT RENDERING
# ==========================================

# MAIN CONTAINER WRAPPER
main = st.container()

with main:
    # --- HEADER ---
    st.markdown("<div class='main-container'>", unsafe_allow_html=True) # Start Flicker Container
    
    # 3-Column Layout for "Clean UI" (Not pushed up, centered)
    col_left, col_center, col_right = st.columns([1, 2, 1])

    # --- LEFT COLUMN: INFO ---
    with col_left:
        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True) # Spacer
        if st.session_state.page == 'playing':
            st.markdown("### 🛡️ ARMOR INTEGRITY")
            # Armor Logic
            elapsed = time.time() - st.session_state.start_time
            max_time = 15.0
            armor_pct = max(0, int((1 - (elapsed / max_time)) * 100))
            if armor_pct == 0 and st.session_state.page == 'playing':
                # Timeout Logic
                handle_answer(False, "TIME OUT")
            
            # Render Bar
            color_stop = "#00eaff" if armor_pct > 50 else "#ff0055"
            st.markdown(f"""
            <div class="armor-container">
                <div class="armor-fill" style="width: {armor_pct}%; background: {color_stop}; box-shadow: 0 0 10px {color_stop};"></div>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"STATUS: {armor_pct}%")

    # --- CENTER COLUMN: THE ARENA ---
    with col_center:
        st.markdown("<h1 style='text-align:center; font-size: 2.5rem; color:#00eaff; margin-bottom:0;'>CYBER STRESS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#888; margin-top:-10px; letter-spacing:4px;'>NEURAL LINK ESTABLISHED</p>", unsafe_allow_html=True)
        
        # --- PAGE: WELCOME ---
        if st.session_state.page == 'welcome':
            st.markdown("---")
            if 'lottie_err' not in st.session_state:
                try:
                    from streamlit_lottie import st_lottie
                    if LOTTIE_ROBOT:
                        st_lottie(LOTTIE_ROBOT, height=180, key="bot_intro")
                except: pass
            
            name = st.text_input("ENTER AGENT ID:", placeholder="CODENAME...")
            if name:
                st.session_state.current_user = name
                st.success(f"IDENTITY CONFIRMED: {name}")
                st.markdown("### SELECT MISSION PROFILE")
                b1, b2, b3 = st.columns(3)
                if b1.button("MODE 1\nSTRESS", use_container_width=True): init_game(1); st.rerun()
                if b2.button("MODE 2\nIPA", use_container_width=True): init_game(2); st.rerun()
                if b3.button("MODE 3\nDECODE", use_container_width=True): init_game(3); st.rerun()
                
            # Global Scores
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("### 📡 DATA UPLINK (LEADERBOARD)")
            if st.session_state.user_data:
                df = pd.DataFrame(st.session_state.user_data).T.fillna(0)
                if not df.empty:
                    df['TOTAL'] = df.sum(axis=1)
                    st.dataframe(df.sort_values('TOTAL', ascending=False), use_container_width=True)
            else:
                st.info("NO DATA PACKETS RECEIVED.")

        # --- PAGE: PLAYING ---
        elif st.session_state.page == 'playing':
            # 1. Feedback Area
            if st.session_state.feedback_msg:
                f_color = "#00eaff" if "✅" in st.session_state.feedback_msg else "#ff0055"
                st.markdown(f"<div style='text-align:center; border:1px solid {f_color}; color:{f_color}; padding:10px; margin-bottom:15px; background:rgba(0,0,0,0.5);'>{st.session_state.feedback_msg}</div>", unsafe_allow_html=True)

            # 2. Check Game End
            if st.session_state.q_index >= 10:
                # Save Score
                if st.session_state.current_user not in st.session_state.user_data:
                    st.session_state.user_data[st.session_state.current_user] = {}
                st.session_state.user_data[st.session_state.current_user][f"MODE {st.session_state.game_mode}"] = st.session_state.score
                
                st.session_state.page = 'result'
                st.rerun()
            
            # 3. Render Question
            else:
                # --- GLITCH CONTAINER ---
                # If malfunction is active, add the CSS class 'system-malfunction'
                malfunction_class = "system-malfunction" if st.session_state.malfunction else ""
                
                if st.session_state.game_mode in [1, 2]:
                    word = st.session_state.shuffled_keys[st.session_state.q_index]
                    correct_stress = WORD_DB[word][0]
                    correct_ipa = WORD_DB[word][1]

                    st.markdown(f"""
                    <div class="hud-box {malfunction_class}">
                        <div class="hud-title">TARGET IDENTIFICATION</div>
                        <div class="word-display">{word}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # MODE 1: STRESS
                    if st.session_state.game_mode == 1:
                        c1, c2, c3, c4 = st.columns(4)
                        with c1: 
                            if st.button("1ST", key="s1"): handle_answer(correct_stress==1, 1)
                        with c2: 
                            if st.button("2ND", key="s2"): handle_answer(correct_stress==2, 2)
                        with c3: 
                            if st.button("3RD", key="s3"): handle_answer(correct_stress==3, 3)
                        with c4:
                            if st.button("4TH", key="s4"): handle_answer(correct_stress==4, 4)

                    # MODE 2: IPA (Smart Distractors)
                    elif st.session_state.game_mode == 2:
                        if not st.session_state.distractors:
                            st.session_state.distractors = generate_smart_distractors(correct_ipa)
                        
                        opts = st.session_state.distractors
                        g1, g2 = st.columns(2)
                        with g1:
                            if st.button(opts[0], use_container_width=True): handle_answer(opts[0]==correct_ipa, correct_ipa)
                            if st.button(opts[1], use_container_width=True): handle_answer(opts[1]==correct_ipa, correct_ipa)
                        with g2:
                            if st.button(opts[2], use_container_width=True): handle_answer(opts[2]==correct_ipa, correct_ipa)
                            if st.button(opts[3], use_container_width=True): handle_answer(opts[3]==correct_ipa, correct_ipa)

                # MODE 3: DECODE
                elif st.session_state.game_mode == 3:
                    idx = st.session_state.shuffled_keys[st.session_state.q_index]
                    item = SENTENCE_DB[idx]
                    
                    st.markdown(f"""
                    <div class="hud-box {malfunction_class}">
                        <div class="hud-title">DECRYPT SIGNAL</div>
                        <div style="font-size:1.8rem; color:#ffcc00; font-family:'Courier New'; word-wrap:break-word;">{item['ipa']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    user_in = st.text_input("TRANSLATION:", key="decode_input")
                    if st.button("SUBMIT TRANSMISSION", use_container_width=True):
                        cln_u = user_in.strip().lower().rstrip('.').replace(',', '')
                        cln_t = item['text'].strip().lower().rstrip('.').replace(',', '')
                        handle_answer(cln_u == cln_t, item['text'])

        # --- PAGE: RESULT ---
        elif st.session_state.page == 'result':
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="hud-box" style="border-color: #00ff00; box-shadow: 0 0 30px rgba(0,255,0,0.2);">
                <div class="hud-title">MISSION DEBRIEF</div>
                <div style="font-size: 5rem; color: #fff; text-shadow: 0 0 20px #00ff00;">{st.session_state.score}</div>
                <div style="color: #00ff00;">TOTAL POINTS ACQUIRED</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("RETURN TO BASE", use_container_width=True):
                st.session_state.page = 'welcome'
                st.rerun()

    # --- RIGHT COLUMN: DECORATION & STATUS ---
    with col_right:
        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
        if st.session_state.page == 'playing':
            st.markdown("### ⚙️ SYSTEM LOG")
            st.caption(f"LEVEL: {st.session_state.q_index + 1} / 10")
            st.caption(f"SCORE: {st.session_state.score}")
            if st.session_state.malfunction:
                st.markdown("<span style='color:red; animation: blink 0.5s infinite;'>⚠️ ANOMALY DETECTED</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:#00eaff;'>● SYSTEM STABLE</span>", unsafe_allow_html=True)
                
    st.markdown("</div>", unsafe_allow_html=True) # End Flicker Container
