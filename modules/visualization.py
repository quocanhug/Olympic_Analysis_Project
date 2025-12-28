import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import StandardScaler

# --- CẤU HÌNH GIAO DIỆN ---


def setup_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10


setup_style()

# --- NHÓM BIỂU ĐỒ CƠ BẢN ---


def plot_gender_trend(df):
    """ Xu hướng giới tính. So sánh số lượng VĐV Nam vs Nữ tham gia qua các kỳ Olympic. """
    data = df.groupby(['Year', 'Sex'])['ID'].nunique().unstack()

    # Gán biến fig để trả về cho UI
    fig = plt.figure(figsize=(10, 6))

    plt.plot(data.index, data['M'], marker='.',
             markersize=8, linewidth=2, label='Nam')
    plt.plot(data.index, data['F'], marker='.',
             markersize=8, linewidth=2, color='red', label='Nữ')
    plt.title('Xu hướng tham gia của VĐV Nam và Nữ qua các năm')
    plt.legend()

    return fig  # Trả về hình thay vì show()


def plot_top_medals(df, top_n=10):
    """Top quốc gia đạt huy chương."""
    df_medals = df[df['Medal'] != 'No Medal']
    top_countries = df_medals['NOC'].value_counts().head(top_n)

    fig = plt.figure(figsize=(10, 6))

    plt.bar(top_countries.index, top_countries.values,
            color=sns.color_palette("viridis", top_n))
    plt.title(f'Top {top_n} quốc gia đạt nhiều huy chương nhất lịch sử')
    plt.xticks(rotation=45)

    return fig


def plot_physical_distribution(df):
    """ Biểu đồ phân phối: Tuổi, Chiều cao, Cân nặng. """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # 1. Biểu đồ Tuổi
    sns.histplot(data=df, x='Age', bins=30, ax=axes[0], color='#9b59b6')
    mean_age = df['Age'].mean()
    axes[0].axvline(mean_age, color='red', linestyle='--',
                    linewidth=2, label=f'TB: {mean_age:.1f} tuổi')
    axes[0].set_title('Phân bố Độ tuổi')
    axes[0].legend()

    # 2. Biểu đồ Chiều cao
    sns.histplot(data=df, x='Height', bins=30, ax=axes[1], color='#3498db')
    mean_height = df['Height'].mean()
    axes[1].axvline(mean_height, color='red', linestyle='--',
                    linewidth=2, label=f'TB: {mean_height:.1f} cm')
    axes[1].set_title('Phân bố Chiều cao')
    axes[1].legend()

    # 3. Biểu đồ Cân nặng
    sns.histplot(data=df, x='Weight', bins=30, ax=axes[2], color='#2ecc71')
    mean_weight = df['Weight'].mean()
    axes[2].axvline(mean_weight, color='red', linestyle='--',
                    linewidth=2, label=f'TB: {mean_weight:.1f} kg')
    axes[2].set_title('Phân bố Cân nặng')
    axes[2].legend()

    plt.tight_layout()
    return fig


def plot_physical_comparison_by_sport(df):
    """ So sánh thể chất giữa các môn (Boxplot) """
    top_sports = df['Sport'].value_counts().head(10).index
    df_top = df[df['Sport'].isin(top_sports)]

    fig, axes = plt.subplots(2, 1, figsize=(12, 12))

    sns.boxplot(data=df_top, x='Sport', y='Height',
                ax=axes[0], hue='Sport', palette='viridis', legend=False)
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].set_title('So sánh Chiều cao giữa các môn')

    sns.boxplot(data=df_top, x='Sport', y='Weight',
                ax=axes[1], hue='Sport', palette='magma', legend=False)
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].set_title('So sánh Cân nặng giữa các môn')

    plt.tight_layout()
    return fig

# --- NHÓM BIỂU ĐỒ NÂNG CAO ---


