import numpy as np
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler

pd.options.mode.chained_assignment = None


@st.cache_data
def load_data(file_path):
    # file_path là đường dẫn chứa file csv: "data/athlete_events.csv"
    try:
        df = pd.read_csv(file_path)
        print("Đọc dữ liệu thành công!")
        return df
    except FileNotFoundError:
        print("Không tìm thấy file dữ liệu!")
        return None
    except Exception as e:
        print("Lỗi khi đọc dữ liệu:", e)
        return None


def clean_data(df):
    """
    Thực hiện làm sạch dữ liệu:
    - Loại bỏ dữ liệu trùng lặp
    - Sửa định dạng sai
    - Xử lý giá trị thiếu (NA)
    - Sửa gán nhãn sai
    - Xử lý outlier
    - Chuẩn hóa dữ liệu số (dùng func data_scaled)
    """
    # 1. Xóa dòng trùng
    df = df.drop_duplicates()

    numeric_cols = ["Age", "Height", "Weight"]
    numeric_cols = [col for col in numeric_cols if col in df.columns]
    # 2. Xử lí định dạng sai
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 3. Xử lí dữ liệu thiếu
    # Xử lý cột số (nếu như giá trị là NA thì sẽ trả về mean của cột số)
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].mean())

    # Xử lý cột chuỗi (TRỪ Medal) (nếu như có giá trị là NA thì sẽ trả về chuỗi xuất hiện nhiều nhất trong cột đó, nếu Medal thì NA thì sẽ là không đạt huy chương)
    categorical_cols = df.select_dtypes(include="object").columns
    for col in categorical_cols:
        if col != "Medal":
            df[col] = df[col].fillna(df[col].mode()[0])

    # Chuyển NA ở Medal về No Medal để dễ nhìn hơn
    if "Medal" in df.columns:
        df["Medal"] = df["Medal"].fillna("No Medal")

    # 4. Xử lí gán nhãn sai
    if "Medal" in df.columns:
        df["Medal"] = df["Medal"].replace({
            "Gold ": "Gold",
            "gold": "Gold",
            "SILVER": "Silver",
            "BRONZE": "Bronze"
        })

    # 5. Xử lí outlier bằng phương pháp IQR (những giá trị bất thường, quá lớn hoặc quá nhỏ so với phần lớn các dữ liệu còn lại)
    for col in numeric_cols:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q2 = df[col].quantile(0.50)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            # Chặn biên (capping)
            df.loc[:, col] = df[col].clip(lower, upper).round(2)

    return df

def clean_team_name(df):
    """
    Làm sạch cột 'Team' bằng cách loại bỏ các ký tự số và dấu gạch ngang thừa ở cuối.
    Ví dụ: 'China-1' -> 'China', 'Denmark/Sweden-2' -> 'Denmark/Sweden'.
    Mục đích: Giúp thống kê thành tích quốc gia chính xác hơn, tránh việc một nước bị chia thành nhiều team nhỏ.
    """
    df = df.copy()
    df['Team'] = df['Team'].str.replace(r'-\d+', '', regex=True)
    return df


def clean_event_name(df):
    """
    Làm sạch cột 'Event' bằng cách cắt bỏ tên môn thể thao (Sport) bị lặp lại ở đầu.
    Ví dụ: Sport='Basketball', Event='Basketball Men's Basketball' -> 'Men's Basketball'.
    Mục đích: Làm ngắn gọn tên sự kiện, giúp bảng biểu hiển thị đẹp và dễ đọc hơn.
    """
    df = df.copy()
    df['Event'] = df.apply(lambda x: x['Event'][len(x['Sport']):].strip()
                           if x['Event'].startswith(x['Sport']) else x['Event'], axis=1)
    return df


def extract_nickname(df):
    """
    Trích xuất biệt danh (Nickname) từ cột 'Name' ra một cột riêng.
    Thường biệt danh nằm trong dấu ngoặc kép "" hoặc đôi khi là ngoặc đơn ().
    Mục đích: Tách biệt danh để phân tích hoặc hiển thị tên vận động viên gọn gàng hơn.
    """
    df = df.copy()
    nickname_quotes = df['Name'].str.extract(r'\"(.*?)\"', expand=False)
    nickname_parens = df['Name'].str.extract(r'\((.*?)\)', expand=False)
    df['Nickname'] = nickname_quotes.combine_first(nickname_parens)
    cols = list(df.columns)
    if 'Nickname' in cols:
        cols.remove('Nickname')
    name_index = cols.index('Name')
    new_cols_order = cols[:name_index + 1] + \
        ['Nickname'] + cols[name_index + 1:]
    return df[new_cols_order]


def scale_data(df):
    """
    Chuẩn hóa các cột số (trừ ID và year nếu có)
    Trả về DataFrame đã chuẩn hóa
    """
    df_scaled = df.copy()

    numeric_cols = ["Age", "Height", "Weight"]
    numeric_cols = [col for col in numeric_cols if col in df.columns]

    scaler = StandardScaler()
    df_scaled[numeric_cols] = scaler.fit_transform(df_scaled[numeric_cols])

    return df_scaled


# --- HÀM LOAD DỮ LIỆU (CACHE ĐỂ CHẠY NHANH HƠN) ---


@st.cache_data
def load_and_clean_data(filepath):
    df = load_data(filepath)
    df = clean_data(df)
    # Áp dụng các hàm làm sạch từ analysis.py ngay khi load
    df = clean_team_name(df)
    df = clean_event_name(df)
    df = extract_nickname(df)
    return df
