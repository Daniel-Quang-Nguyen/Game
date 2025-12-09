import streamlit as st
import random
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Vua Trọng Âm", page_icon="🎤")

# --- DỮ LIỆU TỪ VỰNG (TỪ ẢNH CỦA BẠN) ---
# Format: "Từ": [Vị trí trọng âm, "Phiên âm"]
data = {
    "Also": [1, "/'ɔ:l.sou/"],
    "Apollo": [2, "/ə'pɑ:.lou/"],
    "Auto": [1, "/'ɔ:.tou/"],
    "Bingo": [1, "/'biŋ.gou/"],
    "Bolero": [2, "/bə'ler.ou/"],
    "Photo": [1, "/'fou.tou/"],
    "Picasso": [2, "/pi'kæ.sou/"],
    "Potato": [2, "/pə'tei.tou/"],
    "Inferno": [2, "/in'fз:.nou/"],
    "Morocco": [2, "/mə'rɑ:.kou/"],
    "Psycho": [1, "/'sai.kou/"],
    "Toronto": [2, "/tə'rɑ:n.tou/"],
    "Disco": [1, "/'dis.kou/"],
    "Intro": [1, "/'in.trou/"],
    "Mosquito": [2, "/mə'ski:.tou/"],
    "Motto": [1, "/'mɑ:.tou/"],
    "Casino": [2, "/kə'si:.nou/"],
    "Commando": [2, "/kə'mæn.dou/"],
    "Flamingo": [2, "/flə'miŋ.gou/"],
    "Manifesto": [3, "/,mæn.ə'fes.tou/"]
}

# --- HÀM KHỞI TẠO STATE (LƯU TRẠNG THÁI GAME) ---
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'shuffled_list' not in st.session_state:
    keys = list(data.keys())
    random.shuffle(keys)
    st.session_state.shuffled_list = keys
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'last_result' not in st.session_state:
    st.session_state.last_result = None

# --- GIAO DIỆN CHÍNH ---
st.title("🏆 Sàn Đấu Trọng Âm")
st.markdown("Quy luật: Các từ kết thúc bằng đuôi **-O**")

# --- THANH TIẾN ĐỘ & ĐIỂM SỐ ---
col1, col2 = st.columns(2)
with col1:
    st.metric("Điểm số", f"{st.session_state.score} / {len(data)}")
with col2:
    progress = st.session_state.current_q / len(data)
    st.progress(progress)

# --- LOGIC GAME ---
if not st.session_state.game_over:
    if st.session_state.current_q < len(data):
        # Lấy từ hiện tại
        current_word = st.session_state.shuffled_list[st.session_state.current_q]
        correct_answer = data[current_word][0]
        ipa = data[current_word][1]

        # Hiển thị từ vựng to rõ
        st.markdown(f"<h1 style='text-align: center; color: #4CAF50; font-size: 60px;'>{current_word}</h1>", unsafe_allow_html=True)
        
        st.write("Trọng âm rơi vào âm tiết thứ mấy?")
        
        # Các nút bấm chọn đáp án
        c1, c2, c3 = st.columns(3)
        
        def check_answer(user_choice):
            if user_choice == correct_answer:
                st.session_state.score += 1
                st.session_state.last_result = f"✅ Chính xác! **{current_word}** {ipa} nhấn âm **{correct_answer}**"
                if correct_answer == 3:
                     st.balloons() # Thả bóng bay nếu đúng câu khó
            else:
                st.session_state.last_result = f"❌ Sai rồi! **{current_word}** {ipa} nhấn âm **{correct_answer}**"
            
            st.session_state.current_q += 1
            # Rerun để load câu mới
            # st.experimental_rerun() (Deprecated in new versions)
        
        with c1:
            if st.button("1️⃣ Âm Nhất", use_container_width=True):
                check_answer(1)
                st.rerun()
        with c2:
            if st.button("2️⃣ Âm Hai", use_container_width=True):
                check_answer(2)
                st.rerun()
        with c3:
            if st.button("3️⃣ Âm Ba", use_container_width=True):
                check_answer(3)
                st.rerun()

        # Hiển thị kết quả câu trước đó
        if st.session_state.last_result:
            if "✅" in st.session_state.last_result:
                st.success(st.session_state.last_result)
            else:
                st.error(st.session_state.last_result)

    else:
        st.session_state.game_over = True
        st.rerun()

else:
    # --- MÀN HÌNH KẾT THÚC ---
    st.success("🎉 CHÚC MỪNG BẠN ĐÃ HOÀN THÀNH!")
    final_score = st.session_state.score
    total = len(data)
    
    st.markdown(f"<h2 style='text-align: center;'>Kết quả: {final_score}/{total}</h2>", unsafe_allow_html=True)
    
    if final_score == total:
        st.balloons()
        st.markdown("**Đẳng cấp! Bạn là bậc thầy trọng âm! 👑**")
    elif final_score > total / 2:
        st.markdown("**Khá lắm! Hãy luyện thêm một chút nữa.**")
    else:
        st.markdown("**Cần cố gắng nhiều hơn nhé!**")

    # Nút chơi lại
    if st.button("🔄 Chơi lại từ đầu", type="primary"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.last_result = None
        random.shuffle(st.session_state.shuffled_list)
        st.rerun()

# --- PHẦN ÔN TẬP (ẨN) ---
with st.expander("📖 Xem lại bảng từ vựng"):
    st.table([{"Từ": k, "Phiên âm": v[1], "Trọng âm": v[0]} for k, v in data.items()])
