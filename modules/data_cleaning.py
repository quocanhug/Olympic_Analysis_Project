def clean_data(df):
    """
    Thực hiện làm sạch dữ liệu:
    - Loại bỏ dòng trùng lặp
    - Điền giá trị thiếu cho cột số bằng trung bình
    - Điền giá trị thiếu cho cột chuỗi bằng mode (trừ cột Medal)
    - Chuẩn hóa các cột số
    """
    # 1. Xóa dòng trùng
    df = df.drop_duplicates()

    # 2. Xử lý cột số (nếu như giá trị là NA thì sẽ trả về mean của cột số)
    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].mean())

    # 3. Xử lý cột chuỗi (TRỪ Medal) (nếu như có giá trị là NA thì sẽ trả về chuỗi xuất hiện nhiều nhất trong cột đó, nếu Medal thì NA thì sẽ là không đạt huy chương)
    categorical_cols = df.select_dtypes(include="object").columns
    for col in categorical_cols:
        if col != "Medal":
            df[col] = df[col].fillna(df[col].mode()[0])

    # 4. Chuẩn hóa cột số (Dùng để đưa nhiều cột số về một thang đo chung bằng cách đo mức độ lệch của từng giá trị so với giá trị trung bình của từng cột)
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df
