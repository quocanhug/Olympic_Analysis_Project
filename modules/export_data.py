import pandas as pd
import os
import matplotlib.pyplot as plt
from pathlib import Path


def export_to_csv(df, file_path, index=False):
    """
    Xuất DataFrame ra file CSV.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame cần xuất
    file_path : str
        Đường dẫn file CSV (ví dụ: "results/data.csv")
    index : bool, default=False
        Có xuất index hay không
        
    Returns:
    --------
    bool
        True nếu xuất thành công, False nếu có lỗi
        
    Ví dụ:
    ------
    >>> export_to_csv(df, "results/medal_tally.csv")
    """
    try:
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Xuất ra CSV
        df.to_csv(file_path, index=index, encoding='utf-8-sig')
        print(f"Đã xuất dữ liệu thành công: {file_path}")
        return True
    except Exception as e:
        print(f"Lỗi khi xuất CSV: {e}")
        return False


def export_to_excel(df, file_path, sheet_name='Sheet1', index=False):
    """
    Xuất DataFrame ra file Excel.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame cần xuất
    file_path : str
        Đường dẫn file Excel (ví dụ: "results/data.xlsx")
    sheet_name : str, default='Sheet1'
        Tên sheet trong file Excel
    index : bool, default=False
        Có xuất index hay không
        
    Returns:
    --------
    bool
        True nếu xuất thành công, False nếu có lỗi
        
    Ví dụ:
    ------
    >>> export_to_excel(df, "results/medal_tally.xlsx", sheet_name="Medal Tally")
    """
    try:
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Xuất ra Excel
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=index)
        
        print(f"Đã xuất dữ liệu thành công: {file_path}")
        return True
    except Exception as e:
        print(f"Lỗi khi xuất Excel: {e}")
        return False


def export_multiple_sheets(data_dict, file_path, index=False):
    """
    Xuất nhiều DataFrame vào một file Excel với nhiều sheet.
    
    Parameters:
    -----------
    data_dict : dict
        Dictionary với key là tên sheet, value là DataFrame
        Ví dụ: {"Medal Tally": df1, "Gender Stats": df2}
    file_path : str
        Đường dẫn file Excel
    index : bool, default=False
        Có xuất index hay không
        
    Returns:
    --------
    bool
        True nếu xuất thành công, False nếu có lỗi
        
    Ví dụ:
    ------
    >>> data = {
    ...     "Medal Tally": medal_tally,
    ...     "Gender Stats": gender_stats
    ... }
    >>> export_multiple_sheets(data, "results/analysis_results.xlsx")
    """
    try:
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Xuất nhiều sheet
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for sheet_name, df in data_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=index)
        
        print(f"Đã xuất {len(data_dict)} sheet thành công: {file_path}")
        return True
    except Exception as e:
        print(f"Lỗi khi xuất Excel nhiều sheet: {e}")
        return False


def export_plot(fig, file_path, dpi=300, format='png'):
    """
    Xuất biểu đồ ra file ảnh.
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        Figure object của biểu đồ
    file_path : str
        Đường dẫn file ảnh (ví dụ: "results/plot.png")
    dpi : int, default=300
        Độ phân giải (dots per inch)
    format : str, default='png'
        Định dạng file ('png', 'pdf', 'svg', 'jpg')
        
    Returns:
    --------
    bool
        True nếu xuất thành công, False nếu có lỗi
        
    Ví dụ:
    ------
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [4, 5, 6])
    >>> export_plot(fig, "results/plot.png")
    """
    try:
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Xuất biểu đồ
        fig.savefig(file_path, dpi=dpi, format=format, bbox_inches='tight')
        print(f"Đã xuất biểu đồ thành công: {file_path}")
        return True
    except Exception as e:
        print(f"Lỗi khi xuất biểu đồ: {e}")
        return False


