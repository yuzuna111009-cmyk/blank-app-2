import streamlit as st
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
# UI
# -----------------------------
st.title("📝 レポート構成アドバイザー")
st.write("レポートのテーマを入力すると、構成案・注意点・チェック項目を提示します。")

theme = st.text_input("レポートのテーマを入力してください", key="theme_input")

report_type = st.selectbox(
    "レポートの種類を選択してください",
    ["講義レポート", "調査レポート", "実験レポート", "自由課題レポート"],
    key="report_type"
)

# -----------------------------
# 構成案作成
# -----------------------------
if st.button("構成案を作成する", key="create_outline") and theme:

    # Supabase に保存
    supabase.table("report_usage").insert({
        "theme": theme,
        "report_type": report_type
    }).execute()

    st.success("利用履歴を保存しました ✅")

    st.subheader("📄 レポート構成案")

    st.markdown("### ① はじめに（導入）")
    st.write(f"- テーマ「{theme}」を選んだ理由を書く")
    st.write("- レポートの目的・問題意識を明確にする")
    st.write("【文字数目安】10〜15%")

    st.markdown("### ② 背景・基礎知識")
    st.write("- 基本用語や理論を整理する")
    st.write("- 信頼できる資料を引用する")
    st.write("【文字数目安】20〜25%")

    st.markdown("### ③ 本論・分析")
    st.write("- データや具体例を用いて論じる")
    st.write("【文字数目安】40〜50%")

    st.markdown("### ④ 考察")
    st.write("- 分析結果から分かることを整理")
    st.write("- 自分の意見を論理的に述べる")

    st.m
