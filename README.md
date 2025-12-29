# Dự án Phân tích Dữ liệu Olympic (120 năm)

## 📋 Mô tả dự án

Dự án này là một hệ thống phân tích dữ liệu lịch sử Olympic trong suốt 120 năm (từ năm 1896 đến 2016), được xây dựng bằng Python với mục đích:

- **Phân tích xu hướng phát triển** của thể thao thế giới qua các kỳ Olympic
- **Thống kê và xếp hạng** các quốc gia theo thành tích huy chương
- **Nghiên cứu các yếu tố ngoại cảnh** ảnh hưởng đến thành tích (chính trị, lợi thế sân nhà)
- **Tập trung vào dấu ấn Việt Nam** tại đấu trường Olympic

Dự án được thiết kế theo mô hình modular, tách biệt các chức năng để dễ dàng bảo trì và mở rộng.

## 🎯 Mục tiêu chính

1. **Xu hướng phát triển thể thao:**
   - Số lượng vận động viên tham gia qua các năm
   - Phân tích về giới tính (Nam/Nữ)
   - Sự thay đổi về thể chất của vận động viên

2. **Bảng tổng sắp huy chương:**
   - Xếp hạng các quốc gia theo số lượng huy chương
   - Phân tích thế mạnh của từng quốc gia theo môn thể thao
   - So sánh thành tích qua các kỳ Olympic

3. **Yếu tố ngoại cảnh:**
   - Ảnh hưởng của chiến tranh lạnh (1980, 1984)
   - Lợi thế sân nhà (ví dụ: Trung Quốc 2008)
   - Số lượng quốc gia tham dự qua các năm

4. **Dấu ấn Việt Nam:**
   - Hành trình tham gia Olympic
   - Số lượng vận động viên qua các năm
   - Các môn thể thao thế mạnh
   - Danh sách huy chương đạt được

## 📁 Cấu trúc dự án

```
project/
│
├── data/
│   └── athlete_events.csv          # File dữ liệu (CSV)
│
├── docs/
│   ├── ARCHITECTURE.md             # Tài liệu kiến trúc và luồng hoạt động
│   ├── DATA_INSIGHTS.md            # Insights từ dữ liệu
│   └── USER_GUIDE.md               # Hướng dẫn sử dụng chi tiết
│
├── modules/
│   ├── __init__.py                 # Khởi tạo package
│   ├── data_cleaning.py            # Module tải và làm sạch dữ liệu
│   ├── analysis.py                 # Module phân tích và thống kê
│   ├── visualization.py            # Module vẽ biểu đồ
│   └── export_data.py              # Module xuất dữ liệu
│
├── main.py                         # File chính (chưa hoàn thiện)
├── UI.py                           # Giao diện người dùng (chưa hoàn thiện)
├── matplotlib.ipynb                # Notebook Jupyter chứa workflow đầy đủ
└── requirements.txt                # Danh sách thư viện cần thiết
```

## 🔄 Luồng hoạt động chi tiết

### Bước 1: Tải dữ liệu (Data Loading)

**Module:** `modules/data_cleaning.py`

```python
load_data(file_path) → DataFrame
```

- Đọc file CSV từ đường dẫn được chỉ định
- Xử lý lỗi nếu file không tồn tại
- Trả về DataFrame chứa dữ liệu thô

**Dữ liệu đầu vào:** File CSV `athlete_events.csv` với các cột:
- ID, Name, Sex, Age, Height, Weight
- Team, NOC (National Olympic Committee)
- Games, Year, Season, City
- Sport, Event, Medal

### Bước 2: Làm sạch dữ liệu (Data Cleaning)

**Module:** `modules/data_cleaning.py`

```python
clean_data(df) → DataFrame (đã làm sạch)
```

**Quy trình làm sạch:**

1. **Xóa dòng trùng lặp:**
   - Loại bỏ các bản ghi trùng lặp hoàn toàn

