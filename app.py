import streamlit as st
import random
import time
import pandas as pd
import requests
import re
import base64

# ==========================================
# 1. SYSTEM CONFIGURATION & SAFE LOADER
# ==========================================
st.set_page_config(
    page_title="CYBER STRESS: FINAL v6.0",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Safe Import for Lottie
try:
    from streamlit_lottie import st_lottie
    LOTTIE_LIB_OK = True
except ImportError:
    LOTTIE_LIB_OK = False

# Safe Import for Autorefresh (CRITICAL FOR TIMER)
try:
    from streamlit_autorefresh import st_autorefresh
    REFRESH_OK = True
except ImportError:
    REFRESH_OK = False

def load_lottie_safe(url):
    if not LOTTIE_LIB_OK: return None
    try:
        r = requests.get(url, timeout=2)
        if r.status_code != 200: return None
        return r.json()
    except:
        return None

# Load Robot
LOTTIE_ROBOT = load_lottie_safe("https://lottie.host/6a56e300-47a3-4a1c-99c5-6809e5192102/1sZ8ilG7hS.json")

# ==========================================
# 2. AUDIO ENGINE (NEW)
# ==========================================
def play_sound(sound_type):
    # Using hosted reliable short sounds
    sounds = {
        "correct": "https://codeskulptor-demos.commondatastorage.googleapis.com/dependencies_audio/sound_correct.wav",
        "wrong": "https://rpg.hamsterrepublic.com/wiki-images/d/db/Crush8-Bit.ogg",
        "timeout": "https://codeskulptor-demos.commondatastorage.googleapis.com/GalaxyInvaders/pause.wav",
        "win": "https://codeskulptor-demos.commondatastorage.googleapis.com/dependencies_audio/sound_hook_win.wav"
    }
    
    url = sounds.get(sound_type)
    if url:
        # Invisible HTML Audio Player with Autoplay
        st.markdown(f'''
            <audio autoplay="true" style="display:none;">
            <source src="{url}" type="audio/wav">
            </audio>
            ''', unsafe_allow_html=True)

# ==========================================
# 3. ADVANCED CSS (VISUAL ENGINE)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Roboto+Mono:wght@400;700&display=swap');

    /* BACKGROUND */
    .stApp {
        background-color: #02040a;
        background-image: 
            linear-gradient(rgba(0, 255, 194, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 194, 0.05) 1px, transparent 1px),
            radial-gradient(circle at 50% 50%, #0d1b2a 0%, #000000 100%);
        background-size: 50px 50px, 50px 50px, 100% 100%;
        color: #e0fbfc;
        font-family: 'Roboto Mono', monospace;
    }

    /* CRT SCANLINE */
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

    /* MALFUNCTION SHAKE */
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
    .malfunction {
        animation: shake 0.5s; 
        filter: blur(1px) contrast(1.5) hue-rotate(90deg);
        border: 2px solid #ff0055 !important;
    }

    /* HUD */
    .hud-box {
        background: rgba(10, 15, 20, 0.85);
        border: 1px solid #00eaff;
        box-shadow: 0 0 15px rgba(0, 234, 255, 0.1);
        border-radius: 5px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        backdrop-filter: blur(5px);
    }
    
    .target-word {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: #fff;
        text-shadow: 0 0 15px rgba(0, 234, 255, 0.8);
        margin: 10px 0;
        text-transform: none; /* No Caps */
    }
    
    .ipa-display {
        font-family: 'Roboto Mono', monospace;
        font-size: 1.8rem;
        color: #ffcc00;
        text-transform: none !important;
    }

    /* BUTTONS */
    .stButton>button {
        background: #0d1117;
        color: #00eaff;
        border: 1px solid #30363d;
        font-family: 'Roboto Mono', monospace;
        font-size: 1.3rem;
        padding: 20px;
        text-transform: none !important;
        transition: all 0.2s;
        width: 100%;
    }
    .stButton>button:hover {
        border-color: #00eaff;
        background: rgba(0, 234, 255, 0.1);
        box-shadow: 0 0 20px rgba(0, 234, 255, 0.3);
        color: #fff;
    }

    /* INPUTS */
    .stTextInput input {
        background: #000;
        color: #00eaff;
        border: 2px solid #333;
        text-align: center;
        font-size: 1.5rem;
        font-family: 'Roboto Mono', monospace;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. DATABASE (ALL WORDS)
# ==========================================
WORD_DB = {
    "Horrify": [1, "/'hɒ.rɪ.faɪ/"], "Notify": [1, "/'nəʊ.tɪ.faɪ/"], "Modify": [1, "/'mɒ.dɪ.faɪ/"], "Simplify": [1, "/'sɪm.plɪ.faɪ/"],
    "Identify": [2, "/aɪ'den.tɪ.faɪ/"], "Qualify": [1, "/'kwɒ.lɪ.faɪ/"], "Satisfy": [1, "/'sæ.tɪs.faɪ/"], "Quantify": [1, "/'kwɒn.tɪ.faɪ/"],
    "Intensify": [2, "/ɪn'ten.sɪ.faɪ/"], "Terrify": [1, "/'te.rɪ.faɪ/"], "Magnify": [1, "/'mæg.nɪ.faɪ/"], "Purify": [1, "/'pjʊə.rɪ.faɪ/"],
    "Electrify": [2, "/ɪ'lek.trɪ.faɪ/"], "Verify": [1, "/'ve.rɪ.faɪ/"], "Exemplify": [2, "/ɪg'zem.plɪ.faɪ/"], "Specify": [1, "/'spe.sɪ.faɪ/"],
    "Justify": [1, "/'dʒʌs.tɪ.faɪ/"], "Clarify": [1, "/'klæ.rə.faɪ/"], "Testify": [1, "/'tes.tɪ.faɪ/"], "Personify": [2, "/pə'sɒ.nɪ.faɪ/"],
    "Activity": [2, "/æk'tɪ.və.ti/"], "Capacity": [2, "/kə'pæ.sə.ti/"], "Fragility": [2, "/frə'dʒɪ.lə.ti/"], "Identity": [2, "/aɪ'den.tə.ti/"],
    "Authority": [2, "/ɔ:'θɒ.rə.ti/"], "Celebrity": [2, "/sə'le.brə.ti/"], "Finality": [2, "/faɪ'næ.lə.ti/"], "Impunity": [2, "/ɪm'pju:.nə.ti/"],
    "Civility": [2, "/sə'vɪ.lə.ti/"], "Facility": [2, "/fə'sɪ.lə.ti/"], "Faculty": [1, "/'fæk.əl.ti/"], "Inanity": [2, "/ɪ'næ.nə.ti/"],
    "Commodity": [2, "/kə'mɒ.də.ti/"], "Deputy": [1, "/'dep.ju.ti/"], "Infinity": [2, "/ɪn'fɪ.nə.ti/"],
    "Community": [2, "/kə'mju:.nə.ti/"], "Complexity": [2, "/kəm'plek.sə.ti/"], "Extremity": [2, "/ɪk'stre.mə.ti/"], "Hospitality": [3, "/ˌhɒs.pɪ'tæ.lə.ti/"],
    "Bakery": [1, "/'beɪ.kə.ri/"], "Balcony": [1, "/'bæl.kə.ni/"], "Battery": [1, "/'bæ.tə.ri/"], "Blackberry": [1, "/'blæk.bə.ri/"],
    "Agency": [1, "/'eɪ.dʒən.si/"], "Century": [1, "/'sen.tʃə.ri/"], "Chemistry": [1, "/'ke.mɪ.stri/"], "Colony": [1, "/'kɒ.lə.ni/"],
    "Ancestry": [1, "/'æn.ses.tri/"], "Boundary": [1, "/'baʊn.dri/"], "Comedy": [1, "/'kɒ.mə.di/"], "Contrary": [1, "/'kɒn.trə.ri/"],
    "Atrophy": [1, "/'æ.trə.fi/"], "Bravery": [1, "/'breɪ.və.ri/"], "Currency": [1, "/'kʌ.rən.si/"], "Custody": [1, "/'kʌs.tə.di/"],
    "Bankruptcy": [1, "/'bæŋ.krʌpt.si/"], "Brewery": [1, "/'bru:.ə.ri/"], "Density": [1, "/'den.sə.ti/"], "Dentistry": [1, "/'den.tɪ.stri/"],
    "Mosquito": [2, "/mə'ski:.tou/"], "Manifesto": [3, "/,mæn.ə'fes.tou/"], "Casino": [2, "/kə'si:.nou/"],
    "Potato": [2, "/pə'tei.tou/"], "Flamingo": [2, "/flə'miŋ.gou/"], "Apollo": [2, "/ə'pɑ:.lou/"], "Auto": [1, "/'ɔ:.tou/"],
    "Bingo": [1, "/'biŋ.gou/"], "Bolero": [2, "/bə'ler.ou/"], "Photo": [1, "/'fou.tou/"], "Picasso": [2, "/pi'kæ.sou/"],
    "Morocco": [2, "/mə'rɑ:.kou/"], "Psycho": [1, "/'sai.kou/"], "Toronto": [2, "/tə'rɑ:n.tou/"], "Disco": [1, "/'dis.kou/"],
    "Intro": [1, "/'in.trou/"], "Motto": [1, "/'mɑ:.tou/"], "Commando": [2, "/kə'mæn.dou/"], "Also": [1, "/'ɔ:l.sou/"],
    "Curtilage": [1, "/'kɜː.təl.ɪdʒ/"], "Baronage": [1, "/'bær.ə.nɪdʒ/"], "Patronage": [1, "/'peɪ.trə.nɪdʒ/"], "Pilgrimage": [1, "/'pɪl.grɪ.mɪdʒ/"],
    "Leverage": [1, "/'lev.ər.ɪdʒ/"], "Orphanage": [1, "/'ɔː.fən.ɪdʒ/"], "Parsonage": [1, "/'pɑː.sən.ɪdʒ/"], "Vassalage": [1, "/'væs.ə.lɪdʒ/"],
    "Acknowledge": [2, "/ək'nɒl.ɪdʒ/"], "Advantage": [2, "/əd'vɑːn.tɪdʒ/"], "Appendage": [2, "/ə'pen.dɪdʒ/"], "Assemblage": [2, "/ə'sem.blɪdʒ/"],
    "Beverage": [1, "/'bev.ər.ɪdʒ/"], "Brokerage": [1, "/'brəʊ.kər.ɪdʒ/"], "Coverage": [1, "/'kʌv.ər.ɪdʒ/"], "Percentage": [2, "/pə'sen.tɪdʒ/"],
    "Haemorrhage": [1, "/'hem.ər.ɪdʒ/"], "Hermitage": [1, "/'hɜː.mɪ.tɪdʒ/"], "Privilege": [1, "/'prɪv.əl.ɪdʒ/"], "Porterage": [1, "/'pɔː.tər.ɪdʒ/"],
    "Encourage": [2, "/ɪn'kʌr.ɪdʒ/"], "Parentage": [1, "/'per.ən.tɪdʒ/"],
    "Infirmary": [2, "/ɪn'fɜ:.mə.ri/"], "Itinerary": [2, "/aɪ'tɪ.nə.rə.ri/"], "Luminary": [1, "/'lu:.mɪ.mə.ri/"],
    "Military": [1, "/'mɪ.lɪ.tə.ri/"], "Monetary": [1, "/'mʌ.nɪ.tə.ri/"], "Ordinary": [1, "/'ɔ:.dən.ri/"],
    "Secretary": [1, "/'se.krə.tri/"], "Temporary": [1, "/'tem.pə.rə.ri/"], "February": [1, "/'fe.brʊ.ə.ri/"],
    "Dietary": [1, "/'daɪ.ə.tə.ri/"], "Documentary": [3, "/ˌdɒk.ju'men.tri/"], "Contemporary": [2, "/kən'tem.pə.rə.ri/"],
    "Preliminary": [2, "/prɪ'lɪ.mɪ.nə.ri/"], "Anniversary": [3, "/ˌæ.nɪ'vɜ:.sə.ri/"], "Vocabulary": [2, "/və'kæ.bju.lə.ri/"],
    "Extraordinary": [2, "/ɪk'strɔ:.də.nə.ri/"], "Budgetary": [1, "/'bʌ.dʒɪ.tə.ri/"], "Sanitary": [1, "/'sæ.nɪ.tə.ri/"],
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
    {"ipa": "/hi bɔ:t ə feɪk pi'kæ.sou/", "text": "He bought a fake Picasso"},
    {"ipa": "/ðə 'vju: wɒz ɪk'strɔ:.də.nə.ri/", "text": "The view was extraordinary"},
    {"ipa": "/hi ɪz ə 'le.dʒən.də.ri 'hɪə.rəʊ/", "text": "He is a legendary hero"},
    {"ipa": "/pli:z aɪ'den.tɪ.faɪ jɔ: 'self/", "text": "Please identify yourself"}
]

# ==========================================
# 5. SMART ENGINE
# ==========================================
def generate_smart_distractors(correct_ipa):
    target = correct_ipa.lower()
    distractors = set()
    distractors.add(target)
    
    swaps = [
        ("θ", "ð"), ("ð", "θ"), ("ʃ", "tʃ"), ("tʃ", "ʃ"), ("dʒ", "ʒ"), ("ʒ", "dʒ"),
        ("s", "z"), ("z", "s"), ("æ", "e"), ("e", "æ"), ("ɪ", "i:"), ("i:", "ɪ"),
        ("ɒ", "ɔ:"), ("ɔ:", "ɒ"), ("ə", "ʌ"), ("ʌ", "ə"), ("ŋ", "n"), ("n", "ŋ"),
        ("w", "v"), ("v", "w")
    ]
    
    def shift_stress(txt):
        if "'" not in txt: return txt
        clean = txt.replace("'", "")
        vowels = [m.start() for m in re.finditer(r"[aeiouəʌɒɔɪʊ]", clean)]
        if len(vowels) > 1:
            idx = random.choice(vowels)
            return clean[:idx] + "'" + clean[idx:]
        return txt

    attempts = 0
    while len(distractors) < 4 and attempts < 100:
        fake = target
        if random.random() < 0.6:
            random.shuffle(swaps)
            for s1, s2 in swaps:
                if s1 in fake:
                    fake = fake.replace(s1, s2, 1)
                    break
        else:
            fake = shift_stress(fake)
        
        if not fake.startswith("/"): fake = "/" + fake
        if not fake.endswith("/"): fake = fake + "/"
        
        if fake != target:
            distractors.add(fake)
        attempts += 1
        
    final = list(distractors)
    while len(final) < 4:
        final.append(target.replace("/", "") + ":/")
    random.shuffle(final)
    return final

# ==========================================
# 6. STATE
# ==========================================
if 'user_db' not in st.session_state: st.session_state.user_db = {}
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'score' not in st.session_state: st.session_state.score = 0
if 'q_index' not in st.session_state: st.session_state.q_index = 0
if 'start_time' not in st.session_state: st.session_state.start_time = 0
if 'malfunction' not in st.session_state: st.session_state.malfunction = False
if 'msg' not in st.session_state: st.session_state.msg = ""
if 'distractors' not in st.session_state: st.session_state.distractors = []
if 'sound_to_play' not in st.session_state: st.session_state.sound_to_play = None

def init_game(mode):
    st.session_state.game_mode = mode
    st.session_state.score = 0
    st.session_state.q_index = 0
    st.session_state.malfunction = False
    st.session_state.msg = ""
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

def handle_ans(correct, ans_txt):
    elapsed = time.time() - st.session_state.start_time
    st.session_state.malfunction = True if elapsed < 1.0 else False
    
    LIMIT = 20.0
    if correct:
        if elapsed > LIMIT:
            st.session_state.msg = "⚠️ TIME OUT (0 PTS)"
            st.session_state.sound_to_play = "timeout"
        else:
            bonus = int((LIMIT - elapsed) * 5)
            pts = 100 + max(0, bonus)
            st.session_state.score += pts
            st.session_state.msg = f"✅ TARGET HIT! +{pts}"
            st.session_state.sound_to_play = "correct"
    else:
        st.session_state.msg = f"❌ ERROR. ANS: {ans_txt}"
        st.session_state.sound_to_play = "wrong"
        
    st.session_state.q_index += 1
    st.session_state.start_time = time.time()
    st.session_state.distractors = []
    st.rerun()

# ==========================================
# 7. UI RENDERER
# ==========================================
left, mid, right = st.columns([1, 2, 1])

with left:
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if LOTTIE_LIB_OK and LOTTIE_ROBOT:
        st_lottie(LOTTIE_ROBOT, height=180, key="bot")
    
    if st.session_state.page == 'playing':
        st.markdown("### ⏱️ TIMER")
        
        # --- THE FIX: AUTOREFRESH ---
        if REFRESH_OK:
            st_autorefresh(interval=1000, limit=None, key="timer_refresh")
            
        elapsed = time.time() - st.session_state.start_time
        remain = max(0, 20.0 - elapsed)
        
        t_color = "#00eaff" if remain > 10 else "#ff0055"
        st.markdown(f"<h1 style='color:{t_color}; font-size:4rem; margin:0;'>{int(remain)}s</h1>", unsafe_allow_html=True)
        if remain == 0:
            st.caption("TIME DEPLETED - SUBMIT TO CONTINUE")

with mid:
    # Sound Player trigger
    if st.session_state.sound_to_play:
        play_sound(st.session_state.sound_to_play)
        st.session_state.sound_to_play = None # Reset

    st.markdown("<h1 style='text-align:center; color:#00eaff'>CYBER STRESS</h1>", unsafe_allow_html=True)

    if st.session_state.page == 'welcome':
        user = st.text_input("CODENAME:", placeholder="AGENT...")
        if user:
            st.session_state.current_user = user
            st.success("ACCESS GRANTED")
            c1, c2, c3 = st.columns(3)
            if c1.button("MODE 1\nSTRESS"): init_game(1); st.rerun()
            if c2.button("MODE 2\nIPA"): init_game(2); st.rerun()
            if c3.button("MODE 3\nDECODE"): init_game(3); st.rerun()
            
            st.markdown("### 📡 HALL OF FAME")
            if st.session_state.user_db:
                df = pd.DataFrame(st.session_state.user_db).T.fillna(0)
                # Calculate TOTAL column
                numeric_cols = [c for c in df.columns if c.startswith('M')]
                df['TOTAL'] = df[numeric_cols].sum(axis=1)
                st.dataframe(df.sort_values('TOTAL', ascending=False), use_container_width=True)

    elif st.session_state.page == 'playing':
        if st.session_state.q_index >= 10:
            u = st.session_state.get('current_user', 'Guest')
            if u not in st.session_state.user_db: st.session_state.user_db[u] = {}
            st.session_state.user_db[u][f"M{st.session_state.game_mode}"] = st.session_state.score
            st.session_state.sound_to_play = "win"
            st.session_state.page = 'result'
            st.rerun()
        
        else:
            if st.session_state.msg:
                clr = "#00eaff" if "✅" in st.session_state.msg else "#ff0055"
                st.markdown(f"<div style='text-align:center; border:1px solid {clr}; color:{clr}; padding:10px; margin-bottom:10px; background:rgba(0,0,0,0.8);'>{st.session_state.msg}</div>", unsafe_allow_html=True)

            cls_mal = "malfunction" if st.session_state.malfunction else ""
            
            if st.session_state.game_mode in [1, 2]:
                word = st.session_state.shuffled_keys[st.session_state.q_index]
                correct_stress = WORD_DB[word][0]
                correct_ipa = WORD_DB[word][1]

                st.markdown(f"""
                <div class="hud-box {cls_mal}">
                    <div style="color:#666; font-size:0.8rem; letter-spacing:3px;">TARGET IDENTIFICATION</div>
                    <div class="target-word">{word}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.session_state.game_mode == 1:
                    c1, c2, c3, c4 = st.columns(4)
                    with c1: 
                        if st.button("1ST", use_container_width=True): handle_ans(correct_stress==1, 1)
                    with c2: 
                        if st.button("2ND", use_container_width=True): handle_ans(correct_stress==2, 2)
                    with c3: 
                        if st.button("3RD", use_container_width=True): handle_ans(correct_stress==3, 3)
                    with c4:
                         if st.button("4TH", use_container_width=True): handle_ans(correct_stress==4, 4)

                elif st.session_state.game_mode == 2:
                    if not st.session_state.distractors:
                        st.session_state.distractors = generate_smart_distractors(correct_ipa)
                    opts = st.session_state.distractors
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button(opts[0], use_container_width=True): handle_ans(opts[0]==correct_ipa.lower(), correct_ipa)
                        if st.button(opts[1], use_container_width=True): handle_ans(opts[1]==correct_ipa.lower(), correct_ipa)
                    with c2:
                        if st.button(opts[2], use_container_width=True): handle_ans(opts[2]==correct_ipa.lower(), correct_ipa)
                        if st.button(opts[3], use_container_width=True): handle_ans(opts[3]==correct_ipa.lower(), correct_ipa)

            elif st.session_state.game_mode == 3:
                idx = st.session_state.shuffled_keys[st.session_state.q_index]
                item = SENTENCE_DB[idx]
                st.markdown(f"""
                <div class="hud-box {cls_mal}">
                    <div style="color:#666; font-size:0.8rem; letter-spacing:3px;">DECRYPT SIGNAL</div>
                    <div class="ipa-display" style="margin-top:10px;">{item['ipa']}</div>
                </div>
                """, unsafe_allow_html=True)
                ans = st.text_input("TRANSLATION:", key=f"in_{st.session_state.q_index}")
                if st.button("SUBMIT", use_container_width=True):
                    cln_u = ans.strip().lower().rstrip('.').replace(",", "").replace("'", "")
                    cln_t = item['text'].strip().lower().rstrip('.').replace(",", "").replace("'", "")
                    elapsed = time.time() - st.session_state.start_time
                    if elapsed > 20.0:
                        handle_ans(True, "TIME OUT")
                    else:
                        handle_ans(cln_u == cln_t, item['text'])

    elif st.session_state.page == 'result':
        st.markdown(f"""
        <div class="hud-box" style="margin-top:50px; border-color:#00ff00;">
            <h1>MISSION COMPLETE</h1>
            <h1 style="font-size:5rem; color:#fff;">{st.session_state.score}</h1>
            <p style="color:#00ff00;">TOTAL SCORE</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("MAIN MENU", use_container_width=True):
            st.session_state.page = 'welcome'
            st.rerun()

with right:
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if st.session_state.page == 'playing':
        st.markdown("### ⚙️ STATUS")
        st.caption(f"LEVEL: {st.session_state.q_index + 1}/10")
        st.caption(f"SCORE: {st.session_state.score}")
        if st.session_state.malfunction:
            st.markdown("⚠️ <span style='color:red'>ANOMALY</span>", unsafe_allow_html=True)
        else:
            st.markdown("● <span style='color:#00eaff'>STABLE</span>", unsafe_allow_html=True)
