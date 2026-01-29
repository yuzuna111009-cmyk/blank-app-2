import streamlit as st
from supabase import create_client
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import urllib.parse

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
# Wikipedia検索＋本文取得（超安定版）
# -----------------------------
def get_wiki_summary(theme):
    try:
        # ① 検索API
        search_url = "https://ja.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": theme,
            "format": "json"
        }

        search_response = requests.get(search_url, params=search_params, timeout=5)
        search_data = search_response.json()

        if not search_data.get("query", {}).get("search"):
            return None

        page_title = search_data["query"]["sear]()
