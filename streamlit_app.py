import streamlit as st
from supabase import create_client
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime

# -----------------------------
# ページ設定
# -----------------------------
st.set_page_config(page_title="Report RPG", page_icon="🗡️")

st.title("🗡️ Report RPG - レポート勇者育成ゲーム")
st.write("Wikipediaの知識を使ってレポート勇者を育てよう！")

# -----------------------------
# Supabase接続
# -----------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# Wikipedia検索＋要約取得
# -----------------------------
def get_wiki_summary(theme):
    try:
        search_url = "https://ja.wikipedia.org/w/api.php"

        # ① 検索
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": theme,
            "format": "json"
        }

        search_response = requests.get(search_url, params=search_params)
        search_data = search_response.json()

        if search_data["query"]["search"]:
            page_title = search_data["query"]["search"][0]["title"]

            # ② 要約取得
            summary_url = f"https://ja.wikipedia.org/api/rest_v1/page/summary/{page_title}"
            summary_response = requests.get(summary_url)

            if summary_response.status_code == 200:
                return summary_response.json().get("extract")

        return None

    except Exception:
        return None

# -----------------------------
# 入力フォーム
# -----------------------------
name = st.text_input("勇者の名前を入力")
theme = st.text_input("レポートテーマを入力")

generate = st.button("⚔️ クエスト開始")

# -----------------------------
# クエスト処理
# -----------------------------
if generate:

    if not name or not theme:
        st.warning("名前とテーマを入力してください")
    else:
        summary = get_wiki_summary(theme)

        if summary:

            st.success("クエスト成功！Wikipedia情報を取得！")

            st.subheader("📚 Wikipedia情報")
            st.write(summary)

            # スコア計算（文字数）
            score = len(summary)

            if score > 1500:
                title = "👑 伝説のレポート賢者"
            elif score > 800:
                title = "🧙 上級勇者"
            elif score > 300:
                title = "⚔️ 一人前の勇者"
            else:
                title = "🪵 見習い勇者"

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
            st.error("Wikipediaに十分な情報が見つかりませんでした。別のテーマで挑戦してください。")

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

    # グラフ
    st.subheader("📊 スコア分布")

    plt.figure()
    plt.hist(df_sorted["score"])
    st.pyplot(plt)

    # テーマ人気ランキング
    st.subheader("🔥 人気テーマランキング")

    theme_counts = df["title"].value_counts()
    st.dataframe(theme_counts)

else:
    st.write("まだ勇者はいない...")
