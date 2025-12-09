import streamlit as st
import random
import time
import pandas as pd
import re

# --- CONFIGURATION & STYLE ---
st.set_page_config(page_title="CYBER STRESS", page_icon="💠", layout="centered")

# CSS Styling for Technological/Dark Blue Theme
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        color: #00FFC2;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #161B22;
        color: #00FFC2;
        border: 1px solid #00FFC2;
        border-radius: 0px;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #00FFC2;
        color: #0E1117;
        border-color: #FFFFFF;
        box-shadow: 0 0 10px #00FFC2;
    }
    
    /* Inputs */
    .stTextInput>div>div>input {
        background-color: #0E1117;
        color: #FFFFFF;
        border: 1px solid #30363D;
        border-radius: 0px;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #00FFC2;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Table */
    div[data-testid="stDataFrame"] {
        border: 1px solid #30363D;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATASET ---
word_data = {
    # Từ: [Trọng âm, Phiên âm]
    "Also": [1, "/'ɔ:l.sou/"], "Apollo": [2, "/ə'pɑ:.lou/"], "Auto": [1, "/'ɔ:.tou/"],
    "Bingo": [1, "/'biŋ.gou/"], "Bolero": [2, "/bə'ler.ou/"], "Photo": [1, "/'fou.tou/"],
    "Picasso": [2, "/pi'kæ.sou/"], "Potato": [2, "/pə'tei.tou/"], "Inferno": [2, "/in'fз:.nou/"],
    "Morocco": [2, "/mə'rɑ:.kou/"], "Psycho": [1, "/'sai.kou/"], "Toronto": [2, "/tə'rɑ:n.tou/"],
    "Disco": [1, "/'dis.kou/"], "Intro": [1, "/'in.trou/"], "Mosquito": [2, "/mə'ski:.tou/"],
    "Motto": [1, "/'mɑ:.tou/"], "Casino": [2, "/kə'si:.nou/"], "Commando": [2, "/kə'mæn.dou/"],
    "Flamingo": [2, "/flə'miŋ.gou/"], "Manifesto": [3, "/,mæn.ə'fes.tou/"],
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

# --- SESSION STATE INITIALIZATION ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'score' not in st.session_state: st.session_state.score = 0
if 'user_name' not in st.session_state: st.session_state.user_name = "Guest"
if 'game_mode' not in st.session_state: st.session_state.game_mode = None
if 'q_index' not in st.session_state: st.session_state.q_index = 0
if 'start_time' not in st.session_state: st.session_state.start_time = 0
if 'leaderboard' not in st.session_state: 
    st.session_state.leaderboard = pd.DataFrame(columns=["USER", "SCORE", "MODE", "TIME"])
if 'shuffled_keys' not in st.session_state: st.session_state.shuffled_keys = []
if 'current_options' not in st.session_state: st.session_state.current_options = []

# --- HELPER FUNCTIONS ---
def generate_ipa_distractors(correct_ipa):
    """Tạo ra các đáp án nhiễu cho phiên âm IPA"""
    options = [correct_ipa]
    
    # Fake 1: Dịch chuyển dấu trọng âm
    if "'" in correct_ipa:
        fake1 = correct_ipa.replace("'", "", 1) # Bỏ dấu cũ
        # Thêm dấu vào vị trí ngẫu nhiên khác
        insert_pos = random.randint(1, len(fake1)-2)
        fake1 = fake1[:insert_pos] + "'" + fake1[insert_pos:]
        options.append(fake1)
    
    # Fake 2: Thay đổi nguyên âm (gây nhầm lẫn)
    fake2 = correct_ipa.replace("ei", "e").replace("ou", "o").replace("i", "ai")
    if fake2 == correct_ipa: fake2 = correct_ipa.replace("ə", "e")
    options.append(fake2)
    
    # Fake 3: Thay đổi phụ âm cuối hoặc giữa
    fake3 = correct_ipa.replace("dʒ", "g").replace("ʃ", "s").replace("z", "s")
    if fake3 == correct_ipa: fake3 = correct_ipa + ":"
    options.append(fake3)
    
    random.shuffle(options)
    return options

def calculate_points(start_time):
    elapsed = time.time() - start_time
    # Cơ chế: Điểm tối đa 100, giảm dần theo giây. Tối thiểu 10 điểm.
    points = max(10, 100 - int(elapsed * 2))
    return points, round(elapsed, 2)

def reset_game(mode):
    st.session_state.game_mode = mode
    st.session_state.score = 0
    st.session_state.q_index = 0
    st.session_state.page = 'playing'
    
    if mode == 3: # Sentence mode
        indices = list(range(len(sentence_data)))
        random.shuffle(indices)
        st.session_state.shuffled_keys = indices
    else: # Word mode
        keys = list(word_data.keys())
        random.shuffle(keys)
        st.session_state.shuffled_keys = keys
    
    st.session_state.start_time = time.time()

# --- APP PAGES ---

# 1. WELCOME SCREEN
if st.session_state.page == 'welcome':
    st.title("💠 SYSTEM ENTRY: STRESS_CODE")
    st.markdown("---")
    
    # Leaderboard Mini View
    if not st.session_state.leaderboard.empty:
        st.markdown("### >> HALL OF FAME")
        st.dataframe(st.session_state.leaderboard.sort_values(by="SCORE", ascending=False).head(5), hide_index=True)

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info("DATA_LOADED: -O / -AGE")
        st.markdown("**RULES:**")
        st.markdown("1. Speed is key.")
        st.markdown("2. Accuracy is mandatory.")
        
    with col2:
        # Bảng từ vựng để học trước
        with st.expander(">> ACCESS DATABASE (REVIEW WORDS)", expanded=True):
            df_view = pd.DataFrame([
                {"WORD": k, "IPA": v[1], "STRESS": v[0]} for k, v in word_data.items()
            ])
            st.dataframe(df_view, height=300)

    st.markdown("---")
    st.markdown("### >> IDENTIFICATION")
    name_input = st.text_input("ENTER CODENAME:", placeholder="Type your name here...")
    
    if name_input:
        st.session_state.user_name = name_input
        st.markdown("### >> SELECT MISSION MODE")
        c1, c2, c3 = st.columns(3)
        if c1.button("MODE 1: STRESS TARGET"):
            reset_game(1)
            st.rerun()
        if c2.button("MODE 2: IPA DECODER"):
            reset_game(2)
            st.rerun()
        if c3.button("MODE 3: SIGNAL REWRITE"):
            reset_game(3)
            st.rerun()

# 2. PLAYING SCREEN
elif st.session_state.page == 'playing':
    # Progress Bar
    total_q = 10 # Giới hạn 10 câu mỗi lượt chơi cho nhanh
    progress = st.session_state.q_index / total_q
    st.progress(progress)
    
    # Score Display
    st.markdown(f"**OPERATOR:** {st.session_state.user_name} | **SCORE:** {st.session_state.score} | **Q:** {st.session_state.q_index + 1}/{total_q}")
    st.markdown("---")

    if st.session_state.q_index < total_q and st.session_state.q_index < len(st.session_state.shuffled_keys):
        
        # LOGIC FOR MODE 1 & 2 (Single Words)
        if st.session_state.game_mode in [1, 2]:
            current_word = st.session_state.shuffled_keys[st.session_state.q_index]
            correct_stress = word_data[current_word][0]
            correct_ipa = word_data[current_word][1]
            
            # --- MODE 1: STRESS PLACEMENT ---
            if st.session_state.game_mode == 1:
                st.markdown(f"<h1 style='text-align: center; font-size: 50px; color: white;'>{current_word}</h1>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: gray;'>IDENTIFY STRESS POSITION</p>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns(3)
                
                def check_stress(ans):
                    pts, sec = calculate_points(st.session_state.start_time)
                    if ans == correct_stress:
                        st.success(f">> CORRECT. +{pts} PTS ({sec}s)")
                        st.session_state.score += pts
                        time.sleep(1) # Pause slightly
                    else:
                        st.error(f">> ERROR. CORRECT: {correct_stress}")
                        time.sleep(1.5)
                    st.session_state.q_index += 1
                    st.session_state.start_time = time.time()
                    st.rerun()

                with c1: st.button("STRESS [1]", on_click=check_stress, args=(1,))
                with c2: st.button("STRESS [2]", on_click=check_stress, args=(2,))
                with c3: st.button("STRESS [3]", on_click=check_stress, args=(3,))
            
            # --- MODE 2: IPA QUIZ (Multiple Choice) ---
            elif st.session_state.game_mode == 2:
                st.markdown(f"<h1 style='text-align: center; font-size: 50px; color: white;'>{current_word}</h1>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: gray;'>SELECT ACCURATE TRANSCRIPTION</p>", unsafe_allow_html=True)
                
                # Generate options only once per question to avoid shuffle on click
                if not st.session_state.current_options:
                    st.session_state.current_options = generate_ipa_distractors(correct_ipa)
                
                options = st.session_state.current_options
                
                def check_ipa(ans):
                    pts, sec = calculate_points(st.session_state.start_time)
                    if ans == correct_ipa:
                        st.success(f">> CORRECT. +{pts} PTS")
                        st.session_state.score += pts
                        time.sleep(1)
                    else:
                        st.error(f">> ERROR. TARGET: {correct_ipa}")
                        time.sleep(2)
                    st.session_state.q_index += 1
                    st.session_state.start_time = time.time()
                    st.session_state.current_options = [] # Reset options
                    st.rerun()

                c1, c2 = st.columns(2)
                with c1:
                    st.button(f"A. {options[0]}", on_click=check_ipa, args=(options[0],))
                    st.button(f"C. {options[2]}", on_click=check_ipa, args=(options[2],))
                with c2:
                    st.button(f"B. {options[1]}", on_click=check_ipa, args=(options[1],))
                    if len(options) > 3:
                        st.button(f"D. {options[3]}", on_click=check_ipa, args=(options[3],))

        # --- MODE 3: SENTENCE REWRITE ---
        elif st.session_state.game_mode == 3:
            idx = st.session_state.shuffled_keys[st.session_state.q_index]
            current_item = sentence_data[idx]
            
            st.markdown("<p style='text-align: center; color: #00FFC2;'>DECRYPT THIS SIGNAL:</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; border: 1px dashed #30363D; padding: 20px;'>{current_item['ipa']}</h2>", unsafe_allow_html=True)
            
            user_text = st.text_input("DECODED MESSAGE:", key=f"input_{st.session_state.q_index}")
            
            if st.button("SUBMIT ANSWER"):
                pts, sec = calculate_points(st.session_state.start_time)
                
                # Normalize text (lowercase, remove punctuation at end)
                clean_user = user_text.strip().lower().rstrip('.')
                clean_target = current_item['text'].strip().lower().rstrip('.')
                
                if clean_user == clean_target:
                    st.success(f">> DECRYPTED SUCCESSFULLY. +{pts} PTS")
                    st.session_state.score += pts
                else:
                    st.error(f">> FAILED. TARGET: {current_item['text']}")
                
                time.sleep(2)
                st.session_state.q_index += 1
                st.session_state.start_time = time.time()
                st.rerun()

    else:
        # End of Game
        st.session_state.page = 'result'
        st.rerun()

# 3. RESULT SCREEN
elif st.session_state.page == 'result':
    st.markdown("<h1 style='text-align: center; color: #00FFC2;'>MISSION COMPLETE</h1>", unsafe_allow_html=True)
    
    final_score = st.session_state.score
    st.metric("FINAL SCORE", final_score)
    
    # Save to Leaderboard
    new_entry = pd.DataFrame([{
        "USER": st.session_state.user_name,
        "SCORE": final_score,
        "MODE": f"MODE {st.session_state.game_mode}",
        "TIME": time.strftime("%H:%M")
    }])
    
    # Avoid duplicates if just rerunning
    if st.session_state.leaderboard.empty or final_score != st.session_state.leaderboard.iloc[-1]['SCORE']:
         st.session_state.leaderboard = pd.concat([st.session_state.leaderboard, new_entry], ignore_index=True)
    
    st.markdown("### >> GLOBAL RANKING (SESSION)")
    st.dataframe(
        st.session_state.leaderboard.sort_values(by="SCORE", ascending=False).reset_index(drop=True),
        use_container_width=True
    )
    
    if st.button(">> RESTART SYSTEM"):
        st.session_state.page = 'welcome'
        st.session_state.score = 0
        st.rerun()