2. **Sửa định dạng sai:**
   - Chuyển đổi các cột số (Age, Height, Weight) sang kiểu numeric
   - Xử lý các giá trị không thể chuyển đổi → NaN

3. **Xử lý giá trị thiếu (Missing Values):**
   - **Cột số:** Thay thế NaN bằng giá trị trung bình (mean) của cột
   - **Cột chuỗi (trừ Medal):** Thay thế NaN bằng giá trị xuất hiện nhiều nhất (mode)
   - **Cột Medal:** Thay thế NaN bằng "No Medal"

4. **Sửa gán nhãn sai:**
   - Chuẩn hóa tên huy chương:
     - "Gold " → "Gold"
     - "gold" → "Gold"
     - "SILVER" → "Silver"
     - "BRONZE" → "Bronze"

5. **Xử lý Outlier (giá trị bất thường):**
   - Sử dụng phương pháp IQR (Interquartile Range)
   - Tính Q1 (25%), Q3 (75%), IQR = Q3 - Q1
   - Xác định ngưỡng: Lower = Q1 - 1.5×IQR, Upper = Q3 + 1.5×IQR
   - Capping: Giá trị < Lower → Lower, Giá trị > Upper → Upper
   - Làm tròn đến 2 chữ số thập phân

### Bước 3: Chuẩn hóa dữ liệu (Data Scaling) - Tùy chọn

**Module:** `modules/data_cleaning.py`

```python
scale_data(df) → DataFrame (đã chuẩn hóa)
```

- Sử dụng StandardScaler từ scikit-learn
- Chuẩn hóa các cột số: Age, Height, Weight
- Mục đích: Chuẩn bị dữ liệu cho các thuật toán machine learning

### Bước 4: Phân tích dữ liệu (Data Analysis)

**Module:** `modules/analysis.py`

#### 4.1. Làm sạch dữ liệu nâng cao

- **`clean_team_name()`:** Loại bỏ số và dấu gạch ngang trong tên đội
  - Ví dụ: "China-1" → "China"
  
- **`clean_event_name()`:** Cắt bỏ tên môn thể thao bị lặp trong tên sự kiện
  - Ví dụ: Sport="Basketball", Event="Basketball Men's Basketball" → "Men's Basketball"
  
- **`extract_nickname()`:** Trích xuất biệt danh từ tên vận động viên
  - Tìm trong dấu ngoặc kép "" hoặc ngoặc đơn ()

#### 4.2. Lọc dữ liệu

- **`filter_data_number()`:** Lọc theo điều kiện số
  - Tham số: age, height, weight, year, sex
  - Điều kiện: >= (lớn hơn hoặc bằng)
  
- **`filter_data_string()`:** Lọc theo điều kiện chuỗi (chính xác)
  - Tham số: team, noc, season, city, sport, sex
  
- **`filter_season_and_year()`:** Lọc theo mùa và năm cụ thể
  - Ví dụ: Chỉ lấy Olympic Mùa hè 2016
  
- **`filter_medals()`:** Lọc theo loại huy chương
  - Tham số: type_medal ("Gold", "Silver", "Bronze")

#### 4.3. Thống kê và phân tích

- **`calculate_medal_tally()`:** Tính tổng sắp huy chương theo quốc gia
  - Xử lý môn đồng đội (drop duplicates)
  - Tạo bảng pivot với các cột: Gold, Silver, Bronze
  - Sắp xếp giảm dần theo số huy chương Vàng

- **`analyze_gender_participation()`:** Phân tích số lượng Nam/Nữ qua các năm
  - Đếm số lượng unique ID theo Year và Sex
  - Trả về DataFrame với 2 cột: M (Nam), F (Nữ)

- **`analyze_medals_and_participants_by_age()`:** Thống kê theo nhóm tuổi
  - Nhóm tuổi: U20, 20-30, 30-40, 40-50, Over 50
  - Tính: Số lượng huy chương, Số lượng người tham gia, Tỷ lệ huy chương

