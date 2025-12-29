# Kiến trúc và Luồng hoạt động chi tiết

## 🏗️ Kiến trúc tổng quan

Dự án được thiết kế theo mô hình **Modular Architecture** (Kiến trúc mô-đun), cho phép:

- **Tách biệt trách nhiệm:** Mỗi module có một chức năng cụ thể
- **Dễ bảo trì:** Sửa đổi một module không ảnh hưởng đến các module khác
- **Tái sử dụng:** Các hàm có thể được import và sử dụng ở nhiều nơi
- **Mở rộng:** Dễ dàng thêm tính năng mới

## 📐 Sơ đồ kiến trúc

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                     │
│  (Jupyter Notebook / Python Script / UI - Future)           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Analysis   │  │ Visualization│  │   Export     │       │
│  │   Module     │  │    Module    │  │   Module     │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │               │
└─────────┼─────────────────┼─────────────────┼──────────────
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA PROCESSING LAYER                    │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ Data Loader  │  │ Data Cleaning │  │ Data Scaled  │    │
│  │   Module     │  │    Module     │  │   Module      │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                 │                 │              │
└─────────┼─────────────────┼─────────────────┼──────────────┘
          │                 │                 │
          └─────────────────┴─────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA SOURCE                             │
│              athlete_events.csv (CSV file)                   │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Luồng dữ liệu chi tiết

### Phase 1: Data Ingestion (Thu thập dữ liệu)

```
┌─────────────┐
│ CSV File    │
│ (Raw Data)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  data_loader.py     │
│  load_data()         │
│                     │
│  - Read CSV         │
│  - Error handling   │
│  - Return DataFrame │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  DataFrame (Raw)    │
│  - 269,731 rows     │
│  - 15 columns       │
└─────────────────────┘
```

**Input:** File CSV `athlete_events.csv`  
**Output:** Pandas DataFrame chứa dữ liệu thô  
**Xử lý lỗi:** 
- FileNotFoundError → Thông báo lỗi và trả về None
- Exception khác → In lỗi và trả về None

### Phase 2: Data Cleaning (Làm sạch dữ liệu)

```
┌─────────────────────┐
│  DataFrame (Raw)    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│         data_cleaning.py                │
│         clean_data()                     │
│                                         │
│  Step 1: Remove duplicates             │
│  Step 2: Fix data types                │
│  Step 3: Handle missing values        │
│  Step 4: Fix incorrect labels          │
│  Step 5: Handle outliers (IQR)         │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────┐
│ DataFrame (Clean)   │
│ - No duplicates     │
│ - Correct types     │
│ - No missing values │
│ - No outliers       │
└─────────────────────┘
```

#### Chi tiết các bước làm sạch:

**Step 1: Remove Duplicates**
```python
df = df.drop_duplicates()
```
- Loại bỏ các dòng hoàn toàn giống nhau

**Step 2: Fix Data Types**
```python
df[col] = pd.to_numeric(df[col], errors="coerce")
```
- Chuyển Age, Height, Weight sang numeric
- Giá trị không hợp lệ → NaN

**Step 3: Handle Missing Values**
```python
# Numeric columns: Fill with mean
df[col] = df[col].fillna(df[col].mean())

# Categorical columns (except Medal): Fill with mode
df[col] = df[col].fillna(df[col].mode()[0])

# Medal column: Fill with "No Medal"
df["Medal"] = df["Medal"].fillna("No Medal")
```

**Step 4: Fix Incorrect Labels**
```python
df["Medal"] = df["Medal"].replace({
    "Gold ": "Gold",
    "gold": "Gold",
    "SILVER": "Silver",
    "BRONZE": "Bronze"
})
```

**Step 5: Handle Outliers (IQR Method)**
```python
Q1 = df[col].quantile(0.25)
Q3 = df[col].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
df[col] = df[col].clip(lower, upper)
```

### Phase 3: Data Transformation (Chuẩn hóa - Tùy chọn)

```
┌─────────────────────┐
│ DataFrame (Clean)   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  data_scaled.py     │
│  scale_data()       │
│                     │
│  StandardScaler     │
│  - Age              │
│  - Height           │
│  - Weight           │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ DataFrame (Scaled)  │
│ - Normalized values │
└─────────────────────┘
```

**Mục đích:** Chuẩn bị dữ liệu cho machine learning algorithms  
**Phương pháp:** StandardScaler (z-score normalization)

### Phase 4: Data Analysis (Phân tích dữ liệu)

