import streamlit as st
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="Monty Hall Simulator", layout="centered")
st.title("🎯 Trò chơi Ô Cửa Bí Mật – Monty Hall")

st.markdown("""
Bạn đang chơi một trò chơi có 3 cánh cửa:
- Một cánh cửa có **🚗 xe hơi** (giải thưởng)
- Hai cánh cửa còn lại có **🐐 con dê**

Sau khi bạn chọn 1 cửa, người dẫn chương trình sẽ mở 1 trong 2 cửa còn lại (chắc chắn là cửa có dê).
Sau đó bạn có thể **giữ nguyên lựa chọn** hoặc **đổi sang cửa còn lại**.

👉 Câu hỏi: **Bạn nên đổi hay giữ?**
""")

# Session state to keep track
if 'total_games' not in st.session_state:
    st.session_state.total_games = 0
    st.session_state.switch_wins = 0
    st.session_state.stay_wins = 0

# Step 1: User chooses a door
st.subheader("🔢 Bước 1: Chọn một cánh cửa")
user_choice = st.radio("Bạn chọn cửa nào?", [1, 2, 3], horizontal=True)

# Step 2: Simulate the game round
if st.button("🎲 Chạy trò chơi"):
    car_door = random.randint(1, 3)
    remaining_doors = [d for d in [1, 2, 3] if d != user_choice and d != car_door]
    if user_choice == car_door:
        reveal_door = random.choice(remaining_doors)
    else:
        reveal_door = [d for d in [1, 2, 3] if d != user_choice and d != car_door][0]

    final_choice = [d for d in [1, 2, 3] if d != user_choice and d != reveal_door][0]

    st.markdown(f"**🚪 Người dẫn chương trình mở cửa {reveal_door} – có 🐐 con dê!**")

    decision = st.radio("Bạn muốn:", ["Giữ nguyên", "Đổi sang cửa còn lại"])

    if decision == "Giữ nguyên":
        chosen = user_choice
    else:
        chosen = final_choice

    # Reveal result
    if chosen == car_door:
        st.success("🎉 Bạn đã chọn đúng! Có xe hơi sau cửa này!")
        if decision == "Giữ nguyên":
            st.session_state.stay_wins += 1
        else:
            st.session_state.switch_wins += 1
    else:
        st.error("😢 Tiếc quá! Sau cửa bạn chọn là 🐐 con dê.")

    st.session_state.total_games += 1

# Statistics
if st.session_state.total_games > 0:
    st.subheader("📊 Kết quả tổng hợp")
    switch_win_rate = st.session_state.switch_wins / st.session_state.total_games * 100
    stay_win_rate = st.session_state.stay_wins / st.session_state.total_games * 100

    st.write(f"- Số lần chơi: {st.session_state.total_games}")
    st.write(f"- Thắng khi **đổi cửa**: {st.session_state.switch_wins} lần ({switch_win_rate:.1f}%)")
    st.write(f"- Thắng khi **giữ nguyên**: {st.session_state.stay_wins} lần ({stay_win_rate:.1f}%)")

    # Plot bar chart
    fig, ax = plt.subplots()
    ax.bar(["Đổi cửa", "Giữ nguyên"], [switch_win_rate, stay_win_rate], color=["green", "orange"])
    ax.set_ylabel("Tỷ lệ thắng (%)")
    ax.set_ylim(0, 100)
    ax.set_title("So sánh xác suất thắng")
    st.pyplot(fig)

st.markdown("---")
st.markdown("📌 *Tip: Hãy thử chơi nhiều lần để thấy xác suất đổi cửa > giữ nguyên!* 🚀")
