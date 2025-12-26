import pandas as pd

def load_Data(file_path):
  #file_path là đường dẫn chứa file cvs: "Olympic_Analysis_Project/data/athlete_events.csv"
  try:
    df = pd.read_csv(file_path)
    print("Đọc dữ liệu thành công!")
    return df
  except FileNotFoundError:
    print("Không tìm thấy file dữ liệu!")
  except Exception as e:
    print("Lỗi khi đọc dữ liệu:", e)
