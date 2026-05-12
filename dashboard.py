import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình trang Dashboard
st.set_page_config(page_title="Dashboard TMĐT Việt Nam", layout="wide")
st.title("📊 Dashboard Báo Cáo e-Conomy SEA & Thị phần TMĐT")

# --- DỮ LIỆU GIẢ LẬP VÀ TRÍCH XUẤT ---

# 1. Dữ liệu Tăng trưởng GMV (Vĩ mô)
data_gmv = {
    'Năm': ['2022', '2022', '2022', '2022', 
            '2023', '2023', '2023', '2023', 
            '2024', '2024', '2024', '2024', 
            '2025', '2025', '2025', '2025', 
            '2030', '2030', '2030', '2030'],
    'Ngành': ['TMĐT', 'Du lịch', 'Vận tải & Thực phẩm', 'Truyền thông'] * 5,
    'GMV (Tỷ USD)': [14, 2, 3, 4, 
                     16.5, 3, 3.5, 4.5, 
                     20, 4, 4, 5, 
                     24, 5, 5, 6, 
                     40, 10, 10, 10]
}
df_gmv = pd.DataFrame(data_gmv)

# 2. Dữ liệu Bản đồ/Phân bổ khu vực
data_geo = {
    'Tỉnh/Thành': ['TP. Hồ Chí Minh', 'Hà Nội', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ', 'Khác'],
    'Thị phần (%)': [48, 35, 7, 4, 3, 3]
}
df_geo = pd.DataFrame(data_geo)

# 3. Dữ liệu Phễu mua hàng
data_funnel = {
    'Giai đoạn': ['Truy cập Website/App', 'Xem chi tiết sản phẩm', 'Thêm vào giỏ hàng', 'Bắt đầu thanh toán', 'Mua hàng thành công'],
    'Số lượng người dùng': [100000, 60000, 25000, 10000, 4000]
}
df_funnel = pd.DataFrame(data_funnel)

# 4. Dữ liệu Thị phần Sàn TMĐT 2024 (Từ báo cáo YouNet ECI)
data_market_share = {
    'Sàn TMĐT': ['Shopee', 'TikTok Shop', 'Lazada', 'Tiki'],
    'Doanh thu (Nghìn tỷ VNĐ)': [233.32, 94.17, 19.41, 2.9],
    'Thị phần (%)': [66.7, 26.9, 5.5, 0.9],
    'Tăng trưởng so cùng kỳ': ['+41%', '+99%', '-39%', '-43%']
}
df_market_share = pd.DataFrame(data_market_share)


# --- TẠO GIAO DIỆN CÁC TABS ---
# Đã thêm tab thứ 4 cho thị phần các sàn
tab1, tab2, tab3, tab4 = st.tabs(["📈 Tăng trưởng (GMV)", "🗺️ Mức độ tập trung", "🔻 Phễu Mua hàng", "🛒 Thị phần Sàn TMĐT"])

with tab1:
    st.header("Biểu đồ Tăng trưởng Thị phần theo Ngành")
    fig_gmv = px.bar(
        df_gmv, x="Năm", y="GMV (Tỷ USD)", color="Ngành", 
        title="Tăng trưởng GMV Kinh tế số (2022 - 2030)", text_auto='.1f',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_gmv.update_layout(barmode='stack')
    st.plotly_chart(fig_gmv, width='stretch')

with tab2:
    st.header("Bản đồ nhiệt: Phân bổ thị phần theo Tỉnh/Thành")
    fig_geo = px.treemap(
        df_geo, path=['Tỉnh/Thành'], values='Thị phần (%)',
        title="Phân bổ thị phần Kinh tế số theo khu vực", color='Thị phần (%)', color_continuous_scale='Blues'
    )
    fig_geo.update_traces(textinfo="label+value+percent root")
    st.plotly_chart(fig_geo, width='stretch')

with tab3:
    st.header("Phễu Mua hàng (Sales Funnel)")
    fig_funnel = px.funnel(
        df_funnel, x='Số lượng người dùng', y='Giai đoạn',
        title="Hiệu quả chuyển đổi trong hành trình mua hàng", color_discrete_sequence=['#FF9999']
    )
    st.plotly_chart(fig_funnel, width='stretch')

with tab4:
    st.header("Thị phần Giá trị Giao dịch các Sàn TMĐT (Cả năm 2024)")
    st.markdown("**Tổng giá trị giao dịch (GMV): 349,8 Nghìn Tỷ Đồng** *(Nguồn: YouNet ECI)*")
    
    col1, col2 = st.columns([2, 1]) # Chia làm 2 cột: Cột trái vẽ biểu đồ, cột phải hiển thị bảng số liệu
    
    with col1:
        # Biểu đồ Donut (bánh vòng) cho thị phần
        fig_pie = px.pie(
            df_market_share, 
            names='Sàn TMĐT', 
            values='Doanh thu (Nghìn tỷ VNĐ)',
            hole=0.45, # Tạo khoảng trống ở giữa giống trong ảnh
            color='Sàn TMĐT',
            # Gán màu sắc đặc trưng của từng sàn
            color_discrete_map={
                'Shopee': '#ff5722',      # Cam Shopee
                'TikTok Shop': '#000000', # Đen TikTok
                'Lazada': '#0f146d',      # Xanh đậm Lazada
                'Tiki': '#1a73e8'         # Xanh nhạt Tiki
            }
        )
        fig_pie.update_traces(textinfo='percent+label', textposition='inside', textfont_size=14)
        st.plotly_chart(fig_pie, width='stretch')
        
    with col2:
        st.write("### Chi tiết doanh thu & Tăng trưởng")
        st.dataframe(df_market_share, hide_index=True)
        st.info("💡 **FACT:** Sàn Shopee duy trì vị thế dẫn đầu với thị phần GMV > 60% trong suốt 4 quý năm 2024.")
