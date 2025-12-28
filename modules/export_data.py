import pandas as pd
import os
from datetime import datetime

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
        # Tạo thư mục nếu chưa tồn tại
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for sheet_name, df in dataframes_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=index)
        
        print(f"Đã xuất {len(dataframes_dict)} sheet(s) ra file Excel: {file_path}")
        return True
    except Exception as e:
        print(f"Lỗi khi xuất file Excel nhiều sheet: {e}")
        return False


def export_analysis_results(df_medal_tally=None, df_gender=None, df_age=None, 
                            df_physique=None, df_dominant_sports=None, 
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
        # Tạo thư mục output nếu chưa tồn tại
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Tạo tên file với timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(output_dir, f"{prefix}_{timestamp}.xlsx")
        
        # Tạo dictionary các sheet
        sheets = {}
        
        if df_medal_tally is not None:
            sheets['Medal Tally'] = df_medal_tally
        
        if df_gender is not None:
            sheets['Gender Participation'] = df_gender
        
        if df_age is not None:
            sheets['Age Analysis'] = df_age
        
        if df_physique is not None:
            sheets['Physique Stats'] = df_physique
        
        if df_dominant_sports is not None:
            sheets['Dominant Sports'] = df_dominant_sports
        
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
