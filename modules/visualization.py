import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
# CẤU HÌNH GIAO DIỆN 

from sklearn.cluster import KMeans 
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import StandardScaler

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
    data = df.groupby(['Year', 'Sex'])['ID'].nunique().unstack()
    plt.figure(figsize=(10, 6)) 
    plt.plot(data.index, data['M'], marker='.', markersize=8, linewidth=2)
    plt.plot(data.index, data['F'], marker='.', markersize=8, linewidth=2, color='red')
    plt.title('Xu hướng giới tính')
    plt.show()

def plot_top_medals(df, top_n=10):
    df_medals = df[(df['Medal'].notna()) & (df['Medal'] != 'No Medal')]
    top_countries = df_medals['NOC'].value_counts().head(top_n)
    plt.figure(figsize=(10, 6)) 
    plt.bar(top_countries.index, top_countries.values, color=sns.color_palette("viridis", top_n))
    plt.title(f'Top {top_n} quốc gia đạt huy chương nhiều nhất')

# CÁC BIỂU ĐỒ CƠ BẢN VÀ THỐNG KÊ MÔ TẢ

def plot_gender_trend(df):
    """ Xu hướng giới tính. So sánh số lượng VĐV Nam vs Nữ tham gia qua các kỳ Olympic.
    """
    data = df.groupby(['Year', 'Sex'])['ID'].nunique().unstack()
    plt.figure(figsize=(10, 6)) 
    plt.plot(data.index, data['M'], marker='.', markersize=8, linewidth=2, label='Nam')
    plt.plot(data.index, data['F'], marker='.', markersize=8, linewidth=2, color='red', label='Nữ')
    plt.title('Xu hướng tham gia của VĐV Nam và Nữ qua các năm')
    plt.legend()
    plt.show()

def plot_top_medals(df, top_n=10):
    """Top quốc gia đạt huy chương. Thống kê và xếp hạng các quốc gia có tổng số huy chương nhiều nhất.
    """
    # Lọc bỏ những người không đạt giải
    df_medals = df[df['Medal'] != 'No Medal'] 
    # Đếm số lượng theo quốc gia (NOC)
    top_countries = df_medals['NOC'].value_counts().head(top_n) 
    plt.figure(figsize=(10, 6)) 
    plt.bar(top_countries.index, top_countries.values, color=sns.color_palette("viridis", top_n))
    plt.title(f'Top {top_n} quốc gia đạt nhiều huy chương nhất lịch sử') 
    plt.xticks(rotation=45)
    plt.show() 

def plot_physical_distribution(df):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    sns.histplot(data=df, x='Age', bins=30, ax=axes[0], color='#9b59b6')
    sns.histplot(data=df, x='Height', bins=30, ax=axes[1], color='#3498db')
    sns.histplot(data=df, x='Weight', bins=30, ax=axes[2], color='#2ecc71')
    """ Tuổi, Chiều cao, Cân nặng. Xem xét sự phân bố thể chất chung của toàn bộ VĐV.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Biểu đồ Tuổi
    sns.histplot(data=df, x='Age', bins=30, ax=axes[0], color='#9b59b6')
    axes[0].set_title('Phân bố Độ tuổi')
    
    # Biểu đồ Chiều cao
    sns.histplot(data=df, x='Height', bins=30, ax=axes[1], color='#3498db')
    axes[1].set_title('Phân bố Chiều cao')
    
    # Biểu đồ Cân nặng
    sns.histplot(data=df, x='Weight', bins=30, ax=axes[2], color='#2ecc71')
    axes[2].set_title('Phân bố Cân nặng')
    
    plt.tight_layout()
    plt.show() 

def plot_physical_distribution(df):
    """
    Biểu đồ phân phối: Tuổi, Chiều cao, Cân nặng.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 1. Biểu đồ Tuổi 
    sns.histplot(data=df, x='Age', bins=30, ax=axes[0], color='#9b59b6')
    mean_age = df['Age'].mean()
    axes[0].axvline(mean_age, color='red', linestyle='--', linewidth=2, label=f'TB: {mean_age:.1f} tuổi')
    axes[0].set_title('Phân bố Độ tuổi')
    axes[0].legend() 
    
    #  2. Biểu đồ Chiều cao 
    sns.histplot(data=df, x='Height', bins=30, ax=axes[1], color='#3498db')
    mean_height = df['Height'].mean()
    axes[1].axvline(mean_height, color='red', linestyle='--', linewidth=2, label=f'TB: {mean_height:.1f} cm')
    axes[1].set_title('Phân bố Chiều cao')
    axes[1].legend()
    
    # Biểu đồ Cân nặng 
    sns.histplot(data=df, x='Weight', bins=30, ax=axes[2], color='#2ecc71')
    mean_weight = df['Weight'].mean()
    axes[2].axvline(mean_weight, color='red', linestyle='--', linewidth=2, label=f'TB: {mean_weight:.1f} kg')
    axes[2].set_title('Phân bố Cân nặng')
    axes[2].legend() 
    plt.tight_layout()
    plt.show() 

