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
    page_title="Olympic Data Analysis",  # Đã bỏ icon ở tab trình duyệt
    layout="wide"
)

# Thiết lập style mặc định cho biểu đồ matplotlib/seaborn
vis.setup_style()

# --- CSS TÙY CHỈNH GIAO DIỆN ---
st.markdown(
    """
    <style>
    /* 1. ĐỔI MÀU NỀN SIDEBAR (CỘT TRÁI) */
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

    /* Tăng kích thước chữ tiêu đề trong Sidebar */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #003e6b !important; 
    }

    /* Chỉnh chữ của các ô chọn (Radio button) */
    .stRadio label {
        font-size: 16px !important;
        font-weight: 500 !important; 
    }

    /* 4. [QUAN TRỌNG] CSS CHO KHUNG MÀU GIẢI THÍCH (Explanation Box) */
    /* Phần này giúp hiện cái khung màu nền cho nội dung phân tích */
    .explanation-box {
        background-color: #f0f8ff; /* Màu nền xanh rất nhạt */
        border-left: 6px solid #2b6cb0; /* Viền trái màu xanh đậm */
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


# --- HÀM HỖ TRỢ HIỂN THỊ GIẢI THÍCH (ĐÃ SỬA KHÔNG CÒN ICON) ---
def show_explanation(title, content):
    st.markdown(f"""
    <div class="explanation-box">
        <div class="explanation-title">PHÂN TÍCH & Ý NGHĨA: {title}</div>
        <div class="explanation-text">{content}</div>
    </div>
    """, unsafe_allow_html=True)


# --- 2. LOAD DATA ---
@st.cache_data
def get_data():
    file_path = 'data/athlete_events.csv'
    if not os.path.exists(file_path):
        st.error(f"Không tìm thấy file: {file_path}")
        return None
    return dc.load_and_clean_data(file_path)


df = get_data()

# --- 3. GIAO DIỆN CHÍNH ---
if df is not None:
    st.sidebar.title("DANH MỤC")  # Đã bỏ icon

    # Menu chính
    menu_group = st.sidebar.radio(
        "CHỌN CHỨC NĂNG:",
        ["1. Dữ liệu & Bộ lọc",
         "2. Bảng Thống kê (Analysis)",
         "3. Biểu đồ Trực quan (Visual)"]
    )

    st.sidebar.markdown("---")

    # =========================================================================
    # NHÓM 1: DỮ LIỆU & BỘ LỌC
    # =========================================================================
    if menu_group == "1. Dữ liệu & Bộ lọc":
        sub_menu = st.sidebar.radio("Chi tiết:", ["Tổng quan dữ liệu", "Bộ lọc Đa năng"])

        # --- 1.1 TỔNG QUAN ---
        if sub_menu == "Tổng quan dữ liệu":
            st.title("Tổng quan Bộ dữ liệu Olympic")  # Đã bỏ icon

            show_explanation("Tổng quan",
                             "Đây là cái nhìn toàn cảnh về quy mô dữ liệu lịch sử Olympic từ năm 1896 đến 2016. "
                             "Các con số cho thấy sự phát triển khổng lồ của phong trào Olympic qua hơn một thế kỷ, "
                             "từ số lượng vận động viên, quốc gia tham dự cho đến sự đa dạng của các môn thi đấu.")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Vận động viên", f"{df['ID'].nunique():,}")
            c2.metric("Quốc gia", f"{df['NOC'].nunique()}")
            c3.metric("Môn thi đấu", f"{df['Sport'].nunique()}")
            c4.metric("Giai đoạn", f"{df['Year'].min()} - {df['Year'].max()}")

            st.dataframe(df.head(100), use_container_width=True, height=600)

        # --- 1.2 BỘ LỌC FULL ---
        elif sub_menu == "Bộ lọc Đa năng":
            st.title("Bộ lọc Dữ liệu Chi tiết")  # Đã bỏ icon

            show_explanation("Công cụ lọc",
                             "Công cụ này giúp bạn 'đào sâu' vào dữ liệu để tìm kiếm những thông tin cụ thể. "
                             "Bạn có thể kết hợp nhiều tiêu chí như tìm tất cả VĐV nữ của Việt Nam thi đấu môn Bơi lội, "
                             "hoặc tìm những VĐV có chiều cao trên 2 mét ở các kỳ Thế vận hội mùa Đông.")

            with st.form("filter_form"):
                st.subheader("Tiêu chí lọc")
                c1, c2, c3 = st.columns(3)
                with c1:
                    f_team = st.selectbox("Quốc gia:", ["Tất cả"] + sorted(df['Team'].unique().tolist()))
                    f_noc = st.selectbox("Mã NOC:", ["Tất cả"] + sorted(df['NOC'].unique().tolist()))
                with c2:
                    f_sport = st.selectbox("Môn thể thao:", ["Tất cả"] + sorted(df['Sport'].unique().tolist()))
                    f_city = st.selectbox("Thành phố:", ["Tất cả"] + sorted(df['City'].unique().tolist()))
                with c3:
                    f_season = st.selectbox("Mùa giải:", ["Tất cả", "Summer", "Winter"])
                    f_sex = st.selectbox("Giới tính:", ["Tất cả", "M", "F"])

                st.markdown("---")
                c4, c5, c6, c7 = st.columns(4)
                with c4: f_year_min, f_year_max = st.slider("Giai đoạn:", 1896, 2016, (1896, 2016))
                with c5: f_age = st.number_input("Tuổi (>=):", 0, 100, 0)
                with c6: f_height = st.number_input("Chiều cao (>= cm):", 0, 250, 0)
                with c7: f_weight = st.number_input("Cân nặng (>= kg):", 0, 200, 0)

                # Đã bỏ icon tên lửa ở nút bấm
                if st.form_submit_button("Lọc ngay"):
                    res = ana.filter_data_number(df, age=f_age, height=f_height, weight=f_weight,
                                                 sex=(f_sex if f_sex != "Tất cả" else None))
                    res = res[(res['Year'] >= f_year_min) & (res['Year'] <= f_year_max)]
                    res = ana.filter_data_string(res, team=(f_team if f_team != "Tất cả" else None),
                                                 noc=(f_noc if f_noc != "Tất cả" else None),
                                                 season=(f_season if f_season != "Tất cả" else None),
                                                 city=(f_city if f_city != "Tất cả" else None),
                                                 sport=(f_sport if f_sport != "Tất cả" else None))

                    st.success(f"Tìm thấy **{len(res)}** kết quả.")
                    st.dataframe(res, use_container_width=True, height=600)

    # =========================================================================
    # NHÓM 2: BẢNG THỐNG KÊ (ANALYSIS)
    # =========================================================================
    elif menu_group == "2. Bảng Thống kê (Analysis)":
        st.sidebar.header("Chọn loại thống kê")
        stats_option = st.sidebar.radio("Nội dung:",
                                        ["Huy chương (Bảng tổng)", "Giới tính & Tuổi", "Thể chất (Chiều cao/Cân nặng)",
                                         "Hiệu ứng Sân nhà", "Thống kê Việt Nam"])

        if stats_option == "Huy chương (Bảng tổng)":
            st.title("Bảng Tổng sắp Huy chương Toàn đoàn")  # Đã bỏ icon
            show_explanation("Bảng xếp hạng",
                             "Dưới đây là bảng tổng sắp huy chương trọn đời của tất cả các quốc gia từng tham dự. "
                             "Dữ liệu được sắp xếp ưu tiên theo số lượng Huy chương Vàng, sau đó đến tổng số huy chương. "
                             "Đây là thước đo chính xác nhất cho sức mạnh thể thao của một quốc gia trên đấu trường quốc tế.")

            medal_tally = ana.calculate_medal_tally(df)
            st.dataframe(medal_tally, use_container_width=True, height=800)

        elif stats_option == "Giới tính & Tuổi":
            st.title("Thống kê Nhân khẩu học")  # Đã bỏ icon

            st.subheader("1. Tỷ lệ Nam/Nữ qua các năm")
            show_explanation("Cân bằng giới tính",
                             "Bảng số liệu này theo dõi sự thay đổi trong tỷ lệ vận động viên nữ tham gia Olympic qua từng năm. "
                             "Bạn có thể thấy rõ xu hướng bình đẳng giới đang tăng lên, từ những năm đầu gần như chỉ có nam giới, "
                             "đến nay tỷ lệ nữ giới đã tiệm cận mức cân bằng.")

            gender_stats = ana.analyze_gender_participation(df)
            if 'Female_Ratio (%)' not in gender_stats.columns and 'F' in gender_stats.columns:
                gender_stats['Total'] = gender_stats.get('M', 0) + gender_stats.get('F', 0)
                gender_stats['Female_Ratio (%)'] = round((gender_stats['F'] / gender_stats['Total']) * 100, 2)

            st.dataframe(gender_stats, use_container_width=True)

            st.divider()
            st.subheader("2. Hiệu suất theo Nhóm tuổi")
            show_explanation("Độ tuổi vàng",
                             "Phân tích này giúp trả lời câu hỏi: 'Độ tuổi nào là đỉnh cao phong độ của VĐV?'. "
                             "Thông thường, nhóm tuổi 20-30 chiếm đa số huy chương, nhưng ở một số môn đòi hỏi kinh nghiệm, "
                             "các VĐV lớn tuổi vẫn có thể tỏa sáng.")
            age_stats = ana.analyze_medals_and_participants_by_age(df)
            st.dataframe(age_stats, use_container_width=True)

        elif stats_option == "Thể chất (Chiều cao/Cân nặng)":
            st.title("Thống kê Chỉ số Thể chất")  # Đã bỏ icon

            st.subheader("1. Chỉ số Tổng quát")
            show_explanation("Đặc điểm hình thể",
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
            st.subheader("2. Chỉ số Trung bình theo Môn thể thao")
            sport_phys = ana.analyze_physique_by_sport(df)
            st.dataframe(sport_phys, use_container_width=True, height=600)

        elif stats_option == "Hiệu ứng Sân nhà":
            st.title("Dữ liệu Hiệu ứng Sân nhà")  # Đã bỏ icon
            show_explanation("Lợi thế chủ nhà",
                             "Lịch sử chứng minh các nước chủ nhà thường đạt thành tích vượt trội nhờ sự chuẩn bị kỹ lưỡng, "
                             "tâm lý thi đấu hưng phấn và sự cổ vũ của khán giả nhà. Bảng dưới đây giúp bạn kiểm chứng giả thuyết này "
                             "với bất kỳ quốc gia nào.")

            country_code = st.text_input("Nhập mã quốc gia (NOC) để kiểm tra (VD: CHN, USA, GBR):", "CHN")
            trend, hosts = ana.get_country_performance_and_hosts(df, country_code)

            c1, c2 = st.columns([1, 2])
            with c1:
                st.success(f"Các năm làm chủ nhà: {hosts}")
            with c2:
                st.info(f"Dữ liệu chi tiết huy chương của {country_code} qua các năm:")

            st.dataframe(trend, use_container_width=True, height=500)

        elif stats_option == "Thống kê Việt Nam":
            st.title("Số liệu Đoàn Thể thao Việt Nam")  # Đã bỏ icon
            show_explanation("Dấu ấn Việt Nam",
                             "Tổng hợp hành trình của thể thao Việt Nam tại Olympic. "
                             "Dữ liệu bao gồm số lượng VĐV tham dự tăng dần qua các năm và danh sách những gương mặt xuất sắc "
                             "đã mang vinh quang về cho tổ quốc (Huy chương).")

            vn_stats = ana.analyze_vietnam_participation(df)
            if not vn_stats.empty:
                st.subheader("1. Lịch sử tham dự")
                st.dataframe(vn_stats, use_container_width=True)
                st.subheader("2. Danh sách VĐV đạt Huy chương")
                vn_medals = ana.get_vietnam_medals(df)
                st.table(vn_medals)
            else:
                st.warning("Không tìm thấy dữ liệu.")

    # =========================================================================
    # NHÓM 3: BIỂU ĐỒ TRỰC QUAN (VISUALIZATION)
    # =========================================================================
    elif menu_group == "3. Biểu đồ Trực quan (Visual)":
        st.sidebar.header("Chọn loại biểu đồ")
        chart_option = st.sidebar.radio("Nội dung:",
                                        ["Biểu đồ Huy chương", "Biểu đồ Giới tính", "Biểu đồ Thể chất & AI",
                                         "Biểu đồ Sân nhà", "Biểu đồ Việt Nam"])

        if chart_option == "Biểu đồ Huy chương":
            st.title("Biểu đồ Top Quốc gia")  # Đã bỏ icon
            top_n = st.slider("Số lượng quốc gia hiển thị:", 5, 50, 10)

            fig = vis.plot_top_medals(df, top_n=top_n)
            st.pyplot(fig)

            show_explanation("Biểu đồ Xếp hạng",
                             f"Biểu đồ cột này trực quan hóa sức mạnh của {top_n} quốc gia hàng đầu. "
                             "Bạn có thể thấy sự thống trị của các cường quốc như Mỹ, Liên Xô (cũ) hay sự vươn lên của Trung Quốc. "
                             "Chiều cao cột thể hiện tổng số huy chương, giúp so sánh nhanh chóng sự chênh lệch thành tích.")

        elif chart_option == "Biểu đồ Giới tính":
            st.title("Xu hướng Nam/Nữ tham dự")  # Đã bỏ icon
            fig = vis.plot_gender_trend(df)
            st.pyplot(fig)

            show_explanation("Xu hướng Bình đẳng giới",
                             "Biểu đồ đường biểu diễn số lượng VĐV Nam (xanh) và Nữ (đỏ) qua các kỳ Olympic. "
                             "Đường màu đỏ đi lên mạnh mẽ từ thập niên 1980 phản ánh nỗ lực đưa thể thao nữ vào chương trình thi đấu chính thức. "
                             "Khoảng cách giữa hai đường ngày càng thu hẹp, tiến tới một Olympic cân bằng hoàn toàn.")

        elif chart_option == "Biểu đồ Thể chất & AI":
            st.title("Phân tích Thể chất & Phân cụm")  # Đã bỏ icon

            tab1, tab2, tab3 = st.tabs(["Phân phối", "So sánh Môn", "Phân cụm AI"])

            with tab1:
                st.subheader("Phân phối Tuổi - Chiều cao - Cân nặng")
                fig1 = vis.plot_physical_distribution(df)
                st.pyplot(fig1)
                show_explanation("Phân phối chuẩn",
                                 "Các biểu đồ Histogram cho thấy phần lớn VĐV nằm ở khoảng giữa (phân phối chuẩn). "
                                 "Tuy nhiên, độ tuổi có xu hướng lệch phải (nhiều VĐV trẻ), trong khi chiều cao và cân nặng "
                                 "tập trung quanh mức trung bình lý tưởng cho vận động.")

            with tab2:
                st.subheader("So sánh thể hình giữa các môn")
                fig2 = vis.plot_physical_comparison_by_sport(df)
                if fig2: st.pyplot(fig2)
                show_explanation("Đặc thù môn thể thao",
                                 "Biểu đồ Boxplot này cực kỳ thú vị! Nó cho thấy sự khác biệt rõ rệt về hình thể: "
                                 "VĐV Bóng rổ cao vượt trội, VĐV Cử tạ nặng ký nhưng thấp, trong khi VĐV Thể dục dụng cụ thường nhỏ nhắn. "
                                 "Điều này chứng minh: mỗi môn thể thao chọn lọc ra những kiểu cơ thể tối ưu nhất.")

            with tab3:
                st.subheader("Phân nhóm VĐV (K-Means Clustering)")  # Đã bỏ icon
                with st.spinner("Đang chạy mô hình AI..."):
                    fig3 = vis.plot_athlete_clustering(df)
                    if fig3: st.pyplot(fig3)
                show_explanation("Ứng dụng AI (Machine Learning)",
                                 "Sử dụng thuật toán K-Means Clustering để tự động gom nhóm VĐV mà không cần biết trước môn thi đấu. "
                                 "Máy tính tự nhận ra các cụm: Nhóm 'Nhẹ cân/Nhỏ người' (thường là chạy đường dài, thể dục), "
                                 "nhóm 'Cao lớn' và nhóm 'Cơ bắp'. Đây là ví dụ về cách Khoa học dữ liệu tìm ra các mẫu (pattern) ẩn.")

        elif chart_option == "Biểu đồ Sân nhà":
            st.title("Hiệu ứng Lợi thế Sân nhà")  # Đã bỏ icon

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Trường hợp Trung Quốc (2008)")
                fig_chn = vis.plot_host_advantage_china(df)
                st.pyplot(fig_chn)
                show_explanation("Cú hích Bắc Kinh 2008",
                                 "Biểu đồ cho thấy cột mốc năm 2008 cao đột biến so với các năm trước và sau đó. "
                                 "Khi làm chủ nhà, Trung Quốc đã đầu tư mạnh mẽ và đạt kết quả lịch sử, chứng minh 'Lợi thế sân nhà' là có thật.")

            with col2:
                st.subheader("Ảnh hưởng Chính trị (Tẩy chay)")
                fig_geo = vis.plot_geopolitics_impact(df)
                st.pyplot(fig_geo)
                show_explanation("Chiến tranh lạnh",
                                 "Biểu đồ số lượng quốc gia tham dự bị 'gãy' sâu vào năm 1980 (Moscow) và 1984 (Los Angeles). "
                                 "Đây là minh chứng lịch sử cho thấy Chính trị ảnh hưởng tiêu cực đến Thể thao như thế nào "
                                 "khi các khối quốc gia tẩy chay lẫn nhau.")

        elif chart_option == "Biểu đồ Việt Nam":
            st.title("Biểu đồ Đoàn Việt Nam")  # Đã bỏ icon

            vn_stats = ana.analyze_vietnam_participation(df)
            if not vn_stats.empty:
                st.subheader("Số lượng VĐV qua các năm")
                fig_vn = vis.plot_vietnam_stats(df)
                if fig_vn: st.pyplot(fig_vn)
                show_explanation("Sự phát triển",
                                 "Số lượng VĐV Việt Nam tham dự Olympic có xu hướng tăng dần, thể hiện sự hội nhập sâu rộng. "
                                 "Từ chỗ chỉ có vài đại diện, chúng ta đã có những đoàn thể thao đông đảo hơn ở các kỳ gần đây.")

                st.subheader("Bảng vàng thành tích (Visual)")
                fig_det = vis.plot_vietnam_details(df)
                if fig_det: st.pyplot(fig_det)
                show_explanation("Niềm tự hào dân tộc",
                                 "Bảng danh sách này vinh danh những cột mốc lịch sử: Tấm HCB đầu tiên của Trần Hiếu Ngân (2000), "
                                 "và đỉnh cao là tấm HCV của Hoàng Xuân Vinh (2016).")
            else:
                st.warning("Chưa có dữ liệu.")