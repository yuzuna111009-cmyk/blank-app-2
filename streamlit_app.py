import streamlit as st
from supabase import create_client
from openai import OpenAI
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# -----------------------------
# API設定
# -----------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🗡️ Report RPG - レポート勇者育成ゲーム")

# -----------------------------
# 入力フォーム
# -----------------------------
name = st.text_input("勇者の名前を入力せよ")
theme = st.text_input("レポートテーマ")
report_type = st.selectbox(
    "レポートの種類",
    ["講義レポート", "調査レポート", "実験レポート", "自由課題レポート"]
)

generate = st.button("⚔️ レポートに挑戦する")

# -----------------------------
# AI生成
# -----------------------------
if generate and theme != "" and name != "":

    with st.spinner("魔王（AI）が構成を生成中..."):

        prompt = f"""
        レポートテーマ: {theme}
        種類: {report_type}

        RPG風にレポート構成を作ってください。
        章ごとにレベル形式で。
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        result = response.choices[0].message.content

        st.success("クエスト成功！")
        st.write(result)

        # -----------------------------
        # スコア計算（簡易）
        # -----------------------------
        score = len(theme) * 10

        if score > 200:
            title = "レポート賢者"
        elif score > 120:
            title = "上級勇者"
        else:
            title = "見習い勇者"

        st.subheader("🏆 あなたの称号")
        st.write(title)
        st.write(f"スコア: {score}")

        # -----------------------------
        # Supabase保存
        # -----------------------------
        supabase.table("report_rpg_scores").insert({
            "name": name,
            "score": score,
            "title": title,
            "created_at": datetime.now().isoformat()
        }).execute()

# -----------------------------
# ランキング表示
# -----------------------------
st.subheader("🏅 勇者ランキング")

data = supabase.table("report_rpg_scores").select("*").execute()

if data.data:
    df = pd.DataFrame(data.data)
    df_sorted = df.sort_values(by="score", ascending=False)

    st.dataframe(df_sorted[["name", "score", "title"]])

    # -----------------------------
    # スコアグラフ
    # -----------------------------
    st.subheader("📊 スコア分布")

    plt.figure()
    plt.hist(df_sorted["score"])
    st.pyplot(plt)

else:
    st.write("まだ勇者はいない...")
