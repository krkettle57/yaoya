from typing import Dict

import streamlit as st
from yaoya.exceptions import YaoyaError
from yaoya.models.user import User
from yaoya.sesseion import StreamlitSessionManager


class BasePage:
    def __init__(self, page_id: str, title: str) -> None:
        self.page_id = page_id
        self.title = title

    def render(self) -> None:
        pass


class MultiPageApp:
    def __init__(self, ssm: StreamlitSessionManager, nav_label: str = "ページ一覧") -> None:
        self.pages: Dict[str, BasePage] = dict()
        self.ssm = ssm
        self.nav_label = nav_label

    def add_page(self, page: BasePage) -> None:
        self.pages[page.page_id] = page

    def render(self) -> None:
        current_user: User = self.ssm.get("user")
        st.sidebar.write(f"ユーザ名: {current_user.name}")
        st.sidebar.write(f"ユーザ種別: {current_user.role}")
        page_id = st.sidebar.selectbox(
            self.nav_label,
            list(self.pages.keys()),
            format_func=lambda page_id: self.pages[page_id].title,
        )
        try:
            self.pages[page_id].render()
        except YaoyaError as e:
            st.error(e)
