import pandas as pd

def load_data(file_path):
  #file_path là đường dẫn chứa file csv: "data/athlete_events.csv"
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