```
┌─────────────────────┐
│ DataFrame (Clean)   │
└──────┬──────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│           analysis.py                        │
│                                              │
│  ┌────────────────────────────────────┐      │
│  │  Data Cleaning (Advanced)          │      │
│  │  - clean_team_name()               │      │
│  │  - clean_event_name()              │      │
│  │  - extract_nickname()              │      │
│  └────────────────────────────────────┘      │
│                                              │
│  ┌────────────────────────────────────┐      │
│  │  Data Filtering                    │      │
│  │  - filter_data_number()            │      │
│  │  - filter_data_string()            │      │
│  │  - filter_season_and_year()        │      │
│  │  - filter_medals()                 │      │
│  └────────────────────────────────────┘      │
│                                              │
│  ┌────────────────────────────────────┐      │
│  │  Statistical Analysis              │      │
│  │  - calculate_medal_tally()         │      │
│  │  - analyze_gender_participation()  │      │
│  │  - analyze_medals_by_age()         │      │
│  │  - analyze_physique()              │      │
│  │  - analyze_dominant_sports()       │      │
│  └────────────────────────────────────┘      │
└──────┬──────────────────────────────────────┘
       │
       ▼
┌─────────────────────┐
│ Analysis Results    │
│ - Medal Tally       │
│ - Gender Stats      │
│ - Age Groups        │
│ - Physique Stats    │
│ - Sport Dominance   │
└─────────────────────┘
```

#### Chi tiết các hàm phân tích:

**1. calculate_medal_tally()**
```
Input: DataFrame
Process:
  1. Drop duplicates (handle team sports)
  2. Filter rows with medals
  3. Pivot table: NOC × Medal type
  4. Count medals per country
  5. Sort by Gold (descending)
Output: DataFrame with columns [NOC, Gold, Silver, Bronze]
```

**2. analyze_gender_participation()**
```
Input: DataFrame
Process:
  1. Group by Year and Sex
  2. Count unique IDs
  3. Unstack to create columns M and F
Output: DataFrame with columns [Year, M, F]
```

**3. analyze_medals_and_participants_by_age()**
```
Input: DataFrame
Process:
  1. Filter rows with Age
  2. Create age bins: [0, 20, 30, 40, 50, 100]
  3. Group by AgeGroup
  4. Count medals and participants
  5. Calculate medal ratio
Output: DataFrame with [AgeGroup, Medal_Count, Participant_Count, Medal_Ratio]
```

### Phase 5: Data Visualization (Trực quan hóa)

```
┌─────────────────────┐
│ DataFrame (Clean)    │
│ Analysis Results        │
└──────┬─────────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│        visualization.py                     │
│                                             │
│  ┌────────────────────────────────────┐    │
│  │  Basic Charts                      │    │
│  │  - plot_gender_trend()             │    │
│  │  - plot_top_medals()               │    │
│  │  - plot_physical_distribution()   │    │
│  │  - plot_physical_comparison()      │    │
│  └────────────────────────────────────┘    │
│                                             │
│  ┌────────────────────────────────────┐    │
│  │  Advanced Charts                   │    │
│  │  - plot_host_advantage_china()     │    │
│  │  - plot_geopolitics_impact()       │    │
│  │  - plot_body_evolution_100m()     │    │
│  │  - plot_athlete_clustering()       │    │
│  └────────────────────────────────────┘    │
│                                             │
│  ┌────────────────────────────────────┐    │
│  │  Vietnam Charts                    │    │
│  │  - plot_vietnam_stats()            │    │
│  │  - plot_vietnam_details()          │    │
│  └────────────────────────────────────┘    │
└──────┬──────────────────────────────────────┘
       │
       ▼
┌─────────────────────┐
│  Visualizations     │
│  - Line charts      │
│  - Bar charts       │
│  - Histograms       │
│  - Box plots        │
│  - Scatter plots    │
│  - Tables           │
└─────────────────────┘
```

#### Chi tiết các loại biểu đồ:

**1. Basic Charts (Biểu đồ cơ bản)**
- **Line Chart:** Xu hướng theo thời gian
- **Bar Chart:** So sánh giữa các nhóm
- **Histogram:** Phân bố dữ liệu
- **Box Plot:** So sánh phân bố giữa các nhóm

**2. Advanced Charts (Biểu đồ nâng cao)**
- **Regression Plot:** Xu hướng và mối tương quan
- **Clustering Visualization:** Phân nhóm dữ liệu
- **Annotated Charts:** Biểu đồ có chú thích

**3. Vietnam Charts (Biểu đồ Việt Nam)**
- **Statistics Chart:** Thống kê tổng quan
- **Medal Table:** Bảng danh sách huy chương

### Phase 6: Data Export (Xuất dữ liệu)

