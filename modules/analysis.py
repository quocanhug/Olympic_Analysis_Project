import pandas as pd
import numpy as np
def clean_team_name(df):
    """
    Làm sạch cột 'Team' bằng cách loại bỏ các ký tự số và dấu gạch ngang thừa ở cuối.
    Ví dụ: 'China-1' -> 'China', 'Denmark/Sweden-2' -> 'Denmark/Sweden'.
    Mục đích: Giúp thống kê thành tích quốc gia chính xác hơn, tránh việc một nước bị chia thành nhiều team nhỏ.
    """
    df = df.copy()
    df['Team'] = df['Team'].str.replace(r'-\d+', '', regex=True)
    return df
def clean_event_name(df):
    """
    Làm sạch cột 'Event' bằng cách cắt bỏ tên môn thể thao (Sport) bị lặp lại ở đầu.
    Ví dụ: Sport='Basketball', Event='Basketball Men's Basketball' -> 'Men's Basketball'.
    Mục đích: Làm ngắn gọn tên sự kiện, giúp bảng biểu hiển thị đẹp và dễ đọc hơn.
    """
    df = df.copy()
    df['Event'] = df.apply(lambda x: x['Event'][len(x['Sport']):].strip()
    if x['Event'].startswith(x['Sport']) else x['Event'], axis=1)
    return df
def extract_nickname(df):
    """
    Trích xuất biệt danh (Nickname) từ cột 'Name' ra một cột riêng.
    Thường biệt danh nằm trong dấu ngoặc kép "" hoặc đôi khi là ngoặc đơn ().
    Mục đích: Tách biệt danh để phân tích hoặc hiển thị tên vận động viên gọn gàng hơn.
    """
    df = df.copy()
    nickname_quotes = df['Name'].str.extract(r'\"(.*?)\"', expand=False)
    nickname_parens = df['Name'].str.extract(r'\((.*?)\)', expand=False)
    df['Nickname'] = nickname_quotes.combine_first(nickname_parens)
    cols = list(df.columns)
    if 'Nickname' in cols: cols.remove('Nickname')
    name_index = cols.index('Name')
    new_cols_order = cols[:name_index + 1] + ['Nickname'] + cols[name_index + 1:]
    return df[new_cols_order]
# loc du lieu
def filter_data_number(df, age=None, height=None, weight=None, year=None, sex=None):
    """
    Lọc dữ liệu theo các chỉ số dạng số (lớn hơn hoặc bằng) và giới tính.
    Ví dụ: Tìm VĐV cao trên 1m80, nặng trên 80kg thi đấu từ năm 2000.
    Mục đích: Phân tích nhóm vận động viên có thể hình hoặc độ tuổi cụ thể.
    """
    df_filter = df.copy()
    if age is not None:
        df_filter = df_filter[df_filter['Age'] >= age]
    if height is not None:
        df_filter = df_filter[df_filter['Height'] >= height]
    if weight is not None:
        df_filter = df_filter[df_filter['Weight'] >= weight]
    if year is not None:
        df_filter = df_filter[df_filter['Year'] >= year]
    if sex is not None:
        df_filter = df_filter[df_filter['Sex'].str.lower() == sex.lower()]
    df_filter = df_filter.sort_values("Year", ascending=False)
    return df_filter
def filter_data_string(df, team=None, noc=None, season=None, city=None, sport=None, sex=None):
    """
    Lọc dữ liệu theo các từ khóa chính xác (Team, NOC, Mùa, Thành phố, Môn).
    Ví dụ: Lọc toàn bộ VĐV của đoàn 'Vietnam' tham gia mùa 'Summer'.
    Mục đích: Truy xuất dữ liệu chi tiết cho một đối tượng cụ thể.
    """
    df_filter = df.copy()
    if team is not None:
        df_filter = df_filter[df_filter['Team'].str.lower() == team.lower()]
    if noc is not None:
        df_filter = df_filter[df_filter['NOC'].str.lower() == noc.lower()]
    if season is not None:
        df_filter = df_filter[df_filter['Season'].str.lower() == season.lower()]
    if city is not None:
        df_filter = df_filter[df_filter['City'].str.lower() == city.lower()]
    if sport is not None:
        df_filter = df_filter[df_filter['Sport'].str.lower() == sport.lower()]
    if sex is not None:
        df_filter = df_filter[df_filter['Sex'].str.lower() == sex.lower()]
    df_filter = df_filter.sort_values("Year", ascending=False)
    return df_filter
def filter_season_and_year(df, season=None, year=None):
    """
    Lọc dữ liệu theo Mùa giải và Năm tổ chức cụ thể.
    Ví dụ: Chỉ lấy dữ liệu của Thế vận hội Mùa hè năm 2016.
    Mục đích: Tập trung phân tích vào một kỳ Olympic cụ thể.
    """
    df_filter = df.copy()
    if season is not None and year is not None:
        df_filter = df_filter[
            (df_filter['Year'] == year) &
            (df_filter['Season'].str.lower() == season.lower())
            ]
    elif season is not None:
        df_filter = df_filter[df_filter['Season'].str.lower() == season.lower()]
        df_filter = df_filter.sort_values("Year", ascending=False)
    elif year is not None:
        df_filter = df_filter[df_filter['Year'] == year]
    return df_filter
def filter_medals(df, type_medal):
    """
    Lọc danh sách vận động viên đạt loại huy chương cụ thể (Gold, Silver, Bronze).
    Mục đích: Tạo bảng vinh danh hoặc phân tích đặc điểm của những người chiến thắng.
    """
    df_filter = df.copy()
    # Loại bỏ các dòng không có huy chương trước
    df_filter = df_filter.dropna(subset=['Medal'])
    # Lọc theo loại huy chương yêu cầu
    df_filter = df_filter[df_filter['Medal'] == type_medal]
    return df_filter
