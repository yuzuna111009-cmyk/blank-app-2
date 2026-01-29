import streamlit as st
from supabase import create_client
from datetime import datetime, timezone
import random
import pandas as pd

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
tabs = st.tabs(["🏠 アプリ説明", "⚔ レポート評価"])

with tabs[0]:
    st.header("📚 レポートRPG")
    st.markdown("""
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
    score_table = pd.DataFrame({
        "スコア": ["90]()
