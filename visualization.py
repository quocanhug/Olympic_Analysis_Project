import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# CẤU HÌNH GIAO DIỆN
def setup_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['axes.labelsize'] = 12
    # plt.rcParams['font.sans-serif'] = ['Arial'] # Bật nếu lỗi font tiếng Việt

setup_style()

# NHÓM BIỂU ĐỒ CƠ BẢN

def plot_gender_trend(df):
    """Biểu đồ đường: Xu hướng Nam/Nữ"""
    data = df.groupby(['Year', 'Sex'])['ID'].nunique().unstack()
    plt.figure()
    plt.plot(data.index, data['M'], marker='o', label='Nam', linewidth=2)
    plt.plot(data.index, data['F'], marker='o', label='Nữ', linewidth=2, color='red')
    plt.title('Xu hướng tham gia của VĐV Nam và Nữ qua các năm')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

def plot_top_medals(df, top_n=10):
    """Biểu đồ cột: Top quốc gia nhiều huy chương"""
    df_medals = df.dropna(subset=['Medal'])
    top_countries = df_medals['NOC'].value_counts().head(top_n)
    plt.figure()
    bars = plt.bar(top_countries.index, top_countries.values, color=sns.color_palette("viridis", top_n))
    plt.title(f'Top {top_n} Quốc gia có số lượng Huy chương nhiều nhất')
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width()/2., bar.get_height(), f'{int(bar.get_height())}', ha='center', va='bottom')
    plt.savefig(filename, bbox_inches='tight')
    plt.show()

