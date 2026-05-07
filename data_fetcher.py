import pandas as pd

class SearchConsoleDataFetcher:
	def __init__(self, site_url):
			self.site_url = site_url
			self.service = None
	
	def set_service(self, service):
			self.service = service
	
	def fetch_analytics(self, start_date, end_date, dimensions=['query', 'page', 'device', 'country']):
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
	
	def process_data(self, rows):
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
			
			df = pd.DataFrame(data)
			return df
	
	def get_summary_metrics(self, df):
			return {
					'total_clicks': int(df['clicks'].sum()),
					'total_impressions': int(df['impressions'].sum()),
					'avg_ctr': df['ctr'].mean(),
					'avg_position': df['position'].mean()
			}
	
	def get_top_queries(self, df, limit=10):
			top = df.groupby('query').agg({
					'clicks': 'sum',
					'impressions': 'sum',
					'ctr': 'mean',
					'position': 'mean'
			}).nlargest(limit, 'clicks').reset_index()
			return top
	
	def get_top_countries(self, df, limit=10):
			if 'country' not in df.columns:
					return pd.DataFrame()
			
			top = df.groupby('country').agg({
					'clicks': 'sum',
					'impressions': 'sum',
					'ctr': 'mean',
					'position': 'mean'
			}).nlargest(limit, 'clicks').reset_index()
			return top
	
	def get_top_pages(self, df, limit=10):
			if 'page' not in df.columns:
					return pd.DataFrame()
			
			top = df.groupby('page').agg({
					'clicks': 'sum',
					'impressions': 'sum',
					'ctr': 'mean',
					'position': 'mean'
			}).nlargest(limit, 'clicks').reset_index()
			return top
	
	def get_device_breakdown(self, df):
			if 'device' not in df.columns:
					return pd.DataFrame()
			
			devices = df.groupby('device').agg({
					'clicks': 'sum',
					'impressions': 'sum',
					'ctr': 'mean',
					'position': 'mean'
			}).reset_index()
			return devices