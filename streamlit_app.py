import streamlit as st
from supabase import create_client
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime

# -----------------------------
# Supabase設定
# -----------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("🗡️ Report RPG - レポート勇者育成ゲーム")
st.write("Wikipediaの知識を使ってレポート勇者を育てよう！")

# -----------------------------
# Wikipedia API
# -----------------------------
def get_wiki_summary(theme):
    url = f"https://ja.wikipedia.org/api/rest_v1/page/summary/{theme}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "情報が見つかりませんでした。")
    else:
        return None

# -----------------------------
# 入力
# -----------------------------
name = st.text_input("勇者の名前")
theme = st.text_input("レポートテーマ")

generate = st.button("⚔️ クエスト開始")

# -----------------------------
# クエスト処理
# -----------------------------
if generate and name and theme:

    summary = get_wiki_summary(theme)

    if summary:
        st.success("クエスト成功！Wikipedia情報を取得！")

        st.subheader("📚 Wikipedia情報")
        st.write(summary)

        # スコア計算（文字数で決定）
        score = len(summary)

        if score > 800:
            title = "伝説のレポート賢者"
        elif score > 400:
            title = "上級勇者"
        else:
            title = "見習い勇者"

        st.subheader("🏆 あなたの称号")
        st.write(title)
        st.write(f"スコア: {score}")

        # Supabase保存
        supabase.table("report_rpg_scores").insert({
            "name": name,
            "score": score,
            "title": title,
            "created_at": datetime.now().isoformat()
        }).execute()

    else:
        st.error("Wikipediaに情報が見つかりませんでした。")

# -----------------------------
# ランキング表示
# -----------------------------
st.divider()
st.subheader("🏅 勇者ランキング")

data = supabase.table("report_rpg_scores").select("*").execute()

if data.data:
    df = pd.DataFrame(data.data)
    df_sorted = df.sort_values(by="score", ascending=False)

    st.dataframe(df_sorted[["name", "score", "title"]])

    st.subheader("📊 スコア分布")

    plt.figure()
    plt.hist(df_sorted["score"])
    st.pyplot(plt)

else:
    st.write("まだ勇者はいない...")