- **`analyze_physique_all_athletes()`:** Phân tích thể chất theo môn
  - Tính trung bình: Chiều cao, Cân nặng, BMI
  - Sắp xếp giảm dần theo Cân nặng → Chiều cao → BMI

- **`analyze_dominant_sports()`:** Thống kê thế mạnh của quốc gia
  - Số lượng huy chương theo Team và Sport
  - Xử lý môn đồng đội (drop duplicates)
  - Sắp xếp theo Team (A-Z) và Medal_Count (giảm dần)

### Bước 5: Trực quan hóa dữ liệu (Visualization)

**Module:** `modules/visualization.py`

#### 5.1. Biểu đồ cơ bản

- **`plot_gender_trend()`:** Xu hướng giới tính qua các năm
  - Đường biểu diễn số lượng VĐV Nam và Nữ theo thời gian
  
- **`plot_top_medals()`:** Top quốc gia đạt nhiều huy chương nhất
  - Biểu đồ cột ngang, mặc định top 10
  
- **`plot_physical_distribution()`:** Phân bố thể chất
  - 3 histogram: Tuổi, Chiều cao, Cân nặng
  - Hiển thị đường trung bình
  
- **`plot_physical_comparison_by_sport()`:** So sánh thể chất giữa các môn
  - Boxplot Chiều cao và Cân nặng của top 10 môn phổ biến

#### 5.2. Biểu đồ nâng cao

- **`plot_host_advantage_china()`:** Lợi thế sân nhà Trung Quốc
  - So sánh số huy chương của Trung Quốc tại Olympic 2008 vs các năm khác
  
- **`plot_geopolitics_impact()`:** Ảnh hưởng chiến tranh lạnh
  - Biểu đồ số lượng quốc gia tham dự qua các năm
  - Highlight các năm 1980 (Moscow) và 1984 (Los Angeles)
  
- **`plot_body_evolution_100m()`:** Tiến hóa thể chất môn 100m
  - Regression plot: Chiều cao và Cân nặng theo thời gian
  
- **`plot_athlete_clustering()`:** Phân cụm vận động viên
  - K-means clustering (k=3) dựa trên Tuổi và Cân nặng
  - Phân loại: Nhẹ/Trẻ, Trung bình, Nặng/Già

#### 5.3. Biểu đồ về Việt Nam

- **`plot_vietnam_stats()`:** Thống kê Việt Nam
  - Biểu đồ 1: Số lượng VĐV Việt Nam qua các năm
  - Biểu đồ 2: Top 5 môn thể thao Việt Nam tham gia nhiều nhất
  
- **`plot_vietnam_details()`:** Danh sách huy chương chi tiết
  - Bảng hiển thị: Năm, VĐV, Môn, Loại huy chương

### Bước 6: Xuất dữ liệu (Export)

**Module:** `modules/export_data.py`

#### 6.1. Hàm hỗ trợ

- **`ensure_output_dir()`:** Đảm bảo thư mục output tồn tại
  - Tự động tạo thư mục `output` nếu chưa có
  - Trả về đường dẫn tuyệt đối của thư mục
  - Được sử dụng bởi tất cả các hàm export

#### 6.2. Xuất cơ bản

- **`export_to_csv(df, filename, output_dir=None, index=False)`:** Xuất DataFrame ra file CSV
  - Tự động tạo thư mục `output` nếu chưa tồn tại
  - Hỗ trợ encoding UTF-8 với BOM (hiển thị tiếng Việt đúng trong Excel)
  - Kiểm tra DataFrame hợp lệ trước khi xuất
  
- **`export_to_excel(df, filename, sheet_name='Sheet1', output_dir=None, index=False)`:** Xuất DataFrame ra file Excel (1 sheet)
  - Hỗ trợ tùy chỉnh tên sheet
  - Sử dụng engine openpyxl
  - Tự động tạo thư mục output

#### 6.3. Xuất nâng cao

