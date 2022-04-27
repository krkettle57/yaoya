import streamlit as st
from yaoya.models.cart import Cart
from yaoya.repositories.user import UserMemoryStore


def login(user_store: UserMemoryStore, user_id: str) -> None:
    user = user_store.get_by_id(user_id)
    st.session_state["user"] = user
    st.session_state["cart"] = Cart(user_id)
