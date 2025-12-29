import pandas as pd
import os
from datetime import datetime

# Thư mục output mặc định
DEFAULT_OUTPUT_DIR = 'output'

def ensure_output_dir(output_dir=None):
    """
    Đảm bảo thư mục output tồn tại, nếu chưa có thì tạo mới.
    
    Parameters:
    -----------
    output_dir : str, optional
        Đường dẫn thư mục output. Nếu None thì dùng DEFAULT_OUTPUT_DIR
    
    Returns:
    --------
    str
        Đường dẫn tuyệt đối của thư mục output
    """
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Đã tạo thư mục output: {os.path.abspath(output_dir)}")
    
    return os.path.abspath(output_dir)

def export_to_csv(df, file_path, index=False):
    """
    Xuất DataFrame ra file CSV.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame cần xuất
    file_path : str
        Đường dẫn file CSV (ví dụ: "output/data.csv")
    index : bool, default False
        Có xuất index hay không
    
    Returns:
    --------
    bool
        True nếu xuất thành công, False nếu có lỗi
    """
    try:
        # Kiểm tra DataFrame hợp lệ
        if df is None:
            print("Lỗi: DataFrame là None, không thể xuất!")
            return False
        
        if df.empty:
            print("Cảnh báo: DataFrame rỗng, vẫn sẽ tạo file CSV trống.")
        
        # Tạo thư mục nếu chưa tồn tại
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        df.to_csv(file_path, index=index, encoding='utf-8-sig')
        print(f"Đã xuất dữ liệu ra file CSV: {file_path}")
        return True
    except Exception as e:
        print(f"Lỗi khi xuất file CSV: {e}")
        return False


def export_to_excel(df, file_path, sheet_name='Sheet1', index=False):
    """
    Xuất DataFrame ra file Excel.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame cần xuất
    file_path : str
        Đường dẫn file Excel (ví dụ: "output/data.xlsx")
    sheet_name : str, default 'Sheet1'
        Tên sheet trong file Excel
    index : bool, default False
        Có xuất index hay không
    
    Returns:
    --------
    bool
        True nếu xuất thành công, False nếu có lỗi
    """
    try:
        # Kiểm tra DataFrame hợp lệ
        if df is None:
            print("Lỗi: DataFrame là None, không thể xuất!")
            return False
        
        if df.empty:
            print("Cảnh báo: DataFrame rỗng, vẫn sẽ tạo file Excel trống.")
        
        # Tạo thư mục nếu chưa tồn tại
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        df.to_excel(file_path, sheet_name=sheet_name, index=index, engine='openpyxl')
        print(f"Đã xuất dữ liệu ra file Excel: {file_path}")
        return True
    except Exception as e:
        print(f"Lỗi khi xuất file Excel: {e}")
        return False


def export_to_json(df, file_path, orient='records', index=False):
    """
    Xuất DataFrame ra file JSON.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame cần xuất
    file_path : str
        Đường dẫn file JSON (ví dụ: "output/data.json")
    orient : str, default 'records'
        Định dạng JSON ('records', 'index', 'values', 'table', 'split')
    index : bool, default False
        Có xuất index hay không
    
    Returns:
    --------
    bool
        True nếu xuất thành công, False nếu có lỗi
    """
    try:
        # Kiểm tra DataFrame hợp lệ
        if df is None:
            print("Lỗi: DataFrame là None, không thể xuất!")
            return False
        
        if df.empty:
            print("Cảnh báo: DataFrame rỗng, vẫn sẽ tạo file JSON trống.")
        
        # Tạo thư mục nếu chưa tồn tại
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        df.to_json(file_path, orient=orient, index=index, force_ascii=False, indent=2)
        print(f"Đã xuất dữ liệu ra file JSON: {file_path}")
        return True
    except Exception as e:
        print(f"Lỗi khi xuất file JSON: {e}")
        return False


