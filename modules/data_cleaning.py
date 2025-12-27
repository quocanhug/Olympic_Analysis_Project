import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

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
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
    
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
    
            # Chặn biên (capping)
            df[col] = df[col].clip(lower, upper)

    return df
