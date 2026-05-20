import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Cấu hình trang Dashboard
st.set_page_config(page_title="Dashboard TMĐT Việt Nam", layout="wide")
st.title("📊 Dashboard Báo Cáo e-Conomy SEA & Thị phần TMĐT")

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

# 3. Dữ liệu Tốc độ tăng trưởng B2C 
data_b2c = {
    'Năm': ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
    'Quy mô (tỷ USD)': [2.97, 4.07, 5.0, 6.2, 8.06, 10.08, 11.8, 13.7, 16.4, 20.5, 25.0],
    'Tốc độ tăng trưởng (%)': [None, 37, 23, 24, 30, 25, 18, 16, 20, 25, 30] 
}
df_b2c = pd.DataFrame(data_b2c)

# 4. Dữ liệu Thị phần Sàn TMĐT 2024
data_market_share = {
    'Sàn TMĐT': ['Shopee', 'TikTok Shop', 'Lazada', 'Tiki'],
    'Doanh thu (Nghìn tỷ VNĐ)': [233.32, 94.17, 19.41, 2.9],
    'Thị phần (%)': [66.7, 26.9, 5.5, 0.9],
    'Tăng trưởng so cùng kỳ': ['+41%', '+99%', '-39%', '-43%']
}
df_market_share = pd.DataFrame(data_market_share)

# 5. Dữ liệu Hạ tầng người dùng
data_users = {
    'Phân lớp': ['Tổng dân số Việt Nam', 'Người dùng Internet', 'Người mua hàng Online'],
    'Số lượng (Triệu người)': [100, 78, 55],
    'Tỷ lệ thâm nhập': ['100%', '~79% dân số', '~70% người dùng Internet']
}
df_users = pd.DataFrame(data_users)


# --- TẠO GIAO DIỆN CÁC TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Tăng trưởng (GMV)", 
    "🗺️ Mức độ tập trung", 
    "📊 Tăng trưởng B2C", 
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
    st.header("Tốc độ tăng trưởng thương mại điện tử B2C từ 2014-2024")
    
    fig_b2c = make_subplots(specs=[[{"secondary_y": True}]])

    fig_b2c.add_trace(
        go.Bar(
            x=df_b2c['Năm'], y=df_b2c['Quy mô (tỷ USD)'],
            name="Quy mô TMĐT (tỷ USD)", marker_color='#6ebf33', 
            text=df_b2c['Quy mô (tỷ USD)'], textposition='inside'
        ),
        secondary_y=False,
    )

    fig_b2c.add_trace(
        go.Scatter(
            x=df_b2c['Năm'], y=df_b2c['Tốc độ tăng trưởng (%)'],
            name="Tốc độ tăng trưởng (%)", mode='lines+markers+text',
            marker=dict(color='#b31217', size=8), line=dict(color='#b31217', width=2),
            text=df_b2c['Tốc độ tăng trưởng (%)'].apply(lambda x: f"{int(x)}" if pd.notna(x) else ""),
            textposition='top center', textfont=dict(color='#b31217', weight='bold')
        ),
        secondary_y=True,
    )

    fig_b2c.update_layout(
        plot_bgcolor='white', margin=dict(t=40, b=40),
        legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5)
    )
    fig_b2c.update_yaxes(title_text="Quy mô (Tỷ USD)", secondary_y=False, range=[0, 30], showgrid=True, gridcolor='lightgray', dtick=5)
    fig_b2c.update_yaxes(title_text="Tốc độ tăng trưởng (%)", secondary_y=True, range=[0, 45], showgrid=False, dtick=10)
    
    st.plotly_chart(fig_b2c, use_container_width=True)

with tab4:
    st.header("Mức độ thâm nhập của Thương mại điện tử tại Việt Nam")
    st.markdown("Nền tảng khách hàng trẻ, am hiểu công nghệ và thói quen mua sắm trực tuyến ngày càng phổ biến.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Sử dụng biểu đồ phễu (Funnel) để thể hiện sự thu hẹp tập khách hàng
        fig_users = px.funnel(
            df_users, 
            x='Số lượng (Triệu người)', 
            y='Phân lớp',
            custom_data=['Tỷ lệ thâm nhập'], # Đưa thêm tỷ lệ vào để hiển thị khi hover
            color_discrete_sequence=['#2ecc71'] # Màu xanh lá hiện đại
        )
        
        # Tùy chỉnh hiển thị text trên biểu đồ
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
        st.metric(label="Người dùng Internet", value="~78 Triệu", delta="79% Dân số", delta_color="normal")
        st.metric(label="Người mua hàng Online", value="~55 Triệu", delta="70% ND Internet", delta_color="normal")

with tab5:
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
