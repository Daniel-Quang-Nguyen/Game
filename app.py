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
    page_title="CYBER STRESS: NEURAL LINK v4.0",
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
# 2. ADVANCED VISUAL ENGINE (CSS)
# ==========================================

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

    /* --- GLOBAL RESET & BACKGROUND --- */
    .stApp {
        background-color: #050505;
        /* Cyber Grid Background */
        background-image: 
            linear-gradient(rgba(0, 255, 194, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 194, 0.05) 1px, transparent 1px);
        background-size: 40px 40px;
        color: #e0fbfc;
        font-family: 'Share Tech Mono', monospace;
    }

    /* --- CRT FLICKER ANIMATION --- */
    @keyframes flicker {
        0% { opacity: 0.98; }
        5% { opacity: 0.95; }
        10% { opacity: 0.9; }
        15% { opacity: 0.95; }
        20% { opacity: 0.99; }
        30% { opacity: 0.95; }
        50% { opacity: 0.99; }
        70% { opacity: 0.95; }
        100% { opacity: 0.98; }
    }
    
    .main-flicker-container {
        animation: flicker 0.1s infinite;
        padding: 2rem;
    }

    /* --- SCANLINE OVERLAY --- */
    .stApp::after {
        content: " ";
        display: block;
        position: absolute;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        z-index: 9999;
        background-size: 100% 2px, 3px 100%;
        pointer-events: none;
    }

    /* --- SYSTEM MALFUNCTION EFFECT (SHAKE) --- */
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
        filter: blur(2px) contrast(1.5) hue-rotate(90deg);
        border: 2px solid #ff0055 !important;
        box-shadow: 0 0 30px #ff0055 !important;
    }

    /* --- HUD BOXES --- */
    .hud-box {
        background: rgba(10, 15, 20, 0.9);
        border: 1px solid #00eaff;
        box-shadow: 0 0 20px rgba(0, 234, 255, 0.15);
        border-radius: 6px;
        padding: 30px;
        text-align: center;
        margin-bottom: 25px;
        position: relative;
        backdrop-filter: blur(10px);
    }
    .hud-title {
        color: #556677;
        font-size: 0.9rem;
        letter-spacing: 4px;
        margin-bottom: 15px;
        text-transform: uppercase;
        border-bottom: 1px solid #333;
        padding-bottom: 5px;
    }

    /* --- WORD DISPLAY --- */
    .word-display {
        font-family: 'Orbitron', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        color: #fff;
        text-shadow: 0 0 25px rgba(0, 234, 255, 0.6);
        letter-spacing: 2px;
    }
    
    /* --- MODE 1 BUTTONS (BIGGER) --- */
    .big-button button {
        height: 100px !important;
        font-size: 1.5rem !important;
        background: rgba(0, 234, 255, 0.05) !important;
        border: 1px solid #00eaff !important;
    }
    .big-button button:hover {
        background: #00eaff !important;
        color: #000 !important;
        box-shadow: 0 0 30px #00eaff;
    }

    /* --- GENERAL BUTTONS --- */
    .stButton>button {
        background-color: #0d1117;
        color: #00eaff;
        border: 1px solid #30363d;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2rem;
        padding: 15px;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        border-color: #00eaff;
        box-shadow: 0 0 15px rgba(0, 234, 255, 0.3);
        transform: scale(1.02);
    }

    /* --- INPUT FIELDS --- */
    .stTextInput input {
        background-color: #000 !important;
        color: #00eaff !important;
        border: 2px solid #333 !important;
        text-align: center;
        font-size: 1.5rem;
        font-family: 'Share Tech Mono', monospace;
    }
    .stTextInput input:focus {
        border-color: #00eaff !important;
        box-shadow: 0 0 20px rgba(0, 234, 255, 0.2) !important;
    }

    /* --- ARMOR BAR --- */
    .armor-track {
        width: 100%;
        height: 10px;
        background: #222;
        border-radius: 5px;
        overflow: hidden;
        margin-top: 5px;
    }
    .armor-fill {
        height: 100%;
        transition: width 0.5s linear;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. MASSIVE DATASET (FROM ALL IMAGES)
# ==========================================

WORD_DB = {
    # Image 1 (Pink/Green/Yellow -ify)
    "Horrify": [1, "/'hɒ.rɪ.faɪ/"], "Notify": [1, "/'nəʊ.tɪ.faɪ/"], "Modify": [1, "/'mɒ.dɪ.faɪ/"], "Simplify": [1, "/'sɪm.plɪ.faɪ/"],
    "Identify": [2, "/aɪ'den.tɪ.faɪ/"], "Qualify": [1, "/'kwɒ.lɪ.faɪ/"], "Satisfy": [1, "/'sæ.tɪs.faɪ/"], "Quantify": [1, "/'kwɒn.tɪ.faɪ/"],
    "Intensify": [2, "/ɪn'ten.sɪ.faɪ/"], "Terrify": [1, "/'te.rɪ.faɪ/"], "Magnify": [1, "/'mæg.nɪ.faɪ/"], "Purify": [1, "/'pjʊə.rɪ.faɪ/"],
    "Electrify": [2, "/ɪ'lek.trɪ.faɪ/"], "Verify": [1, "/'ve.rɪ.faɪ/"], "Exemplify": [2, "/ɪg'zem.plɪ.faɪ/"], "Specify": [1, "/'spe.sɪ.faɪ/"],
    "Justify": [1, "/'dʒʌs.tɪ.faɪ/"], "Clarify": [1, "/'klæ.rə.faɪ/"], "Testify": [1, "/'tes.tɪ.faɪ/"], "Personify": [2, "/pə'sɒ.nɪ.faɪ/"],

    # Image 2 (Blue/Yellow -ity)
    "Activity": [2, "/æk'tɪ.və.ti/"], "Capacity": [2, "/kə'pæ.sə.ti/"], "Fragility": [2, "/frə'dʒɪ.lə.ti/"], "Identity": [2, "/aɪ'den.tə.ti/"],
    "Authority": [2, "/ɔ:'θɒ.rə.ti/"], "Celebrity": [2, "/sə'le.brə.ti/"], "Finality": [2, "/faɪ'næ.lə.ti/"], "Impunity": [2, "/ɪm'pju:.nə.ti/"],
    "Civility": [2, "/sə'vɪ.lə.ti/"], "Facility": [2, "/fə'sɪ.lə.ti/"], "Faculty": [1, "/'fæk.əl.ti/"], "Inanity": [2, "/ɪ'næ.nə.ti/"],
    "Commodity": [2, "/kə'mɒ.də.ti/"], "Deputy": [1, "/'dep.ju.ti/"], "Indignity": [2, "/ɪn'dɪg.nə.ti/"], "Infinity": [2, "/ɪn'fɪ.nə.ti/"],
    "Community": [2, "/kə'mju:.nə.ti/"], "Complexity": [2, "/kəm'plek.sə.ti/"], "Extremity": [2, "/ɪk'stre.mə.ti/"], "Hospitality": [3, "/ˌhɒs.pɪ'tæ.lə.ti/"],

    # Image 3 (Blue/Yellow/Green -y)
    "Bakery": [1, "/'beɪ.kə.ri/"], "Balcony": [1, "/'bæl.kə.ni/"], "Battery": [1, "/'bæ.tə.ri/"], "Blackberry": [1, "/'blæk.bə.ri/"],
    "Agency": [1, "/'eɪ.dʒən.si/"], "Century": [1, "/'sen.tʃə.ri/"], "Chemistry": [1, "/'ke.mɪ.stri/"], "Colony": [1, "/'kɒ.lə.ni/"],
    "Ancestry": [1, "/'æn.ses.tri/"], "Boundary": [1, "/'baʊn.dri/"], "Comedy": [1, "/'kɒ.mə.di/"], "Contrary": [1, "/'kɒn.trə.ri/"],
    "Atrophy": [1, "/'æ.trə.fi/"], "Bravery": [1, "/'breɪ.və.ri/"], "Currency": [1, "/'kʌ.rən.si/"], "Custody": [1, "/'kʌs.tə.di/"],
    "Bankruptcy": [1, "/'bæŋ.krʌpt.si/"], "Brewery": [1, "/'bru:.ə.ri/"], "Density": [1, "/'den.sə.ti/"], "Dentistry": [1, "/'den.tɪ.stri/"],

    # Image 4 (Green -o)
    "Also": [1, "/'ɔ:l.sou/"], "Apollo": [2, "/ə'pɑ:.lou/"], "Auto": [1, "/'ɔ:.tou/"], "Bingo": [1, "/'biŋ.gou/"],
    "Bolero": [2, "/bə'ler.ou/"], "Photo": [1, "/'fou.tou/"], "Picasso": [2, "/pi'kæ.sou/"], "Potato": [2, "/pə'tei.tou/"],
    "Inferno": [2, "/in'fз:.nou/"], "Morocco": [2, "/mə'rɑ:.kou/"], "Psycho": [1, "/'sai.kou/"], "Toronto": [2, "/tə'rɑ:n.tou/"],
    "Disco": [1, "/'dis.kou/"], "Intro": [1, "/'in.trou/"], "Mosquito": [2, "/mə'ski:.tou/"], "Motto": [1, "/'mɑ:.tou/"],
    "Casino": [2, "/kə'si:.nou/"], "Commando": [2, "/kə'mæn.dou/"], "Flamingo": [2, "/flə'miŋ.gou/"], "Manifesto": [3, "/,mæn.ə'fes.tou/"],

    # Image 5 (Orange -age)
    "Curtilage": [1, "/'kɜː.təl.ɪdʒ/"], "Baronage": [1, "/'bær.ə.nɪdʒ/"], "Patronage": [1, "/'peɪ.trə.nɪdʒ/"], "Pilgrimage": [1, "/'pɪl.grɪ.mɪdʒ/"],
    "Leverage": [1, "/'lev.ər.ɪdʒ/"], "Orphanage": [1, "/'ɔː.fən.ɪdʒ/"], "Parsonage": [1, "/'pɑː.sən.ɪdʒ/"], "Vassalage": [1, "/'væs.ə.lɪdʒ/"],
    "Acknowledge": [2, "/ək'nɒl.ɪdʒ/"], "Advantage": [2, "/əd'vɑːn.tɪdʒ/"], "Appendage": [2, "/ə'pen.dɪdʒ/"], "Assemblage": [2, "/ə'sem.blɪdʒ/"],
    "Beverage": [1, "/'bev.ər.ɪdʒ/"], "Brokerage": [1, "/'brəʊ.kər.ɪdʒ/"], "Coverage": [1, "/'kʌv.ər.ɪdʒ/"], "Percentage": [2, "/pə'sen.tɪdʒ/"],
    "Haemorrhage": [1, "/'hem.ər.ɪdʒ/"], "Hermitage": [1, "/'hɜː.mɪ.tɪdʒ/"], "Privilege": [1, "/'prɪv.əl.ɪdʒ/"], "Porterage": [1, "/'pɔː.tər.ɪdʒ/"],
    "Encourage": [2, "/ɪn'kʌr.ɪdʒ/"], "Parentage": [1, "/'per.ən.tɪdʒ/"],

    # Image 6 (White/Grey -ary)
    "Infirmary": [2, "/ɪn'fɜ:.mə.ri/"], "Itinerary": [2, "/aɪ'tɪ.nə.rə.ri/"], "Luminary": [1, "/'lu:.mɪ.mə.ri/"],
    "Military": [1, "/'mɪ.lɪ.tə.ri/"], "Monetary": [1, "/'mʌ.nɪ.tə.ri/"], "Ordinary": [1, "/'ɔ:.dən.ri/"],
    "Secretary": [1, "/'se.krə.tri/"], "Temporary": [1, "/'tem.pə.rə.ri/"], "February": [1, "/'fe.brʊ.ə.ri/"],
    "Dietary": [1, "/'daɪ.ə.tə.ri/"], "Documentary": [3, "/ˌdɒk.ju'men.tri/"], "Contemporary": [2, "/kən'tem.pə.rə.ri/"],
    "Preliminary": [2, "/prɪ'lɪ.mɪ.nə.ri/"], "Anniversary": [3, "/ˌæ.nɪ'vɜ:.sə.ri/"], "Vocabulary": [2, "/və'kæ.bju.lə.ri/"],
    "Extraordinary": [2, "/ɪk'strɔ:.də.nə.ri/"], "Budgetary": [1, "/'bʌ.dʒɪ.tə.ri/"], "Sanitary": [1, "/'sæ.nɪ.tə.ri/"],

    # Image 7 (Colorful -ize/ise)
    "Advertise": [1, "/'æd.və.taɪz/"], "Analyse": [1, "/'æn.əl.aɪz/"], "Authorise": [1, "/'ɔ:.θə.raɪz/"], "Capitalise": [1, "/'kæp.ə.təl.aɪz/"],
    "Catalyse": [1, "/'kæt.əl.aɪz/"], "Centralise": [1, "/'sen.trə.laɪz/"], "Colonise": [1, "/'kɒ.lə.naɪz/"], "Compromise": [1, "/'kɒm.prə.maɪz/"],
    "Customise": [1, "/'kʌs.tə.maɪz/"], "Deputise": [1, "/'dep.ju.taɪz/"], "Enterprise": [1, "/'en.tə.praɪz/"], "Energise": [1, "/'en.ə.dʒaɪz/"],
    "Empathise": [1, "/'em.pə.θaɪz/"], "Moralise": [1, "/'mɔ:.rəl.aɪz/"], "Emphasize": [1, "/'em.fə.saɪz/"], "Equalise": [1, "/'i:.kwə.laɪz/"],
    "Exercise": [1, "/'ek.sə.saɪz/"], "Finalise": [1, "/'faɪ.nəl.aɪz/"], "Maximise": [1, "/'mæk.sə.maɪz/"], "Memorise": [1, "/'mem.ə.raɪz/"]
}

SENTENCE_DB = [
    {"ipa": "/aɪ ə'k.nɒl.ɪdʒ maɪ 'prɪv.əl.ɪdʒ/", "text": "I acknowledge my privilege"},
    {"ipa": "/ðə 'fəʊ.təʊ ɪz ɪn ðə 'ɔː.fən.ɪdʒ/", "text": "The photo is in the orphanage"},
    {"ipa": "/hi 'sæ.tɪs.faɪd ðə 'ɔ:.di.əns/", "text": "He satisfied the audience"},
    {"ipa": "/ʃi wɒnts tu 'kæp.ə.təl.aɪz ɒn ɪt/", "text": "She wants to capitalise on it"},
    {"ipa": "/ðeɪ 'ɔ:.θə.raɪz ðə 'kɒn.trækt/", "text": "They authorise the contract"},
    {"ipa": "/ðæts ə 'ne.sə.sə.ri 'sæ.krɪ.faɪs/", "text": "Thats a necessary sacrifice"},
    {"ipa": "/ʃi ɪz ə 'se.krə.tri/", "text": "She is a secretary"},
    {"ipa": "/ðə 'vju: wɒz ɪk'strɔ:.də.nə.ri/", "text": "The view was extraordinary"},
    {"ipa": "/hi ɪz ə 'le.dʒən.də.ri 'hɪə.rəʊ/", "text": "He is a legendary hero"}
]

# ==========================================
# 4. INTELLIGENT MODE 2 ENGINE (PHONETIC SWAPPER)
# ==========================================

def generate_smart_distractors(correct_ipa):
    """
    Creates plausible distractors by swapping similar sounds.
    ENSURES NO CAPITALIZATION.
    """
    correct_ipa = correct_ipa.lower() # Strict enforcement
    distractors = set()
    distractors.add(correct_ipa)
    
    # Confusing phonetic pairs (The "Trap" Logic)
    swaps = [
        ("θ", "ð"), ("ð", "θ"),  # th sounds
        ("ʃ", "tʃ"), ("tʃ", "ʃ"), # sh / ch
        ("ʒ", "dʒ"), ("dʒ", "ʒ"), # zh / j
        ("s", "z"), ("z", "s"),   # s / z
        ("æ", "e"), ("e", "æ"),   # a / e
        ("ɪ", "i:"), ("i:", "ɪ"), # short i / long i
        ("ɒ", "ɔ:"), ("ɔ:", "ɒ"), # short o / long o
        ("ə", "ʌ"), ("ʌ", "ə"),   # schwa / u
        ("n", "ŋ"), ("ŋ", "n"),   # n / ng
        ("w", "v"), ("v", "w")    # w / v
    ]
    
    # Helper: Stress shifter
    def shift_stress(text):
        if "'" not in text: return text
        clean = text.replace("'", "")
        # Find vowel indices
        vowels = [m.start() for m in re.finditer(r"[aeiouəʌɒɔɪʊ]", clean)]
        if len(vowels) > 1:
            new_idx = random.choice(vowels)
            return clean[:new_idx] + "'" + clean[new_idx:]
        return text

    attempts = 0
    while len(distractors) < 4 and attempts < 50:
        fake = correct_ipa
        
        # 70% chance to swap a sound, 30% chance to shift stress
        if random.random() < 0.7:
            # Try to find a swappable sound
            random.shuffle(swaps)
            for target, replacement in swaps:
                if target in fake:
                    fake = fake.replace(target, replacement, 1) # Swap only one occurrence
                    break
        else:
            fake = shift_stress(fake)
        
        # Formatting safety
        if not fake.startswith("/"): fake = "/" + fake
        if not fake.endswith("/"): fake = fake + "/"
        
        if fake != correct_ipa:
            distractors.add(fake)
        attempts += 1
        
    # Failsafe: if word is too simple (no swaps possible), append junk
    final_list = list(distractors)
    while len(final_list) < 4:
        final_list.append(correct_ipa.replace("/", "") + ":/")
    
    random.shuffle(final_list)
    return final_list

# ==========================================
# 5. STATE MANAGEMENT
# ==========================================

if 'user_data' not in st.session_state: st.session_state.user_data = {}
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'score' not in st.session_state: st.session_state.score = 0
if 'q_index' not in st.session_state: st.session_state.q_index = 0
if 'start_time' not in st.session_state: st.session_state.start_time = 0
if 'malfunction' not in st.session_state: st.session_state.malfunction = False
if 'feedback' not in st.session_state: st.session_state.feedback = ""
if 'distractors' not in st.session_state: st.session_state.distractors = []

def init_game(mode):
    st.session_state.game_mode = mode
    st.session_state.score = 0
    st.session_state.q_index = 0
    st.session_state.malfunction = False
    st.session_state.feedback = ""
    st.session_state.distractors = []
    
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

def handle_answer(correct, correct_val):
    elapsed = time.time() - st.session_state.start_time
    
    # --- MALFUNCTION LOGIC (ANTI-CHEAT) ---
    # If answered in under 1 second, screen shakes next turn
    if elapsed < 1.0:
        st.session_state.malfunction = True
    else:
        st.session_state.malfunction = False

    # --- SCORING (BASED ON 20s TIMER) ---
    TIME_LIMIT = 20.0
    
    if correct:
        bonus = max(0, int((TIME_LIMIT - elapsed) * 5)) # 5 pts per remaining second
        total = 100 + bonus
        st.session_state.score += total
        st.session_state.feedback = f"✅ TARGET ACQUIRED! +{total} PTS"
    else:
        st.session_state.feedback = f"❌ SYSTEM ERROR. ANS: {correct_val}"

    # Next Question
    st.session_state.q_index += 1
    st.session_state.start_time = time.time()
    st.session_state.distractors = [] # Reset Mode 2 options
    st.rerun()

# ==========================================
# 6. UI COMPOSITION
# ==========================================

main_container = st.container()

with main_container:
    # --- FLICKER WRAPPER ---
    st.markdown("<div class='main-flicker-container'>", unsafe_allow_html=True)

    # --- 3-COLUMN LAYOUT (CENTERED) ---
    left, mid, right = st.columns([1, 2, 1])

    # --- LEFT: INFO & ROBOT ---
    with left:
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if LOTTIE_ROBOT:
            from streamlit_lottie import st_lottie
            st_lottie(LOTTIE_ROBOT, height=150, key="bot")
        
        if st.session_state.page == 'playing':
            st.markdown("### 🛡️ ARMOR")
            # Calculate Armor based on 20s timer
            elapsed = time.time() - st.session_state.start_time
            limit = 20.0
            pct = max(0, int((1 - (elapsed/limit)) * 100))
            
            # Timeout Check
            if pct == 0:
                handle_answer(False, "TIME OUT")
            
            # Color logic
            color = "#00eaff" if pct > 50 else "#ff0055"
            st.markdown(f"""
            <div class='armor-track'>
                <div class='armor-fill' style='width:{pct}%; background:{color}; box-shadow:0 0 10px {color};'></div>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"{pct}% INTEGRITY")

    # --- MID: GAME AREA ---
    with mid:
        st.markdown("<h1 style='text-align:center; color:#00eaff; margin-bottom:0;'>CYBER STRESS</h1>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center; color:#666; letter-spacing:3px; font-size:0.8rem; margin-bottom:30px;'>NEURAL LINK ESTABLISHED</div>", unsafe_allow_html=True)

        # PAGE: WELCOME
        if st.session_state.page == 'welcome':
            username = st.text_input("ENTER CODENAME:", placeholder="AGENT_001")
            if username:
                st.session_state.current_user = username
                st.success("ACCESS GRANTED")
                c1, c2, c3 = st.columns(3)
                if c1.button("MODE 1\nSTRESS", use_container_width=True): init_game(1); st.rerun()
                if c2.button("MODE 2\nIPA", use_container_width=True): init_game(2); st.rerun()
                if c3.button("MODE 3\nDECODE", use_container_width=True): init_game(3); st.rerun()
                
                # Leaderboard
                st.markdown("### 📡 DATA UPLINK")
                if st.session_state.user_data:
                    df = pd.DataFrame(st.session_state.user_data).T.fillna(0)
                    st.dataframe(df, use_container_width=True)

        # PAGE: PLAYING
        elif st.session_state.page == 'playing':
            
            # SAFEGUARD: Prevent Index Error
            if st.session_state.q_index >= 10:
                # Save & Exit
                if 'current_user' not in st.session_state: st.session_state.current_user = "Guest"
                u = st.session_state.current_user
                if u not in st.session_state.user_data: st.session_state.user_data[u] = {}
                st.session_state.user_data[u][f"M{st.session_state.game_mode}"] = st.session_state.score
                
                st.session_state.page = 'result'
                st.rerun()

            else:
                # Feedback Display
                if st.session_state.feedback:
                    fc = "#00eaff" if "✅" in st.session_state.feedback else "#ff0055"
                    st.markdown(f"<div style='text-align:center; border:1px solid {fc}; color:{fc}; padding:10px; margin-bottom:20px; background:rgba(0,0,0,0.8);'>{st.session_state.feedback}</div>", unsafe_allow_html=True)

                # Malfunction Class
                mal_class = "system-malfunction" if st.session_state.malfunction else ""

                # --- MODE 1 & 2 LOGIC ---
                if st.session_state.game_mode in [1, 2]:
                    word = st.session_state.shuffled_keys[st.session_state.q_index]
                    correct_stress = WORD_DB[word][0]
                    correct_ipa = WORD_DB[word][1]

                    st.markdown(f"""
                    <div class="hud-box {mal_class}">
                        <div class="hud-title">TARGET IDENTIFICATION</div>
                        <div class="word-display">{word}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.session_state.game_mode == 1:
                        # BIG BUTTONS LAYOUT
                        c1, c2, c3, c4 = st.columns(4)
                        # Helper to create big button container
                        def big_btn(col, label, ans):
                            with col:
                                st.markdown('<div class="big-button">', unsafe_allow_html=True)
                                if st.button(label, key=f"btn_{label}", use_container_width=True):
                                    handle_answer(correct_stress == ans, ans)
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        big_btn(c1, "1ST", 1)
                        big_btn(c2, "2ND", 2)
                        big_btn(c3, "3RD", 3)
                        big_btn(c4, "4TH", 4)

                    elif st.session_state.game_mode == 2:
                        if not st.session_state.distractors:
                            st.session_state.distractors = generate_smart_distractors(correct_ipa)
                        
                        opts = st.session_state.distractors
                        g1, g2 = st.columns(2)
                        with g1:
                            if st.button(opts[0], use_container_width=True): handle_answer(opts[0]==correct_ipa.lower(), correct_ipa)
                            if st.button(opts[1], use_container_width=True): handle_answer(opts[1]==correct_ipa.lower(), correct_ipa)
                        with g2:
                            if st.button(opts[2], use_container_width=True): handle_answer(opts[2]==correct_ipa.lower(), correct_ipa)
                            if st.button(opts[3], use_container_width=True): handle_answer(opts[3]==correct_ipa.lower(), correct_ipa)

                # --- MODE 3 LOGIC ---
                elif st.session_state.game_mode == 3:
                    idx = st.session_state.shuffled_keys[st.session_state.q_index]
                    item = SENTENCE_DB[idx]
                    
                    st.markdown(f"""
                    <div class="hud-box {mal_class}">
                        <div class="hud-title">DECRYPT SIGNAL</div>
                        <div style="font-size:1.5rem; color:#ffcc00; font-family:'Courier New'; line-height:1.5;">{item['ipa']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # DYNAMIC KEY forces reset on every question change
                    user_in = st.text_input("TRANSLATION:", key=f"input_{st.session_state.q_index}")
                    
                    if st.button("SUBMIT", use_container_width=True):
                        # Normalize inputs
                        u_clean = user_in.strip().lower().rstrip('.').replace(',', '').replace("'", "")
                        t_clean = item['text'].strip().lower().rstrip('.').replace(',', '').replace("'", "")
                        handle_answer(u_clean == t_clean, item['text'])

        # PAGE: RESULT
        elif st.session_state.page == 'result':
            st.markdown(f"""
            <div class="hud-box" style="border-color:#00ff00; margin-top:50px;">
                <div class="hud-title">MISSION COMPLETE</div>
                <div style="font-size:5rem; color:#fff; text-shadow:0 0 30px #00ff00;">{st.session_state.score}</div>
                <div style="color:#00ff00;">TOTAL POINTS</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("RETURN TO BASE", use_container_width=True):
                st.session_state.page = 'welcome'
                st.rerun()

    # --- RIGHT: STATUS ---
    with right:
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.session_state.page == 'playing':
            st.markdown("### ⚙️ SYS LOG")
            st.caption(f"LEVEL: {st.session_state.q_index + 1}/10")
            st.caption(f"SCORE: {st.session_state.score}")
            if st.session_state.malfunction:
                st.markdown("<span style='color:red; animation:blink 0.5s infinite;'>⚠️ ANOMALY DETECTED</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:#00eaff;'>● SYSTEM STABLE</span>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True) # End Flicker
