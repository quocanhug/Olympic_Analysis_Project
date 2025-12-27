from sklearn.preprocessing import StandardScaler
import numpy as np

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
