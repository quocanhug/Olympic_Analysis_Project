# 🏅 Olympic Data Analysis Project

Dự án phân tích dữ liệu lịch sử Thế vận hội Olympic (1896-2016) sử dụng Python, Streamlit và Matplotlib.

## 🚀 Bắt đầu nhanh (Quick Start)

### 1. Cài đặt

Yêu cầu Python 3.7+

```bash
# Cài đặt thư viện
pip install -r requirements.txt

```

### 2. Chạy ứng dụng (Dashboard)

Để xem biểu đồ tương tác trên trình duyệt:

```bash
streamlit run UI.py

```

*(Mở trình duyệt tại `http://localhost:8501`)*

### 3. Xuất báo cáo (Report)

Để tự động tạo file Excel và ảnh biểu đồ vào thư mục `output/`:

```bash
python export_data.py

```

---

## 📂 Cấu trúc dự án

```text
.
├── modules/               # Core logic (Cleaning, Analysis, Viz)
├── output/                # Kết quả xuất ra (Reports, Charts)
├── docs/                  # Tài liệu chi tiết hướng dẫn & kiến trúc
├── data/
        athlete_events.csv # Dữ liệu nguồn
├── UI.py                  # Giao diện Web
└── export_data.py         # Script xuất báo cáo

```

## 📖 Tài liệu tham khảo

Chi tiết về kiến trúc và cách sử dụng nâng cao vui lòng xem trong thư mục `docs/`:

* [📘 Hướng dẫn sử dụng chi tiết](https://github.com/quocanhug/Olympic_Analysis_Project/blob/main/docs/USER_GUIDE.md)
* [🏗️ Kiến trúc hệ thống](https://github.com/quocanhug/Olympic_Analysis_Project/blob/main/docs/ARCHITECTURE.md)
* [📊 Ý nghĩa dữ liệu](https://github.com/quocanhug/Olympic_Analysis_Project/blob/main/docs/ARCHITECTURE.md)

---

**Nhóm thực hiện:**
ĐINH QUỐC ANH
LÝ GIA HÂN
BÙI THANH PHÚC
PHAN TUẤN THANH
ĐỖ THANH THÀNH TÀI

**Môn học:** Lập trình Python (IPPA233277)
