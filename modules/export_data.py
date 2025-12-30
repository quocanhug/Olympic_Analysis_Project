import pandas as pd
import os
import inspect
import matplotlib.pyplot as plt
from datetime import datetime
import data_cleaning as dc
import analysis as ana
import visualization as vis

# --- CẤU HÌNH ---
INPUT_FILE_PATH = 'data/athlete_events.csv'
BASE_OUTPUT_DIR = 'output'

# =============================================================================
# PHẦN 1: CÁC HÀM TIỆN ÍCH HỆ THỐNG
# =============================================================================


def setup_directories():
    """Tạo cấu trúc thư mục đầu ra ngăn nắp."""
    dirs = {
        'root': BASE_OUTPUT_DIR,
        'csv': os.path.join(BASE_OUTPUT_DIR, 'csv_data'),
        'charts': os.path.join(BASE_OUTPUT_DIR, 'charts'),
        'reports': os.path.join(BASE_OUTPUT_DIR, 'reports')
    }

    for key, path in dirs.items():
        if not os.path.exists(path):
            os.makedirs(path)

    print(f"--> Đã khởi tạo thư mục tại: {os.path.abspath(BASE_OUTPUT_DIR)}")
    return dirs


def save_dataframe_to_csv(data, filename, folder):
    """Lưu dữ liệu (DataFrame/Series/Dict) ra CSV một cách thông minh."""
    full_path = os.path.join(folder, filename)
    try:
        # 1. Xử lý Dict (Ví dụ: Physical Summary)
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        # 2. Xử lý Series (Ví dụ: Value Counts)
        elif isinstance(data, pd.Series):
            data = data.reset_index()

        # 3. Lưu DataFrame
        if isinstance(data, pd.DataFrame):
            if data.empty:
                return False
            data.to_csv(full_path, index=False, encoding='utf-8-sig')
            print(f"   [CSV] Đã lưu: {filename}")
            return True

        return False
    except Exception as e:
        print(f"   [LỖI CSV] Không thể lưu {filename}: {e}")
        return False

# =============================================================================
# PHẦN 2: TỰ ĐỘNG CHẠY PHÂN TÍCH (ANALYSIS AUTOMATION)
# =============================================================================


def run_auto_analysis(df, output_csv_dir):
    """
    Quét toàn bộ file analysis.py và chạy mọi hàm bắt đầu bằng 
    'analyze_', 'calculate_', 'get_'.
    """
    print("\n--- ĐANG CHẠY TỰ ĐỘNG CÁC HÀM PHÂN TÍCH ---")

    results_dict = {}  # Lưu lại để dùng cho báo cáo Excel sau này

    # Lấy danh sách tất cả các hàm trong module analysis
    functions_list = inspect.getmembers(ana, inspect.isfunction)

    valid_prefixes = ('analyze_', 'calculate_', 'get_', 'count_', 'sum_')

    for func_name, func_obj in functions_list:
        # Chỉ chạy các hàm thuộc module analysis (tránh hàm import)
        if func_obj.__module__ == ana.__name__ and func_name.startswith(valid_prefixes):
            try:
                # Gọi hàm
                result = func_obj(df)

                if result is not None:
                    # 1. Lưu vào dict tổng hợp
                    results_dict[func_name] = result

                    # 2. Xuất ra file CSV riêng lẻ
                    save_dataframe_to_csv(
                        result, f"{func_name}.csv", output_csv_dir)
                else:
                    print(f"   [SKIP] Hàm '{func_name}' trả về dữ liệu rỗng.")

            except TypeError:
                pass  # Bỏ qua các hàm yêu cầu tham số phức tạp
            except Exception as e:
                print(f"   [WARN] Lỗi khi chạy '{func_name}': {e}")

    return results_dict

# =============================================================================
# PHẦN 3: XUẤT BÁO CÁO EXCEL TỔNG HỢP
# =============================================================================