def plot_physical_distribution(df):

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 1. Phân bố Tuổi
    sns.histplot(data=df, x='Age', bins=30, kde=True, color='#9b59b6', ax=axes[0])
    axes[0].set_title('Phân bố Độ tuổi (Age)')
    axes[0].set_xlabel('Tuổi (Năm)')
    axes[0].axvline(df['Age'].mean(), color='red', linestyle='--', label='Trung bình')
    axes[0].legend()

    # 2. Phân bố Chiều cao
    sns.histplot(data=df, x='Height', bins=30, kde=True, color='#3498db', ax=axes[1])
    axes[1].set_title('Phân bố Chiều cao (Height)')
    axes[1].set_xlabel('Chiều cao (cm)')
    axes[1].axvline(df['Height'].mean(), color='red', linestyle='--', label='Trung bình')
    axes[1].legend()

    # 3. Phân bố Cân nặng
    sns.histplot(data=df, x='Weight', bins=30, kde=True, color='#2ecc71', ax=axes[2])
    axes[2].set_title('Phân bố Cân nặng (Weight)')
    axes[2].set_xlabel('Cân nặng (kg)')
    axes[2].axvline(df['Weight'].mean(), color='red', linestyle='--', label='Trung bình')
    axes[2].legend()

    plt.suptitle('Tổng quan Thể chất Vận động viên Olympic (Toàn bộ các môn)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

def plot_physical_comparison_by_sport(df):
    # Lấy Top 15 môn có nhiều VĐV tham gia nhất
    top_sports = df['Sport'].value_counts().head(15).index
    df_top = df[df['Sport'].isin(top_sports)]

    fig, axes = plt.subplots(2, 1, figsize=(14, 12))

    # Boxplot Chiều cao
    sns.boxplot(data=df_top, x='Sport', y='Height', ax=axes[0], palette='viridis', order=top_sports)
    axes[0].set_title('So sánh Chiều cao giữa Top 15 môn thể thao phổ biến', fontsize=14)
    axes[0].set_ylabel('Chiều cao (cm)')
    axes[0].set_xlabel('')
    axes[0].tick_params(axis='x', rotation=45)

    # Boxplot Cân nặng
    sns.boxplot(data=df_top, x='Sport', y='Weight', ax=axes[1], palette='magma', order=top_sports)
    axes[1].set_title('So sánh Cân nặng giữa Top 15 môn thể thao phổ biến', fontsize=14)
    axes[1].set_ylabel('Cân nặng (kg)')
    axes[1].set_xlabel('Môn thể thao')
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

# NHÓM BIỂU ĐỒ NÂNG CAO

def plot_host_advantage_china(df):
    """Insight 1: Lợi thế sân nhà (Trung Quốc 2008)"""
    years = [1996, 2000, 2004, 2008, 2012, 2016]
    df_chn = df[(df['NOC'] == 'CHN') & (df['Year'].isin(years))]
    # Đếm số dòng có huy chương (Medal không phải NaN/No Medal)
    medals = df_chn[df_chn['Medal'].isin(['Gold', 'Silver', 'Bronze'])].groupby('Year')['Medal'].count()
    
    plt.figure()
    colors = ['#ff9999' if x != 2008 else '#CC0000' for x in medals.index]
    bars = plt.bar(medals.index, medals.values, color=colors, edgecolor='black')
    
    plt.title('Hiệu ứng "Lợi thế sân nhà": Trung Quốc tại Olympic 2008', fontsize=16)
    plt.xlabel('Năm'); plt.ylabel('Số lượng Huy chương')
    
    plt.annotate('SÂN NHÀ (HOST)', xy=(2008, medals[2008]), xytext=(2008, medals[2008]+30),
                 arrowprops=dict(facecolor='black', shrink=0.05), ha='center', fontweight='bold')
    plt.show()

def plot_body_evolution_100m(df):
    """Insight 2: Sự tiến hóa cơ thể VĐV chạy 100m"""
    subset = df[(df['Event'] == "Athletics Men's 100 metres") & (df['Year'] > 1900)].dropna(subset=['Height', 'Weight'])
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    sns.regplot(data=subset, x='Year', y='Height', ax=ax1, scatter_kws={'alpha':0.3, 'color':'blue'}, line_kws={'color':'blue'}, label='Chiều cao')
    ax1.set_ylabel('Chiều cao (cm)', color='blue')
    
    ax2 = ax1.twinx()
    sns.regplot(data=subset, x='Year', y='Weight', ax=ax2, scatter_kws={'alpha':0.3, 'color':'orange'}, line_kws={'color':'orange'}, label='Cân nặng')
    ax2.set_ylabel('Cân nặng (kg)', color='orange')
    
    plt.title('Sự thay đổi thể hình VĐV chạy 100m Nam qua 1 thế kỷ')
    plt.show()

def plot_geopolitics_impact(df):
    """Insight 3: Ảnh hưởng chiến tranh lạnh (1980, 1984)"""
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
# VIỆT NAM

def plot_vietnam_stats(df):
    """Việt Nam: Số lượng tham gia & Môn thế mạnh"""
    df_vn = df[df['NOC'] == 'VIE']
    if df_vn.empty: return
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    plt.subplots_adjust(hspace=0.4)
    
    # Biểu đồ 1: Số lượng VĐV
    vn_part = df_vn.groupby('Year')['ID'].nunique()
    sns.barplot(x=vn_part.index, y=vn_part.values, ax=ax1, color='#DA251D', alpha=0.8)
    ax1.set_title('Số lượng VĐV Việt Nam tham gia Olympic')
    
    # Đánh dấu sao vàng năm có huy chương
    medal_years = df_vn[df_vn['Medal'].notna()]['Year'].unique()
    years_list = list(vn_part.index)
    for year in medal_years:
        if year in years_list:
            idx = years_list.index(year)
            ax1.plot(idx, vn_part[year]+1, marker='*', color='#FFFF00', markersize=18, markeredgecolor='black')

    # Biểu đồ 2: Top môn thể thao
    top_sports = df_vn['Sport'].value_counts().head(5)
    sns.barplot(x=top_sports.values, y=top_sports.index, ax=ax2, palette='OrRd_r')
    ax2.set_title('Top 5 Môn thể thao VN tham gia nhiều nhất')
    
    plt.show()

def plot_vietnam_details(df):
    """Bảng danh sách huy chương VN"""
    df_vn = df[df['NOC'] == 'VIE']
    # Chỉ lấy dòng có huy chương (Gold/Silver/Bronze)
    medals = df_vn[df_vn['Medal'].isin(['Gold', 'Silver', 'Bronze'])].sort_values('Year')
    
    cell_text = []
    for _, row in medals.iterrows():
        cell_text.append([row['Year'], row['Name'].split('(')[0], row['Sport'], row['Medal']])
        
    if not cell_text: return

    fig, ax = plt.subplots(figsize=(10, len(cell_text)*0.8 + 1))
    ax.axis('off')
    table = ax.table(cellText=cell_text, colLabels=["Năm", "VĐV", "Môn", "Huy chương"], loc='center', cellLoc='center')
    table.set_fontsize(12); table.scale(1.2, 2)
    plt.title('Bảng vàng thành tích Thể thao Việt Nam', fontweight='bold')
    plt.show()
