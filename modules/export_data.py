import pandas as pd
import os
from datetime import datetime

# --- CẤU HÌNH MẶC ĐỊNH ---
DEFAULT_OUTPUT_DIR = 'output'

def ensure_output_dir(output_dir=None):
    """
    Kiểm tra và tạo thư mục output nếu chưa tồn tại.
    """
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR
    
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"[INFO] Đã tạo thư mục mới: {os.path.abspath(output_dir)}")
        except OSError as e:
            print(f"[ERROR] Không thể tạo thư mục {output_dir}: {e}")
            return None
    
    return os.path.abspath(output_dir)

# =============================================================================
# PHẦN 1: CÁC HÀM XUẤT DỮ LIỆU CƠ BẢN (GENERIC EXPORT)
# =============================================================================

def export_to_csv(df, filename, output_dir=None, index=False):
    """Xuất DataFrame ra file CSV."""
    if df is None or df.empty:
        print(f"[WARNING] Dữ liệu trống, bỏ qua xuất CSV: {filename}")
        return False

    path = ensure_output_dir(output_dir)
    full_path = os.path.join(path, filename)
    
    try:
        # utf-8-sig để hỗ trợ tiếng Việt trên Excel
        df.to_csv(full_path, index=index, encoding='utf-8-sig')
        print(f"[SUCCESS] Đã xuất CSV: {full_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Lỗi khi xuất CSV {filename}: {e}")
        return False

def export_to_excel(df, filename, sheet_name='Sheet1', output_dir=None, index=False):
    """Xuất DataFrame ra file Excel (1 sheet)."""
    if df is None or df.empty:
        print(f"[WARNING] Dữ liệu trống, bỏ qua xuất Excel: {filename}")
        return False

    path = ensure_output_dir(output_dir)
    full_path = os.path.join(path, filename)
    
    try:
        df.to_excel(full_path, sheet_name=sheet_name, index=index, engine='openpyxl')
        print(f"[SUCCESS] Đã xuất Excel: {full_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Lỗi khi xuất Excel {filename}: {e}")
        return False

def export_multiple_sheets(data_dict, filename, output_dir=None):
    """
    Xuất nhiều DataFrame vào 1 file Excel (Mỗi DF là 1 sheet).
    
    Args:
        data_dict (dict): Dạng {'Tên Sheet': dataframe, 'Tên Sheet 2': dataframe2}
    """
    valid_data = {k: v for k, v in data_dict.items() if v is not None and not v.empty}
    
    if not valid_data:
        print(f"[WARNING] Không có dữ liệu hợp lệ để xuất file {filename}")
        return False

    path = ensure_output_dir(output_dir)
    full_path = os.path.join(path, filename)

    try:
        with pd.ExcelWriter(full_path, engine='openpyxl') as writer:
            for sheet_name, df in valid_data.items():
# Cắt tên sheet nếu quá dài (Excel giới hạn 31 ký tự)
                safe_sheet_name = sheet_name[:31]
                df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
        print(f"[SUCCESS] Đã xuất Multi-sheet Excel: {full_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Lỗi khi xuất Multi-sheet Excel {filename}: {e}")
        return False

# =============================================================================
# PHẦN 2: CÁC HÀM XUẤT BÁO CÁO CỤ THỂ (SPECIFIC REPORT)
# =============================================================================

