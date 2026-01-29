import streamlit as st
from supabase import create_client
from datetime import datetime, timezone
import random

# =========================
# 初期設定
# =========================
st.set_page_config(page_title="📚 Report　評価 RPG", page_icon="🧙")

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("🧙 レポート評価RPG")
st.write("レポート全文を入力するとAIが評価し、スコアと称号を与えます。")

# =========================
# 入力
# =========================
name = st.text_input("あなたの名前")
report_text = st.text_area("レポート全文を貼ってください", height=250)

# =========================
# スコア計算（簡易AI風ロジック）
# =========================
def evaluate_report(text):
    length_score = min(len(text) // 20, 50)
    keyword_bonus = 20 if "考察" in text else 0
    structure_bonus = 20 if "まとめ" in text else 0
    random_bonus = random.randint(0, 10)
    total = length_score + keyword_bonus + structure_bonus + random_bonus
    return min(total, 100)

def get_title(score):
    if score >= 90:
        return "🏆 伝説の大賢者"
    elif score >= 75:
        return "🧙 大賢者"
    elif score >= 60:
        return "⚔ 勇者"
    elif score >= 40:
        return "🛡 見習い戦士"
    else:
        return "🐣 初心者"

# =========================
# 評価ボタン
# =========================
if st.button("⚔ 評価する"):
    if name and report_text:
        score = evaluate_report(report_text)
        title = get_title(score)

        # 保存
        supabase.table("report_rpg_scores").insert({
            "name": name,
            "score": score,
            "title": title
        }).execute()

        st.success("評価完了！")
        st.subheader(f"🎯 スコア：{score}点")
        st.subheader(f"称号：{title}")

    else:
        st.warning("名前とレポートを入力してください")

# =========================
# 今日のランキング
# =========================
st.divider()
st.subheader("🏆 今日のランキング")

today_start = datetime.now(timezone.utc).replace(
    hour=0, minute=0, second=0, microsecond=0
).isoformat()

data = supabase.table("report_rpg_scores") \
    .select("*") \
    .gte("created_at", today_start) \
    .order("score", desc=True) \
    .execute()

if data.data:
    for i, row in enumerate(data.data[:10], start=1):
        st.write(f"{i}位：{row['name']} - {row['score']}点（{row['title']}）")
else:
    st.write("今日はまだ挑戦者がいません。")