def export_analysis_results(medal_tally=None, gender_stats=None, age_stats=None, 
                           physique_stats=None, dominant_sports=None, 
                           output_dir="results", file_prefix="analysis"):
    """
    Xuất tất cả kết quả phân tích ra file Excel với nhiều sheet.
    
    Parameters:
    -----------
    medal_tally : pandas.DataFrame, optional
        Bảng tổng sắp huy chương
    gender_stats : pandas.DataFrame, optional
        Thống kê giới tính
    age_stats : pandas.DataFrame, optional
        Thống kê theo độ tuổi
    physique_stats : pandas.DataFrame, optional
        Thống kê thể chất
    dominant_sports : pandas.DataFrame, optional
        Thế mạnh của các quốc gia
    output_dir : str, default="results"
        Thư mục xuất file
    file_prefix : str, default="analysis"
        Tiền tố tên file
        
    Returns:
    --------
    str
        Đường dẫn file đã xuất, None nếu có lỗi
        
    Ví dụ:
    ------
    >>> export_analysis_results(
    ...     medal_tally=medal_tally,
    ...     gender_stats=gender_stats,
    ...     output_dir="results"
    ... )
    """
    try:
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(output_dir, exist_ok=True)
        
        # Tạo dictionary chứa các DataFrame
        data_dict = {}
        
        if medal_tally is not None:
            data_dict["Tổng sắp huy chương"] = medal_tally
            
        if gender_stats is not None:
            data_dict["Thống kê giới tính"] = gender_stats
            
        if age_stats is not None:
            data_dict["Thống kê độ tuổi"] = age_stats
            
        if physique_stats is not None:
            data_dict["Thống kê thể chất"] = physique_stats
            
        if dominant_sports is not None:
            data_dict["Thế mạnh quốc gia"] = dominant_sports
        
        # Kiểm tra xem có dữ liệu nào không
        if not data_dict:
            print("Không có dữ liệu để xuất!")
            return None
        
        # Tạo tên file
        file_path = os.path.join(output_dir, f"{file_prefix}_results.xlsx")
        
        # Xuất ra Excel
        success = export_multiple_sheets(data_dict, file_path)
        
        if success:
            return file_path
        else:
            return None
            
    except Exception as e:
        print(f"Lỗi khi xuất kết quả phân tích: {e}")
        return None


def export_vietnam_report(df, output_dir="results"):
    """
    Xuất báo cáo chi tiết về Việt Nam ra file Excel.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame đã được làm sạch
    output_dir : str, default="results"
        Thư mục xuất file
        
    Returns:
    --------
    str
        Đường dẫn file đã xuất, None nếu có lỗi
        
    Ví dụ:
    ------
    >>> export_vietnam_report(df_clean, output_dir="results")
    """
    try:
        from modules.analysis import (
            filter_data_string,
            calculate_medal_tally,
            analyze_gender_participation
        )
        
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(output_dir, exist_ok=True)
        
        # Lọc dữ liệu Việt Nam
        df_vietnam = filter_data_string(df, team="Vietnam")
        
        if df_vietnam.empty:
            print("Không tìm thấy dữ liệu về Việt Nam!")
            return None
        
        # Tạo dictionary chứa các bảng
        data_dict = {}
        
        # 1. Tổng quan
        overview = pd.DataFrame({
            'Chỉ số': [
                'Tổng số VĐV',
                'Số kỳ Olympic tham gia',
                'Số môn thể thao',
                'Số huy chương Vàng',
                'Số huy chương Bạc',
                'Số huy chương Đồng'
            ],
            'Giá trị': [
                df_vietnam['ID'].nunique(),
                df_vietnam['Year'].nunique(),
                df_vietnam['Sport'].nunique(),
                len(df_vietnam[df_vietnam['Medal'] == 'Gold']),
                len(df_vietnam[df_vietnam['Medal'] == 'Silver']),
                len(df_vietnam[df_vietnam['Medal'] == 'Bronze'])
            ]
        })
        data_dict["Tổng quan"] = overview
        
        # 2. Số lượng VĐV theo năm
        vn_by_year = df_vietnam.groupby('Year')['ID'].nunique().reset_index()
        vn_by_year.columns = ['Năm', 'Số lượng VĐV']
        data_dict["VĐV theo năm"] = vn_by_year
        
        # 3. Top môn thể thao
        top_sports = df_vietnam['Sport'].value_counts().head(10).reset_index()
        top_sports.columns = ['Môn thể thao', 'Số lượng VĐV']
        data_dict["Top môn thể thao"] = top_sports
        
        # 4. Danh sách huy chương
        medals = df_vietnam[df_vietnam['Medal'].isin(['Gold', 'Silver', 'Bronze'])]
        if not medals.empty:
            medal_list = medals[['Year', 'Name', 'Sport', 'Event', 'Medal']].sort_values('Year')
            medal_list.columns = ['Năm', 'VĐV', 'Môn', 'Nội dung', 'Huy chương']
            data_dict["Danh sách huy chương"] = medal_list
        
        # 5. Chi tiết VĐV
        athlete_details = df_vietnam[['Year', 'Name', 'Sex', 'Age', 'Height', 'Weight', 
                                     'Sport', 'Event', 'Medal']].copy()
        athlete_details.columns = ['Năm', 'Tên', 'Giới tính', 'Tuổi', 'Chiều cao', 
                                  'Cân nặng', 'Môn', 'Nội dung', 'Huy chương']
        data_dict["Chi tiết VĐV"] = athlete_details
        
        # Xuất ra Excel
        file_path = os.path.join(output_dir, "vietnam_report.xlsx")
        success = export_multiple_sheets(data_dict, file_path)
        
        if success:
            return file_path
        else:
            return None
            
    except Exception as e:
        print(f"Lỗi khi xuất báo cáo Việt Nam: {e}")
        return None