def export_multiple_sheets_to_excel(dataframes_dict, file_path, index=False):
    """
    Xuất nhiều DataFrame vào một file Excel với nhiều sheet.
    
    Parameters:
    -----------
    dataframes_dict : dict
        Dictionary với key là tên sheet, value là DataFrame
        Ví dụ: {'Medal Tally': df1, 'Gender Stats': df2}
    file_path : str
        Đường dẫn file Excel (ví dụ: "output/analysis.xlsx")
    index : bool, default False
        Có xuất index hay không
    
    Returns:
    --------
    bool
        True nếu xuất thành công, False nếu có lỗi
    """
    try:
        # Kiểm tra dictionary hợp lệ
        if not dataframes_dict:
            print("Lỗi: Dictionary rỗng, không có dữ liệu để xuất!")
            return False
        
        # Lọc bỏ các DataFrame None hoặc rỗng
        valid_sheets = {}
        for sheet_name, df in dataframes_dict.items():
            if df is not None:
                if df.empty:
                    print(f"Cảnh báo: Sheet '{sheet_name}' rỗng, sẽ bỏ qua.")
                else:
                    valid_sheets[sheet_name] = df
        
        if not valid_sheets:
            print("Lỗi: Không có DataFrame hợp lệ nào để xuất!")
            return False
        
        # Tạo thư mục nếu chưa tồn tại
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for sheet_name, df in valid_sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=index)
        
        print(f"Đã xuất {len(valid_sheets)} sheet(s) ra file Excel: {file_path}")
        return True
    except Exception as e:
        print(f"Lỗi khi xuất file Excel nhiều sheet: {e}")
        return False


def export_analysis_results(df_medal_tally=None, df_gender=None, df_age=None, 
                            df_physique=None, df_dominant_sports=None, 
                            df_vietnam_participation=None, df_vietnam_medals=None,
                            df_country_performance=None, df_physical_summary=None,
                            output_dir='output', prefix='analysis'):
    """
    Xuất tất cả kết quả phân tích vào một file Excel với nhiều sheet.
    
    Parameters:
    -----------
    df_medal_tally : pandas.DataFrame, optional
        Kết quả từ calculate_medal_tally()
    df_gender : pandas.DataFrame, optional
        Kết quả từ analyze_gender_participation()
    df_age : pandas.DataFrame, optional
        Kết quả từ analyze_medals_and_participants_by_age()
    df_physique : pandas.DataFrame, optional
        Kết quả từ analyze_physique_all_athletes()
    df_dominant_sports : pandas.DataFrame, optional
        Kết quả từ analyze_dominant_sports()
    df_vietnam_participation : pandas.DataFrame, optional
        Kết quả từ analyze_vietnam_participation()
    df_vietnam_medals : pandas.DataFrame, optional
        Kết quả từ get_vietnam_medals()
    df_country_performance : pandas.DataFrame, optional
        Kết quả từ get_country_performance_and_hosts() (chỉ DataFrame, không bao gồm list)
    df_physical_summary : pandas.DataFrame, optional
        Kết quả từ analyze_physical_summary() (sẽ được chuyển đổi thành DataFrame)
    output_dir : str, default 'output'
        Thư mục chứa file xuất
    prefix : str, default 'analysis'
        Tiền tố tên file
    
    Returns:
    --------
    str or None
        Đường dẫn file đã xuất nếu thành công, None nếu có lỗi
    """
    try:
        # Đảm bảo thư mục output tồn tại
        output_dir = ensure_output_dir(output_dir)
        
        # Tạo tên file với timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(output_dir, f"{prefix}_{timestamp}.xlsx")
        
        # Tạo dictionary các sheet
        sheets = {}
        
        if df_medal_tally is not None and not df_medal_tally.empty:
            sheets['Medal Tally'] = df_medal_tally
        
        if df_gender is not None and not df_gender.empty:
            sheets['Gender Participation'] = df_gender
        
        if df_age is not None and not df_age.empty:
            sheets['Age Analysis'] = df_age
        
        if df_physique is not None and not df_physique.empty:
            sheets['Physique Stats'] = df_physique
        
        if df_dominant_sports is not None and not df_dominant_sports.empty:
            sheets['Dominant Sports'] = df_dominant_sports
        
        if df_vietnam_participation is not None and not df_vietnam_participation.empty:
            sheets['Vietnam Participation'] = df_vietnam_participation
        
        if df_vietnam_medals is not None and not df_vietnam_medals.empty:
            sheets['Vietnam Medals'] = df_vietnam_medals
        
        if df_country_performance is not None and not df_country_performance.empty:
            sheets['Country Performance'] = df_country_performance
        
        if df_physical_summary is not None:
            # Chuyển đổi dict thành DataFrame nếu cần
            if isinstance(df_physical_summary, dict):
                df_physical_summary = pd.DataFrame([df_physical_summary])
            if not df_physical_summary.empty:
                sheets['Physical Summary'] = df_physical_summary
        
        if not sheets:
            print("Không có dữ liệu nào để xuất!")
            return None
        
        # Xuất ra Excel
        export_multiple_sheets_to_excel(sheets, file_path)
        return file_path
        
    except Exception as e:
        print(f"Lỗi khi xuất kết quả phân tích: {e}")
        return None


