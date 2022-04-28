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
        # 注文テーブルの表示
        st.subheader("注文")
        col_size = [1, 2, 2, 2, 4]
        columns = st.columns(col_size)
        headers = ["No", "注文番号", "ユーザID", "合計", "注文日付"]
        for col, field_name in zip(columns, headers):
            col.write(field_name)

        for index, order in enumerate(orders):
            (
                col1,
                col2,
                col3,
                col4,
                col5,
            ) = st.columns(col_size)
            col1.write(index + 1)
            col2.write(order.order_id[-8:])
            col3.write(order.user_id)
            col4.write(order.total_price)
            col5.write(order.ordered_at.strftime("%Y-%m-%d %H:%M:%S"))

        # 注文詳細テーブルの表示
        st.subheader("注文詳細")
        col_size = [1, 2, 2, 2, 2, 2, 2]
        columns = st.columns(col_size)
        headers = ["No", "注文番号", "注文No", "商品ID", "単価", "数量", "小計"]
        for col, field_name in zip(columns, headers):
            col.write(field_name)

        for order in orders:
            for index, order_detail in enumerate(order.details):
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
                col2.write(order.order_id[-8:])
                col3.write(order_detail.order_no)
                col4.write(order_detail.item_id[-8:])
                col5.write(order_detail.unit_price)
                col6.write(order_detail.quantity)
                col7.write(order_detail.subtotal_price)
