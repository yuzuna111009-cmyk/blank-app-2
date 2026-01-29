import streamlit as st
from supabase import create_client
from datetime import datetime, timezone
import random

# =========================
# 初期設定
# =========================
st.set_page_config(page_title="📚 レポートRPG", page_icon="🧙", layout="wide")

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# タブ切り替え
# =========================
tab = st.tabs(["🏠 アプリ説明", "⚔ レポート評価"])

with tab[0]:
    st.header("📚 レポートRPG")
    st.write("""
    Streamlitを利用した、レポート全文を評価して**スコアと称号**を付与するWebアプリケーションです。  
    楽しみながら自分のレポートを客観的に確認でき、今日のランキングで他の挑戦者と競えます。
    """)
    
    st.subheader("🌟 主な機能")
    st.markdown("""
    - **レポート評価モード**: レポート全文をAI風ロジックで評価し、スコアと称号を付与します。  
    - **称号システム**: スコアに応じて「伝説の大賢者」「大賢者」「勇者」「見習い戦士」「初心者」の称号を自動で表示。  
    - **今日のランキング表示**: 今日投稿されたレポートのスコアランキングを確認できます。  
    - **Supabase連携**: 名前・スコア・称号を永続的に保存し、アプリ再起動後もデータを保持。  
    - **簡易操作UI**: 名前とレポートを入力 → 評価ボタン → スコア・称号表示。
    """)

    st.subheader("💻 使用技術")
    st.markdown("""
    - **Frontend/UI**: [Streamlit](https://streamlit.io/)  
    - **Backend/DB**: [Supabase (PostgreSQL)](https://supabase.com/)  
    - **Language**: Python
    """)

    st.subheader("⚔ スコアと称号の目安")
    st.table({
        "スコア": ["90以上", "75以上", "60以上", "40以上", "それ以下"],
        "称号": ["🏆 伝説の大賢者", "🧙 大賢者", "⚔ 勇者", "🛡 見習い戦士", "🐣 初心者"]
    })

    st.subheader("💡 今後の拡張案")
    st.markdown("""
    - 過去スコアや称号の履歴グラフ表示  
    - キーワード分析による詳細評価  
    - クイズやゲーム要素の追加でさらに楽しめる仕組み
    """)

with tab[1]:
    st.header("⚔ レポート評価")
    name = st.text_input("あなたの名前")
    report_text = st.text_area("レポート全文を貼ってください", height=250)

    # =========================
    # 評価関数
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