def export_filtered_data(df, file_path, format='csv', **kwargs):
    """
    Xuất dữ liệu đã lọc ra file với định dạng chỉ định.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame đã được lọc
    file_path : str
        Đường dẫn file xuất
    format : str, default 'csv'
        Định dạng file ('csv', 'excel', 'json')
    **kwargs
        Các tham số bổ sung cho hàm export tương ứng
    
    Returns:
    --------
    bool
        True nếu xuất thành công, False nếu có lỗi
    """
    # Kiểm tra DataFrame hợp lệ
    if df is None:
        print("Lỗi: DataFrame là None, không thể xuất!")
        return False
    
    format = format.lower()
    
    if format == 'csv':
        return export_to_csv(df, file_path, **kwargs)
    elif format == 'excel' or format == 'xlsx':
        return export_to_excel(df, file_path, **kwargs)
    elif format == 'json':
        return export_to_json(df, file_path, **kwargs)
    else:
        print(f"Định dạng '{format}' không được hỗ trợ. Chỉ hỗ trợ: csv, excel, json")
        return False


def export_vietnam_analysis(df_vietnam_participation=None, df_vietnam_medals=None,
                            output_dir='output', prefix='vietnam_analysis'):
    """
    Xuất các phân tích về Việt Nam vào một file Excel.
    
    Parameters:
    -----------
    df_vietnam_participation : pandas.DataFrame, optional
        Kết quả từ analyze_vietnam_participation()
    df_vietnam_medals : pandas.DataFrame, optional
        Kết quả từ get_vietnam_medals()
    output_dir : str, default 'output'
        Thư mục chứa file xuất
    prefix : str, default 'vietnam_analysis'
        Tiền tố tên file
    
    Returns:
    --------
    str or None
        Đường dẫn file đã xuất nếu thành công, None nếu có lỗi
    """
    try:
        # Đảm bảo thư mục output tồn tại
        output_dir = ensure_output_dir(output_dir)
        
        # Tạo tên file với timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(output_dir, f"{prefix}_{timestamp}.xlsx")
        
        # Tạo dictionary các sheet
        sheets = {}
        
        if df_vietnam_participation is not None and not df_vietnam_participation.empty:
            sheets['Vietnam Participation'] = df_vietnam_participation
        
        if df_vietnam_medals is not None and not df_vietnam_medals.empty:
            sheets['Vietnam Medals'] = df_vietnam_medals
        
        if not sheets:
            print("Không có dữ liệu về Việt Nam để xuất!")
            return None
        
        # Xuất ra Excel
        export_multiple_sheets_to_excel(sheets, file_path)
        return file_path
        
    except Exception as e:
        print(f"Lỗi khi xuất phân tích Việt Nam: {e}")
        return None
        # INSERT_YOUR_CODE