- **`export_multiple_sheets(data_dict, filename, output_dir=None)`:** Xuất nhiều DataFrame vào 1 file Excel
  - Nhận dictionary với key là tên sheet, value là DataFrame
  - Mỗi DataFrame là một sheet riêng
  - Tự động lọc bỏ DataFrame None hoặc rỗng
  - Tự động cắt tên sheet nếu quá 31 ký tự (giới hạn Excel)
  
- **`export_full_report(df_clean, analysis_module)`:** Xuất báo cáo tổng hợp
  - Tự động tạo thư mục `output` nếu chưa có
  - Tạo file Excel với nhiều sheet
  - Tên file có timestamp (ví dụ: `Olympic_Full_Report_20241201_143022.xlsx`)
  - Bao gồm: Top 50 Rows, Physical Stats, Vietnam Medals
  - Sử dụng try-except để xử lý lỗi từng phần phân tích
  
- **`export_vietnam_specific(df_clean, analysis_module)`:** Xuất báo cáo chuyên sâu về Việt Nam
  - Tự động tạo thư mục `output`
  - Tạo file Excel với tên: `Vietnam_Olympic_History.xlsx`
  - Bao gồm: Danh Sách Huy Chương, Lịch Sử Tham Gia

#### 6.4. Chạy trực tiếp module

File `export_data.py` có thể chạy trực tiếp để demo:
```bash
python modules/export_data.py
```

Sẽ tự động:
- Tạo thư mục `output` nếu chưa có
- Tạo dữ liệu mẫu và xuất ra các file: CSV, Excel, JSON, Excel nhiều sheet

**Ví dụ sử dụng:**
```python
from modules.export_data import export_to_csv, export_to_excel, export_multiple_sheets, export_full_report
import modules.analysis as analysis_module

# Đảm bảo thư mục output tồn tại
from modules.export_data import ensure_output_dir
output_dir = ensure_output_dir('output')

# Xuất đơn giản
export_to_csv(df_clean, "data.csv", output_dir='output')
export_to_excel(df_clean, "data.xlsx", sheet_name="Athletes", output_dir='output')

# Xuất nhiều sheet
sheets_dict = {
    'Medal Tally': medal_tally,
    'Gender Stats': gender_stats
}
export_multiple_sheets(sheets_dict, "analysis.xlsx", output_dir='output')

# Xuất báo cáo tổng hợp
export_full_report(df_clean, analysis_module)

# Xuất báo cáo Việt Nam
from modules.export_data import export_vietnam_specific
export_vietnam_specific(df_clean, analysis_module)
```

### Bước 7: Giao diện người dùng (UI) - Chưa hoàn thiện

**Module:** `modules/UI.py`

- Dự kiến: Tạo giao diện tương tác để người dùng dễ dàng sử dụng

## 🚀 Hướng dẫn sử dụng

### Cài đặt môi trường

```bash
# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### Sử dụng qua Notebook

1. Mở file `matplotlib.ipynb` trong Jupyter Notebook
2. Chạy các cell theo thứ tự
3. Xem kết quả phân tích và biểu đồ

### Sử dụng qua Python script

```python
# Ví dụ sử dụng
from modules.data_cleaning import load_data, clean_data
from modules.analysis import calculate_medal_tally, analyze_gender_participation
from modules.visualization import plot_top_medals
from modules.export_data import export_analysis_results

# 1. Tải dữ liệu
df = load_data("data/athlete_events.csv")

# 2. Làm sạch dữ liệu
df_clean = clean_data(df)

# 3. Phân tích
medal_tally = calculate_medal_tally(df_clean)
gender_stats = analyze_gender_participation(df_clean)
print(medal_tally.head(10))

# 4. Vẽ biểu đồ
plot_top_medals(df_clean, top_n=10)

# 5. Xuất kết quả (tự động tạo thư mục output)
from modules.export_data import export_multiple_sheets, export_full_report
import modules.analysis as analysis_module

# Xuất nhiều sheet
sheets_dict = {
    'Medal Tally': medal_tally,
    'Gender Stats': gender_stats
}
export_multiple_sheets(sheets_dict, "olympic_analysis.xlsx", output_dir='output')

