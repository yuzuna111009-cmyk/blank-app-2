import streamlit as st

st.set_page_config(page_title="📚 レポートRPG", page_icon="🧙")

st.title("📚 レポートRPG README")

readme_text = """
# 📚 レポートRPG

**概要**  
Streamlit を利用した、レポート全文をAI風に評価して**スコアと称号**を付与するWebアプリです。  
楽しみながら自分のレポートを客観的に確認でき、今日のランキングで他の挑戦者と競えます。

---

## 🔗 アプリURL

[レポートRPG](https://your-app-url.streamlit.app/)  
※スリープ状態のときは青色の起動ボタンで開始

---

## 🌟 主な機能

- **レポート全文評価**  
  レポート内容を分析し、簡易AI風ロジックでスコア化
- **称号付与**  
  スコアに応じて称号を自動で表示
- **今日のランキング表示**  
  今日投稿されたレポートのスコアランキングを表示
- **Supabase 連携**  
  名前・スコア・称号を永続的に保存
- **簡易操作UI**  
  名前とレポートを入力 → ボタンで評価 → スコア表示

---

## ⚔ スコアと称号

| スコア | 称号 |
| ------ | ---- |
| 90以上 | 🏆 伝説の大賢者 |
| 75以上 | 🧙 大賢者 |
| 60以上 | ⚔ 勇者 |
| 40以上 | 🛡 見習い戦士 |
| それ以下 | 🐣 初心者 |

---

## 🛠 使用技術

- **Frontend/UI**: Streamlit  
- **Backend/DB**: Supabase（PostgreSQL）  
- **Language**: Python  
- **Hosting**: Streamlit Cloud  

---

## 💡 今後の拡張案

- 過去スコアや称号の履歴グラフ表示
- キーワード分析による詳細評価
- クイズやゲーム要素の追加でさらに楽しめる仕組み

---

© Report RPG
"""

st.markdown(readme_text)