def main():
    """
    Hàm main để test các hàm export sử dụng data đã làm sạch thực sự.
    """
    import pandas as pd

    # Giả sử đã có file output/data.csv chứa dữ liệu đã xử lý, load nó
    data_path = "output/data.csv"
    if not os.path.exists(data_path):
        print(f"Không tìm thấy file dữ liệu đã làm sạch: {data_path}")
        print("Vui lòng chạy bước làm sạch và xuất dữ liệu trước!")
        return
    
    # Đọc dữ liệu đã làm sạch
    df_clean = pd.read_csv(data_path)

    # Test export_to_csv (xuất lại với tên khác)
    print("==> Xuất thử ra CSV")
    file_csv = "output/test_export_from_clean.csv"
    export_to_csv(df_clean, file_csv)
    print(f"Đã xuất CSV: {file_csv}")

    # Test export_to_excel
    print("==> Xuất thử ra Excel (1 sheet)")
    file_excel = "output/test_export_from_clean.xlsx"
    export_to_excel(df_clean, file_excel, sheet_name="CleanedData")
    print(f"Đã xuất Excel: {file_excel}")

    # Test export_to_json
    print("==> Xuất thử ra JSON")
    file_json = "output/test_export_from_clean.json"
    export_to_json(df_clean, file_json, orient='records')
    print(f"Đã xuất JSON: {file_json}")

    # Test export_multiple_sheets_to_excel
    print("==> Xuất thử ra Excel (nhiều sheet)")
    # Một số thống kê cơ bản làm các sheet
    describe = df_clean.describe(include='all')
    head_data = df_clean.head(20)
    sheets = {
        "CleanedData": head_data,
        "Describe": describe
    }
    file_excel_multi = "output/test_multi_sheets_from_clean.xlsx"
    export_multiple_sheets_to_excel(sheets, file_excel_multi)
    print(f"Đã xuất multi-sheet Excel: {file_excel_multi}")

    # Test export_analysis_results (giả lập phân tích)
    print("==> Xuất thử export_analysis_results")
    # Tạo giả kết quả phân tích nếu có thể
    medal_tally = None
    gender_stats = None
    age_stats = None
    try:
        from modules.analysis import calculate_medal_tally, analyze_gender_participation, analyze_medals_and_participants_by_age
        medal_tally = calculate_medal_tally(df_clean)
        gender_stats = analyze_gender_participation(df_clean)
        age_stats = analyze_medals_and_participants_by_age(df_clean)
    except Exception as e:
        print(f"Lỗi import hoặc thực thi phân tích: {e}")

    file_path_analysis = export_analysis_results(
        medal_tally=medal_tally,
        gender_stats=gender_stats,
        age_stats=age_stats,
        output_dir="output",
        prefix="test_analysis"
    )
    print(f"Đã xuất tổng hợp kết quả phân tích: {file_path_analysis}")

    # Test export_vietnam_analysis
    print("==> Xuất thử export_vietnam_analysis")
    # Giả lập lấy dữ liệu liên quan tới Vietnam
    vietnam_participation = None
    vietnam_medals = None
    try:
        # Chỉ chọn các dòng có 'Team' là Vietnam hoặc NOC là VIE
        if "Team" in df_clean.columns:
            vietnam_participation = df_clean[(df_clean["Team"].str.lower() == "vietnam") | (df_clean.get("NOC", "") == "VIE")]
        elif "NOC" in df_clean.columns:
            vietnam_participation = df_clean[df_clean["NOC"] == "VIE"]
        # Dữ liệu huy chương
        if vietnam_participation is not None and "Medal" in vietnam_participation.columns:
            vietnam_medals = vietnam_participation[vietnam_participation["Medal"].notna() & (vietnam_participation["Medal"] != "No Medal")]
    except Exception as e:
        print(f"Lỗi khi lọc dữ liệu Vietnam: {e}")

    file_path_vietnam = export_vietnam_analysis(
        df_vietnam_participation=vietnam_participation,
        df_vietnam_medals=vietnam_medals,
        output_dir="output"
    )
    print(f"Đã xuất phân tích Việt Nam: {file_path_vietnam}")

if __name__ == "__main__":
    main()
