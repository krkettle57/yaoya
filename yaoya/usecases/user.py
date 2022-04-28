import streamlit as st
from yaoya.models.cart import Cart
from yaoya.repositories.user import UserMemoryRepository


def login(user_repo: UserMemoryRepository, user_id: str) -> None:
    user = user_repo.get_by_id(user_id)
    st.session_state["user"] = user
    st.session_state["cart"] = Cart(user_id)
