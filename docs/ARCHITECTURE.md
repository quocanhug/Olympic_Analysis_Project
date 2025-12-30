Dưới đây là file `architecture.md` được viết lại chính xác theo định dạng bạn yêu cầu, dựa trên cấu trúc thực tế của dự án.


# Kiến trúc và Luồng hoạt động chi tiết

## 🏗️ Kiến trúc tổng quan

Dự án được thiết kế theo mô hình **Modular Architecture** (Kiến trúc mô-đun) kết hợp với **Pipeline Processing**, cho phép:

- **Tách biệt trách nhiệm:** Mỗi module (Cleaning, Analysis, Visualization) có một chức năng cụ thể.
- **Dễ bảo trì:** Sửa đổi logic phân tích không ảnh hưởng đến phần giao diện.
- **Tái sử dụng:** Các hàm vẽ biểu đồ được dùng chung cho cả Web App (`UI.py`) và Báo cáo tự động (`export_data.py`).
- **Mở rộng:** Dễ dàng thêm các loại biểu đồ hoặc phân tích mới mà không phá vỡ cấu trúc cũ.

## 📐 Sơ đồ kiến trúc


```

┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                    │
│           (Streamlit Web App / Export Automation)           │
│         ┌──────────────┐           ┌──────────────┐         │
│         │    UI.py     │           │export_data.py│         │
│         └──────┬───────┘           └──────┬───────┘         │
└────────────────┼──────────────────────────┼─────────────────┘
│                          │
▼                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Analysis   │  │ Visualization│  │ Data Cleaning│       │
│  │    Module    │◄─┤    Module    │◄─┤    Module    │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │               │
└─────────┼─────────────────┼─────────────────┼───────────────┘
│                 │                 │
▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA PROCESSING LAYER                    │
│                                                             │
│  ┌──────────────┐                                           │
│  │ Data Loader  │                                           │
│  │ (in cleaning)│                                           │
│  └──────┬───────┘                                           │
│         │                                                   │
└─────────┼───────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│                         DATA SOURCE                         │
│                 athlete_events.csv (CSV file)               │
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
│  data_cleaning.py   │
│  load_data()        │
│                     │
│  - Read CSV         │
│  - Error handling   │
│  - Return DataFrame │
└──────┬──────────────┘
│
▼
┌─────────────────────┐
│  DataFrame (Raw)    │
│  - 271,116 rows     │
│  - 15 columns       │
└─────────────────────┘

```

**Input:** File CSV `athlete_events.csv`  
**Output:** Pandas DataFrame chứa dữ liệu thô  
**Xử lý lỗi:** - `FileNotFoundError` → Thông báo lỗi console và trả về `None`.
- `Exception` khác → In chi tiết lỗi để debug.

### Phase 2: Data Cleaning (Làm sạch dữ liệu)


```

┌─────────────────────┐
│  DataFrame (Raw)    │
└──────┬──────────────┘
│
▼
┌─────────────────────────────────────────┐
│         data_cleaning.py                │
│         clean_data()                    │
│                                         │
│  Step 1: Remove duplicates              │
│  Step 2: Fix data types (to_numeric)    │
│  Step 3: Handle missing values (Impute) │
│  Step 4: Fix incorrect labels           │
│  Step 5: Handle outliers (IQR Method)   │
└──────┬──────────────────────────────────┘
│
▼
┌─────────────────────┐
│ DataFrame (Clean)   │
│ - No duplicates     │
│ - Correct types     │
│ - No missing values │
│ - Outliers capped   │
└─────────────────────┘

```

#### Chi tiết các bước làm sạch:

**Step 1: Remove Duplicates**
```python
df = df.drop_duplicates()

```

* Loại bỏ các dòng trùng lặp hoàn toàn.

**Step 2: Fix Data Types**

```python
df[col] = pd.to_numeric(df[col], errors="coerce")

```

* Chuyển Age, Height, Weight sang kiểu số thực (float).
* Giá trị lỗi (string trong cột số) → NaN.

