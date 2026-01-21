import streamlit as st

st.set_page_config(page_title="レポート構成アドバイザー", page_icon="📝")

st.title("📝 レポート構成アドバイザー")
st.write("レポートのテーマを入力すると、基本的な構成案と注意点を提示します。")

theme = st.text_input("レポートのテーマを入力してください")

if st.button("構成案を作成する") and theme:
    st.subheader("📄 レポート構成案")

    st.markdown("### ① はじめに（導入）")
    st.write(f"- テーマ「{theme}」を選んだ理由を書く")
    st.write("- 本レポートで何を明らかにするのかを示す")

    st.markdown("### ② 背景・基礎知識")
    st.write("- テーマに関する基本的な用語や考え方を説明")
    st.write("- 参考文献や資料を簡潔にまとめる")

    st.markdown("### ③ 本論・分析")
    st.write("- テーマについての主張や分析を詳しく述べる")
    st.write("- 図や具体例があれば効果的")

    st.markdown("### ④ 考察")
    st.write("- 分析結果から分かったことを整理する")
    st.write("- 自分の意見や解釈を明確に書く")

    st