def export_full_report(df_clean, analysis_module):
    """
    Tổng hợp tất cả phân tích và xuất ra một file Excel báo cáo tổng thể.
    
    Args:
        df_clean (pd.DataFrame): Dữ liệu sạch.
        analysis_module (module): Module analysis đã được import.
    """
    print("\n--- ĐANG TẠO BÁO CÁO TỔNG HỢP ---")
    
    # 1. Tạo timestamp để tên file không bị trùng
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Olympic_Full_Report_{timestamp}.xlsx"

    # 2. Thực hiện các phân tích (gọi hàm từ module analysis)
    # Lưu ý: Sử dụng try-except để nếu một hàm phân tích lỗi thì vẫn xuất các hàm khác
    report_data = {}

    # Sheet 1: Dữ liệu tóm tắt (50 dòng đầu)
    report_data['Top 50 Rows'] = df_clean.head(50)

    # Sheet 2: Thống kê thể chất (Physical Summary)
    try:
        # Vì hàm analyze_physical_summary trả về dict, cần chuyển sang DataFrame
        phys_dict = analysis_module.analyze_physical_summary(df_clean)
        report_data['Physical Stats'] = pd.DataFrame(phys_dict)
    except Exception as e:
        print(f"Lỗi phân tích thể chất: {e}")

    # Sheet 3: Huy chương Việt Nam
    try:
        vn_medals = analysis_module.get_vietnam_medals(df_clean)
        report_data['Vietnam Medals'] = vn_medals
    except Exception as e:
        print(f"Lỗi phân tích VN: {e}")

    # Sheet 4: Top Quốc gia (Nếu hàm tồn tại trong analysis.py của bạn)
    # Ở đây tôi ví dụ gọi hàm nếu có, bạn có thể bỏ comment nếu đã viết hàm này
    # try:
    #     medal_tally = analysis_module.calculate_medal_tally(df_clean)
    #     report_data['Medal Tally'] = medal_tally
    # except:
    #     pass

    # 3. Xuất file
    export_multiple_sheets(report_data, filename)


def export_vietnam_specific(df_clean, analysis_module):
    """
    Xuất báo cáo chuyên sâu chỉ dành riêng cho Việt Nam.
    """
    print("\n--- ĐANG TẠO BÁO CÁO VIỆT NAM ---")
    filename = "Vietnam_Olympic_History.xlsx"
    
    vn_data = {}
    
    # Lấy danh sách huy chương
    try:
        vn_medals = analysis_module.get_vietnam_medals(df_clean)
        vn_data['Danh Sách Huy Chương'] = vn_medals
    except Exception as e:
        print(f"Lỗi lấy danh sách huy chương: {e}")
        pass

    # Lấy toàn bộ lịch sử tham gia của VN (Lọc thủ công nếu hàm chưa có)
    try:
        # Sử dụng logic lọc từ analysis hoặc pandas trực tiếp
        vn_history = df_clean[df_clean['NOC'] == 'VIE']
        vn_data['Lịch Sử Tham Gia'] = vn_history
    except Exception:
        pass
        
    export_multiple_sheets(vn_data, filename)

# =============================================================================
# PHẦN 3: MAIN EXECUTION (TEST)
# =============================================================================

def main():
    """
    Hàm này mô phỏng quy trình: Load -> Clean -> Analyze -> Export
    Sử dụng trực tiếp các file trong thư mục modules.
    """
    # Import cục bộ để tránh lỗi vòng lặp nếu file này được gọi từ nơi khác
    try:
        import modules.data_cleaning as dc
        import modules.analysis as ana
        print("Import modules thành công!")
    except ImportError as e:
        print(f"Lỗi Import: {e}")
        print("Hãy đảm bảo bạn đang chạy file từ thư mục gốc (chứa folder 'modules')")
        return

    # 1. Định nghĩa đường dẫn file dữ liệu
    # Giả sử file csv nằm trong thư mục data hoặc ngay bên ngoài
    input_file = 'athlete_events.csv' 
    if not os.path.exists(input_file):
        print(f"Không tìm thấy file: {input_file}")
        return

    # 2. Load và Clean dữ liệu (Sử dụng data_cleaning.py)
    print("\n[STEP 1] Loading Data...")
    df = dc.load_data(input_file)
    
    if df is not None:
        print("[STEP 2] Cleaning Data...")
        df_clean = dc.clean_data(df)
        
        # 3. Export Dữ liệu sạch ra CSV để lưu trữ
        print("[STEP 3] Exporting Cleaned Data...")
        export_to_csv(df_clean, "cleaned_data.csv")
        
        # 4. Chạy phân tích và Xuất báo cáo tổng hợp
        print("[STEP 4] Generating Reports...")
        export_full_report(df_clean, ana)
        export_vietnam_specific(df_clean, ana)
        
        print("\n=== HOÀN TẤT QUÁ TRÌNH ===")
    else:
        print("Không thể tải dữ liệu.")

if __name__ == "__main__":
    main()