# thong ke du lieu:
def calculate_medal_tally(df):
    """
    Tính tổng sắp huy chương theo Quốc gia.
    """
    # Bước quan trọng: Trong môn đồng đội (vd: Bóng đá), mỗi cầu thủ có 1 dòng.
    # Nếu đếm dòng sẽ sai số huy chương của quốc gia. Cần drop duplicates.
    subset_data = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Event', 'Medal'])
    # Chỉ lấy những dòng có huy chương
    subset_data = subset_data.dropna(subset=['Medal'])
    # Dùng pivot_table để tạo bảng tổng sắp (Gold, Silver, Bronze thành các cột)
    medal_tally = subset_data.pivot_table(
        index='NOC',
        columns='Medal',
        values='Event',
        aggfunc='count',
        fill_value=0
    )
    cols = ['Gold', 'Silver', 'Bronze']
    existing_cols = [c for c in cols if c in medal_tally.columns]
    medal_tally = medal_tally[existing_cols]
    # Sắp xếp giảm dần theo số lượng huy chương Vàng
    if 'Gold' in medal_tally.columns:
        medal_tally = medal_tally.sort_values(by='Gold', ascending=False)
    return medal_tally
def analyze_gender_participation(df):
    """
    Phân tích số lượng Nam/Nữ qua các năm.
    """
    # Đếm số lượng unique ID (VĐV thực tế) theo Năm và Giới tính
    gender_counts = df.groupby(['Year', 'Sex'])['ID'].nunique()
    # Unstack để chuyển Nam/Nữ thành 2 cột riêng biệt
    gender_counts = gender_counts.unstack(fill_value=0)
    return gender_counts
def analyze_medals_and_participants_by_age(df):
    """
    Thống kê số lượng huy chương VÀ số lượng người tham gia theo nhóm tuổi.
    """
    # 1. Lọc dữ liệu: Chỉ bỏ những dòng thiếu thông tin Tuổi (giữ lại người không có huy chương)
    df_age = df.dropna(subset=['Age']).copy()
    # 2. Định nghĩa các khoảng tuổi (bins) và nhãn (labels)
    bins = [0, 20, 30, 40, 50, 100]
    labels = ['U20', '20-30', '30-40', '40-50', 'Over 50']
    # 3. Tạo cột phân nhóm tuổi
    df_age['AgeGroup'] = pd.cut(df_age['Age'], bins=bins, labels=labels, right=False)
    # 4. Gom nhóm và tính toán 2 chỉ số cùng lúc bằng hàm agg
    stats = df_age.groupby('AgeGroup', observed=False).agg({
        'Medal': 'count',
        'ID': 'nunique'
    })
    # 5. Đổi tên cột cho dễ hiểu
    stats.columns = ['Medal_Count', 'Participant_Count']
    stats['Medal_Ratio'] = round(stats['Medal_Count'] / stats['Participant_Count'], 2)
    return stats
def analyze_physique_all_athletes(df):
    """
    Tính chiều cao, cân nặng trung bình và BMI của TẤT CẢ VĐV (kể cả không có huy chương) theo từng môn.
    Trả về DataFrame sắp xếp giảm dần theo Cân nặng, Chiều cao và BMI. chỉ ra mối tương quan của cơ thể
    với các môn thể thao
    """
    # 1. Lọc dữ liệu: Chỉ bỏ những dòng thiếu Chiều cao hoặc Cân nặng
    valid_data = df.dropna(subset=['Height', 'Weight'])
    # 2. Group theo Môn thể thao và tính trung bình Chiều cao, Cân nặng
    physique_stats = valid_data.groupby('Sport')[['Height', 'Weight']].mean()
    # 3. Tạo cột BMI
    physique_stats['BMI'] = physique_stats['Weight'] / ((physique_stats['Height'] / 100) ** 2)
    # 4. Sắp xếp giảm dần theo 3 tiêu chí: Cân nặng -> Chiều cao -> BMI
    physique_stats = physique_stats.sort_values(
        by=['Weight', 'Height', 'BMI'],
        ascending=[False, False, False]
    )
    return physique_stats.round(2)
def analyze_dominant_sports(df):
    """
    Thống kê số lượng huy chương của từng Quốc gia (Team) theo từng Môn thể thao (Sport).
    Mục đích: Chỉ ra thế mạnh của từng quốc gia (Ví dụ: Trung Quốc mạnh Cầu lông, Mỹ mạnh Bơi lội).
    """
    # 1. Chỉ lấy dữ liệu có huy chương
    medals_df = df.dropna(subset=['Medal'])
    # 2. Xử lý môn đồng đội:
    # Nếu không drop duplicates, đội bóng 11 người sẽ được tính là 11 huy chương
    # Ta giữ lại 1 dòng đại diện cho mỗi nội dung thi đấu (Event) của mỗi quốc gia trong mỗi kỳ vận hội.
    medals_df = medals_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Event', 'Medal'])
    # 3. Gom nhóm theo Quốc gia (Team) và Môn thể thao (Sport) rồi đếm số huy chương
    sport_strength = medals_df.groupby(['Team', 'Sport'])['Event'].count().reset_index()
    sport_strength.rename(columns={'Event': 'Medal_Count'}, inplace=True)
    # 4. Sắp xếp dữ liệu
    # Ưu tiên sắp xếp theo Quốc gia (A-Z), sau đó đến Số huy chương giảm dần (để môn mạnh nhất lên đầu)
    sport_strength = sport_strength.sort_values(by=['Team', 'Medal_Count'], ascending=[True, False])
    return sport_strength
