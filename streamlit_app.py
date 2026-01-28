from supabase import create_client, Client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)
if st.button("構成案を作成する") and theme:
    # --- Supabase に利用データを保存 ---
    supabase.table("report_usage").insert({
        "theme": theme,
        "report_type": report_type
    }).execute()

    st.subheader("📄 レポート構成案（文字数目安つき）")
    ...

import streamlit as st

st.set_page_config(page_title="レポート構成アドバイザー", page_icon="📝")

st.title("📝 レポート構成アドバイザー")
st.write("レポートのテーマと種類を選ぶと、構成案・テンプレート・注意点を提示します。")

# --- 入力 ---
theme = st.text_input("レポートのテーマを入力してください")

report_type = st.selectbox(
    "レポートの種類を選んでください",
    ["調査レポート", "考察レポート", "実験・実習レポート"]
)

if st.button("構成案を作成する") and theme:
    st.subheader("📄 レポート構成案（文字数目安つき）")

    st.markdown("### ① はじめに（200〜300字）")
    st.write(f"- テーマ「{theme}」を選んだ理由を書く")
    st.write("- 本レポートの目的を明確に示す")
    st.write("❌ NG例：「とても興味を持ったから選んだ」")

    st.markdown("### ② 背景・基礎知識（400〜600字）")
    st.write("- 用語や理論を説明する")
    st.write("- 参考文献を用いて説明する")
    st.write("❌ NG例：出典のない説明、Wikipediaだけを参考にする")

    if report_type == "調査レポート":
        st.markdown("### ③ 調査内容・分析（800〜1200字）")
        st.write("- 調査方法と結果を客観的に示す")
        st.write("❌ NG例：結果と感想を混ぜて書く")

    elif report_type == "考察レポート":
        st.markdown("### ③ 本論・考察（800〜1200字）")
        st.write("- 主張と根拠をセットで書く")
        st.write("❌ NG例：「〜だと思う」だけで根拠がない")

    else:
        st.markdown("### ③ 実験・実習内容（600〜1000字）")
        st.write("- 目的・方法・結果を分けて書く")
        st.write("❌ NG例：手順が曖昧、結果が文章だけ")

    st.markdown("### ④ まとめ・結論（200〜300字）")
    st.write("- 全体を簡潔に振り返る")
    st.write("❌ NG例：新しい内容を書く")

    st.divider()

    # =========================
    # 🥇 構成テンプレ（コピー用）
    # =========================
    st.subheader("📋 コピペ用レポートテンプレート")

    template = f"""【はじめに】
（テーマ：{theme}）
（目的を書く）

【背景・基礎知識】
（用語・理論・先行研究）

【本論】
（分析・考察を書く）

【まとめ】
（結論・今後の課題）
"""

    st.text_area(
        "以下をコピーして Word や Google Docs に貼り付けてください",
        template,
        height=220
    )

    st.divider()

    # =========================
    # 🥈 提出前チェックリスト
    # =========================
    st.subheader("✅ 提出前チェックリスト")

    st.checkbox("テーマと目的が導入に書かれている")
    st.checkbox("主張と根拠が対応している")
    st.checkbox("文字数条件を満たしている")
    st.checkbox("参考文献・出典を明記している")
    st.checkbox("誤字・脱字を確認した")

    st.divider()

    # =========================
    # 🥉 具体的NG表現例
    # =========================
    st.subheader("⚠ よくあるNG表現と言い換え例")

    st.markdown("""
❌ **とても重要だと思った**  
✅ **〇〇の点から重要である**

❌ **すごく影響がある**  
✅ **△△に対して大きな影響を与えている**

❌ **なんとなくそう感じた**  
✅ **データや事例からそのように考えられる**
""")

    st.info("※ この構成は一例です。授業の指示に応じて調整してください。")
