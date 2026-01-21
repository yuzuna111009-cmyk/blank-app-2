import streamlit as st
import openai

# OpenAI APIキー（Streamlit Cloud の Secrets に設定）
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🌟 アイドル適性診断メーカー")
st.write("質問に答えて、もしあなたがアイドルだったらどんなタイプか診断します。")

# 質問と点数設定
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

if q1 == "とても好き":
    score += 3
elif q1 == "普通":
    score += 2
else:
    score += 1

if q2 == "得意":
    score += 3
elif q2 == "まあまあ":
    score += 2
else:
    score += 1

if q3 == "得意":
    score += 3
elif q3 == "普通":
    score += 2
else:
    score += 1

# 診断ボタン
if st.button("診断する"):
    if score >= 8:
        idol_type = "センター型アイドル"
    elif score >= 6:
        idol_type = "パフォーマンス特化型アイドル"
    else:
        idol_type = "サポート・バラエティ型アイドル"

    st.subheader(f"🎤 診断結果：{idol_type}")

    # AIに診断コメント生成を指示
    prompt = f"""
    以下のアイドルタイプについて、ポジティブで楽しい診断コメントを日本語で作成してください。
    タイプ：{idol_type}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    comment = response["choices"][0]["message"]["content"]
    st.write(comment)

