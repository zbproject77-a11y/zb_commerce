import streamlit as st
import pandas as pd
from pathlib import Path  # 1. pathlib 임포트

# @st.cache_data : 데이터 로딩을 한 번만 실행하여 앱 속도를 향상시킵니다.
# 여러 페이지에서 이 함수를 호출해도 데이터는 한 번만 읽어옵니다.
@st.cache_data
def load_all_data(base_path="./data/"):
    """모든 CSV 파일을 불러오고 2023년 데이터로 필터링합니다."""

    SCRIPT_DIR = Path(__file__).resolve().parent
    BASE_PATH = SCRIPT_DIR / "data"
    
    try:
        # 1. 모든 CSV 파일 불러오기
        users = pd.read_csv(BASE_PATH / "users.csv")
        orders = pd.read_csv(BASE_PATH / "orders.csv")
        order_items = pd.read_csv(BASE_PATH / "order_items.csv")
        events = pd.read_csv(BASE_PATH /"events.csv")
        inventory_items = pd.read_csv(BASE_PATH / "inventory_items.csv")
  

        # 필요 없는 데이터프레임은 여기서 주석 처리하거나 삭제해도 됩니다.
        products = pd.read_csv(base_path + "products.csv")
        # distribution_centers = pd.read_csv(base_path + "distribution_centers.csv")

        # 2. 날짜 컬럼을 datetime 형식으로 변환 (안정적인 필터링을 위해)
        for df in [users, orders, order_items, events, inventory_items]:
            df['created_at'] = pd.to_datetime(df['created_at'])

        # 3. 2023년 데이터로 필터링
        users = users[users['created_at'].dt.year == 2023]
        # orders = orders[orders['created_at'].dt.year == 2023]
        order_items = order_items[order_items['created_at'].dt.year == 2023]
        events = events[events['created_at'].dt.year == 2023]
        inventory_items = inventory_items[inventory_items['created_at'].dt.year == 2023]
        # products = products[products['created_at'].dt.year == 2023]
        # distribution_centers = distribution_centers[distribution_centers['created_at'].dt.year == 2023]


        # 4. 여러 데이터프레임을 딕셔너리 형태로 반환
        return {
            "users": users,
            "orders": orders,
            "order_items": order_items,
            "events": events,
            "inventory_items": inventory_items,
            "products": products,
            # "distribution_centers": distribution_centers
        }
    
    except FileNotFoundError as e:
        st.error(f"데이터 파일 로딩 중 오류 발생: {e}")

        return None

