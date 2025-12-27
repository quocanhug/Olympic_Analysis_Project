import streamlit as st
import pandas as pd
import plotly.express as px
import modules.analysis as ana  # Import file analysis từ thư mục modules

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Olympic Data Analysis",
    page_icon="🏅",
    layout="wide"
)


# --- HÀM LOAD DỮ LIỆU (CACHE ĐỂ CHẠY NHANH HƠN) ---
@st.cache_data
def load_and_clean_data():
    # Đọc dữ liệu
    try:
        df = pd.read_csv('data/athlete_events.csv')
    except FileNotFoundError:
        st.error("Lỗi: Không tìm thấy file 'data/athlete_events.csv'. Vui lòng kiểm tra lại đường dẫn.")
        return None

    # Áp dụng các hàm làm sạch từ analysis.py ngay khi load
    df = ana.clean_team_name(df)
    df = ana.clean_event_name(df)
    df = ana.extract_nickname(df)
    return df


# Load dữ liệu
df = load_and_clean_data()

if df is not None:
    # --- THANH SIDEBAR (MENU BÊN TRÁI) ---
    st.sidebar.title("Menu Phân Tích")
    options = st.sidebar.radio("Chọn chức năng:",
                               ["Tổng quan dữ liệu",
                                "Bộ lọc nâng cao",
                                "Thống kê huy chương",
                                "Phân tích giới tính & độ tuổi",
                                "Thể chất & Môn thi đấu",
                                "Thế mạnh Quốc gia"])

    st.title("🏅 Phân Tích Dữ Liệu Olympic (1896 - 2016)")
    st.markdown("---")

    # =========================================================================
    # 1. TỔNG QUAN DỮ LIỆU
    # =========================================================================
    # =========================================================================
    # 1. TỔNG QUAN DỮ LIỆU (Đã sửa lỗi hiển thị & thêm thanh cuộn)
    # =========================================================================
    if options == "Tổng quan dữ liệu":
        st.header("1. Xem dữ liệu gốc & Đã làm sạch")
        st.write(f"Kích thước dữ liệu: **{df.shape[0]}** dòng, **{df.shape[1]}** cột.")

        st.subheader("Bảng dữ liệu chi tiết:")

        # SỬA LỖI Ở ĐÂY:
        # 1. Bỏ .head(10) để hiển thị toàn bộ dữ liệu
        # 2. Thêm height=600 để tạo khung cao, tự động có thanh cuộn dọc
        # 3. use_container_width=True để bảng giãn rộng full màn hình
        st.dataframe(df, height=600, use_container_width=True)
        st.info("Dữ liệu đã được tự động làm sạch cột Team, Event và tách Nickname bằng module 'analysis.py'.")
    # =========================================================================
    # 2. BỘ LỌC NÂNG CAO (FULL TÍNH NĂNG)
    # =========================================================================
    elif options == "Bộ lọc nâng cao":
        st.header("2. Công cụ lọc dữ liệu đa năng")

        # Chia giao diện thành 3 cột cho gọn
        col1, col2, col3 = st.columns(3)

        # --- CỘT 1: LỌC CHỈ SỐ (SỐ) ---
        with col1:
            st.subheader(" Chỉ số cơ thể & độ tuổi")
            f_year = st.slider("Từ năm:", 1896, 2016, 1896)
            f_age = st.number_input("Tuổi (tối thiểu):", min_value=0, value=0, step=1)
            f_height = st.number_input("Chiều cao (cm, tối thiểu):", min_value=0.0, value=0.0, step=1.0)
            f_weight = st.number_input("Cân nặng (kg, tối thiểu):", min_value=0.0, value=0.0, step=1.0)

        # --- CỘT 2: THÔNG TIN SỰ KIỆN ---
        with col2:
            st.subheader("Thông tin Sự kiện")
            f_season = st.selectbox("Mùa giải:", ["Tất cả", "Summer", "Winter"])
            f_city = st.text_input("Thành phố đăng cai (City):", "")
            f_sport = st.text_input("Môn thể thao (Sport):", "")
            f_medal = st.selectbox("Loại Huy chương:", ["Tất cả (Kể cả không có)", "Gold", "Silver", "Bronze"])

        # --- CỘT 3: THÔNG TIN ĐOÀN ---
        with col3:
            st.subheader("Thông tin Đoàn")
            f_sex = st.selectbox("Giới tính:", ["Tất cả", "M", "F"])
            f_team = st.text_input("Tên Quốc gia (Team):", "", placeholder="Ví dụ: China, USA...")
            f_noc = st.text_input("Mã Quốc gia (NOC):", "", placeholder="Ví dụ: CHN, USA, VIE...")

        st.markdown("---")

        # Nút bấm để kích hoạt lọc
        if st.button("Áp dụng bộ lọc", type="primary"):
            # 1. Chuẩn bị dữ liệu đầu vào (Biến đổi "Tất cả" thành None)
            sex_val = f_sex if f_sex != "Tất cả" else None
            season_val = f_season if f_season != "Tất cả" else None

            # Xử lý chuỗi rỗng thành None
            team_val = f_team.strip() if f_team.strip() != "" else None
            noc_val = f_noc.strip() if f_noc.strip() != "" else None
            city_val = f_city.strip() if f_city.strip() != "" else None
            sport_val = f_sport.strip() if f_sport.strip() != "" else None

            # 2. GỌI CÁC HÀM TỪ ANALYSIS.PY THEO TRÌNH TỰ

            # Bước 1: Lọc theo số
            res = ana.filter_data_number(df, age=f_age, height=f_height, weight=f_weight, year=f_year, sex=sex_val)

            # Bước 2: Lọc theo chuỗi
            res = ana.filter_data_string(res, team=team_val, noc=noc_val, season=season_val, city=city_val,
                                         sport=sport_val)

            # Bước 3: Lọc theo Huy chương (Nếu có chọn)
            if f_medal != "Tất cả (Kể cả không có)":
                res = ana.filter_medals(res, f_medal)

            # 3. HIỂN THỊ KẾT QUẢ
            st.success(f"🎉 Tìm thấy **{len(res)}** vận động viên phù hợp tiêu chí.")

            if not res.empty:
                st.dataframe(res)
                st.info(
                    f"Trong danh sách lọc được có: **{res['NOC'].nunique()}** quốc gia và **{res['Sport'].nunique()}** môn thể thao.")
            else:
                st.warning("Không tìm thấy dữ liệu nào khớp với bộ lọc này. Hãy thử nới lỏng điều kiện.")

    # =========================================================================
    # 3. THỐNG KÊ HUY CHƯƠNG
    # =========================================================================
    elif options == "Thống kê huy chương":
        st.header("3. Bảng tổng huy chương các nước (giảm dần)")

        tally = ana.calculate_medal_tally(df)

        # Cho người dùng chọn xem Top bao nhiêu
        top_n = st.slider("Chọn số lượng quốc gia hiển thị:", 5, 50, 10)
        top_countries = tally.head(top_n)

        col_table, col_chart = st.columns([1, 2])

        with col_table:
            st.write("Bảng số liệu:")
            st.dataframe(top_countries)

        with col_chart:
            st.write(f"Biểu đồ Top {top_n} quốc gia:")
            fig = px.bar(top_countries, y=['Gold', 'Silver', 'Bronze'],
                         title="Tổng sắp huy chương", barmode='group')
            st.plotly_chart(fig, use_container_width=True)

    # =========================================================================
    # 4. PHÂN TÍCH GIỚI TÍNH & TUỔI
    # =========================================================================
    elif options == "Phân tích giới tính & độ tuổi":
        st.header("4. Xu hướng tham gia theo Giới tính & Độ tuổi")

        st.subheader("A. Số lượng Nam/Nữ qua các năm")
        gender_data = ana.analyze_gender_participation(df)

        fig_gender = px.line(gender_data, markers=True,
                             title="Sự thay đổi số lượng VĐV Nam/Nữ theo thời gian")
        st.plotly_chart(fig_gender, use_container_width=True)

        st.markdown("---")

        st.subheader("B. Hiệu suất huy chương theo nhóm tuổi")
        age_stats = ana.analyze_medals_and_participants_by_age(df)

        st.dataframe(age_stats)

        fig_age = px.bar(age_stats, y='Medal_Count',
                         title="Số lượng huy chương đạt được theo nhóm tuổi",
                         color_discrete_sequence=['gold'])
        st.plotly_chart(fig_age, use_container_width=True)
        st.caption("Nhận xét: Biểu đồ cho thấy độ tuổi nào thường đạt đỉnh cao phong độ.")

    # =========================================================================
    # 5. THỂ CHẤT & MÔN THI ĐẤU
    # =========================================================================
    elif options == "Thể chất & Môn thi đấu":
        st.header("5. Tương quan Chiều cao - Cân nặng - BMI")

        physique_df = ana.analyze_physique_all_athletes(df)

        st.write("Top các môn thể thao có VĐV 'nặng ký' nhất:")
        st.dataframe(physique_df.head(10))

        st.subheader("Biểu đồ tương quan Cân nặng vs Chiều cao trung bình các môn")

        # Reset index để lấy tên cột Sport ra vẽ biểu đồ
        chart_data = physique_df.reset_index()

        fig_physique = px.scatter(chart_data, x="Weight", y="Height",
                                  size="BMI", hover_name="Sport", color="BMI",
                                  title="Phân bố thể hình các môn (Bóng to bong bóng = BMI lớn)")
        st.plotly_chart(fig_physique, use_container_width=True)
        st.info("💡 Mẹo: Di chuột vào các chấm tròn để xem tên môn thể thao.")

    # =========================================================================
    # 6. THẾ MẠNH QUỐC GIA
    # =========================================================================
    elif options == "Thế mạnh Quốc gia":
        st.header("6. Tìm môn thể thao thế mạnh của từng nước")

        dominant_df = ana.analyze_dominant_sports(df)

        all_countries = sorted(df['Team'].astype(str).unique())
        selected_country = st.selectbox("Chọn Quốc gia để xem thế mạnh:", all_countries,
                                        index=all_countries.index("China") if "China" in all_countries else 0)

        country_data = dominant_df[dominant_df['Team'] == selected_country].head(10)

        if not country_data.empty:
            st.write(f"Top 10 môn thể thao đạt nhiều huy chương nhất của **{selected_country}**:")

            fig_dom = px.bar(country_data, x="Medal_Count", y="Sport", orientation='h',
                             title=f"Thành tích của {selected_country} theo môn",
                             color="Medal_Count")
            fig_dom.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_dom, use_container_width=True)
        else:
            st.warning("Quốc gia này chưa đạt huy chương nào.")