**Step 3: Handle Missing Values**

```python
# Numeric columns: Fill with Mean
df[col] = df[col].fillna(df[col].mean())

# Categorical columns (Team, Sport...): Fill with Mode
df[col] = df[col].fillna(df[col].mode()[0])

# Medal column: Fill with "No Medal" string
df["Medal"] = df["Medal"].fillna("No Medal")

```

**Step 4: Fix Incorrect Labels**

```python
df["Medal"] = df["Medal"].replace({
    "Gold ": "Gold", "gold": "Gold", 
    "SILVER": "Silver", "BRONZE": "Bronze"
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

### Phase 3: Data Analysis (Phân tích dữ liệu)

```
┌─────────────────────┐
│ DataFrame (Clean)   │
└──────┬──────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│            analysis.py                       │
│                                              │
│  ┌────────────────────────────────────┐      │
│  │  Data Filtering (Search Logic)     │      │
│  │  - filter_data_number()            │      │
│  │  - filter_data_string()            │      │
│  └────────────────────────────────────┘      │
│                                              │
│  ┌────────────────────────────────────┐      │
│  │  Core Analysis Logic               │      │
│  │  - calculate_medal_tally()         │      │
│  │  - analyze_gender_participation()  │      │
│  │  - analyze_physical_summary()      │      │
│  │  - analyze_dominant_sports()       │      │
│  └────────────────────────────────────┘      │
│                                              │
│  ┌────────────────────────────────────┐      │
│  │  Vietnam Specific Analysis         │      │
│  │  - get_vietnam_medals()            │      │
│  │  - analyze_vietnam_participation() │      │
│  └────────────────────────────────────┘      │
└──────┬──────────────────────────────────────┘
       │
       ▼
┌─────────────────────┐
│ Analysis Results    │
│ - Medal Tally DF    │
│ - Gender Stats DF   │
│ - Vietnam Medals DF │
│ - Physical Dict     │
└─────────────────────┘

```

#### Chi tiết logic phân tích quan trọng:

**1. calculate_medal_tally() - Xử lý môn đồng đội**

```python
# Loại bỏ dòng trùng lặp Event/Medal của cùng 1 đội trước khi đếm
df_dedup = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Event', 'Medal'])
medal_counts = df_dedup.groupby('NOC')['Medal'].value_counts().unstack().fillna(0)

```

* Đảm bảo Đội bóng đá 11 người chỉ tính là 1 Huy chương Vàng.

**2. get_vietnam_medals() - Lọc dữ liệu Việt Nam**

```python
df_vn = df[df['NOC'] == 'VIE']
medals = df_vn[df_vn['Medal'].isin(['Gold', 'Silver', 'Bronze'])]

```

### Phase 4: Data Visualization (Trực quan hóa)

```
┌─────────────────────┐
│ DataFrame (Clean)   │
└──────┬──────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│        visualization.py                      │
│                                              │
│  ┌────────────────────────────────────┐      │
│  │  Global Trends                     │      │
│  │  - plot_gender_trend()             │      │
│  │  - plot_top_medals()               │      │
│  │  - plot_physical_distribution()    │      │
│  └────────────────────────────────────┘      │
│                                              │
│  ┌────────────────────────────────────┐      │
│  │  Advanced / Specific Charts        │      │
│  │  - plot_host_advantage_china()     │      │
│  │  - plot_geopolitics_impact()       │      │
│  │  - plot_athlete_clustering()       │      │
│  └────────────────────────────────────┘      │
│                                              │
│  ┌────────────────────────────────────┐      │
│  │  Vietnam Charts                    │      │
│  │  - plot_vietnam_stats()            │      │
│  │  - plot_vietnam_details()          │      │
│  └────────────────────────────────────┘      │
└──────┬──────────────────────────────────────-┘
       │
       ▼
┌─────────────────────┐
│ Matplotlib Figures  │
│ - Figure Objects    │
│ (Ready for UI/Save) │
└─────────────────────┘

