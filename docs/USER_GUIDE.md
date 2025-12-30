📚 Mục lục

1. Cài đặt

2. Cấu trúc dữ liệu

3. Sử dụng cơ bản

4. Sử dụng nâng cao

5. Xuất báo cáo (Quan trọng)

6. Troubleshooting

🚀 Cài đặt
Yêu cầu hệ thống
Python 3.7 trở lên

Các thư viện: pandas, numpy, matplotlib, seaborn, openpyxl

Cài đặt Python packages
Bash

# Cài đặt các thư viện cần thiết
pip install pandas numpy matplotlib seaborn openpyxl scikit-learn streamlit
📁 Cấu trúc dữ liệu
Chuẩn bị file dữ liệu
Đặt file athlete_events.csv vào thư mục gốc hoặc thư mục data/ (tùy theo cấu hình trong code).

Đảm bảo file có các cột chuẩn: ID, Name, Sex, Age, Height, Weight, Team, NOC, Year, Sport, Event, Medal.

Kiểm tra dữ liệu
Python

from modules.data_cleaning import load_data

# Tải dữ liệu (Lưu ý đường dẫn file)
df = load_data("athlete_events.csv") 

if df is not None:
    print(f"Số dòng: {len(df)}")
    print(df.head())
🎯 Sử dụng cơ bản
Workflow đơn giản
Python

# 1. Import các modules
from modules.data_cleaning import load_data, clean_data
from modules.analysis import calculate_medal_tally
from modules.visualization import plot_top_medals
import matplotlib.pyplot as plt

# 2. Tải và làm sạch dữ liệu
df = load_data("athlete_events.csv")
df_clean = clean_data(df)

# 3. Phân tích cơ bản (Bảng tổng sắp)
medal_tally = calculate_medal_tally(df_clean)
print(medal_tally.head(10))

# 4. Vẽ biểu đồ
fig = plot_top_medals(df_clean)
if fig:
    plt.show()
Ví dụ 1: Phân tích xu hướng giới tính
Python

from modules.analysis import analyze_gender_participation
from modules.visualization import plot_gender_trend
import matplotlib.pyplot as plt

# Phân tích số liệu
gender_stats = analyze_gender_participation(df_clean)
print(gender_stats.head())

# Vẽ biểu đồ
fig = plot_gender_trend(df_clean)
plt.show()
🔧 Sử dụng nâng cao
Lọc dữ liệu
Python

from modules.analysis import filter_data_number, filter_data_string, filter_medals

# Lọc VĐV cao trên 1m80, nặng trên 80kg
df_big = filter_data_number(df_clean, height=180, weight=80)

# Lọc VĐV Việt Nam (Team="Vietnam" hoặc NOC="VIE")
df_vn = filter_data_string(df_clean, team="Vietnam")

# Lọc chỉ lấy Huy chương Vàng
df_gold = filter_medals(df_clean, medal="Gold")
Làm sạch dữ liệu nâng cao (Sửa lại Import)
Lưu ý: Các hàm này nằm trong data_cleaning, không phải analysis.

Python

# ĐÚNG: Import từ data_cleaning
from modules.data_cleaning import clean_team_name, clean_event_name, extract_nickname

# Làm sạch tên đội
df_clean = clean_team_name(df_clean)

# Trích xuất biệt danh
df_clean = extract_nickname(df_clean)
print(df_clean[['Name', 'Nickname']].head())
Phân tích chuyên sâu
Python

from modules.analysis import analyze_physique_all_athletes, analyze_medals_and_participants_by_age

# Phân tích thể chất (Chiều cao, Cân nặng trung bình)
physique = analyze_physique_all_athletes(df_clean)
print(physique.head())

# Phân tích theo nhóm tuổi
age_stats = analyze_medals_and_participants_by_age(df_clean)
print(age_stats)
💾 Xuất báo cáo (Đã cập nhật theo code mới)
Module export_data.py của bạn hiện tại được thiết kế để tự động hóa. Bạn không cần gọi từng hàm lẻ tẻ mà có thể chạy toàn bộ quy trình.

Cách 1: Chạy tự động (Khuyên dùng)
Mở terminal và chạy lệnh:

Bash

python export_data.py
Code sẽ tự động:

Tạo thư mục output/

Xuất các file CSV phân tích vào output/csv_data/

Xuất file Excel báo cáo tổng hợp vào output/reports/

Vẽ và lưu ảnh biểu đồ vào output/charts/

Cách 2: Sử dụng code thủ công
Nếu bạn muốn tùy chỉnh việc xuất trong code Python:

Python

from modules.export_data import setup_directories, save_dataframe_to_csv, create_excel_report
from modules.analysis import calculate_medal_tally

# 1. Khởi tạo thư mục
dirs = setup_directories()  # Trả về dict đường dẫn {'csv': ..., 'reports': ...}

# 2. Xuất CSV lẻ
tally = calculate_medal_tally(df_clean)
save_dataframe_to_csv(tally, "medal_tally.csv", dirs['csv'])

# 3. Xuất Excel tổng hợp (Tự động gom các kết quả)
# Bạn cần một dictionary chứa các kết quả phân tích
results = {'Medal Tally': tally}
create_excel_report(df_clean, results, dirs['reports'])
📊 Ví dụ thực tế: Phân tích Việt Nam
Python

from modules.analysis import get_vietnam_medals, analyze_vietnam_participation
from modules.visualization import plot_vietnam_stats, plot_vietnam_details

# 1. Lấy danh sách huy chương
vn_medals = get_vietnam_medals(df_clean)
print("Danh sách huy chương của Việt Nam:")
print(vn_medals)

# 2. Thống kê tham gia
vn_participation = analyze_vietnam_participation(df_clean)
print("\nSố lượng VĐV Việt Nam theo năm:")
print(vn_participation)

# 3. Vẽ biểu đồ
plot_vietnam_stats(df_clean)
plot_vietnam_details(df_clean)
plt.show()
🐛 Troubleshooting
Lỗi: ModuleNotFoundError: No module named 'modules'
Nguyên nhân: Bạn đang chạy file từ bên trong thư mục con thay vì thư mục gốc dự án. Giải pháp:

Luôn chạy lệnh python từ thư mục gốc (nơi chứa export_data.py và thư mục modules).

Ví dụ: D:\Project_Olympic> python modules/data_cleaning.py (Sai) -> D:\Project_Olympic> python -m modules.data_cleaning (Đúng hơn) hoặc chạy file main ở root.

Lỗi: 'DataFrame' object has no attribute 'map' (hoặc lỗi version pandas)
Giải pháp: Code sử dụng cú pháp pandas hiện đại. Hãy đảm bảo version pandas >= 1.0.

Lỗi: Biểu đồ không hiện ra
Giải pháp: Thêm plt.show() sau khi gọi các hàm vẽ biểu đồ nếu bạn không dùng Jupyter Notebook.