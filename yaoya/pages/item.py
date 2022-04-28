import streamlit as st
from yaoya.models.cart import Cart
from yaoya.repositories.item import ItemMemoryRepository
from yaoya.usecases.item import add_cart


def item_page(cart: Cart, item_repo: ItemMemoryRepository) -> None:
    st.title("商品")
    message_box = st.empty()

    # 商品テーブルの表示
    col_size = [1, 2, 2, 2, 3, 2]
    columns = st.columns(col_size)
    headers = ["No", "名前", "価格", "生産地", "数量", ""]
    for col, field_name in zip(columns, headers):
        col.write(field_name)

    for index, item in enumerate(item_repo.get_all()):
        (
            col1,
            col2,
            col3,
            col4,
            col5,
            col6,
        ) = st.columns(col_size)
        col1.write(index + 1)
        col2.write(item.name)
        col3.write(item.price)
        col4.write(item.producing_area)
        quantity = col5.number_input("", key=item.item_id, min_value=1, max_value=9, step=1)
        button_col = col6.empty()

        # カート追加
        if button_col.button("追加", key=item.item_id):
            add_cart(item_repo, cart, item.item_id, quantity)
            message_box.info("カートに追加しました")
