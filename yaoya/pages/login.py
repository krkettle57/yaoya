import streamlit as st
from yaoya.pages.base import BasePage
from yaoya.repositories.user import UserMemoryRepository
from yaoya.sesseion import StreamlitSessionManager
from yaoya.usecases.user import login


class LoginPage(BasePage):
    def __init__(self, ssm: StreamlitSessionManager) -> None:
        self.title = "ログイン"
        self.page_id = "login"
        self.ssm = ssm

    def render(self) -> None:
        user_repo: UserMemoryRepository = self.ssm.get("user_repo")

        st.title("ユーザ")
        message_box = st.empty()

        # ユーザテーブルの表示
        col_size = [1, 2, 2, 2, 5, 2, 3]
        columns = st.columns(col_size)
        headers = ["No", "ユーザID", "名前", "生年月日", "メールアドレス", "種別", ""]
        for col, field_name in zip(columns, headers):
            col.write(field_name)

        for index, user in enumerate(user_repo.get_all()):
            user_id = user.user_id
            user_name = user.name
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
            col3.write(user.name)
            col4.write(user.birthday)
            col5.write(user.email)
            col6.write(user.role)
            button_col = col7.empty()

            # ログイン処理
            if button_col.button("ログイン", key=user_id):
                login(user_repo, user_id)
                message_box.info(f"{user_name} でログインしました。")
