import streamlit as st

# タイトル
st.title("🍳 簡単レシピ検索アプリ")

# 説明文
st.write("食材を入力すると、その食材を使ったレシピを表示します。")

# 簡易レシピデータ（APIなし）
recipes = {
    "卵": ["卵焼き", "オムライス", "親子丼"],
    "じゃがいも": ["ポテトサラダ", "肉じゃが"],
    "鶏肉": ["唐揚げ", "チキン南蛮"],
    "玉ねぎ": ["オニオンスープ", "カレー"]
}

# 入力欄
ingredient = st.text_input("食材を入力してください（例：卵）")

# ボタン
if st.button("レシピを検索"):
    if ingredient in recipes:
        st.subheader("おすすめレシピ")
        for recipe in recipes[ingredient]:
            st.write("・", recipe)
    else:
        st.warning("該当するレシピが見つかりませんでした。")

