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
# Wikipedia取得（User-Agent付き）
# -----------------------------
def get_wiki_summary(theme):
    try:
        url = "https://ja.wikipedia.org/w/api.php"

        headers = {
            "User-Agent": "ReportRPGApp/1.0 (educational project)"
        }

        # ① 検索
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": theme,
            "format": "json"
        }

        search_response = requests.get(url, params=search_params, headers=headers, timeout=5)
        search_data = search_response.json()

        if not search_data.get("query", {}).get("search"):
            return None

        page_title = search_data["query"]["search"][0]["title"]

        # ② 本文取得
        extract_params = {
            "action": "query",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": page_title,
            "format": "json"
        }

        extract_response = requests.get(url, params=extract_params, headers=headers, timeout=5)
        extract_data = extract_response.json()

        pages = extract_data.get("query", {}).get("pages", {})
        if not pages:
            return None

        page = next(iter(pages.values()))
        return page.get("extract")

    except Exception as e:
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

        if summary and len(summary) > 50:

            st.success("クエスト成功！Wikipedia情報を取得！")

            st.subheader("📚 Wikipedia情報")
            st.write(summary)

            score = len(summary)

            if score > 2000:
                title = "👑 伝説のレポート賢者"
            elif score > 1000:
                title = "🧙 上級勇者"
            elif score > 500:
                title = "⚔️ 一人前の勇者"
            else:
                title = "🪵 見習い勇者"

            st.subheader("🏆 あなたの称号")
            st.write(title)
            st.write(f"スコア: {score}")

            supabase.table("report_rpg_scores").insert({
                "name": name,
                "score": score,
                "title": title,
                "created_at": datetime.now().isoformat()
            }).execute()

        else:
            st.error("Wikipedia情報の取得に失敗しました。別のテーマを試してください。")

# -----------------------------
# ランキング
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
