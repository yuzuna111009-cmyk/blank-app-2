import streamlit as st

st.set_page_config(page_title="アイドル総合適性診断", page_icon="🎤")

st.title("🎤 アイドル総合適性診断")
st.write("12の質問に答えて、あなたのアイドルとしての強みを診断します。")

# 回答選択肢
choices = {
    "とても当てはまる": 3,
    "少し当てはまる": 2,
    "あまり当てはまらない": 1
}

def q(text):
    return st.radio(text, list(choices.keys()), index=1)

st.header("🌟 ステージ・表現")
s1 = q("① 人前に立つと緊張よりワクワクする")
s2 = q("② 注目されるとやる気が出る")
s3 = q("③ 表情や仕草で感情を表現するのが得意")

st.header("💃 努力・練習")
e1 = q("④ 毎日同じ練習を続けるのは苦ではない")
e2 = q("⑤ 自分の弱点を分析するのが好き")
e3 = q("⑥ すぐ結果が出なくても頑張れる")

st.header("🎤 コミュニケーション")
m1 = q("⑦ 初対面の人とも比較的すぐ話せる")
m2 = q("⑧ 周囲の雰囲気をよく気にする")
m3 = q("⑨ 場を盛り上げる役になることが多い")

st.header("🤝 チーム意識")
t1 = q("⑩ グループ全体の成功を大事にしたい")
t2 = q("⑪ 困っている人に気づきやすい")
t3 = q("⑫ 裏方の役割も重要だと思う")

if st.button("診断する"):
    star = sum(choices[x] for x in [s1, s2, s3])
    effort = sum(choices[x] for x in [e1, e2, e3])
    mood = sum(choices[x] for x in [m1, m2, m3])
    team = sum(choices[x] for x in [t1, t2, t3])

    scores = {
        "🌟 スター型アイドル": star,
        "💃 ストイック型アイドル": effort,
        "🎤 ムードメーカー型アイドル": mood,
        "🤝 チーム支援型アイドル": team
    }

    result = max(scores, key=scores.get)

    comments = {
        "🌟 スター型アイドル":
            "強い存在感と発信力があり、自然と注目を集めるタイプです。ステージの中心で輝く素質があります。",
        "💃 ストイック型アイドル":
            "努力を惜しまない職人気質。実力で信頼を勝ち取る、成長型のアイドルです。",
        "🎤 ムードメーカー型アイドル":
            "トーク力と空気感で場を明るくする存在。バラエティやMCで力を発揮します。",
        "🤝 チーム支援型アイドル":
            "周囲をよく見て支える縁の下の力持ち。グループに欠かせない存在です。"
    }

    st.subheader(f"🎉 診断結果：{result}")
    st.write(comments[result])

    st.markdown("### 📊 分野別スコア")
    for k, v in scores.items():
        st.write(f"- {k}：{v} 点")