```

**Đặc điểm kỹ thuật:**

* Tất cả hàm trả về đối tượng `fig` (Figure) thay vì `plt.show()`.
* Sử dụng `seaborn` theme whitegrid.
* Hỗ trợ hiển thị tiếng Việt (nếu cấu hình font).

### Phase 5: Presentation & Export (Hiển thị & Xuất)

Hệ thống có 2 đầu ra chính:

**A. Giao diện Web (UI.py)**

```
User -> Streamlit App -> Calls Load/Clean -> Calls Analysis/Viz -> Displays Charts

```

* Interactive Dashboard.
* Sidebar filtering.
* Data Explorer view.

**B. Báo cáo Tự động (export_data.py)**

```
┌──────────────────────────────────────────────┐
│          export_data.py                      │
│                                              │
│  1. Auto-Scan Analysis Module (inspect)      │
│  2. Run all functions -> Save to CSVs        │
│  3. Run all Viz functions -> Save PNGs       │
│  4. Compile Full Report -> Save Excel        │
└──────┬──────────────────────┬────────────────┘
       │                      │
       ▼                      ▼
┌─────────────────┐    ┌──────────────────┐
│ output/csv_data │    │ output/charts    │
│ - analyze_*.csv │    │ - 1_Gender.png   │
│ - get_*.csv     │    │ - 2_Medals.png   │
└─────────────────┘    └──────────────────┘
       │
       ▼
┌───────────────────────────┐
│ output/reports            │
│ - Olympic_Full_Report.xlsx│
└───────────────────────────┘

```

## 📊 Cấu trúc dữ liệu

### Input Schema (athlete_events.csv)

```python
{
    'ID': int,              # Mã định danh VĐV
    'Name': str,            # Tên VĐV
    'Sex': str,             # Giới tính (M/F)
    'Age': float,           # Tuổi (đã xử lý NA)
    'Height': float,        # Chiều cao (cm)
    'Weight': float,        # Cân nặng (kg)
    'Team': str,            # Tên đội
    'NOC': str,             # Mã quốc gia (3 ký tự)
    'Games': str,           # Tên kỳ Olympic (VD: "2016 Summer")
    'Year': int,            # Năm tổ chức
    'Season': str,          # Mùa (Summer/Winter)
    'City': str,            # Thành phố đăng cai
    'Sport': str,           # Môn thể thao
    'Event': str,           # Nội dung thi đấu
    'Medal': str            # Huy chương (Gold/Silver/Bronze/No Medal)
}

```

## 🔧 Cấu hình và Tùy chỉnh

### Cấu hình Visualization (`setup_style`)

```python
def setup_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)
    # Tùy chỉnh font size để dễ đọc trên báo cáo

```

### Cấu trúc Output Directory

Hệ thống tự động tạo cây thư mục:

* `output/`
* `csv_data/`: Dữ liệu thô sau phân tích.
* `charts/`: Hình ảnh biểu đồ chất lượng cao (DPI 150).
* `reports/`: File Excel tổng hợp nhiều sheet.



## 🚨 Xử lý lỗi và Cảnh báo

### Cơ chế Auto-Export

* **Try-Except Block:** Mỗi hàm phân tích được chạy trong khối try-except riêng biệt. Nếu một hàm lỗi, quy trình export không dừng lại mà tiếp tục sang hàm tiếp theo.
* **Data Type Handling:** Tự động nhận diện kết quả trả về là `DataFrame`, `Series` hay `Dict` để chuyển đổi format phù hợp trước khi ghi vào Excel/CSV.

### Cảnh báo thường gặp

* `SettingWithCopyWarning`: Đã được xử lý bằng cách dùng `.copy()` khi lọc dữ liệu trong `analysis.py`.
* `Font Warning`: Có thể xảy ra nếu hệ thống thiếu font hỗ trợ tiếng Việt (nhưng không ảnh hưởng đến logic chạy).

---

**Tài liệu này phản ánh chính xác mã nguồn hiện tại của dự án.**

```

```
