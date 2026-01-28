import streamlit as st
from supabase import create_client, Client
from datetime import datetime

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
# ボタン処理
# -----------------------------
if st.button("構成案を作成する", key="create_outline") and theme:

    # Supabase に保存
    supabase.table("report_logs").insert({
        "theme": theme,
        "report_type": report_type,
        "created_at": datetime.now().isoformat()
    }).execute()

    # -----------------------------
    # 出力
    # -----------------------------
    st.subheader("📄 レポート構成案")

    st.markdown("### ① はじめに（導入）")
    st.write(f"- テーマ「{theme}」を選んだ理由を書く")
    st.write("- レポートの目的・問題意識を明確にする")
    st.write("【文字数目安】全体の10〜15%")

    st.markdown("### ② 背景・基礎知識")
    st.write("- 基本用語や理論を整理する")
    st.write("- 信頼できる資料を引用する")
    st.write("【文字数目安】20〜25%")

    st.markdown("### ③ 本論・分析")
    st.write("- データ・具体例を用いて論じる")
    st.write("- 図表があれば効果的")
    st.write("【文字数目安】40〜50%")

    st.markdown("### ④ 考察")
    st.write("- 分析結果から分かることを整理")
    st.write("- 自分の意見を論理的に述べる")
    st.write("【文字数目安】15〜20%")

    st.markdown("### ⑤ まとめ")
    st.write("- 全体の要点を簡潔に振り返る")
    st.write("- 今後の課題を示す")

    # -----------------------------
    # NG例
    # -----------------------------
    st.subheader("❌ よくあるミス（NG例）")
    st.write("- 感想だけで終わっている")
    st.write("- 根拠や資料が示されていない")
    st.write("- 話題が途中で変わる")

    st.subheader("🚫 具体的NG表現例")
    st.write("×「なんとなく重要だと思った」")
    st.write("×「すごいと感じた」")
    st.write("→ 理由・根拠を必ず書く")

    # -----------------------------
    # コピー用テンプレ
    # -----------------------------
    st.subheader("📋 構成テンプレ（コピー用）")
    template = f"""
① はじめに
・テーマ：{theme}
・目的：

② 背景・基礎知識

③ 本論・分析

④ 考察

⑤ まとめ
"""
    st.code(template)

    # -----------------------------
    # チェックリスト
    # -----------------------------
    st.subheader("✅ 提出前チェックリスト")
    st.checkbox("テーマと内容が一致している")
    st.checkbox("根拠・資料が示されている")
    st.checkbox("自分の考察が書かれている")
    st.checkbox("誤字脱字を確認した")

# -----------------------------
# フッター
# -----------------------------
st.caption("© Report Structure Advisor with Supabase")