def plot_physical_comparison_by_sport(df):
    top_sports = df['Sport'].value_counts().head(10).index
    df_top = df[df['Sport'].isin(top_sports)]
    fig, axes = plt.subplots(2, 1, figsize=(12, 12))
    
    sns.boxplot(data=df_top, x='Sport', y='Height', ax=axes[0], hue='Sport', palette='viridis', legend=False)
    axes[0].tick_params(axis='x', rotation=45)
    
    sns.boxplot(data=df_top, x='Sport', y='Weight', ax=axes[1], hue='Sport', palette='magma', legend=False)
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show() 

# --- NHÓM BIỂU ĐỒ NÂNG CAO ---

def plot_host_advantage_china(df):
    """So sánh thể chất giữa các môn"""
    top_sports = df['Sport'].value_counts().head(10).index
    df_top = df[df['Sport'].isin(top_sports)]
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 12))
    
    sns.boxplot(data=df_top, x='Sport', y='Height', ax=axes[0], hue='Sport', palette='viridis', legend=False)
    axes[0].set_title('So sánh Chiều cao giữa các môn')
    axes[0].tick_params(axis='x', rotation=45)
    
    sns.boxplot(data=df_top, x='Sport', y='Weight', ax=axes[1], hue='Sport', palette='magma', legend=False)
    axes[1].set_title('So sánh Cân nặng giữa các môn')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

def plot_athlete_clustering(df):
    """ Gom nhóm các VĐV dựa trên sự tương đồng về Tuổi và Cân nặng. Phát hiện các nhóm đặc thù (VD: Nhóm trẻ nhẹ cân, Nhóm già nặng cân...).
    """
    df_cluster = df[['Age', 'Weight']].dropna().copy()
    if len(df_cluster) == 0: return
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_cluster)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df_cluster['Cluster'] = kmeans.fit_predict(X_scaled)

    cluster_means = df_cluster.groupby('Cluster')['Weight'].mean().sort_values()
    mapping = {original: new for new, original in enumerate(cluster_means.index)}
    df_cluster['Sorted_Cluster'] = df_cluster['Cluster'].map(mapping)
    custom_colors = ['#FFD700', '#008080', '#4B0082'] 
    cmap = ListedColormap(custom_colors)
    
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df_cluster['Age'], df_cluster['Weight'], 
                          c=df_cluster['Sorted_Cluster'], cmap=cmap, s=50, alpha=0.6)
 
    handles, _ = scatter.legend_elements()
    legend_labels = ['Nhóm 1: Nhẹ/Trẻ (Vàng)', 'Nhóm 2: Trung bình (Xanh)', 'Nhóm 3: Nặng/Già (Tím)']
    plt.legend(handles, legend_labels, title="Phân nhóm thể trạng", loc='upper right')
    
    plt.title('Phân cụm VĐV theo Tuổi và Cân nặng ')
    plt.xlabel('Tuổi (Age)')
    plt.ylabel('Cân nặng (Weight) - kg')
    plt.show()
    
# CÁC BIỂU ĐỒ PHÂN TÍCH CHUYÊN SÂU 

def plot_host_advantage_china(df):
    """
    Hiệu ứng 'Lợi thế sân nhà'. 
    So sánh thành tích của Trung Quốc tại Olympic 2008 (sân nhà) so với các năm khác.
    """
    years = [1996, 2000, 2004, 2008, 2012, 2016]
    df_chn = df[(df['NOC'] == 'CHN') & 
                    (df['Year'].isin(years)) & 
                    (df['Medal'] != 'No Medal') & 
                    (df['Medal'].notna())]
    medals = df_chn.groupby('Year')['Medal'].count()
    plt.figure(figsize=(10, 6)) 
    plt.bar(medals.index.astype(str), medals.values, color='red')
    plt.title('Lợi thế sân nhà TQ')
    plt.show()

def plot_geopolitics_impact(df):
    """ Ảnh hưởng chiến tranh lạnh (1980, 1984)"""
    summer = df[df['Season'] == 'Summer']
    noc_count = summer.groupby('Year')['NOC'].nunique()

    plt.figure()
    plt.plot(noc_count.index, noc_count.values,
             marker='o', color='green', linewidth=2)
    plt.title('Số lượng quốc gia tham dự & Ảnh hưởng Chiến tranh lạnh')
    plt.annotate('Tẩy chay 1980\n(Moscow)', xy=(1980, noc_count[1980]), xytext=(1960, 120),
                 arrowprops=dict(facecolor='red', shrink=0.05), color='red', fontweight='bold')
    plt.annotate('Tẩy chay 1984\n(Los Angeles)', xy=(1984, noc_count[1984]), xytext=(1990, 100),
                 arrowprops=dict(facecolor='red', shrink=0.05), color='red', fontweight='bold')
    plt.figure(figsize=(10, 6)) 
    plt.plot(noc_count.index, noc_count.values, linewidth=2, color='green')
    plt.title('Số quốc gia tham dự')
    plt.show() 