```
┌─────────────────────┐
│ Analysis Results    │
│ - Medal Tally       │
│ - Gender Stats      │
│ - Age Groups        │
│ - Physique Stats    │
│ - Sport Dominance   │
└──────┬──────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│        export_data.py                         │
│                                               │
│  ┌────────────────────────────────────┐      │
│  │  Basic Export                      │      │
│  │  - export_to_csv()                 │      │
│  │  - export_to_excel()               │      │
│  │  - export_to_json()                 │      │
│  └────────────────────────────────────┘      │
│                                               │
│  ┌────────────────────────────────────┐      │
│  │  Advanced Export                   │      │
│  │  - export_multiple_sheets_to_excel()│      │
│  │  - export_analysis_results()       │      │
│  │  - export_filtered_data()         │      │
│  └────────────────────────────────────┘      │
└──────┬───────────────────────────────────────┘
       │
       ▼
┌─────────────────────┐
│  Exported Files     │
│  - CSV files        │
│  - Excel files      │
│  - JSON files       │
└─────────────────────┘
```

#### Chi tiết các hàm export:

**1. Basic Export Functions (Hàm xuất cơ bản)**

**ensure_output_dir():**
```
Input: output_dir (optional, default: 'output')
Process:
  1. Check if directory exists
  2. Create directory if not exists
  3. Return absolute path
Output: Absolute path to output directory
```

**export_to_csv():**
```
Input: DataFrame, filename, output_dir, index
Process:
  1. Validate DataFrame (check None and empty)
  2. Ensure output directory exists (using ensure_output_dir)
  3. Export to CSV with UTF-8-sig encoding
  4. Handle errors gracefully
Output: CSV file (returns True/False)
```

**export_to_excel():**
```
Input: DataFrame, filename, sheet_name, output_dir, index
Process:
  1. Validate DataFrame (check None and empty)
  2. Ensure output directory exists
  3. Export to Excel using openpyxl engine
  4. Handle errors gracefully
Output: Excel file (single sheet, returns True/False)
```

**2. Advanced Export Functions (Hàm xuất nâng cao)**

**export_multiple_sheets():**
```
Input: data_dict (dict of DataFrames), filename, output_dir
Process:
  1. Filter out None and empty DataFrames
  2. Ensure output directory exists
  3. Use ExcelWriter to create multi-sheet file
  4. Each DataFrame becomes a separate sheet
  5. Truncate sheet names to 31 characters (Excel limit)
Output: Excel file (multiple sheets, returns True/False)
```

**export_full_report():**
```
Input: df_clean, analysis_module
Process:
  1. Generate filename with timestamp (Olympic_Full_Report_YYYYMMDD_HHMMSS.xlsx)
  2. Call analysis functions from analysis_module
  3. Collect results: Top 50 Rows, Physical Stats, Vietnam Medals
  4. Use try-except for each analysis to handle errors gracefully
  5. Export all results using export_multiple_sheets
Output: Excel file with comprehensive report
```

**export_vietnam_specific():**
```
Input: df_clean, analysis_module
Process:
  1. Generate filename: Vietnam_Olympic_History.xlsx
  2. Call get_vietnam_medals from analysis_module
  3. Filter Vietnam data manually (NOC == 'VIE')
  4. Collect: Danh Sách Huy Chương, Lịch Sử Tham Gia
  5. Use try-except to handle errors gracefully
  6. Export using export_multiple_sheets
Output: Excel file with Vietnam-specific analysis
```

## 🔀 Luồng xử lý dữ liệu đặc biệt

### Xử lý môn đồng đội (Team Sports)

**Vấn đề:** Trong môn đồng đội (ví dụ: Bóng đá), mỗi cầu thủ có một dòng dữ liệu. Nếu đếm trực tiếp sẽ bị trùng lặp huy chương.

**Giải pháp:**
```python
# Trong calculate_medal_tally() và analyze_dominant_sports()
subset_data = df.drop_duplicates(
    subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Event', 'Medal']
)
```

**Ví dụ:**
- Đội bóng 11 người, mỗi người 1 dòng → 11 dòng
- Sau khi drop duplicates → 1 dòng (đại diện cho 1 huy chương)

### Xử lý giá trị thiếu (Missing Values)

**Chiến lược khác nhau cho từng loại cột:**

1. **Cột số (Age, Height, Weight):**
   - Thay bằng giá trị trung bình
   - Lý do: Giữ được đặc tính phân bố của dữ liệu

2. **Cột chuỗi (Team, Sport, Event, ...):**
   - Thay bằng giá trị mode (xuất hiện nhiều nhất)
   - Lý do: Giữ được giá trị phổ biến nhất

3. **Cột Medal:**
   - Thay bằng "No Medal"
   - Lý do: Phân biệt rõ ràng giữa có và không có huy chương

### Xử lý Outlier (Giá trị bất thường)

**Phương pháp IQR (Interquartile Range):**

```
Q1 (25%) ──────── Median ──────── Q3 (75%)
    │                                │
    │                                │
    └──────── IQR ───────────────────┘
    │                                │
    │                                │
Lower Bound                    Upper Bound
(Q1 - 1.5×IQR)              (Q3 + 1.5×IQR)
```

