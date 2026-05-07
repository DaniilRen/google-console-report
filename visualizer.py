import matplotlib.pyplot as plt
import seaborn as sns
from config import CHARTS_DIR, CHART_COLORS
import matplotlib

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Roboto', 'Arial', 'DejaVu Sans', 'WenQuanYi Zen Hei', 'Noto Sans CJK JP']
matplotlib.rcParams['axes.unicode_minus'] = False

sns.set_style("whitegrid")

class ChartGenerator:
    @staticmethod
    def create_empty_chart(output_path, message):
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, message, 
                ha='center', va='center', fontsize=14, 
                transform=plt.gca().transAxes,
                color='gray')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path
    
    @staticmethod
    def create_top_queries_chart(df, output_path):
        if df.empty:
            return ChartGenerator.create_empty_chart(output_path, "Нет данных по запросам")
        
        plt.figure(figsize=(12, 7))
        top_queries = df.groupby('query')['clicks'].sum().nlargest(10)
        
        colors = CHART_COLORS[:len(top_queries)]
        bars = plt.bar(range(len(top_queries)), top_queries.values, color=colors)
        
        plt.title('Топ-10 поисковых запросов', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Поисковый запрос', fontsize=13, labelpad=10)
        plt.ylabel('Клики', fontsize=13, labelpad=10)
        plt.xticks(range(len(top_queries)), top_queries.index, rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=11)
        
        max_value = max(top_queries.values)
        for bar, value in zip(bars, top_queries.values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (max_value * 0.01),
                    f'{int(value)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.ylim(0, max_value * 1.1)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path
    
    @staticmethod
    def create_clicks_by_device_bar_chart(df, output_path):
        if df.empty or 'device' not in df.columns:
            return ChartGenerator.create_empty_chart(output_path, "Нет данных по устройствам")
        
        device_clicks = df.groupby('device')['clicks'].sum()
        device_clicks = device_clicks[device_clicks > 0]
        
        if device_clicks.empty:
            ChartGenerator.create_empty_chart(output_path, "Нет данных по устройствам")
            return output_path
        
        device_clicks = device_clicks.sort_values(ascending=True)
        
        plt.figure(figsize=(10, 6))
        colors = CHART_COLORS[:len(device_clicks)]
        bars = plt.barh(range(len(device_clicks)), device_clicks.values, color=colors)
        
        plt.title('Клики по устройствам', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Клики', fontsize=13, labelpad=10)
        plt.ylabel('Устройство', fontsize=13, labelpad=10)
        plt.yticks(range(len(device_clicks)), device_clicks.index, fontsize=12)
        plt.xticks(fontsize=11)
        
        max_value = max(device_clicks.values)
        for bar, value in zip(bars, device_clicks.values):
            plt.text(bar.get_width() + (max_value * 0.02), 
                    bar.get_y() + bar.get_height()/2,
                    f'{int(value):,}', 
                    ha='left', va='center', fontsize=11, fontweight='bold')
        
        plt.xlim(0, max_value * 1.15)
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path
    
    @staticmethod
    def create_top_countries_chart(df, output_path):
        if df.empty or 'country' not in df.columns:
            return ChartGenerator.create_empty_chart(output_path, "Нет данных по странам")
        
        top_countries = df.groupby('country')['clicks'].sum().nlargest(10)
        top_countries = top_countries[top_countries > 0]
        
        if top_countries.empty:
            return ChartGenerator.create_empty_chart(output_path, "Нет данных по странам")
        
        plt.figure(figsize=(12, 7))
        colors = CHART_COLORS[:len(top_countries)]
        bars = plt.bar(range(len(top_countries)), top_countries.values, color=colors)
        
        plt.title('Топ-10 стран по кликам', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Страна', fontsize=13, labelpad=10)
        plt.ylabel('Клики', fontsize=13, labelpad=10)
        plt.xticks(range(len(top_countries)), top_countries.index, rotation=45, ha='right', fontsize=11)
        plt.yticks(fontsize=11)
        
        max_value = max(top_countries.values)
        for bar, value in zip(bars, top_countries.values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (max_value * 0.01),
                    f'{int(value):,}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.ylim(0, max_value * 1.1)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path
    
    @staticmethod
    def create_ctr_distribution_chart(df, output_path):
        if df.empty:
            return ChartGenerator.create_empty_chart(output_path, "Нет данных для CTR")
        
        plt.figure(figsize=(12, 6))
        
        plt.hist(df['ctr'], bins=30, color=CHART_COLORS[1], alpha=0.7, edgecolor='black', linewidth=1.2)
        
        mean_ctr = df['ctr'].mean()
        median_ctr = df['ctr'].median()
        
        plt.axvline(mean_ctr, color='red', linestyle='--', linewidth=2, label=f'Среднее: {mean_ctr:.1f}%')
        plt.axvline(median_ctr, color='green', linestyle='--', linewidth=2, label=f'Медиана: {median_ctr:.1f}%')
        
        plt.title('Распределение CTR', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('CTR (%)', fontsize=13, labelpad=10)
        plt.ylabel('Частота', fontsize=13, labelpad=10)
        plt.xticks(fontsize=11)
        plt.yticks(fontsize=11)
        plt.legend(fontsize=11, loc='upper right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path
    
    @staticmethod
    def create_position_distribution_chart(df, output_path):
        if df.empty:
            return ChartGenerator.create_empty_chart(output_path, "Нет данных для позиций")
        
        plt.figure(figsize=(12, 6))
        
        bins = list(range(1, 21))
        plt.hist(df['position'], bins=bins, color=CHART_COLORS[2], alpha=0.7, edgecolor='black', linewidth=1.2)
        
        mean_pos = df['position'].mean()
        median_pos = df['position'].median()
        
        plt.axvline(mean_pos, color='red', linestyle='--', linewidth=2, label=f'Среднее: {mean_pos:.1f}')
        plt.axvline(median_pos, color='green', linestyle='--', linewidth=2, label=f'Медиана: {median_pos:.1f}')
        
        plt.title('Распределение позиций в выдаче', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Позиция', fontsize=13, labelpad=10)
        plt.ylabel('Частота', fontsize=13, labelpad=10)
        plt.xticks(range(1, 21), fontsize=11)
        plt.yticks(fontsize=11)
        plt.legend(fontsize=11, loc='upper right')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path