import pandas as pd
import streamlit as st
from yaoya.models.user import User
from yaoya.pages.base import BasePage
from yaoya.repositories.order import OrderMemoryRepository
from yaoya.sesseion import StreamlitSessionManager


class OrderListPage(BasePage):
    def __init__(self, ssm: StreamlitSessionManager) -> None:
        self.title = "注文一覧"
        self.page_id = "order_list"
        self.ssm = ssm

    def render(self) -> None:
        order_repo: OrderMemoryRepository = self.ssm.get("order_repo")
        current_user: User = self.ssm.get("user")

        st.title(self.title)
        if current_user.role != "admin":
            st.warning("管理者専用ページです")
            return

        orders = order_repo.get_all()
        show_order_df = pd.DataFrame(
            [
                {
                    "order_id": order.order_id[-8:],
                    "user_id": order.user_id,
                    "total_price": order.total_price,
                    "ordered_at": order.ordered_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for order in orders
            ]
        )

        st.subheader("注文")
        st.dataframe(show_order_df)

        show_order_detail_df = pd.DataFrame(
            [
                {
                    "order_no": order_detail.order_no,
                    "item_id": order_detail.item_id[-8:],
                    "unit_price": order_detail.unit_price,
                    "quantity": order_detail.quantity,
                    "subtotal_price": order_detail.subtotal_price,
                }
                for order in orders
                for order_detail in order.details
            ]
        )

        st.subheader("注文詳細")
        st.dataframe(show_order_detail_df)