# Hoặc xuất báo cáo tổng hợp
export_full_report(df_clean, analysis_module)
```

### Chạy trực tiếp module export

```bash
# Chạy file export_data.py để demo các chức năng export
python modules/export_data.py
```

Sẽ tự động:
- Tạo thư mục `output` nếu chưa có
- Tạo dữ liệu mẫu và xuất ra các định dạng: CSV, Excel, JSON

## 📊 Kết quả phân tích chính

### 1. Xu hướng phát triển

- Số lượng vận động viên tăng dần qua các năm
- Tỷ lệ nữ vận động viên tăng đáng kể từ những năm 1980
- Thể chất vận động viên có xu hướng cải thiện (chiều cao, cân nặng)

### 2. Bảng tổng sắp

- Top quốc gia: USA, Soviet Union, Germany, Great Britain, France...
- Mỗi quốc gia có thế mạnh riêng về môn thể thao

### 3. Yếu tố ngoại cảnh

- **Chiến tranh lạnh:** Số lượng quốc gia tham dự giảm đáng kể năm 1980 và 1984
- **Lợi thế sân nhà:** Trung Quốc đạt thành tích cao nhất tại Olympic 2008

### 4. Dấu ấn Việt Nam

- Bắt đầu tham gia đông đảo từ năm 1980
- Thế mạnh: Bơi lội, Điền kinh, Bắn súng, Cử tạ
- **Huy chương:**
  - 2000: Trần Hiếu Ngân - Bạc Taekwondo (lịch sử)
  - 2008: Hoàng Anh Tuấn - Bạc Cử tạ
  - 2016: Hoàng Xuân Vinh - Vàng và Bạc Bắn súng

## 🛠️ Công nghệ sử dụng

- **Python 3.x**
- **Pandas:** Xử lý và phân tích dữ liệu
- **NumPy:** Tính toán số học
- **Matplotlib & Seaborn:** Vẽ biểu đồ
- **Scikit-learn:** Machine learning (clustering, scaling)
- **Openpyxl:** Xử lý file Excel
- **Streamlit:** Giao diện người dùng (dự kiến)
- **Jupyter Notebook:** Môi trường phát triển và trình bày

## 📝 Lưu ý

1. **File dữ liệu:** Cần có file `athlete_events.csv` trong thư mục `data/`
2. **Cảnh báo:** Có một số SettingWithCopyWarning trong `data_cleaning.py` cần được xử lý
3. **Chưa hoàn thiện:** 
   - `main.py` - File chính để chạy toàn bộ workflow
   - `UI.py` - Module giao diện

## 🔮 Hướng phát triển

- [x] Hoàn thiện module xuất dữ liệu
- [ ] Tạo giao diện người dùng (Streamlit hoặc Flask)
- [ ] Thêm các phân tích machine learning nâng cao
- [ ] Tối ưu hóa hiệu suất xử lý dữ liệu lớn
- [ ] Thêm unit tests cho các modules
- [ ] Tạo API để truy vấn dữ liệu
- [ ] Thêm hỗ trợ xuất PDF cho báo cáo
- [ ] Tích hợp export vào UI module

## 📚 Tài liệu tham khảo

Để tìm hiểu chi tiết hơn về dự án, vui lòng xem các tài liệu trong thư mục `docs/`:

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Kiến trúc hệ thống và luồng hoạt động chi tiết
- **[DATA_INSIGHTS.md](docs/DATA_INSIGHTS.md)** - Insights và phân tích từ dữ liệu
- **[USER_GUIDE.md](docs/USER_GUIDE.md)** - Hướng dẫn sử dụng chi tiết với ví dụ

## 👥 Tác giả

Dự án được phát triển để phân tích và hiểu rõ hơn về lịch sử Olympic và thành tích của Việt Nam.

---

**Phiên bản:** 1.0  
**Ngày cập nhật:** 2024

