import matplotlib.pyplot as plt
import seaborn as sns
from config import CHARTS_DIR, CURRENT_THEME

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Roboto', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

sns.set_style("whitegrid")

class ChartService:
    def __init__(self):
        self.theme = CURRENT_THEME
        self.colors = [
            self.theme['primary'],
            self.theme['secondary'],
            self.theme['tertiary'],
            self.theme['quaternary'],
            self.theme['grid'],
        ]
    
    def create_empty_chart(self, output_path, message):
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, message, ha='center', va='center', fontsize=14, 
                transform=plt.gca().transAxes, color='gray')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path
    
    def create_top_queries_chart(self, df, output_path):
        if df.empty:
            return self.create_empty_chart(output_path, "Нет данных по запросам")
        
        plt.figure(figsize=(12, 7))
        top_queries = df.groupby('query')['clicks'].sum().nlargest(10)
        
        colors = self.colors[:len(top_queries)]
        bars = plt.bar(range(len(top_queries)), top_queries.values, color=colors)
        
        plt.title('Топ поисковых запросов', fontsize=16, fontweight='bold', pad=20, color=self.theme['text_dark'])
        plt.xlabel('Поисковый запрос', fontsize=13, labelpad=10, color=self.theme['text_dark'])
        plt.ylabel('Клики', fontsize=13, labelpad=10, color=self.theme['text_dark'])
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
    
    def create_device_chart(self, df, output_path):
        if df.empty or 'device' not in df.columns:
            return self.create_empty_chart(output_path, "Нет данных по устройствам")
        
        device_clicks = df.groupby('device')['clicks'].sum()
        device_clicks = device_clicks[device_clicks > 0]
        
        if device_clicks.empty:
            return self.create_empty_chart(output_path, "Нет данных по устройствам")
        
        device_clicks = device_clicks.sort_values(ascending=True)
        
        plt.figure(figsize=(10, 6))
        colors = self.colors[:len(device_clicks)]
        bars = plt.barh(range(len(device_clicks)), device_clicks.values, color=colors)
        
        plt.title('Клики по устройствам', fontsize=16, fontweight='bold', pad=20, color=self.theme['text_dark'])
        plt.xlabel('Клики', fontsize=13, labelpad=10, color=self.theme['text_dark'])
        plt.ylabel('Устройство', fontsize=13, labelpad=10, color=self.theme['text_dark'])
        plt.yticks(range(len(device_clicks)), device_clicks.index, fontsize=12)
        plt.xticks(fontsize=11)
        
        max_value = max(device_clicks.values)
        for bar, value in zip(bars, device_clicks.values):
            plt.text(bar.get_width() + (max_value * 0.02), bar.get_y() + bar.get_height()/2,
                    f'{int(value):,}', ha='left', va='center', fontsize=11, fontweight='bold')
        
        plt.xlim(0, max_value * 1.15)
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path
    
    def create_top_countries_chart(self, df, output_path):
        if df.empty or 'country' not in df.columns:
            return self.create_empty_chart(output_path, "Нет данных по странам")
        
        top_countries = df.groupby('country')['clicks'].sum().nlargest(10)
        top_countries = top_countries[top_countries > 0]
        
        if top_countries.empty:
            return self.create_empty_chart(output_path, "Нет данных по странам")
        
        plt.figure(figsize=(12, 7))
        colors = self.colors[:len(top_countries)]
        bars = plt.bar(range(len(top_countries)), top_countries.values, color=colors)
        
        plt.title('Топ стран по кликам', fontsize=16, fontweight='bold', pad=20, color=self.theme['text_dark'])
        plt.xlabel('Страна', fontsize=13, labelpad=10, color=self.theme['text_dark'])
        plt.ylabel('Клики', fontsize=13, labelpad=10, color=self.theme['text_dark'])
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
    
    def create_ctr_chart(self, df, output_path):
        if df.empty:
            return self.create_empty_chart(output_path, "Нет данных для CTR")
        
        plt.figure(figsize=(12, 6))
        plt.hist(df['ctr'], bins=30, color=self.colors[1], alpha=0.7, edgecolor='black', linewidth=1.2)
        
        mean_ctr = df['ctr'].mean()
        median_ctr = df['ctr'].median()
        
        plt.axvline(mean_ctr, color='red', linestyle='--', linewidth=2, label=f'Среднее: {mean_ctr:.1f}%')
        plt.axvline(median_ctr, color='green', linestyle='--', linewidth=2, label=f'Медиана: {median_ctr:.1f}%')
        
        plt.title('Распределение CTR', fontsize=16, fontweight='bold', pad=20, color=self.theme['text_dark'])
        plt.xlabel('CTR (%)', fontsize=13, labelpad=10, color=self.theme['text_dark'])
        plt.ylabel('Частота', fontsize=13, labelpad=10, color=self.theme['text_dark'])
        plt.xticks(fontsize=11)
        plt.yticks(fontsize=11)
        plt.legend(fontsize=11, loc='upper right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path
    
    def create_position_chart(self, df, output_path):
        if df.empty:
            return self.create_empty_chart(output_path, "Нет данных для позиций")
        
        plt.figure(figsize=(12, 6))
        bins = list(range(1, 21))
        plt.hist(df['position'], bins=bins, color=self.colors[2], alpha=0.7, edgecolor='black', linewidth=1.2)
        
        mean_pos = df['position'].mean()
        median_pos = df['position'].median()
        
        plt.axvline(mean_pos, color='red', linestyle='--', linewidth=2, label=f'Среднее: {mean_pos:.1f}')
        plt.axvline(median_pos, color='green', linestyle='--', linewidth=2, label=f'Медиана: {median_pos:.1f}')
        
        plt.title('Распределение позиций в выдаче', fontsize=16, fontweight='bold', pad=20, color=self.theme['text_dark'])
        plt.xlabel('Позиция', fontsize=13, labelpad=10, color=self.theme['text_dark'])
        plt.ylabel('Частота', fontsize=13, labelpad=10, color=self.theme['text_dark'])
        plt.xticks(range(1, 21), fontsize=11)
        plt.yticks(fontsize=11)
        plt.legend(fontsize=11, loc='upper right')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path
    
    def generate_all_charts(self, df):
        charts = []
        
        chart1 = f"{CHARTS_DIR}/top_queries.png"
        self.create_top_queries_chart(df, chart1)
        charts.append(chart1)
        
        chart2 = f"{CHARTS_DIR}/device_distribution.png"
        self.create_device_chart(df, chart2)
        charts.append(chart2)
        
        chart3 = f"{CHARTS_DIR}/top_countries.png"
        self.create_top_countries_chart(df, chart3)
        charts.append(chart3)
        
        chart4 = f"{CHARTS_DIR}/ctr_distribution.png"
        self.create_ctr_chart(df, chart4)
        charts.append(chart4)
        
        chart5 = f"{CHARTS_DIR}/position_distribution.png"
        self.create_position_chart(df, chart5)
        charts.append(chart5)
        
        return charts
    
    def generate_empty_charts(self, start_date, end_date):
        charts = []
        for name in ['top_queries', 'device_distribution', 'top_countries', 'ctr_distribution', 'position_distribution']:
            path = f"{CHARTS_DIR}/{name}_empty.png"
            self.create_empty_chart(path, f"Нет данных за период {start_date} - {end_date}")
            charts.append(path)
        return charts