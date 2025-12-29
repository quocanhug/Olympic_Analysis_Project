# Hướng dẫn sử dụng

## 📚 Mục lục

1. [Cài đặt](#cài-đặt)
2. [Cấu trúc dữ liệu](#cấu-trúc-dữ-liệu)
3. [Sử dụng cơ bản](#sử-dụng-cơ-bản)
4. [Sử dụng nâng cao](#sử-dụng-nâng-cao)
5. [Ví dụ thực tế](#ví-dụ-thực-tế)
6. [Troubleshooting](#troubleshooting)

## 🚀 Cài đặt

### Yêu cầu hệ thống

- Python 3.7 trở lên
- RAM: Tối thiểu 4GB (khuyến nghị 8GB)
- Dung lượng ổ cứng: ~500MB

### Cài đặt Python packages

```bash
# Clone hoặc tải dự án về
cd project

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### Kiểm tra cài đặt

```python
# Chạy trong Python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

print("Tất cả thư viện đã được cài đặt thành công!")
```

## 📁 Cấu trúc dữ liệu

### Chuẩn bị file dữ liệu

1. Đặt file `athlete_events.csv` vào thư mục `data/`
2. Đảm bảo file có đầy đủ các cột:
   - ID, Name, Sex, Age, Height, Weight
   - Team, NOC, Games, Year, Season, City
   - Sport, Event, Medal

### Kiểm tra dữ liệu

```python
from modules.data_cleaning import load_data

# Tải dữ liệu
df = load_data("data/athlete_events.csv")

# Kiểm tra thông tin cơ bản
print(f"Số dòng: {len(df)}")
print(f"Số cột: {len(df.columns)}")
print(df.head())
print(df.info())
```

## 🎯 Sử dụng cơ bản

### Workflow đơn giản

```python
# 1. Import các modules
from modules.data_cleaning import load_data
from modules.data_cleaning import clean_data
from modules.analysis import calculate_medal_tally
from modules.visualization import plot_top_medals

# 2. Tải và làm sạch dữ liệu
df = load_data("data/athlete_events.csv")
df_clean = clean_data(df)

# 3. Phân tích cơ bản
medal_tally = calculate_medal_tally(df_clean)
print(medal_tally.head(10))

# 4. Vẽ biểu đồ
plot_top_medals(df_clean, top_n=10)
```

### Ví dụ 1: Xem bảng tổng sắp huy chương

```python
from modules.data_cleaning import load_data
from modules.data_cleaning import clean_data
from modules.analysis import calculate_medal_tally

# Tải và làm sạch dữ liệu
df = load_data("data/athlete_events.csv")
df_clean = clean_data(df)

# Tính tổng sắp
medal_tally = calculate_medal_tally(df_clean)

# Hiển thị top 10
print("Top 10 quốc gia đạt nhiều huy chương nhất:")
print(medal_tally.head(10))

# Lưu kết quả
medal_tally.to_csv("results/medal_tally.csv")
```

### Ví dụ 2: Phân tích xu hướng giới tính

```python
from modules.data_cleaning import load_data
from modules.data_cleaning import clean_data
from modules.analysis import analyze_gender_participation
from modules.visualization import plot_gender_trend

# Tải và làm sạch dữ liệu
df = load_data("data/athlete_events.csv")
df_clean = clean_data(df)

# Phân tích
gender_stats = analyze_gender_participation(df_clean)
print(gender_stats)

# Vẽ biểu đồ
plot_gender_trend(df_clean)
```

### Ví dụ 3: Phân tích thể chất

```python
from modules.data_cleaning import load_data
from modules.data_cleaning import clean_data
from modules.analysis import analyze_physique_all_athletes
from modules.visualization import plot_physical_distribution

# Tải và làm sạch dữ liệu
df = load_data("data/athlete_events.csv")
df_clean = clean_data(df)

# Phân tích thể chất
physique = analyze_physique_all_athletes(df_clean)
print("Thể chất trung bình theo môn:")
print(physique.head(10))

# Vẽ biểu đồ phân bố
plot_physical_distribution(df_clean)
```

## 🔧 Sử dụng nâng cao

### Lọc dữ liệu theo điều kiện

#### Lọc theo số (Age, Height, Weight)

```python
from modules.analysis import filter_data_number

# Lọc VĐV cao trên 180cm, nặng trên 80kg, từ năm 2000
df_filtered = filter_data_number(
    df_clean,
    height=180,
    weight=80,
    year=2000
)

print(f"Số VĐV thỏa mãn: {len(df_filtered)}")
print(df_filtered.head())
```

#### Lọc theo chuỗi (Team, Sport, Season)

```python
from modules.analysis import filter_data_string

# Lọc VĐV Việt Nam tham gia Olympic Mùa hè
df_vietnam = filter_data_string(
    df_clean,
    team="Vietnam",
    season="Summer"
)

print(f"Số VĐV Việt Nam: {len(df_vietnam)}")
```

#### Lọc theo mùa và năm cụ thể

```python
from modules.analysis import filter_season_and_year

# Chỉ lấy Olympic Mùa hè 2016
df_2016 = filter_season_and_year(
    df_clean,
    season="Summer",
    year=2016
)

print(f"Số VĐV Olympic 2016: {len(df_2016)}")
```

#### Lọc theo loại huy chương

```python
from modules.analysis import filter_medals

# Chỉ lấy VĐV đạt huy chương Vàng
df_gold = filter_medals(df_clean, "Gold")

print(f"Số VĐV đạt huy chương Vàng: {len(df_gold)}")
```

### Làm sạch dữ liệu nâng cao

```python
from modules.analysis import clean_team_name, clean_event_name, extract_nickname

# Làm sạch tên đội (loại bỏ số và dấu gạch ngang)
df_clean = clean_team_name(df_clean)

# Làm sạch tên sự kiện (cắt bỏ tên môn bị lặp)
df_clean = clean_event_name(df_clean)

# Trích xuất biệt danh
df_clean = extract_nickname(df_clean)

# Kiểm tra kết quả
print(df_clean[['Name', 'Nickname']].head())
```

### Phân tích theo nhóm tuổi

```python
from modules.analysis import analyze_medals_and_participants_by_age

# Phân tích theo nhóm tuổi
age_stats = analyze_medals_and_participants_by_age(df_clean)

print("Thống kê theo nhóm tuổi:")
print(age_stats)
```

### Phân tích thế mạnh của quốc gia

```python
from modules.analysis import analyze_dominant_sports

# Phân tích thế mạnh
dominant = analyze_dominant_sports(df_clean)

# Xem thế mạnh của USA
usa_sports = dominant[dominant['Team'] == 'United States']
print("Thế mạnh của USA:")
print(usa_sports.sort_values('Medal_Count', ascending=False).head(10))
```

### Chuẩn hóa dữ liệu (cho Machine Learning)

```python
from modules.data_cleaning import scale_data

# Chuẩn hóa dữ liệu
df_scaled = scale_data(df_clean)

# Kiểm tra kết quả
print("Dữ liệu đã được chuẩn hóa:")
print(df_scaled[['Age', 'Height', 'Weight']].head())
print(df_scaled[['Age', 'Height', 'Weight']].describe())
```

### Xuất dữ liệu (Export)

#### Đảm bảo thư mục output tồn tại

```python
from modules.export_data import ensure_output_dir

# Tự động tạo thư mục output nếu chưa có
output_dir = ensure_output_dir('output')
print(f"Thư mục output: {output_dir}")
```

#### Xuất đơn giản

```python
from modules.export_data import export_to_csv, export_to_excel

# Xuất ra CSV (tự động tạo thư mục nếu chưa có)
export_to_csv(df_clean, "data.csv", output_dir='output')

# Xuất ra Excel
export_to_excel(df_clean, "data.xlsx", sheet_name="Athletes", output_dir='output')
```

#### Xuất nhiều sheet vào một file Excel

```python
from modules.export_data import export_multiple_sheets

# Tạo dictionary với các DataFrame
sheets = {
    'Medal Tally': medal_tally,
    'Gender Stats': gender_stats,
    'Age Analysis': age_stats
}

# Xuất tất cả vào một file Excel (tự động tạo thư mục output)
export_multiple_sheets(sheets, "analysis.xlsx", output_dir='output')
```

#### Xuất báo cáo tổng hợp

```python
from modules.export_data import export_full_report, export_vietnam_specific
import modules.analysis as analysis_module

# Xuất báo cáo tổng hợp (tự động tạo thư mục output)
# File sẽ có tên: Olympic_Full_Report_YYYYMMDD_HHMMSS.xlsx
export_full_report(df_clean, analysis_module)

# Xuất báo cáo chuyên sâu về Việt Nam
# File sẽ có tên: Vietnam_Olympic_History.xlsx
export_vietnam_specific(df_clean, analysis_module)
```

**Lưu ý:** Tất cả các hàm export đều tự động tạo thư mục `output` nếu chưa tồn tại. Bạn không cần tạo thư mục thủ công.
```

#### Xuất dữ liệu đã lọc

```python
from modules.export_data import export_to_csv, export_to_excel
from modules.analysis import filter_data_string

# Lọc dữ liệu Việt Nam
df_vietnam = filter_data_string(df_clean, team="Vietnam")

# Xuất với định dạng tùy chọn
export_to_csv(df_vietnam, "vietnam.csv", output_dir='output')
export_to_excel(df_vietnam, "vietnam.xlsx", sheet_name="Vietnam", output_dir='output')
```

## 📊 Ví dụ thực tế

### Ví dụ 1: Phân tích Olympic 2016

```python
from modules.data_cleaning import load_data
from modules.data_cleaning import clean_data
from modules.analysis import (
    filter_season_and_year,
    calculate_medal_tally,
    analyze_gender_participation
)
from modules.visualization import plot_top_medals, plot_gender_trend

# Tải và làm sạch
df = load_data("data/athlete_events.csv")
df_clean = clean_data(df)

# Lọc chỉ Olympic 2016
df_2016 = filter_season_and_year(df_clean, season="Summer", year=2016)

# Phân tích
medal_tally_2016 = calculate_medal_tally(df_2016)
print("Bảng tổng sắp Olympic 2016:")
print(medal_tally_2016.head(10))

# Vẽ biểu đồ
plot_top_medals(df_2016, top_n=10)
```

### Ví dụ 2: So sánh giữa các kỳ Olympic

```python
# So sánh 2008, 2012, 2016
years = [2008, 2012, 2016]
results = {}

for year in years:
    df_year = filter_season_and_year(df_clean, season="Summer", year=year)
    medal_tally = calculate_medal_tally(df_year)
    results[year] = medal_tally.head(5)

# In kết quả
for year, medals in results.items():
    print(f"\nTop 5 Olympic {year}:")
    print(medals)
```

### Ví dụ 3: Phân tích Việt Nam chi tiết

```python
from modules.analysis import filter_data_string
from modules.visualization import plot_vietnam_stats, plot_vietnam_details

# Lọc dữ liệu Việt Nam
df_vietnam = filter_data_string(df_clean, team="Vietnam")

# Thống kê
print(f"Tổng số VĐV Việt Nam: {df_vietnam['ID'].nunique()}")
print(f"Số kỳ Olympic tham gia: {df_vietnam['Year'].nunique()}")

# Phân tích theo năm
vn_by_year = df_vietnam.groupby('Year')['ID'].nunique()
print("\nSố VĐV theo năm:")
print(vn_by_year)

# Vẽ biểu đồ
plot_vietnam_stats(df_clean)
plot_vietnam_details(df_clean)
```

### Ví dụ 4: Phân tích môn thể thao cụ thể

```python
# Phân tích môn Bơi lội
df_swimming = filter_data_string(df_clean, sport="Swimming")

# Thống kê
print(f"Tổng số VĐV Bơi lội: {df_swimming['ID'].nunique()}")
print(f"Số quốc gia: {df_swimming['NOC'].nunique()}")

# Top quốc gia trong Bơi lội
swimming_medals = filter_medals(df_swimming, "Gold")
top_countries = swimming_medals['NOC'].value_counts().head(10)
print("\nTop 10 quốc gia đạt nhiều huy chương Vàng Bơi lội:")
print(top_countries)
```

### Ví dụ 5: Phân tích thể chất theo môn

```python
from modules.analysis import analyze_physique_all_athletes

# Phân tích thể chất
physique = analyze_physique_all_athletes(df_clean)

# Môn có VĐV cao nhất
print("Top 5 môn có VĐV cao nhất:")
print(physique.nlargest(5, 'Height')[['Height']])

# Môn có VĐV nặng nhất
print("\nTop 5 môn có VĐV nặng nhất:")
print(physique.nlargest(5, 'Weight')[['Weight']])

# Môn có BMI cao nhất
print("\nTop 5 môn có BMI cao nhất:")
print(physique.nlargest(5, 'BMI')[['BMI']])
```

## 🐛 Troubleshooting

### Lỗi: FileNotFoundError

**Nguyên nhân:** Không tìm thấy file dữ liệu

**Giải pháp:**
```python
# Kiểm tra đường dẫn
import os
print(os.path.exists("data/athlete_events.csv"))

# Sử dụng đường dẫn tuyệt đối nếu cần
df = load_data(r"D:\python\project\data\athlete_events.csv")
```

### Lỗi: SettingWithCopyWarning

**Nguyên nhân:** Thao tác trên bản copy của DataFrame

**Giải pháp:**
```python
# Sử dụng .copy() khi cần
df_new = df.copy()
df_new['NewColumn'] = df_new['OldColumn'] * 2

# Hoặc sử dụng .loc[]
df.loc[:, 'NewColumn'] = df['OldColumn'] * 2
```

### Lỗi: Memory Error

**Nguyên nhân:** Dữ liệu quá lớn

**Giải pháp:**
```python
# Xử lý theo chunk
chunk_size = 10000
for chunk in pd.read_csv("data/athlete_events.csv", chunksize=chunk_size):
    # Xử lý từng chunk
    process_chunk(chunk)
```

### Lỗi: ModuleNotFoundError

**Nguyên nhân:** Chưa cài đặt thư viện

**Giải pháp:**
```bash
# Cài đặt lại
pip install -r requirements.txt

# Hoặc cài từng thư viện
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl
```

### Biểu đồ không hiển thị

**Nguyên nhân:** Thiếu cấu hình matplotlib

**Giải pháp:**
```python
# Thêm vào đầu script
import matplotlib
matplotlib.use('TkAgg')  # Hoặc 'Qt5Agg' tùy hệ thống

# Hoặc trong Jupyter
%matplotlib inline
```

### Kết quả phân tích không chính xác

**Nguyên nhân:** Chưa làm sạch dữ liệu

**Giải pháp:**
```python
# Luôn làm sạch dữ liệu trước khi phân tích
df_clean = clean_data(df)

# Kiểm tra dữ liệu sau khi làm sạch
print(df_clean.isnull().sum())
print(df_clean.describe())
```

## 💡 Tips và Best Practices

### 1. Luôn làm sạch dữ liệu trước

```python
# ✅ Đúng
df_clean = clean_data(df)
result = calculate_medal_tally(df_clean)

# ❌ Sai
result = calculate_medal_tally(df)  # Dữ liệu chưa được làm sạch
```

### 2. Lưu kết quả trung gian

```python
from modules.export_data import export_to_csv, export_to_excel

# Lưu dữ liệu đã làm sạch
export_to_csv(df_clean, "data/athlete_events_clean.csv")

# Lưu kết quả phân tích
export_to_excel(medal_tally, "results/medal_tally.xlsx", sheet_name="Medal Tally")
```

### 3. Sử dụng Jupyter Notebook cho phân tích

- Dễ dàng xem kết quả từng bước
- Có thể chỉnh sửa và chạy lại từng cell
- Dễ dàng trình bày kết quả

### 4. Kiểm tra dữ liệu thường xuyên

```python
# Kiểm tra sau mỗi bước
print(f"Số dòng: {len(df)}")
print(f"Số cột: {len(df.columns)}")
print(df.head())
print(df.info())
```

### 5. Tối ưu hiệu suất

```python
# Sử dụng vectorization thay vì loop
# ✅ Đúng
df['NewColumn'] = df['OldColumn'] * 2

# ❌ Chậm
for idx, row in df.iterrows():
    df.loc[idx, 'NewColumn'] = row['OldColumn'] * 2
```

## 📚 Tài liệu tham khảo

- [README.md](../README.md) - Tổng quan dự án
- [ARCHITECTURE.md](ARCHITECTURE.md) - Kiến trúc và luồng hoạt động
- [DATA_INSIGHTS.md](DATA_INSIGHTS.md) - Dữ liệu và insights

## ❓ Câu hỏi thường gặp

**Q: Làm sao để thêm môn thể thao mới vào phân tích?**  
A: Dữ liệu sẽ tự động cập nhật khi file CSV được cập nhật. Chỉ cần reload dữ liệu.

**Q: Có thể phân tích dữ liệu Olympic mới nhất không?**  
A: Có, chỉ cần thêm dữ liệu mới vào file CSV và chạy lại các hàm phân tích.

**Q: Làm sao để xuất kết quả ra file?**  
A: Sử dụng module `export_data.py`. Tất cả các hàm đều tự động tạo thư mục `output`:
```python
from modules.export_data import export_to_csv, export_to_excel, export_multiple_sheets, export_full_report
import modules.analysis as analysis_module

# Đảm bảo thư mục output tồn tại (tùy chọn, vì các hàm export đã tự động tạo)
from modules.export_data import ensure_output_dir
output_dir = ensure_output_dir('output')

# Xuất đơn giản
export_to_csv(df, "data.csv", output_dir='output')
export_to_excel(df, "data.xlsx", sheet_name="Data", output_dir='output')

# Xuất nhiều sheet
sheets_dict = {
    'Medal Tally': medal_tally,
    'Gender Stats': gender_stats
}
export_multiple_sheets(sheets_dict, "analysis.xlsx", output_dir='output')

# Xuất báo cáo tổng hợp
export_full_report(df_clean, analysis_module)
```

**Q: Có thể chạy trực tiếp module export không?**  
A: Có, chạy lệnh:
```bash
python modules/export_data.py
```
Sẽ tự động tạo thư mục `output` và xuất dữ liệu mẫu để test các chức năng export.

**Q: Có thể tùy chỉnh biểu đồ không?**  
A: Có, chỉnh sửa các hàm trong `modules/visualization.py` hoặc tạo hàm mới.

---

**Hướng dẫn này cung cấp các ví dụ thực tế để sử dụng dự án một cách hiệu quả.**

