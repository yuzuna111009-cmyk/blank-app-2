import streamlit as st
import pandas as pd
import requests
from supabase import create_client, Client

# -----------------------------
# 初期設定
# -----------------------------
st.set_page_config(page_title="レポート構成アドバイザー", page_icon="📝")

# Supabase 接続
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# -----------------------------
# Wikipedia API関数
# -----------------------------
def get_wikipedia_summary(keyword):
    url = "https://ja.wikipedia.org/api/rest_v1/page/summary/" + keyword
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "概要が見つかりませんでした。")
    else:
        return "Wikipediaに該当ページがありません。"

# -----------------------------
# UI
# -----------------------------
st.title("📝 レポート構成アドバイザー（Wikipedia連携版）")
st.write("テーマを入力すると、Wikipediaの情報をもとに構成案を生成します。")

theme = st.text_input("レポートのテーマを入力してください")

report_type = st.selectbox(
    "レポートの種類を選択してください",
    ["講義レポート", "調査レポート", "実験レポート", "自由課題レポート"]
)

# -----------------------------
# 構成案生成
# -----------------------------
if st.button("構成案を作成する") and theme:

    with st.spinner("Wikipediaから情報取得中..."):

        summary = get_wikipedia_summary(theme)

    st.subheader("📚 Wikipedia概要")
    st.write(summary)

    st.subheader("📄 レポート構成案")

    st.markdown("### ① はじめに")
    st.write(f"- テーマ「{theme}」の概要と重要性を説明する")
    st.write("- 本レポートの目的を示す")

    st.markdown("### ② 背景・基礎知識")
    st.write("- Wikipediaの内容を整理する")
    st.write("- 基本用語や歴史をまとめる")

    st.markdown("### ③ 本論・分析")
    st.write("- Wikipedia情報をもとに詳しく分析")
    st.write("- 他資料と比較する")

    st.markdown("### ④ 考察")
    st.write("- 課題点や問題点を整理")
    st.write("- 自分の意見を述べる")

    st.markdown("### ⑤ まとめ")
    st.write("- 全体の要点を整理")

    # Supabase保存
    supabase.table("report_usage").insert({
        "theme": theme,
        "report_type": report_type
    }).execute()

    st.success("利用履歴を保存しました ✅")

# -----------------------------
# 利用状況表示
# -----------------------------
st.divider()
st.subheader("📊 アプリの利用状況")

data = supabase.table("report_usage") \
    .select("*") \
    .order("created_at", desc=True) \
    .execute()

if data.data:
    df = pd.DataFrame(data.data)

    st.write(f"🟢 これまでの利用回数：**{len(df)} 回**")

    st.subheader("📊 レポート種類別利用回数")
    st.bar_chart(df["report_type"].value_counts())

    st.subheader("🏆 人気テーマランキング")
    theme_ranking = df["theme"].value_counts().reset_index()
    theme_ranking.columns = ["テーマ", "回数"]
    st.dataframe(theme_ranking.head(5))

else:
    st.write("まだ利用履歴がありません。")

# -----------------------------
# フッター
# -----------------------------
st.caption("© Report Structure Advisor / Wikipedia API + Supabase 対応版")
