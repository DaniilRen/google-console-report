import sys
from datetime import datetime
from dotenv import load_dotenv
from auth import GoogleAuth
from models.data_fetcher import DataFetcher
from services.chart_service import ChartService
from services.report_service import ReportService
from config import CHARTS_DIR, get_date_range, SITE_URL, URLS_TO_INSPECT
import pandas as pd

load_dotenv()

def main():
    print("=" * 60)
    print("Google Search Console Report Generator")
    print("=" * 60)
    
    site_url = SITE_URL
    if not site_url:
        site_url = input("Enter your website URL (e.g., https://example.com/): ").strip()
    
    if not site_url:
        print("Error: Website URL cannot be empty")
        return
    
    print(f"\nURLs to inspect: {', '.join(URLS_TO_INSPECT)}")
    
    start_date, end_date = get_date_range()
    print(f"\nLoading data for period {start_date} to {end_date}...")
    
    try:
        service = GoogleAuth.authenticate()
        fetcher = DataFetcher(service, site_url)
        
        rows = fetcher.analytics.fetch(
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d'),
            dimensions=['query', 'page', 'device', 'country']
        )
        
        if not rows:
            print("No data found for selected period. Generating report with zero values...")
            analytics_df = pd.DataFrame(columns=['query', 'page', 'device', 'country', 'clicks', 'impressions', 'ctr', 'position'])
        else:
            analytics_df = fetcher.analytics.process(rows)
        
        metrics_summary = fetcher.analytics.get_summary(analytics_df)
        top_queries = fetcher.analytics.get_top_queries(analytics_df, 10)
        top_countries = fetcher.analytics.get_top_countries(analytics_df, 10)
        devices = fetcher.analytics.get_device_breakdown(analytics_df)
        
        print(f"Records processed: {len(analytics_df)}")
        print(f"Total clicks: {metrics_summary['total_clicks']:,}")
        print(f"Total impressions: {metrics_summary['total_impressions']:,}")
        
        print("\nFetching URL inspection data...")
        inspection_df = fetcher.inspection.fetch(URLS_TO_INSPECT)
        indexing_summary = fetcher.inspection.get_summary(inspection_df)
        
        if indexing_summary['urls_checked'] > 0:
            print(f"URLs inspected: {indexing_summary['urls_checked']}")
            print(f"Indexed: {indexing_summary['urls_indexed']}")
        else:
            print("No URL inspection data available")
        
        print("\nGenerating charts...")
        chart_service = ChartService()
        
        if not analytics_df.empty:
            charts = chart_service.generate_all_charts(analytics_df)
        else:
            charts = chart_service.generate_empty_charts(start_date.strftime('%d.%m.%Y'), end_date.strftime('%d.%m.%Y'))
        
        print("Generating PDF report...")
        report_service = ReportService()
        output_file = report_service.generate(
            analytics_df, top_queries, top_countries, devices,
            inspection_df, indexing_summary, charts,
            start_date.strftime('%d.%m.%Y'), end_date.strftime('%d.%m.%Y'), site_url
        )
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nMake sure client_secrets.json is in the project folder")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nPossible solutions:")
        print("1. Check your .env configuration")
        print("2. Verify the site URL is verified in Google Search Console")
        print("3. Ensure Google Search Console API is enabled")

if __name__ == "__main__":
    main()