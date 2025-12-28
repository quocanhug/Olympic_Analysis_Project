# chạy bằng lệnh trên terminal:
# D:\Olympic_Analysis_Project\.venv\Scripts\python.exe -m streamlit run UI.py
import streamlit as st
import pandas as pd
import os
# --- IMPORT MODULES ---
import modules.data_cleaning as dc
import modules.analysis as ana
import modules.visualization as vis

# --- 1. CẤU HÌNH TRANG & CSS TÙY CHỈNH ---
st.set_page_config(
    page_title="Olympic Data Analysis",
    layout="wide"
)

# Thiết lập style mặc định cho biểu đồ matplotlib/seaborn
vis.setup_style()

# --- CSS TÙY CHỈNH GIAO DIỆN ---
st.markdown(
    """
    <style>
    /* 1. ĐỔI MÀU NỀN SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #eaf4f4; 
    }

    /* 2. THIẾT LẬP PHÔNG CHỮ */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Roboto', 'Helvetica', sans-serif;
    }

    /* 3. CHỈNH MÀU CHỮ TRONG SIDEBAR */
    [data-testid="stSidebar"] * {
        color: #102a43 !important; 
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #003e6b !important; 
    }

    .stRadio label {
        font-size: 16px !important;
        font-weight: 500 !important; 
    }

    /* 4. CSS CHO KHUNG MÀU GIẢI THÍCH */
    .explanation-box {
        background-color: #f0f8ff;
        border-left: 6px solid #2b6cb0;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 5px;
    }
    .explanation-title {
        color: #2b6cb0;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    .explanation-text {
        color: #333333;
        font-size: 16px;
        line-height: 1.6;
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --- HÀM HỖ TRỢ HIỂN THỊ GIẢI THÍCH ---
def show_explanation(title, content):
    st.markdown(f"""
    <div class="explanation-box">
        <div class="explanation-title">PHÂN TÍCH & Ý NGHĨA: {title}</div>
        <div class="explanation-text">{content}</div>
    </div>
    """, unsafe_allow_html=True)


# --- 2. LOAD DATA ---
try:
    df_unclean = dc.load_data("data/athlete_events.csv")  # Dữ liệu gốc
    df = dc.clean_data(df_unclean.copy())  # Dữ liệu sạch
except Exception as e:
    st.error(f"Lỗi khi tải dữ liệu: {e}")
    df = None
    df_unclean = None

# --- 3. GIAO DIỆN CHÍNH ---
if df is not None:
    st.sidebar.title("DANH MỤC")

    # Menu chính (Đã sửa Title Case)
    menu_group = st.sidebar.radio(
        "CHỌN CHỨC NĂNG:",
        ["1. Dữ Liệu & Bộ Lọc",
         "2. Bảng Thống Kê (Analysis)",
         "3. Biểu Đồ Trực Quan (Visual)"]
    )

    st.sidebar.markdown("---")

    # =========================================================================
    # NHÓM 1: DỮ LIỆU & BỘ LỌC
    # =========================================================================
    if menu_group == "1. Dữ Liệu & Bộ Lọc":
        sub_menu = st.sidebar.radio(
            "Chi tiết:", ["Tổng Quan Dữ Liệu", "Bộ Lọc Đa Năng"])

        # --- 1.1 TỔNG QUAN ---
        if sub_menu == "Tổng Quan Dữ Liệu":
            st.title("Tổng Quan Bộ Dữ Liệu Olympic")

            # Phần Metrics
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Vận Động Viên", f"{df['ID'].nunique():,}")
            c2.metric("Quốc Gia", f"{df['NOC'].nunique()}")
            c3.metric("Môn Thi Đấu", f"{df['Sport'].nunique()}")
            c4.metric("Giai Đoạn", f"{df['Year'].min()} - {df['Year'].max()}")

            st.divider()

            # Chọn chế độ xem
            col_sel, col_empty = st.columns([1, 2])
            with col_sel:
                data_view_mode = st.radio(" Chọn Chế Độ Xem Dữ Liệu:",
                                          ["Dữ Liệu Đã Làm Sạch (Cleaned)", "Dữ Liệu Gốc (Raw Data)"])

            if data_view_mode == "Dữ Liệu Gốc (Raw Data)":
                st.warning(
                    "⚠️ Đang hiển thị dữ liệu gốc chưa qua xử lý (Có thể chứa: Giá trị rỗng NaN, Lỗi định dạng, Outlier...)")
                st.dataframe(df_unclean.head(100), use_container_width=True, height=500)
            else:
                st.success("✅ Đang hiển thị dữ liệu đã được làm sạch và chuẩn hóa phục vụ phân tích.")
                st.dataframe(df.head(100), use_container_width=True, height=500)

            # Giải thích quy trình
            show_explanation("Quy Trình Xử Lý Dữ Liệu (Data Cleaning)",
                             """
                             Để đảm bảo kết quả phân tích chính xác, dữ liệu thô đã được xử lý qua 5 bước nghiêm ngặt:
                             <br>
                             <b>1. Xóa dữ liệu trùng lặp (Duplicates):</b> Loại bỏ hoàn toàn các dòng trùng lặp trong file gốc.
                             <br>
                             <b>2. Chuẩn hóa định dạng (Formatting):</b> Ép kiểu các cột số liệu (Tuổi, Chiều cao, Cân nặng) về định dạng số thực, loại bỏ các ký tự lỗi.
                             <br>
                             <b>3. Xử lý giá trị thiếu (Missing Values):</b>
                             <ul style="margin-top:0px; margin-bottom:5px;">
                                <li>Cột số (Age, Height, Weight): Điền các ô trống bằng giá trị trung bình (Mean).</li>
                                <li>Cột phân loại (trừ Huy chương): Điền bằng giá trị xuất hiện nhiều nhất (Mode).</li>
                                <li>Cột Huy chương (Medal): Các ô trống được gán nhãn "No Medal".</li>
                             </ul>
                             <b>4. Sửa lỗi nhập liệu (Label Correction):</b> Chuẩn hóa tên huy chương (ví dụ: gộp "Gold ", "gold" thành "Gold").
                             <br>
                             <b>5. Xử lý giá trị ngoại lai (Outliers):</b> Sử dụng phương pháp IQR (Interquartile Range) để chặn biên trên và biên dưới, loại bỏ các giá trị quá lớn hoặc quá nhỏ bất thường (ví dụ: tuổi quá cao hoặc cân nặng phi lý) để tránh làm lệch biểu đồ.
                             """)

        # --- 1.2 BỘ LỌC FULL ---
        elif sub_menu == "Bộ Lọc Đa Năng":
            st.title("Bộ Lọc Dữ Liệu Chi Tiết")

            show_explanation("Công Cụ Lọc",
                             "Công cụ này giúp bạn 'đào sâu' vào dữ liệu để tìm kiếm những thông tin cụ thể. "
                             "Bạn có thể kết hợp nhiều tiêu chí như tìm tất cả VĐV nữ của Việt Nam thi đấu môn Bơi lội, "
                             "hoặc tìm những VĐV có chiều cao trên 2 mét ở các kỳ Thế vận hội mùa Đông.")

            with st.form("filter_form"):
                st.subheader("Tiêu Chí Lọc")
                c1, c2, c3 = st.columns(3)
                with c1:
                    f_team = st.selectbox(
                        "Quốc Gia:", ["Tất cả"] + sorted(df['Team'].unique().tolist()))
                    f_noc = st.selectbox(
                        "Mã NOC:", ["Tất cả"] + sorted(df['NOC'].unique().tolist()))
                with c2:
                    f_sport = st.selectbox(
                        "Môn Thể Thao:", ["Tất cả"] + sorted(df['Sport'].unique().tolist()))
                    f_city = st.selectbox(
                        "Thành Phố:", ["Tất cả"] + sorted(df['City'].unique().tolist()))
                with c3:
                    f_season = st.selectbox(
                        "Mùa Giải:", ["Tất cả", "Summer", "Winter"])
                    f_sex = st.selectbox("Giới Tính:", ["Tất cả", "M", "F"])

                st.markdown("---")
                c4, c5, c6, c7 = st.columns(4)
                with c4:
                    f_year_min, f_year_max = st.slider(
                        "Giai Đoạn:", 1896, 2016, (1896, 2016))
                with c5:
                    f_age = st.number_input("Tuổi (>=):", 0, 100, 0)
                with c6:
                    f_height = st.number_input("Chiều Cao (>= cm):", 0, 250, 0)
                with c7:
                    f_weight = st.number_input("Cân Nặng (>= kg):", 0, 200, 0)

                if st.form_submit_button("Lọc Ngay"):
                    res = ana.filter_data_number(df, age=f_age, height=f_height, weight=f_weight,
                                                 sex=(f_sex if f_sex != "Tất cả" else None))
                    res = res[(res['Year'] >= f_year_min) &
                              (res['Year'] <= f_year_max)]
                    res = ana.filter_data_string(res, team=(f_team if f_team != "Tất cả" else None),
                                                 noc=(f_noc if f_noc !=
                                                               "Tất cả" else None),
                                                 season=(
                                                     f_season if f_season != "Tất cả" else None),
                                                 city=(f_city if f_city !=
                                                                 "Tất cả" else None),
                                                 sport=(f_sport if f_sport != "Tất cả" else None))

                    st.success(f"Tìm thấy **{len(res)}** kết quả.")
                    st.dataframe(res, use_container_width=True, height=600)

    # =========================================================================
    # NHÓM 2: BẢNG THỐNG KÊ (ANALYSIS)
    # =========================================================================
    elif menu_group == "2. Bảng Thống Kê (Analysis)":
        st.sidebar.header("Chọn Loại Thống Kê")
        stats_option = st.sidebar.radio("Nội Dung:",
                                        ["Huy Chương (Bảng Tổng)",
                                         "Giới Tính & Tuổi",
                                         "Thể Chất (Chiều Cao/Cân Nặng)",
                                         "Thống Kê Cho Hiệu Ứng Sân Nhà",
                                         "Thống Kê Việt Nam"])

        if stats_option == "Huy Chương (Bảng Tổng)":
            st.title("Bảng Tổng Sắp Huy Chương Toàn Đoàn")
            show_explanation("Bảng Xếp Hạng",
                             "Dưới đây là bảng tổng sắp huy chương trọn đời của tất cả các quốc gia từng tham dự. "
                             "Dữ liệu được sắp xếp ưu tiên theo số lượng Huy chương Vàng, sau đó đến tổng số huy chương. "
                             "Đây là thước đo chính xác nhất cho sức mạnh thể thao của một quốc gia trên đấu trường quốc tế.")

            medal_tally = ana.calculate_medal_tally(df)
            st.dataframe(medal_tally, use_container_width=True, height=800)

        elif stats_option == "Giới Tính & Tuổi":
            st.title("Thống Kê Nhân Khẩu Học")

            st.subheader("1. Tỷ Lệ Nam/Nữ Qua Các Năm")
            show_explanation("Cân Bằng Giới Tính",
                             "Bảng số liệu này theo dõi sự thay đổi trong tỷ lệ vận động viên nữ tham gia Olympic qua từng năm. "
                             "Bạn có thể thấy rõ xu hướng bình đẳng giới đang tăng lên, từ những năm đầu gần như chỉ có nam giới, "
                             "đến nay tỷ lệ nữ giới đã tiệm cận mức cân bằng.")

            gender_stats = ana.analyze_gender_participation(df)
            if 'Female_Ratio (%)' not in gender_stats.columns and 'F' in gender_stats.columns:
                gender_stats['Total'] = gender_stats.get(
                    'M', 0) + gender_stats.get('F', 0)
                gender_stats['Female_Ratio (%)'] = round(
                    (gender_stats['F'] / gender_stats['Total']) * 100, 2)

            st.dataframe(gender_stats, use_container_width=True)

            st.divider()
            st.subheader("2. Hiệu Suất Theo Nhóm Tuổi")
            show_explanation("Độ Tuổi Vàng",
                             "Phân tích này giúp trả lời câu hỏi: 'Độ tuổi nào là đỉnh cao phong độ của VĐV?'. "
                             "Thông thường, nhóm tuổi 20-30 chiếm đa số huy chương, nhưng ở một số môn đòi hỏi kinh nghiệm, "
                             "các VĐV lớn tuổi vẫn có thể tỏa sáng.")
            age_stats = ana.analyze_medals_and_participants_by_age(df)
            st.dataframe(age_stats, use_container_width=True)

        elif stats_option == "Thể Chất (Chiều Cao/Cân Nặng)":
            st.title("Thống Kê Chỉ Số Thể Chất")

            st.subheader("1. Chỉ Số Tổng Quát")
            show_explanation("Đặc Điểm Hình Thể",
                             "Các chỉ số trung bình, thấp nhất và cao nhất về Chiều cao và Cân nặng của toàn bộ VĐV. "
                             "Điều này cho ta cái nhìn tổng quan về 'cơ thể Olympic' tiêu chuẩn, mặc dù có sự biến thiên rất lớn giữa các môn.")

            phys_summary = ana.analyze_physical_summary(df)
            summary_data = {
                "Chỉ số": ["Tuổi (Age)", "Chiều cao (Height)", "Cân nặng (Weight)"],
                "Trung bình (Mean)": [phys_summary['Age']['Mean'], phys_summary['Height']['Mean'],
                                      phys_summary['Weight']['Mean']],
                "Thấp nhất (Min)": [df['Age'].min(), df['Height'].min(), df['Weight'].min()],
                "Cao nhất (Max)": [phys_summary['Age']['Max'], phys_summary['Height']['Max'],
                                   phys_summary['Weight']['Max']]
            }
            st.table(pd.DataFrame(summary_data))

            st.divider()
            st.subheader("2. Chỉ Số Trung Bình Theo Môn Thể Thao")
            sport_phys = ana.analyze_physique_by_sport(df)
            st.dataframe(sport_phys, use_container_width=True, height=600)

        elif stats_option == "Thống Kê Cho Hiệu Ứng Sân Nhà":
            st.title("Dữ Liệu Thống Kê Cho Nước Sân Nhà")
            show_explanation("Lợi Thế Chủ Nhà",
                             "Lịch sử chứng minh các nước chủ nhà thường đạt thành tích vượt trội nhờ sự chuẩn bị kỹ lưỡng, "
                             "tâm lý thi đấu hưng phấn và sự cổ vũ của khán giả nhà. Bảng dưới đây giúp bạn kiểm chứng giả thuyết này "
                             "với bất kỳ quốc gia nào.")

            country_code = st.text_input(
                "Nhập mã quốc gia (NOC) để kiểm tra (VD: CHN, USA, GBR):", "CHN")
            trend, hosts = ana.get_country_performance_and_hosts(
                df, country_code)

            c1, c2 = st.columns([1, 2])
            with c1:
                st.success(f"Các năm làm chủ nhà: {hosts}")
            with c2:
                st.info(
                    f"Dữ liệu chi tiết huy chương của {country_code} qua các năm:")

            st.dataframe(trend, use_container_width=True, height=500)

        elif stats_option == "Thống Kê Việt Nam":
            st.title("Số Liệu Đoàn Thể Thao Việt Nam")
            show_explanation("Dấu Ấn Việt Nam",
                             "Tổng hợp hành trình của thể thao Việt Nam tại Olympic. "
                             "Dữ liệu bao gồm số lượng VĐV tham dự tăng dần qua các năm và danh sách những gương mặt xuất sắc "
                             "đã mang vinh quang về cho tổ quốc (Huy chương).")

            vn_stats = ana.analyze_vietnam_participation(df)
            if not vn_stats.empty:
                st.subheader("1. Lịch Sử Tham Dự")
                st.dataframe(vn_stats, use_container_width=True)
                st.subheader("2. Danh Sách VĐV Đạt Huy Chương")
                vn_medals = ana.get_vietnam_medals(df)
                st.table(vn_medals)
            else:
                st.warning("Không tìm thấy dữ liệu.")

    # =========================================================================
    # NHÓM 3: BIỂU ĐỒ TRỰC QUAN (VISUALIZATION)
    # =========================================================================
    elif menu_group == "3. Biểu Đồ Trực Quan (Visual)":
        st.sidebar.header("Chọn Loại Biểu Đồ")
        chart_option = st.sidebar.radio("Nội Dung:",
                                        ["Biểu Đồ Huy Chương",
                                         "Biểu Đồ Giới Tính",
                                         "Biểu Đồ Thể Chất & AI",
                                         "Biểu Đồ Hiệu Ứng Sân Nhà Và Chính Trị",
                                         "Biểu Đồ Các Lần Việt Nam Tham Gia Olympic"])

        if chart_option == "Biểu Đồ Huy Chương":
            st.title("Biểu Đồ Top Quốc Gia")
            top_n = st.slider("Số lượng quốc gia hiển thị:", 5, 50, 10)

            fig = vis.plot_top_medals(df, top_n=top_n)
            st.pyplot(fig)

            show_explanation("Biểu Đồ Xếp Hạng",
                             f"Biểu đồ cột này trực quan hóa sức mạnh của {top_n} quốc gia hàng đầu. "
                             "Bạn có thể thấy sự thống trị của các cường quốc như Mỹ, Liên Xô (cũ) hay sự vươn lên của Trung Quốc. "
                             "Chiều cao cột thể hiện tổng số huy chương, giúp so sánh nhanh chóng sự chênh lệch thành tích.")

        elif chart_option == "Biểu Đồ Giới Tính":
            st.title("Xu Hướng Nam/Nữ Tham Dự")
            fig = vis.plot_gender_trend(df)
            st.pyplot(fig)

            show_explanation("Xu Hướng Bình Đẳng Giới",
                             "Biểu đồ đường biểu diễn số lượng VĐV Nam (xanh) và Nữ (đỏ) qua các kỳ Olympic. "
                             "Đường màu đỏ đi lên mạnh mẽ từ thập niên 1980 phản ánh nỗ lực đưa thể thao nữ vào chương trình thi đấu chính thức. "
                             "Khoảng cách giữa hai đường ngày càng thu hẹp, tiến tới một Olympic cân bằng hoàn toàn.")

        elif chart_option == "Biểu Đồ Thể Chất & AI":
            st.title("Phân Tích Thể Chất & Phân Cụm Theo AI")

            tab1, tab2, tab3 = st.tabs(
                ["Phân Phối", "So Sánh Môn", "Phân Cụm AI"])

            with tab1:
                st.subheader("Phân Phối Tuổi - Chiều Cao - Cân Nặng")
                fig1 = vis.plot_physical_distribution(df)
                st.pyplot(fig1)
                show_explanation("Phân Phối Chuẩn",
                                 "Các biểu đồ Histogram cho thấy phần lớn VĐV nằm ở khoảng giữa (phân phối chuẩn). "
                                 "Tuy nhiên, độ tuổi có xu hướng lệch phải (nhiều VĐV trẻ), trong khi chiều cao và cân nặng "
                                 "tập trung quanh mức trung bình lý tưởng cho vận động.")

            with tab2:
                st.subheader("So Sánh Thể Hình Giữa Các Môn")
                fig2 = vis.plot_physical_comparison_by_sport(df)
                if fig2:
                    st.pyplot(fig2)
                show_explanation("Đặc Thù Môn Thể Thao",
                                 "Biểu đồ Boxplot này cực kỳ thú vị! Nó cho thấy sự khác biệt rõ rệt về hình thể: "
                                 "VĐV Bóng rổ cao vượt trội, VĐV Cử tạ nặng ký nhưng thấp, trong khi VĐV Thể dục dụng cụ thường nhỏ nhắn. "
                                 "Điều này chứng minh: mỗi môn thể thao chọn lọc ra những kiểu cơ thể tối ưu nhất.")

            with tab3:
                st.subheader("Phân Nhóm VĐV (K-Means Clustering)")
                with st.spinner("Đang chạy mô hình AI..."):
                    fig3 = vis.plot_athlete_clustering(df)
                    if fig3:
                        st.pyplot(fig3)
                show_explanation("Ứng Dụng AI (Machine Learning)",
                                 "Sử dụng thuật toán K-Means Clustering để tự động gom nhóm VĐV mà không cần biết trước môn thi đấu. "
                                 "Máy tính tự nhận ra các cụm: Nhóm 'Nhẹ cân/Nhỏ người' (thường là chạy đường dài, thể dục), "
                                 "nhóm 'Cao lớn' và nhóm 'Cơ bắp'. Đây là ví dụ về cách Khoa học dữ liệu tìm ra các mẫu (pattern) ẩn.")

        elif chart_option == "Biểu Đồ Hiệu Ứng Sân Nhà Và Chính Trị":
            st.title("Hiệu Ứng Lợi Thế Sân Nhà")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Trường Hợp Trung Quốc (2008)")
                fig_chn = vis.plot_host_advantage_china(df)
                st.pyplot(fig_chn)
                show_explanation("Cú Hích Bắc Kinh 2008",
                                 "Biểu đồ cho thấy cột mốc năm 2008 cao đột biến so với các năm trước và sau đó. "
                                 "Khi làm chủ nhà, Trung Quốc đã đầu tư mạnh mẽ và đạt kết quả lịch sử, chứng minh 'Lợi thế sân nhà' là có thật.")

            with col2:
                st.subheader("Ảnh Hưởng Chính Trị (Tẩy Chay)")
                fig_geo = vis.plot_geopolitics_impact(df)
                st.pyplot(fig_geo)
                show_explanation("Chiến Tranh Lạnh",
                                 "Biểu đồ số lượng quốc gia tham dự bị 'gãy' sâu vào năm 1980 (Moscow) và 1984 (Los Angeles). "
                                 "Đây là minh chứng lịch sử cho thấy Chính trị ảnh hưởng tiêu cực đến Thể thao như thế nào "
                                 "khi các khối quốc gia tẩy chay lẫn nhau.")

        elif chart_option == "Biểu Đồ Các Lần Việt Nam Tham Gia Olympic":
            st.title("Biểu Đồ Đoàn Việt Nam")

            vn_stats = ana.analyze_vietnam_participation(df)
            if not vn_stats.empty:
                st.subheader("Số Lượng VĐV Qua Các Năm")
                fig_vn = vis.plot_vietnam_stats(df)
                if fig_vn:
                    st.pyplot(fig_vn)
                show_explanation("Sự Phát Triển",
                                 "Số lượng VĐV Việt Nam tham dự Olympic có xu hướng tăng dần, thể hiện sự hội nhập sâu rộng. "
                                 "Từ chỗ chỉ có vài đại diện, chúng ta đã có những đoàn thể thao đông đảo hơn ở các kỳ gần đây.")

                st.subheader("Bảng Vàng Thành Tích (Visual)")
                fig_det = vis.plot_vietnam_details(df)
                if fig_det:
                    st.pyplot(fig_det)
                show_explanation("Niềm Tự Hào Dân Tộc",
                                 "Bảng danh sách này vinh danh những cột mốc lịch sử: Tấm HCB đầu tiên của Trần Hiếu Ngân (2000), "
                                 "và đỉnh cao là tấm HCV của Hoàng Xuân Vinh (2016).")
            else:
                st.warning("Chưa có dữ liệu.")