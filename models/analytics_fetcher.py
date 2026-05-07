import pandas as pd

class AnalyticsFetcher:
    def __init__(self, service, site_url):
        self.service = service
        self.site_url = site_url
    
    def fetch(self, start_date, end_date, dimensions=['query', 'page', 'device', 'country']):
        request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions,
            'rowLimit': 25000
        }
        
        response = self.service.searchanalytics().query(
            siteUrl=self.site_url, 
            body=request
        ).execute()
        
        return response.get('rows', [])
    
    def process(self, rows):
        if not rows:
            return pd.DataFrame()
        
        data = []
        for row in rows:
            row_data = {
                'clicks': row['clicks'],
                'impressions': row['impressions'],
                'ctr': row['ctr'] * 100,
                'position': row['position']
            }
            
            for i, key in enumerate(row['keys']):
                if i == 0:
                    row_data['query'] = key
                elif i == 1:
                    row_data['page'] = key
                elif i == 2:
                    row_data['device'] = key
                elif i == 3:
                    row_data['country'] = key
            
            data.append(row_data)
        
        return pd.DataFrame(data)
    
    def get_summary(self, df):
        return {
            'total_clicks': int(df['clicks'].sum()) if not df.empty else 0,
            'total_impressions': int(df['impressions'].sum()) if not df.empty else 0,
            'avg_ctr': df['ctr'].mean() if not df.empty else 0,
            'avg_position': df['position'].mean() if not df.empty else 0
        }
    
    def get_top_queries(self, df, limit=10):
        if df.empty:
            return pd.DataFrame()
        
        return df.groupby('query').agg({
            'clicks': 'sum',
            'impressions': 'sum',
            'ctr': 'mean',
            'position': 'mean'
        }).nlargest(limit, 'clicks').reset_index()
    
    def get_top_countries(self, df, limit=10):
        if df.empty or 'country' not in df.columns:
            return pd.DataFrame()
        
        return df.groupby('country').agg({
            'clicks': 'sum',
            'impressions': 'sum',
            'ctr': 'mean',
            'position': 'mean'
        }).nlargest(limit, 'clicks').reset_index()
    
    def get_device_breakdown(self, df):
        if df.empty or 'device' not in df.columns:
            return pd.DataFrame()
        
        return df.groupby('device').agg({
            'clicks': 'sum',
            'impressions': 'sum',
            'ctr': 'mean',
            'position': 'mean'
        }).reset_index()