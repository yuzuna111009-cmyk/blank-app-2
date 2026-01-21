import streamlit as st

st.title("🌟 アイドル適性診断メーカー")
st.write("質問に答えて、もしあなたがアイドルだったらどんなタイプか診断します。")

# 質問
q1 = st.radio(
    "① 人前に立つのは好きですか？",
    ("とても好き", "普通", "少し苦手")
)

q2 = st.radio(
    "② コツコツ練習するのは得意ですか？",
    ("得意", "まあまあ", "苦手")
)

q3 = st.radio(
    "③ トークやバラエティは得意ですか？",
    ("得意", "普通", "苦手")
)

# 点数計算
score = 0

score += 3 if q1 == "とても好き" else 2 if q1 == "普通" else 1
score += 3 if q2 == "得意" else 2 if q2 == "まあまあ" else 1
score += 3 if q3 == "得意" else 2 if q3 == "普通" else 1

# 診断
if st.button("診断する"):
    if score >= 8:
        idol_type = "🌟 センター型アイドル"
        comment = "あなたは人を惹きつける華のある存在です。ステージの中心で輝く素質があります。"
    elif score >= 6:
        idol_type = "💃 パフォーマンス特化型アイドル"
        comment = "努力を重ねて実力で魅せるタイプです。ライブで真価を発揮します。"
    else:
        idol_type = "🎤 サポート・バラエティ型アイドル"
        comment = "周囲を支え、場の雰囲気を明るくする大切な存在です。"

    st.subheader(f"診断結果：{idol_type}")
    st.write(comment)


