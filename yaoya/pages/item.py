import streamlit as st
from yaoya.models.cart import Cart
from yaoya.repositories.item import ItemMemoryStore
from yaoya.usecases.item import add_cart


def item_page(cart: Cart, item_store: ItemMemoryStore) -> None:
    st.title("商品")
    message_box = st.empty()

    # 商品テーブルの表示
    col_size = [1, 2, 2, 2, 3, 2]
    columns = st.columns(col_size)
    headers = ["No", "名前", "価格", "生産地", "数量", ""]
    for col, field_name in zip(columns, headers):
        col.write(field_name)

    for index, row in item_store.df.iterrows():
        (
            col1,
            col2,
            col3,
            col4,
            col5,
            col6,
        ) = st.columns(col_size)
        item_id = row["item_id"]
        col1.write(index + 1)
        col2.write(row["name"])
        col3.write(row["price"])
        col4.write(row["producing_area"])
        quantity = col5.number_input("", key=item_id, min_value=1, max_value=9, step=1)
        button_col = col6.empty()

        # カート追加
        if button_col.button("追加", key=item_id):
            add_cart(item_store, cart, item_id, quantity, tax_ratio=0.1)
            message_box.info("カートに追加しました")
