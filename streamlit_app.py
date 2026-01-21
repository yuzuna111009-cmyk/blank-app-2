import streamlit as st

st.title("🌟 アイドル適性診断メーカー")
st.write("質問に答えて、あなたのアイドル適性タイプを診断します。")

def question(text):
    return st.radio(
        text,
        ("とても当てはまる", "少し当てはまる", "あまり当てはまらない"),
        index=1
    )

q1 = question("① 人前に立つのは好きですか？")
q2 = question("② ダンスや歌の練習は好きですか？")
q3 = question("③ トークやバラエティは得意ですか？")
q4 = question("④ 毎日コツコツ努力するのは得意ですか？")
q5 = question("⑤ チームのまとめ役になることが多いですか？")
q6 = question("⑥ 失敗してもすぐ切り替えられますか？")

def score(ans):
    return 3 if ans == "とても当てはまる" else 2 if ans == "少し当てはまる" else 1

total = sum(map(score, [q1, q2, q3, q4, q5, q6]))

if st.button("診断する"):
    if total >= 13:
        idol_type = "🌟 センター型アイドル"
        comment = "自然と視線を集める華があり、ステージの中心で輝く存在です。"
    elif total >= 11:
        idol_type = "💃 パフォーマンス特化型アイドル"
        comment = "努力と実力で魅せるタイプ。ライブで真価を発揮します。"
    elif total >= 9:
        idol_type = "🎤 バラエティ型アイドル"
        comment = "トークやリアクションで場を盛り上げるムードメーカーです。"
    elif total >= 7:
        idol_type = "🧠 努力家プロ型アイドル"
        comment = "地道な努力を積み重ね、着実に成長していくタイプです。"
    else:
        idol_type = "🤝 サポート型アイドル"
        comment = "周囲をよく見て支える、グループに欠かせない存在です。"

    st.subheader(f"診断結果：{idol_type}")
    st.write(comment)
    st.caption(f"合計点：{total} 点")
