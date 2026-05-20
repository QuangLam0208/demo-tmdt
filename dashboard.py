import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. CẤU HÌNH TRANG & GIAO DIỆN CHUNG
st.set_page_config(page_title="Dashboard TMĐT Việt Nam", page_icon="🛒", layout="wide")

# CSS Tuỳ chỉnh để làm đẹp giao diện (Thẻ Metric, Font chữ, Background)
st.markdown("""
<style>
    /* Tuỳ chỉnh thẻ Metric */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e6ed;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    /* Ẩn bớt viền dư thừa của tab */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard Báo Cáo e-Conomy SEA & Thị phần TMĐT")
st.markdown("---")

# 2. CHUẨN BỊ DỮ LIỆU (Giữ nguyên cấu trúc)
data_gmv = {
    'Năm': ['2022']*4 + ['2023']*4 + ['2024']*4 + ['2025']*4 + ['2030']*4,
    'Ngành': ['TMĐT', 'Du lịch', 'Vận tải & Thực phẩm', 'Truyền thông'] * 5,
    'GMV (Tỷ USD)': [14, 2, 3, 4, 16.5, 3, 3.5, 4.5, 20, 4, 4, 5, 24, 5, 5, 6, 40, 10, 10, 10]
}
df_gmv = pd.DataFrame(data_gmv)

data_geo = {
    'Tỉnh/Thành': ['TP. Hồ Chí Minh', 'Hà Nội', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ', 'Khác'],
    'Thị phần (%)': [48, 35, 7, 4, 3, 3]
}
df_geo = pd.DataFrame(data_geo)

data_b2c = {
    'Năm': ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
    'Quy mô (tỷ USD)': [2.97, 4.07, 5.0, 6.2, 8.06, 10.08, 11.8, 13.7, 16.4, 20.5, 25.0],
    'Tốc độ tăng trưởng (%)': [None, 37, 23, 24, 30, 25, 18, 16, 20, 25, 30] 
}
df_b2c = pd.DataFrame(data_b2c)

data_market_share = {
    'Sàn TMĐT': ['Shopee', 'TikTok Shop', 'Lazada', 'Tiki'],
    'Doanh thu (Nghìn tỷ VNĐ)': [233.32, 94.17, 19.41, 2.9],
    'Thị phần (%)': [66.7, 26.9, 5.5, 0.9],
    'Tăng trưởng so cùng kỳ': ['+41%', '+99%', '-39%', '-43%']
}
df_market_share = pd.DataFrame(data_market_share)

data_users = {
    'Phân lớp': ['Tổng dân số Việt Nam', 'Người dùng Internet', 'Người mua hàng Online'],
    'Số lượng (Triệu người)': [100, 78, 55],
    'Tỷ lệ thâm nhập': ['100%', '~79% dân số', '~70% người dùng Internet']
}
df_users = pd.DataFrame(data_users)

# 3. TẠO GIAO DIỆN CÁC TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Tăng trưởng (GMV)", 
    "🗺️ Mức độ tập trung", 
    "📊 Tăng trưởng B2C", 
    "👥 Hạ tầng",
    "🛒 Thị phần Sàn TMĐT"
])

# Cấu hình chung cho hover label
hover_style = dict(bgcolor="white", font_size=14, font_family="Arial")

with tab1:
    st.subheader("Biểu đồ Tăng trưởng GMV Kinh tế số theo Ngành")
    fig_gmv = px.bar(
        df_gmv, x="Năm", y="GMV (Tỷ USD)", color="Ngành", 
        text_auto='.1f', color_discrete_sequence=px.colors.qualitative.Pastel
    )
    # UI Nâng cấp: Chế độ hover gộp (x unified), viền mỏng tạo khối
    fig_gmv.update_traces(marker_line_width=1, marker_line_color="black", opacity=0.9)
    fig_gmv.update_layout(
        barmode='stack', hovermode='x unified', hoverlabel=hover_style,
        plot_bgcolor='rgba(0,0,0,0)', yaxis_gridcolor='lightgray'
    )
    st.plotly_chart(fig_gmv, use_container_width=True)

with tab2:
    st.subheader("Bản đồ nhiệt: Phân bổ thị phần theo Tỉnh/Thành")
    fig_geo = px.treemap(
        df_geo, path=['Tỉnh/Thành'], values='Thị phần (%)',
        color='Thị phần (%)', color_continuous_scale='Blues'
    )
    # UI Nâng cấp: Bo góc, hiệu ứng hover tooltip sắc nét hơn
    fig_geo.update_traces(
        textinfo="label+value+percent root",
        hovertemplate="<b>%{label}</b><br>Thị phần: %{value}%<extra></extra>",
        marker=dict(line=dict(color='white', width=2))
    )
    fig_geo.update_layout(hoverlabel=hover_style, margin=dict(t=20, l=0, r=0, b=0))
    st.plotly_chart(fig_geo, use_container_width=True)

with tab3:
    st.subheader("Tốc độ tăng trưởng thương mại điện tử B2C (2014-2024)")
    
    fig_b2c = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_b2c.add_trace(
        go.Bar(
            x=df_b2c['Năm'], y=df_b2c['Quy mô (tỷ USD)'],
            name="Quy mô TMĐT", marker_color='#4CAF50', 
            text=df_b2c['Quy mô (tỷ USD)'], textposition='inside',
            marker_line_color='rgba(0,0,0,0.2)', marker_line_width=1, opacity=0.85
        ), secondary_y=False,
    )

    fig_b2c.add_trace(
        go.Scatter(
            x=df_b2c['Năm'], y=df_b2c['Tốc độ tăng trưởng (%)'],
            name="Tốc độ tăng trưởng", mode='lines+markers+text',
            marker=dict(color='#E53935', size=10, line=dict(width=2, color='white')), 
            line=dict(color='#E53935', width=3, shape='spline'), # shape='spline' tạo đường cong mềm mại
            text=df_b2c['Tốc độ tăng trưởng (%)'].apply(lambda x: f"{int(x)}%" if pd.notna(x) else ""),
            textposition='top center', textfont=dict(color='#E53935', weight='bold')
        ), secondary_y=True,
    )

    # UI Nâng cấp: x unified hover, nền trắng, xoá viền dư
    fig_b2c.update_layout(
        plot_bgcolor='white', margin=dict(t=40, b=40),
        hovermode="x unified", hoverlabel=hover_style,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_b2c.update_yaxes(title_text="Quy mô (Tỷ USD)", secondary_y=False, showgrid=True, gridcolor='#f0f0f0')
    fig_b2c.update_yaxes(title_text="Tăng trưởng (%)", secondary_y=True, showgrid=False)
    
    st.plotly_chart(fig_b2c, use_container_width=True)

with tab4:
    st.subheader("Mức độ thâm nhập của Thương mại điện tử")
    st.markdown("Nền tảng khách hàng trẻ, am hiểu công nghệ và thói quen mua sắm trực tuyến ngày càng phổ biến.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_users = px.funnel(
            df_users, x='Số lượng (Triệu người)', y='Phân lớp',
            custom_data=['Tỷ lệ thâm nhập'], 
            color_discrete_sequence=['#3b82f6'] # Đổi màu xanh dương hiện đại
        )
        # UI Nâng cấp: Hover mượt mà
        fig_users.update_traces(
            texttemplate="%{y}: <br><b>%{x} Triệu</b>",
            textposition="inside",
            hovertemplate="<b>%{y}</b><br>Số lượng: %{x} Triệu<br>Tỷ lệ: %{customdata[0]}<extra></extra>",
            opacity=0.9
        )
        fig_users.update_layout(yaxis_title=None, hoverlabel=hover_style, plot_bgcolor='white')
        st.plotly_chart(fig_users, use_container_width=True)
        
    with col2:
        st.write("### 📌 Tóm tắt chỉ số")
        st.metric(label="👥 Tổng dân số", value="100 Triệu")
        st.metric(label="🌐 Người dùng Internet", value="78 Triệu", delta="79% Dân số", delta_color="normal")
        st.metric(label="📦 Người mua hàng Online", value="55 Triệu", delta="70% ND Internet", delta_color="normal")

with tab5:
    st.subheader("Thị phần Giá trị Giao dịch các Sàn TMĐT (2024)")
    st.markdown("**Tổng GMV: 349,8 Nghìn Tỷ Đồng** *(Nguồn: YouNet ECI)*")
    
    col1, col2 = st.columns([1.5, 1]) 
    
    with col1:
        fig_pie = px.pie(
            df_market_share, names='Sàn TMĐT', values='Doanh thu (Nghìn tỷ VNĐ)', hole=0.45,
            color='Sàn TMĐT',
            color_discrete_map={'Shopee': '#FF5722', 'TikTok Shop': '#000000', 'Lazada': '#0F146D', 'Tiki': '#1A73E8'},
            custom_data=['Tăng trưởng so cùng kỳ']
        )
        # UI Nâng cấp: Hiệu ứng nổi bật (pull) nhẹ, thêm viền trắng, hover xịn
        fig_pie.update_traces(
            textinfo='percent+label', textposition='outside', textfont_size=14,
            marker=dict(line=dict(color='#FFFFFF', width=2)),
            hovertemplate="<b>Sàn: %{label}</b><br>Doanh thu: %{value} Nghìn tỷ<br>Thị phần: %{percent}<br>Tăng trưởng: %{customdata[0]}<extra></extra>",
            pull=[0.05, 0, 0, 0] # Làm nổi bật Shopee
        )
        fig_pie.update_layout(hoverlabel=hover_style, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col2:
        st.write("### 📈 Chi tiết doanh thu")
        st.dataframe(
            df_market_share.style.format({
                'Doanh thu (Nghìn tỷ VNĐ)': "{:.2f}",
                'Thị phần (%)': "{:.1f}%"
            }), 
            hide_index=True, use_container_width=True
        )
        st.info("💡 **FACT:** Shopee duy trì vị thế dẫn đầu với thị phần GMV > 60% trong suốt 4 quý năm 2024.")