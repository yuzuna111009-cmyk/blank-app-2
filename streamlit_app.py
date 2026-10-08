import streamlit as st
import sqlite3
from datetime import datetime, timedelta, timezone
import random

# =========================
# 初期設定
# =========================
st.set_page_config(
    page_title="📚 Report 評価 RPG",
    page_icon="🧙"
)

# =========================
# SQLite3 データベース設定
# =========================
DB_NAME = "report_rpg.db"

JST = timezone(timedelta(hours=9))


def get_connection():
    return sqlite3.connect(DB_NAME, timeout=10)


# テーブル作成（初回のみ）
def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS report_rpg_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER NOT NULL,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


init_db()

# =========================
# アプリタイトル
# =========================
st.title("🧙 レポート評価RPG")
st.write("レポート全文を入力するとAIが評価し、スコアと称号を与えます。")

# =========================
# 入力
# =========================
name = st.text_input("あなたの名前")

report_text = st.text_area(
    "レポート全文を貼ってください",
    height=250
)

# =========================
# スコア計算（簡易AI風ロジック）
# =========================
def evaluate_report(text):
    length_score = min(len(text) // 20, 50)

    keyword_bonus = 20 if "考察" in text else 0

    structure_bonus = 20 if "まとめ" in text else 0

    random_bonus = random.randint(0, 10)

    total = (
        length_score
        + keyword_bonus
        + structure_bonus
        + random_bonus
    )

    return min(total, 100)


# =========================
# 称号判定
# =========================
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
# SQLite3に結果を保存
# =========================
def save_score(name, score, title):
    created_at = datetime.now(JST).isoformat()

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO report_rpg_scores
            (name, score, title, created_at)
            VALUES (?, ?, ?, ?)
        """, (name, score, title, created_at))


# =========================
# 今日のランキング取得
# =========================
def get_today_ranking():
    today = datetime.now(JST).date().isoformat()

    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT name, score, title
            FROM report_rpg_scores
            WHERE substr(created_at, 1, 10) = ?
            ORDER BY score DESC, created_at ASC
            LIMIT 10
        """, (today,))

        return cursor.fetchall()


# =========================
# 評価ボタン
# =========================
if st.button("⚔ 評価する"):

    if name.strip() and report_text.strip():

        score = evaluate_report(report_text)

        title = get_title(score)

        # SQLite3に保存
        save_score(name.strip(), score, title)

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

ranking = get_today_ranking()

if ranking:

    for i, row in enumerate(ranking, start=1):

        name, score, title = row

        st.write(
            f"{i}位：{name} - {score}点（{title}）"
        )

else:
    st.write("今日はまだ挑戦者がいません。")
