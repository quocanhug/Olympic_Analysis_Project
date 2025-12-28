import pandas as pd
import numpy as np

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
        df_filter = df_filter[df_filter['Season'].str.lower()
                              == season.lower()]
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
        df_filter = df_filter[df_filter['Season'].str.lower()
                              == season.lower()]
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
    subset_data = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Event', 'Medal'])
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
    df_age['AgeGroup'] = pd.cut(
        df_age['Age'], bins=bins, labels=labels, right=False)
    # 4. Gom nhóm và tính toán 2 chỉ số cùng lúc bằng hàm agg
    stats = df_age.groupby('AgeGroup', observed=False).agg({
        'Medal': 'count',
        'ID': 'nunique'
    })
    # 5. Đổi tên cột cho dễ hiểu
    stats.columns = ['Medal_Count', 'Participant_Count']
    stats['Medal_Ratio'] = round(
        stats['Medal_Count'] / stats['Participant_Count'], 2)
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
    physique_stats['BMI'] = physique_stats['Weight'] / \
        ((physique_stats['Height'] / 100) ** 2)
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
    medals_df = medals_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Event', 'Medal'])
    # 3. Gom nhóm theo Quốc gia (Team) và Môn thể thao (Sport) rồi đếm số huy chương
    sport_strength = medals_df.groupby(['Team', 'Sport'])[
        'Event'].count().reset_index()
    sport_strength.rename(columns={'Event': 'Medal_Count'}, inplace=True)
    # 4. Sắp xếp dữ liệu
    # Ưu tiên sắp xếp theo Quốc gia (A-Z), sau đó đến Số huy chương giảm dần (để môn mạnh nhất lên đầu)
    sport_strength = sport_strength.sort_values(
        by=['Team', 'Medal_Count'], ascending=[True, False])
    return sport_strength

def get_country_performance_and_hosts(df, noc_code):
    """
    1. DataFrame thống kê số huy chương theo năm của quốc gia (noc_code).
    2. List các năm mà quốc gia đó là chủ nhà.
    """
    # 1. Từ điển ánh xạ Thành phố đăng cai -> Mã quốc gia (NOC)
    city_to_noc = {
        'Beijing': 'CHN', 'London': 'GBR', 'Sydney': 'AUS', 'Athens': 'GRE',
        'Atlanta': 'USA', 'Los Angeles': 'USA', 'Salt Lake City': 'USA', 'St. Louis': 'USA', 'Lake Placid': 'USA',
        'Barcelona': 'ESP', 'Seoul': 'KOR', 'Moscow': 'URS', 'Sochi': 'RUS',
        'Tokyo': 'JPN', 'Nagano': 'JPN', 'Sapporo': 'JPN',
        'Paris': 'FRA', 'Albertville': 'FRA', 'Grenoble': 'FRA',
        'Munich': 'GER', 'Berlin': 'GER', 'Garmisch-Partenkirchen': 'GER',
        'Rome': 'ITA', 'Turin': 'ITA', 'Cortina d\'Ampezzo': 'ITA',
        'Rio de Janeiro': 'BRA', 'Montreal': 'CAN', 'Vancouver': 'CAN', 'Calgary': 'CAN',
        'Mexico City': 'MEX', 'Helsinki': 'FIN', 'Stockholm': 'SWE',
        'Melbourne': 'AUS', 'Amsterdam': 'NED', 'Antwerpen': 'BEL'
    }
    # 2. Tìm các năm làm chủ nhà
    # Lọc các dòng trong dữ liệu mà City tương ứng với noc_code đầu vào
    host_data = df[df['City'].map(city_to_noc) == noc_code]
    host_years = sorted(host_data['Year'].unique().tolist())
    # 3. Thống kê huy chương từng năm của quốc gia đó
    # Lọc quốc gia -> Lọc có huy chương -> Bỏ trùng môn đồng đội -> Đếm
    country_df = df[(df['NOC'] == noc_code) & (df['Medal'] != 'No Medal')]
    # Quan trọng: Drop duplicates để môn đồng đội (bóng đá,...) chỉ tính 1 huy chương
    country_df = country_df.drop_duplicates(subset=['Event', 'Year', 'Medal'])
    # Đếm số lượng
    medal_trend = country_df.groupby('Year')['Medal'].count().reset_index()
    medal_trend.columns = ['Year', 'Medal_Count']
    return medal_trend, host_years


def analyze_vietnam_participation(df):
    """Thống kê tổng quan Việt Nam."""
    df_vn = df[df['NOC'] == 'VIE'].copy()
    if df_vn.empty:
        return pd.DataFrame()
    stats = df_vn.groupby('Year').agg({
        'ID': 'nunique',
        'Sport': lambda x: sorted(list(set(x)))
    }).reset_index()
    stats.columns = ['Year', 'Athlete_Count', 'Sports_List']
    stats['Sports_Count'] = stats['Sports_List'].apply(len)
    stats['Sports_Text'] = stats['Sports_List'].apply(lambda x: ", ".join(x))
    return stats.sort_values('Year')


def get_vietnam_medals(df):
    """Lấy danh sách huy chương Việt Nam (Hàm đang bị báo lỗi thiếu)."""
    df_vn = df[df['NOC'] == 'VIE']
    # Lọc lấy Gold, Silver, Bronze
    medals = df_vn[df_vn['Medal'].isin(['Gold', 'Silver', 'Bronze'])].sort_values('Year')
    return medals[['Year', 'Name', 'Sport', 'Event', 'Medal']]


def analyze_physical_summary(df):
    """Thống kê Min/Max/Mean cho Thể chất (Hàm đang bị thiếu)."""
    valid_age = df['Age'].dropna()
    valid_height = df['Height'].dropna()
    valid_weight = df['Weight'].dropna()

    summary = {
        'Age': {'Mean': round(valid_age.mean(), 1), 'Max': valid_age.max()},
        'Height': {'Mean': round(valid_height.mean(), 1), 'Max': valid_height.max()},
        'Weight': {'Mean': round(valid_weight.mean(), 1), 'Max': valid_weight.max()}
    }
    return summary


def analyze_physique_by_sport(df):
    """Thống kê thể chất theo môn (Hàm đang bị thiếu)."""
    valid_data = df.dropna(subset=['Height', 'Weight'])
    physique_stats = valid_data.groupby('Sport')[['Height', 'Weight']].mean()
    physique_stats['BMI'] = physique_stats['Weight'] / ((physique_stats['Height'] / 100) ** 2)
    return physique_stats.sort_values(by='Weight', ascending=False).round(2)