def plot_athlete_clustering(df):
    """ Phân cụm VĐV (KMeans) """
    df_cluster = df[['Age', 'Weight']].dropna().copy()
    if len(df_cluster) == 0:
        return None

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_cluster)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df_cluster['Cluster'] = kmeans.fit_predict(X_scaled)

    cluster_means = df_cluster.groupby(
        'Cluster')['Weight'].mean().sort_values()
    mapping = {original: new for new,
               original in enumerate(cluster_means.index)}
    df_cluster['Sorted_Cluster'] = df_cluster['Cluster'].map(mapping)

    custom_colors = ['#FFD700', '#008080', '#4B0082']
    cmap = ListedColormap(custom_colors)

    fig = plt.figure(figsize=(10, 6))

    scatter = plt.scatter(df_cluster['Age'], df_cluster['Weight'],
                          c=df_cluster['Sorted_Cluster'], cmap=cmap, s=50, alpha=0.6)

    handles, _ = scatter.legend_elements()
    legend_labels = [
        'Nhóm 1: Nhẹ/Trẻ (Vàng)', 'Nhóm 2: Trung bình (Xanh)', 'Nhóm 3: Nặng/Già (Tím)']
    plt.legend(handles, legend_labels,
               title="Phân nhóm thể trạng", loc='upper right')

    plt.title('Phân cụm VĐV theo Tuổi và Cân nặng ')
    plt.xlabel('Tuổi (Age)')
    plt.ylabel('Cân nặng (Weight) - kg')

    return fig


def plot_host_advantage_china(df):
    """ Hiệu ứng 'Lợi thế sân nhà' của TQ năm 2008 """
    years = [1996, 2000, 2004, 2008, 2012, 2016]
    df_chn = df[(df['NOC'] == 'CHN') &
                (df['Year'].isin(years)) &
                (df['Medal'] != 'No Medal') &
                (df['Medal'].notna())]
    medals = df_chn.groupby('Year')['Medal'].count()

    fig = plt.figure(figsize=(10, 6))
    plt.bar(medals.index.astype(str), medals.values, color='red')
    plt.title('Lợi thế sân nhà TQ tại Olympic 2008')

    return fig


def plot_geopolitics_impact(df):
    """ Ảnh hưởng chiến tranh lạnh (1980, 1984) """
    summer = df[df['Season'] == 'Summer']
    noc_count = summer.groupby('Year')['NOC'].nunique()

    fig = plt.figure(figsize=(10, 6))
    plt.plot(noc_count.index, noc_count.values,
             marker='o', color='green', linewidth=2)
    plt.title('Số lượng quốc gia tham dự & Ảnh hưởng Chiến tranh lạnh')

    # Highlight
    plt.annotate('Tẩy chay 1980\n(Moscow)', xy=(1980, noc_count[1980]), xytext=(1960, 120),
                 arrowprops=dict(facecolor='red', shrink=0.05), color='red', fontweight='bold')
    plt.annotate('Tẩy chay 1984\n(Los Angeles)', xy=(1984, noc_count[1984]), xytext=(1990, 100),
                 arrowprops=dict(facecolor='red', shrink=0.05), color='red', fontweight='bold')

    return fig

# --- NHÓM 3: THỐNG KÊ VỀ VIỆT NAM ---


def plot_vietnam_stats(df):
    """ Thống kê Việt Nam: Số lượng VĐV và Môn thế mạnh """
    df_vn = df[df['NOC'] == 'VIE']
    if df_vn.empty:
        print("Không tìm thấy dữ liệu về Việt Nam")
        return None

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Biểu đồ số lượng VĐV
    vn_part = df_vn.groupby('Year')['ID'].nunique()
    sns.barplot(x=vn_part.index.astype(str),
                y=vn_part.values, ax=ax1, color='red')
    ax1.set_title('Số lượng VĐV Việt Nam tham gia Olympic')
    ax1.tick_params(axis='x', rotation=90)

    # Biểu đồ môn thế mạnh
    top_sports = df_vn['Sport'].value_counts().head(5)
    sns.barplot(x=top_sports.values, y=top_sports.index, ax=ax2,
                hue=top_sports.index, palette='OrRd', legend=False)
    ax2.set_title('Top 5 Môn thể thao Việt Nam tham gia nhiều nhất')

    plt.tight_layout()
    return fig


def plot_vietnam_details(df):
    """ Bảng vàng thành tích Việt Nam """
    df_vn = df[df['NOC'] == 'VIE']
    medals = df_vn[df_vn['Medal'].isin(
        ['Gold', 'Silver', 'Bronze'])].sort_values('Year')

    if medals.empty:
        return None

    cell_text = [[row['Year'], row['Name'], row['Sport'], row['Medal']]
                 for _, row in medals.iterrows()]

    fig, ax = plt.subplots(figsize=(12, len(cell_text)*0.5 + 2))
    ax.axis('off')
    ax.table(cellText=cell_text, colLabels=[
             "Năm", "VĐV", "Môn", "Huy chương"], loc='center').scale(1, 2)
    plt.title("Danh sách Huy chương của Đoàn thể thao Việt Nam")

    return fig
