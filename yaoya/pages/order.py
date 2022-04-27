import streamlit as st
from yaoya.repositories.order import OrderDetailMemoryStore, OrderMemoryStore


def order_page(order_store: OrderMemoryStore, order_detail_store: OrderDetailMemoryStore) -> None:
    show_order_df = order_store.df.copy()
    show_order_df["order_id"] = show_order_df["order_id"].apply(lambda x: x[-8:])

    st.subheader("注文")
    st.dataframe(show_order_df)

    show_order_detail_df = order_detail_store.df.copy()
    show_order_detail_df["order_id"] = show_order_detail_df["order_id"].apply(lambda x: x[-8:])

    st.subheader("注文詳細")
    st.dataframe(show_order_detail_df)
