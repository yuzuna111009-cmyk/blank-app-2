import streamlit as st
import pandas as pd
from supabase import create_client, Client
from openai import OpenAI

# -----------------------------
# 初期設定
# -----------------------------
st.set_page_config(page_title="レポート構成アドバイザー", page_icon="📝")

# Supabase 接続
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# OpenAI 接続
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# UI
# -----------------------------
st.title("📝 レポート構成アドバイザー")
st.write("テーマを入力するとAIが構成案を生成します。")

theme = st.text_input("レポートのテーマを入力してください")

report_type = st.selectbox(
    "レポートの種類を選択してください",
    ["講義レポート", "調査レポート", "実験レポート", "自由課題レポート"]
)

# -----------------------------
# 構成案生成
# -----------------------------
if st.button("構成案を作成する") and theme:

    with st.spinner("AIが構成案を生成中..."):

        prompt = f"""
        テーマ「{theme}」の{report_type}の構成案を作成してください。

        以下の形式で出力してください：

        ① はじめに
        ② 背景・基礎知識
        ③ 本論・分析
        ④ 考察
        ⑤ まとめ

        各項目に簡単な説明もつけてください。
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは大学レポート指導の専門家です。"},
                {"role": "user", "content": prompt}
            ],
        )

        ai_outline = response.choices[0].message.content

    st.subheader("📄 AI生成構成案")
    st.write(ai_outline)

    # Supabaseに保存
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

    # レポート種類別グラフ
    st.subheader("📊 レポート種類別利用回数")
    st.bar_chart(df["report_type"].value_counts())

    # 人気テーマランキング
    st.subheader("🏆 人気テーマランキング")
    theme_ranking = df["theme"].value_counts().reset_index()
    theme_ranking.columns = ["テーマ", "回数"]
    st.dataframe(theme_ranking.head(5))

else:
    st.write("まだ利用履歴がありません。")

# -----------------------------
# フッター
# -----------------------------
st.caption("© Report Structure Advisor / AI + Supabase 対応版")
