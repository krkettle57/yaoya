from typing import Dict

import streamlit as st


class BasePage:
    def __init__(self, page_id: str, title: str) -> None:
        self.page_id = page_id
        self.title = title

    def render(self) -> None:
        pass


class MultiPageApp:
    def __init__(self, nav_label: str = "ページ一覧") -> None:
        self.pages: Dict[str, BasePage] = dict()
        self.nav_label = nav_label

    def add_page(self, page: BasePage) -> None:
        self.pages[page.page_id] = page

    def render(self) -> None:
        page_id = st.sidebar.selectbox(
            self.nav_label,
            list(self.pages.keys()),
            format_func=lambda page_id: self.pages[page_id].title,
        )
        self.pages[page_id].render()
