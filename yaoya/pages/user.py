import streamlit as st
from yaoya.repositories.user import UserMemoryStore
from yaoya.usecases.user import login


def user_page(user_store: UserMemoryStore) -> None:
    st.title("ユーザ")
    message_box = st.empty()

    # ユーザテーブルの表示
    col_size = [1, 2, 2, 2, 5, 2, 3]
    columns = st.columns(col_size)
    headers = ["No", "ユーザID", "名前", "生年月日", "メールアドレス", "種別", ""]
    for col, field_name in zip(columns, headers):
        col.write(field_name)

    for index, row in user_store.df.iterrows():
        user_id = row["user_id"]
        user_name = row["name"]
        (
            col1,
            col2,
            col3,
            col4,
            col5,
            col6,
            col7,
        ) = st.columns(col_size)
        col1.write(index + 1)
        col2.write(user_id)
        col3.write(row["name"])
        col4.write(row["birthday"])
        col5.write(row["email"])
        col6.write(row["role"])
        button_col = col7.empty()

        # ログイン処理
        if button_col.button("ログイン", key=user_id):
            login(user_store, user_id)
            message_box.info(f"{user_name} でログインしました。")