def create_excel_report(df_clean, analysis_results, output_dir):
    """Gom tất cả kết quả phân tích vào 1 file Excel nhiều sheet."""
    print("\n--- ĐANG TẠO BÁO CÁO EXCEL TỔNG HỢP ---")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"Olympic_Full_Report_{timestamp}.xlsx"
    full_path = os.path.join(output_dir, filename)

    try:
        with pd.ExcelWriter(full_path, engine='openpyxl') as writer:
            # Sheet 1: Dữ liệu gốc (Top 50 dòng)
            df_clean.head(50).to_excel(
                writer, sheet_name='Top 50 Data', index=False)

            # Các Sheet phân tích
            for func_name, data in analysis_results.items():
                sheet_name = func_name.replace("analyze_", "").replace(
                    "calculate_", "").replace("get_", "")[:31]

                # Xử lý dữ liệu trước khi ghi
                if isinstance(data, dict):
                    pd.DataFrame(data).to_excel(writer, sheet_name=sheet_name)
                elif isinstance(data, pd.Series):
                    data.reset_index().to_excel(writer, sheet_name=sheet_name, index=False)
                elif isinstance(data, pd.DataFrame):
                    data.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"   [EXCEL] Xuất thành công: {full_path}")
    except Exception as e:
        print(f"   [LỖI EXCEL] {e}")

# =============================================================================
# PHẦN 4: XUẤT BIỂU ĐỒ HÌNH ẢNH (VISUALIZATION)
# =============================================================================


def export_charts(df, output_dir):
    """Quét và chạy các hàm vẽ trong visualization.py"""
    print("\n--- ĐANG VẼ VÀ XUẤT HÌNH ẢNH ---")

    # Định nghĩa các biểu đồ cần vẽ
    chart_tasks = [
        (vis.plot_gender_trend, "1_Xu_huong_gioi_tinh.png"),
        (vis.plot_top_medals, "2_Top_quoc_gia_huy_chuong.png"),
        (vis.plot_physical_distribution, "3_Phan_phoi_the_chat.png"),
        (vis.plot_physical_comparison_by_sport, "4_So_sanh_mon_the_thao.png"),
        (vis.plot_athlete_clustering, "5_Phan_cum_VDV.png"),
        (vis.plot_host_advantage_china, "6_Loi_the_san_nha_TQ.png"),
        (vis.plot_geopolitics_impact, "7_Anh_huong_chinh_tri.png"),
        (vis.plot_vietnam_stats, "8_VietNam_so_luong_VDV.png"),
        (vis.plot_vietnam_details, "9_VietNam_bang_vang.png")
    ]

    count = 0
    for func, filename in chart_tasks:
        if hasattr(vis, func.__name__):
            try:
                print(f"   -> Đang vẽ: {filename}...")
                fig = func(df)

                if fig:
                    save_path = os.path.join(output_dir, filename)
                    fig.savefig(save_path, bbox_inches='tight', dpi=150)
                    plt.close(fig)  # Giải phóng RAM
                    count += 1
                else:
                    print(f"      [SKIP] Hàm {func.__name__} trả về None.")
            except Exception as e:
                print(f"      [LỖI CHART] {filename}: {e}")

    print(f"   -> Đã lưu {count} biểu đồ vào thư mục '{output_dir}'.")

# =============================================================================
# CHƯƠNG TRÌNH CHÍNH (MAIN)
# =============================================================================


def main():
    print("=======================================================")
    print("   BẮT ĐẦU QUY TRÌNH XUẤT DỮ LIỆU TOÀN DIỆN")
    print("=======================================================")

    # 1. Khởi tạo thư mục
    dirs = setup_directories()

    # 2. Load và Clean dữ liệu
    print("\n[BƯỚC 1] Đọc và làm sạch dữ liệu...")
    if not os.path.exists(INPUT_FILE_PATH):
        print(f"[LỖI] Không tìm thấy file '{INPUT_FILE_PATH}'")
        return

    df_raw = dc.load_data(INPUT_FILE_PATH)
    if df_raw is None:
        return

    df_clean = dc.clean_data(df_raw)

    # Lưu file Master Cleaned Data
    save_dataframe_to_csv(df_clean, "00_MASTER_CLEANED_DATA.csv", dirs['csv'])

    # 3. Chạy phân tích & Xuất CSV
    # Hàm này trả về dict kết quả để dùng tiếp cho Excel
    analysis_results = run_auto_analysis(df_clean, dirs['csv'])

    # 4. Xuất báo cáo Excel
    create_excel_report(df_clean, analysis_results, dirs['reports'])

    # 5. Xuất hình ảnh
    export_charts(df_clean, dirs['charts'])

    print("\n=======================================================")
    print("   HOÀN TẤT! KIỂM TRA THƯ MỤC 'output'")
    print("=======================================================")


if __name__ == "__main__":
    main()