**Capping Strategy:**
- Giá trị < Lower Bound → Gán = Lower Bound
- Giá trị > Upper Bound → Gán = Upper Bound
- Giữ nguyên các giá trị trong khoảng

**Lý do:** Giữ lại dữ liệu nhưng loại bỏ ảnh hưởng của giá trị cực đoan

## 📊 Cấu trúc dữ liệu

### Input Data Schema

```python
{
    'ID': int,              # Mã định danh vận động viên
    'Name': str,            # Tên vận động viên
    'Sex': str,             # Giới tính (M/F)
    'Age': float,           # Tuổi
    'Height': float,         # Chiều cao (cm)
    'Weight': float,         # Cân nặng (kg)
    'Team': str,             # Tên đội/quốc gia
    'NOC': str,              # Mã quốc gia (3 chữ cái)
    'Games': str,            # Tên kỳ Olympic (e.g., "2016 Summer")
    'Year': int,             # Năm tổ chức
    'Season': str,           # Mùa (Summer/Winter)
    'City': str,             # Thành phố đăng cai
    'Sport': str,            # Môn thể thao
    'Event': str,            # Nội dung thi đấu
    'Medal': str             # Loại huy chương (Gold/Silver/Bronze/No Medal)
}
```

### Output Data Examples

**Medal Tally:**
```python
NOC      Gold    Silver    Bronze
USA      1022     794       704
URS      395      319       296
GBR      263      295       289
...
```

**Gender Participation:**
```python
Year    M       F
1896    241     0
1900    975     22
1904    645     6
...
```

## 🔧 Cấu hình và Tùy chỉnh

### Cấu hình Visualization

```python
def setup_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
```

### Tùy chỉnh phân tích

Các hàm phân tích đều có tham số để tùy chỉnh:
- `top_n`: Số lượng kết quả hiển thị
- `age`, `height`, `weight`: Điều kiện lọc
- `team`, `noc`, `sport`: Lọc theo đối tượng cụ thể

## 🚨 Xử lý lỗi và Cảnh báo

### Cảnh báo hiện tại

**SettingWithCopyWarning trong data_cleaning.py:**
- Nguyên nhân: Thao tác trên bản copy của DataFrame
- Giải pháp: Sử dụng `.copy()` hoặc `.loc[]`

### Xử lý lỗi

**FileNotFoundError:**
```python
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print("Không tìm thấy file dữ liệu!")
    return None
```

**Empty DataFrame:**
- Kiểm tra `df.empty` trước khi xử lý
- Trả về thông báo phù hợp

## 🔄 Workflow hoàn chỉnh

```
1. START
   │
   ├─► Load CSV file
   │   └─► data_loader.load_data()
   │
   ├─► Clean data
   │   └─► data_cleaning.clean_data()
   │
   ├─► (Optional) Scale data
   │   └─► data_scaled.scale_data()
   │
   ├─► Advanced cleaning
   │   ├─► analysis.clean_team_name()
   │   ├─► analysis.clean_event_name()
   │   └─► analysis.extract_nickname()
   │
   ├─► Filter data (if needed)
   │   ├─► analysis.filter_data_number()
   │   ├─► analysis.filter_data_string()
   │   ├─► analysis.filter_season_and_year()
   │   └─► analysis.filter_medals()
   │
   ├─► Statistical analysis
   │   ├─► analysis.calculate_medal_tally()
   │   ├─► analysis.analyze_gender_participation()
   │   ├─► analysis.analyze_medals_and_participants_by_age()
   │   ├─► analysis.analyze_physique_all_athletes()
   │   └─► analysis.analyze_dominant_sports()
   │
   ├─► Visualization
   │   ├─► visualization.plot_gender_trend()
   │   ├─► visualization.plot_top_medals()
   │   ├─► visualization.plot_physical_distribution()
   │   ├─► visualization.plot_vietnam_stats()
   │   └─► ... (other charts)
   │
   ├─► Export results
   │   ├─► export_data.export_to_csv()
   │   ├─► export_data.export_to_excel()
   │   ├─► export_data.export_to_json()
   │   ├─► export_data.export_multiple_sheets_to_excel()
   │   └─► export_data.export_analysis_results()
   │
   └─► END
```

## 📈 Hiệu suất và Tối ưu hóa

### Điểm cần cải thiện

1. **Memory Usage:**
   - Xử lý dữ liệu lớn (269K+ rows)
   - Có thể cần chunking cho file lớn hơn

2. **Processing Speed:**
   - Một số hàm có thể được vectorize hơn
   - Có thể sử dụng multiprocessing cho các tác vụ độc lập

3. **Code Optimization:**
   - Tránh SettingWithCopyWarning
   - Sử dụng `.loc[]` thay vì indexing trực tiếp

---

**Tài liệu này mô tả chi tiết kiến trúc và luồng hoạt động của dự án phân tích dữ liệu Olympic.**