def export_comprehensive_report(df, output_dir="results"):
    """
    Xuất báo cáo tổng hợp đầy đủ về Olympic.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame đã được làm sạch
    output_dir : str, default="results"
        Thư mục xuất file
        
    Returns:
    --------
    str
        Đường dẫn file đã xuất, None nếu có lỗi
        
    Ví dụ:
    ------
    >>> export_comprehensive_report(df_clean, output_dir="results")
    """
    try:
        from modules.analysis import (
            calculate_medal_tally,
            analyze_gender_participation,
            analyze_medals_and_participants_by_age,
            analyze_physique_all_athletes,
            analyze_dominant_sports
        )
        
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(output_dir, exist_ok=True)
        
        print("Đang tính toán các thống kê...")
        
        # Tính toán các thống kê
        medal_tally = calculate_medal_tally(df)
        gender_stats = analyze_gender_participation(df)
        age_stats = analyze_medals_and_participants_by_age(df)
        physique_stats = analyze_physique_all_athletes(df)
        dominant_sports = analyze_dominant_sports(df)
        
        # Tạo dictionary chứa tất cả kết quả
        data_dict = {
            "Tổng sắp huy chương": medal_tally,
            "Thống kê giới tính": gender_stats,
            "Thống kê độ tuổi": age_stats,
            "Thống kê thể chất": physique_stats,
            "Thế mạnh quốc gia": dominant_sports
        }
        
        # Xuất ra Excel
        file_path = os.path.join(output_dir, "comprehensive_report.xlsx")
        success = export_multiple_sheets(data_dict, file_path)
        
        if success:
            print(f"Đã tạo báo cáo tổng hợp: {file_path}")
            return file_path
        else:
            return None
            
    except Exception as e:
        print(f"Lỗi khi xuất báo cáo tổng hợp: {e}")
        return None


def export_filtered_data(df, filters, output_path, format='excel'):
    """
    Xuất dữ liệu đã được lọc theo các điều kiện.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame gốc
    filters : dict
        Dictionary chứa các điều kiện lọc
        Ví dụ: {"team": "Vietnam", "year": 2016, "season": "Summer"}
    output_path : str
        Đường dẫn file xuất
    format : str, default='excel'
        Định dạng xuất ('excel' hoặc 'csv')
        
    Returns:
    --------
    bool
        True nếu xuất thành công, False nếu có lỗi
        
    Ví dụ:
    ------
    >>> filters = {"team": "Vietnam", "year": 2016}
    >>> export_filtered_data(df, filters, "results/vietnam_2016.xlsx")
    """
    try:
        from modules.analysis import (
            filter_data_number,
            filter_data_string,
            filter_season_and_year
        )
        
        # Áp dụng các bộ lọc
        df_filtered = df.copy()
        
        # Lọc theo số
        number_filters = {k: v for k, v in filters.items() 
                         if k in ['age', 'height', 'weight', 'year', 'sex']}
        if number_filters:
            df_filtered = filter_data_number(df_filtered, **number_filters)
        
        # Lọc theo chuỗi
        string_filters = {k: v for k, v in filters.items() 
                         if k in ['team', 'noc', 'season', 'city', 'sport']}
        if string_filters:
            df_filtered = filter_data_string(df_filtered, **string_filters)
        
        # Lọc theo mùa và năm
        if 'season' in filters and 'year' in filters:
            df_filtered = filter_season_and_year(
                df_filtered, 
                season=filters.get('season'),
                year=filters.get('year')
            )
        
        # Xuất theo định dạng
        if format.lower() == 'excel':
            return export_to_excel(df_filtered, output_path, 
                                 sheet_name="Filtered Data", index=False)
        else:
            return export_to_csv(df_filtered, output_path, index=False)
            
    except Exception as e:
        print(f"Lỗi khi xuất dữ liệu đã lọc: {e}")
        return False

