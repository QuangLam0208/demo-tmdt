import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Cấu hình trang Dashboard
st.set_page_config(page_title="Dashboard TMĐT Việt Nam", layout="wide")
st.title("📊 Dashboard Báo Cáo e-Conomy SEA & Thị phần TMĐT")

# --- DỮ LIỆU ---

# 1. Dữ liệu Tăng trưởng GMV (Vĩ mô) - Đã xóa mốc 2025
data_gmv = {
    'Năm': ['2022', '2022', '2022', '2022', 
            '2023', '2023', '2023', '2023', 
            '2024', '2024', '2024', '2024', 
            '2030', '2030', '2030', '2030'],
    'Ngành': ['TMĐT', 'Du lịch', 'Vận tải & Thực phẩm', 'Truyền thông'] * 4,
    'GMV (Tỷ USD)': [14, 2, 3, 4, 
                     16.5, 3, 3.5, 4.5, 
                     20, 4, 4, 5, 
                     40, 10, 10, 10]
}
df_gmv = pd.DataFrame(data_gmv)

# 2. Dữ liệu Bản đồ/Phân bổ khu vực
data_geo = {
    'Tỉnh/Thành': ['TP. Hồ Chí Minh', 'Hà Nội', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ', 'Khác'],
    'Thị phần (%)': [48, 35, 7, 4, 3, 3]
}
df_geo = pd.DataFrame(data_geo)

# 3. Dữ liệu Hạ tầng người dùng
data_users = {
    'Phân lớp': ['Tổng dân số Việt Nam', 'Người dùng Internet', 'Người mua hàng Online'],
    'Số lượng (Triệu người)': [100, 79, 55],
    'Tỷ lệ thâm nhập': ['100%', '~79% dân số', '~70% người dùng Internet']
}
df_users = pd.DataFrame(data_users)

# 4. Dữ liệu Thị phần Sàn TMĐT 2024
data_market_share = {
    'Sàn TMĐT': ['Shopee', 'TikTok Shop', 'Lazada', 'Tiki'],
    'Doanh thu (Nghìn tỷ VNĐ)': [233.32, 94.17, 19.41, 2.9],
    'Thị phần (%)': [66.7, 26.9, 5.5, 0.9],
    'Tăng trưởng so cùng kỳ': ['+41%', '+99%', '-39%', '-43%']
}
df_market_share = pd.DataFrame(data_market_share)


# --- TẠO GIAO DIỆN CÁC TABS (Đã gom lại còn 4 Tabs) ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tăng trưởng (GMV)", 
    "🗺️ Mức độ tập trung", 
    "👥 Hạ tầng người dùng",
    "🛒 Thị phần Sàn TMĐT"
])

with tab1:
    st.header("Biểu đồ Tăng trưởng Thị phần theo Ngành")
    fig_gmv = px.bar(
        df_gmv, x="Năm", y="GMV (Tỷ USD)", color="Ngành", 
        title="Tăng trưởng GMV Kinh tế số (2022 - 2030)", text_auto='.1f',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_gmv.update_layout(barmode='stack')
    st.plotly_chart(fig_gmv, use_container_width=True)

with tab2:
    st.header("Bản đồ nhiệt: Phân bổ thị phần theo Tỉnh/Thành")
    fig_geo = px.treemap(
        df_geo, path=['Tỉnh/Thành'], values='Thị phần (%)',
        title="Phân bổ thị phần Kinh tế số theo khu vực", color='Thị phần (%)', color_continuous_scale='Blues'
    )
    fig_geo.update_traces(textinfo="label+value+percent root")
    st.plotly_chart(fig_geo, use_container_width=True)

with tab3:
    st.header("Mức độ thâm nhập của Thương mại điện tử tại Việt Nam")
    st.markdown("Nền tảng khách hàng trẻ, am hiểu công nghệ và thói quen mua sắm trực tuyến ngày càng phổ biến.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_users = px.funnel(
            df_users, 
            x='Số lượng (Triệu người)', 
            y='Phân lớp',
            custom_data=['Tỷ lệ thâm nhập'],
            color_discrete_sequence=['#2ecc71'] 
        )
        
        fig_users.update_traces(
            texttemplate="%{y}: <br><b>%{x} Triệu người</b>",
            textposition="inside",
            hovertemplate="<b>%{y}</b><br>Số lượng: %{x} Triệu<br>Tỷ lệ: %{customdata[0]}<extra></extra>"
        )
        
        fig_users.update_layout(yaxis_title=None, xaxis_title="Số lượng (Triệu người)")
        st.plotly_chart(fig_users, use_container_width=True)
        
    with col2:
        st.write("### 📌 Tóm tắt chỉ số")
        st.metric(label="Tổng dân số", value="~100 Triệu")
        st.metric(label="Người dùng Internet", value="~79 Triệu", delta="79% Dân số", delta_color="normal")
        st.metric(label="Người mua hàng Online", value="~55 Triệu", delta="70% ND Internet", delta_color="normal")

with tab4:
    st.header("Thị phần Giá trị Giao dịch các Sàn TMĐT (Cả năm 2024)")
    st.markdown("**Tổng giá trị giao dịch (GMV): 349,8 Nghìn Tỷ Đồng** *(Nguồn: YouNet ECI)*")
    
    col1, col2 = st.columns([2, 1]) 
    
    with col1:
        fig_pie = px.pie(
            df_market_share, names='Sàn TMĐT', values='Doanh thu (Nghìn tỷ VNĐ)', hole=0.45, color='Sàn TMĐT',
            color_discrete_map={'Shopee': '#ff5722', 'TikTok Shop': '#000000', 'Lazada': '#0f146d', 'Tiki': '#1a73e8'}
        )
        fig_pie.update_traces(textinfo='percent+label', textposition='inside', textfont_size=14)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col2:
        st.write("### Chi tiết doanh thu & Tăng trưởng")
        st.dataframe(df_market_share, hide_index=True)
        st.info("💡 **FACT:** Sàn Shopee duy trì vị thế dẫn đầu với thị phần GMV > 60% trong suốt 4 quý năm 2024.")