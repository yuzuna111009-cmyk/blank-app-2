import streamlit as st
from supabase import create_client
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import re

# -----------------------------
# ページ設定
# -----------------------------
st.set_page_config(page_title="Report RPG Pro", page_icon="📚")
st.title("📚 Report RPG ")
st.write("あなたのレポートを本気で評価します。")

# -----------------------------
# Supabase接続
# -----------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# 評価関数
# -----------------------------
def evaluate_report(text):

    score = 0

    # ① 文字数
    length = len(text)
    score += length // 5

    # ② 段落数
    paragraphs = text.count("\n")
    score += paragraphs * 50

    # ③ 論理語チェック
    logic_words = ["しかし", "なぜ", "つまり", "したがって", "一方で"]
    logic_count = sum(text.count(word) for word in logic_words)
    score += logic_count * 100

    # ④ 数字（データ使用）
    numbers = re.findall(r"\d+", text)
    if len(numbers) > 0:
        score += 200

    # ⑤ 結論表現
    if "結論" in text or "まとめ" in text:
        score += 300

    return score, length

# -----------------------------
# 入力フォーム
# -----------------------------
name = st.text_input("名前を入力")
report_text = st.text_area("レポート全文を貼ってください", height=300)

if st.button("📊 評価する"):

    if not name or not report_text:
        st.warning("名前とレポートを入力してください")
    else:
        score, length = evaluate_report(report_text)

        if score > 5000:
            title = "👑 伝説の論文王"
        elif score > 3000:
            title = "🧙 上級研究者"
        elif score > 1500:
            title = "⚔️ 優秀レポーター"
        else:
            title = "🪵 見習い学生"

        st.subheader("🏆 評価結果")
        st.write(f"文字数: {length}")
        st.write(f"総合スコア: {score}")
        st.write(f"称号: {title}")

        # 保存
        supabase.table("report_rpg_scores").insert({
            "name": name,
            "score": score,
            "title": title,
            "length": length,
            "created_at": datetime.now().isoformat()
        }).execute()

# -----------------------------
# ランキング
# -----------------------------
st.divider()
st.subheader("🏅 ランキング")

data = supabase.table("report_rpg_scores").select("*").execute()

if data.data:
    df = pd.DataFrame(data.data)
    df_sorted = df.sort_values(by="score", ascending=False)

    st.dataframe(df_sorted[["name", "score", "title", "length"]])

    st.subheader("📈 スコア分布")

    plt.figure()
    plt.hist(df_sorted["score"])
    st.pyplot(plt)

else:
    st.write("まだ評価データがありません。")
