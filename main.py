import sys
from datetime import datetime
from dotenv import load_dotenv
from auth import GoogleAuth
from data_fetcher import SearchConsoleDataFetcher
from visualizer import ChartGenerator
from report_generator import PDFReportGenerator
from config import CHARTS_DIR, get_date_range, SITE_URL
import pandas as pd

load_dotenv()

def main():
    print("=" * 60)
    print("Генератор отчётов Google Search Console")
    print("=" * 60)
    
    site_url = SITE_URL
    if not site_url:
        site_url = input("Введите URL вашего сайта (например, https://example.com/): ").strip()
    
    if not site_url:
        print("Ошибка: URL сайта не может быть пустым")
        return
    
    start_date, end_date = get_date_range()
    
    print(f"\nЗагрузка данных за период {start_date} - {end_date}...")
    
    try:
        service = GoogleAuth.authenticate()
        
        fetcher = SearchConsoleDataFetcher(site_url)
        fetcher.set_service(service)
        
        rows = fetcher.fetch_analytics(
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d'),
            dimensions=['query', 'page', 'device', 'country']
        )
        
        if not rows:
            print("Данные за выбранный период не найдены. Генерация отчёта с нулевыми показателями...")
            df = pd.DataFrame(columns=['query', 'page', 'device', 'country', 'clicks', 'impressions', 'ctr', 'position'])
            metrics = {
                'total_clicks': 0,
                'total_impressions': 0,
                'avg_ctr': 0,
                'avg_position': 0
            }
            top_queries = pd.DataFrame(columns=['query', 'clicks', 'impressions', 'ctr', 'position'])
            top_countries = pd.DataFrame(columns=['country', 'clicks', 'impressions', 'ctr', 'position'])
            devices = pd.DataFrame(columns=['device', 'clicks', 'impressions', 'ctr', 'position'])
        else:
            df = fetcher.process_data(rows)
            metrics = fetcher.get_summary_metrics(df)
            top_queries = fetcher.get_top_queries(df, 10)
            top_countries = fetcher.get_top_countries(df, 10)
            devices = fetcher.get_device_breakdown(df)
        
        print(f"Обработано записей: {len(df)}")
        print(f"Всего кликов: {metrics['total_clicks']:,}")
        print(f"Всего показов: {metrics['total_impressions']:,}")
        print(f"Стран: {len(top_countries)}")
        print(f"Устройств: {len(devices)}")
        
        print("\nГенерация графиков...")
        
        charts = []
        
        chart1 = f"{CHARTS_DIR}/top_queries.png"
        ChartGenerator.create_top_queries_chart(df, chart1)
        charts.append(chart1)
        
        chart2 = f"{CHARTS_DIR}/device_distribution.png"
        ChartGenerator.create_clicks_by_device_bar_chart(df, chart2)
        charts.append(chart2)
        
        chart3 = f"{CHARTS_DIR}/top_countries.png"
        ChartGenerator.create_top_countries_chart(df, chart3)
        charts.append(chart3)
        
        chart4 = f"{CHARTS_DIR}/ctr_distribution.png"
        ChartGenerator.create_ctr_distribution_chart(df, chart4)
        charts.append(chart4)
        
        chart5 = f"{CHARTS_DIR}/position_distribution.png"
        ChartGenerator.create_position_distribution_chart(df, chart5)
        charts.append(chart5)
        
        print("Формирование PDF отчёта...")
        
        generator = PDFReportGenerator()
        output_file = generator.generate(
            metrics, top_queries, top_countries, devices, charts,
            start_date.strftime('%d.%m.%Y'),
            end_date.strftime('%d.%m.%Y'),
            site_url
        )
        
        print(f"\nОтчёт успешно сохранён: {output_file}")
        
    except FileNotFoundError as e:
        print(f"\nОшибка: {e}")
        print("\nУбедитесь, что файл client_secrets.json находится в папке проекта")
    except Exception as e:
        print(f"\nОшибка: {e}")
        print("\nВозможные решения:")
        print("1. Проверьте настройки в файле .env")
        print("2. Убедитесь, что URL сайта подтверждён в Google Search Console")
        print("3. Проверьте, что API Google Search Console включён в Google Cloud Console")

if __name__ == "__main__":
    main()