# --- VIỆT NAM ---

def plot_vietnam_stats(df):
    df_vn = df[df['NOC'] == 'VIE']
    if df_vn.empty: return
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12)) 
    
    vn_part = df_vn.groupby('Year')['ID'].nunique()
    sns.barplot(x=vn_part.index.astype(str), y=vn_part.values, ax=ax1, color='red')
    ax1.tick_params(axis='x', rotation=90)
    
    top_sports = df_vn['Sport'].value_counts().head(5)
    sns.barplot(x=top_sports.values, y=top_sports.index, ax=ax2, hue=top_sports.index, palette='OrRd', legend=False)
    """Ảnh hưởng chiến tranh lạnh (1980, 1984)"""
    summer = df[df['Season'] == 'Summer']
    noc_count = summer.groupby('Year')['NOC'].nunique()
    
    plt.figure()
    plt.plot(noc_count.index, noc_count.values, marker='o', color='green', linewidth=2)
    plt.title('Số lượng quốc gia tham dự & Ảnh hưởng Chiến tranh lạnh')
    
    # Highlight
    plt.annotate('Tẩy chay 1980\n(Moscow)', xy=(1980, noc_count[1980]), xytext=(1960, 120),
                 arrowprops=dict(facecolor='red', shrink=0.05), color='red', fontweight='bold')
    plt.annotate('Tẩy chay 1984\n(Los Angeles)', xy=(1984, noc_count[1984]), xytext=(1990, 100),
                 arrowprops=dict(facecolor='red', shrink=0.05), color='red', fontweight='bold')
    plt.show() 
    

# NHÓM 3: THỐNG KÊ VỀ VIỆT NAM

def plot_vietnam_stats(df):
    """
    - Biểu đồ 1: Số lượng VĐV Việt Nam tham gia qua từng năm.
    - Biểu đồ 2: Top 5 môn thể thao mà VN tham gia nhiều nhất.
    """
    df_vn = df[df['NOC'] == 'VIE']
    if df_vn.empty: 
        print("Không tìm thấy dữ liệu về Việt Nam")
        return
        
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12)) 
    
    # Biểu đồ số lượng VĐV
    vn_part = df_vn.groupby('Year')['ID'].nunique()
    sns.barplot(x=vn_part.index.astype(str), y=vn_part.values, ax=ax1, color='red')
    ax1.set_title('Số lượng VĐV Việt Nam tham gia Olympic')
    ax1.tick_params(axis='x', rotation=90)
    
    # Biểu đồ môn thế mạnh
    top_sports = df_vn['Sport'].value_counts().head(5)
    sns.barplot(x=top_sports.values, y=top_sports.index, ax=ax2, hue=top_sports.index, palette='OrRd', legend=False)
    ax2.set_title('Top 5 Môn thể thao Việt Nam tham gia nhiều nhất')
    plt.tight_layout()
    plt.show()

def plot_vietnam_details(df):
    df_vn = df[df['NOC'] == 'VIE']
    real_medals = ['Gold', 'Silver', 'Bronze']
    medals = df_vn[df_vn['Medal'].isin(real_medals)].sort_values('Year')
    cell_text = [[row['Year'], row['Name'], row['Sport'], row['Medal']] for _, row in medals.iterrows()]
    if not cell_text: return
    fig, ax = plt.subplots(figsize=(12, len(cell_text)*0.5 + 2))
    ax.axis('off')
    ax.table(cellText=cell_text, colLabels=["Năm", "VĐV", "Môn", "Huy chương"], loc='center').scale(1, 2)
    plt.show()
    """Thống kê Việt Nam: Bảng vàng thành tích.
    """
    df_vn = df[df['NOC'] == 'VIE']
    medals = df_vn[df_vn['Medal'].isin(['Gold', 'Silver', 'Bronze'])].sort_values('Year')
    cell_text = [[row['Year'], row['Name'], row['Sport'], row['Medal']] for _, row in medals.iterrows()]  
    if not cell_text: 
        print("Việt Nam chưa có huy chương nào trong dữ liệu này.")
        return
    fig, ax = plt.subplots(figsize=(12, len(cell_text)*0.5 + 2))
    ax.axis('off')
    ax.table(cellText=cell_text, colLabels=["Năm", "VĐV", "Môn", "Huy chương"], loc='center').scale(1, 2)
    plt.title("Danh sách Huy chương của Đoàn thể thao Việt Nam")
    plt.show()
