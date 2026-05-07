import pandas as pd

class InspectionFetcher:
    def __init__(self, service, site_url):
        self.service = service
        self.site_url = site_url
    
    def fetch(self, urls_to_inspect):
        results = []
        for url_path in urls_to_inspect[:10]:
            try:
                full_url = self.site_url.rstrip('/') + url_path
                body = {
                    'inspectionUrl': full_url,
                    'siteUrl': self.site_url
                }
                
                response = self.service.urlInspection().index().inspect(body=body).execute()
                result = response.get('inspectionResult', {})
                index_status = result.get('indexStatusResult', {})
                
                results.append({
                    'url': url_path,
                    'verdict': index_status.get('verdict', 'UNKNOWN'),
                    'coverage_state': index_status.get('coverageState', 'UNKNOWN'),
                    'indexing_state': index_status.get('indexingState', 'UNKNOWN'),
                    'robots_txt_state': index_status.get('robotsTxtState', 'UNKNOWN'),
                    'page_fetch_state': index_status.get('pageFetchState', 'UNKNOWN'),
                    'google_canonical': index_status.get('googleCanonical', ''),
                    'user_canonical': index_status.get('userCanonical', ''),
                    'last_crawl_time': index_status.get('lastCrawlTime', ''),
                    'crawled_as': index_status.get('crawledAs', '')
                })
            except Exception as e:
                print(f"Warning: Could not inspect URL {url_path}: {e}")
                results.append({
                    'url': url_path,
                    'verdict': 'ERROR',
                    'coverage_state': 'Inspection failed',
                    'indexing_state': 'UNKNOWN',
                    'robots_txt_state': 'UNKNOWN',
                    'page_fetch_state': 'UNKNOWN',
                    'google_canonical': '',
                    'user_canonical': '',
                    'last_crawl_time': '',
                    'crawled_as': ''
                })
        
        return pd.DataFrame(results)
    
    def get_summary(self, df):
        if df.empty:
            return {
                'urls_checked': 0,
                'urls_indexed': 0,
                'urls_not_indexed': 0,
                'urls_blocked_by_robots': 0,
                'urls_with_fetch_errors': 0
            }
        
        indexed = sum(1 for _, row in df.iterrows() if 'INDEXED' in str(row['coverage_state']))
        not_indexed = sum(1 for _, row in df.iterrows() if 'NOT_INDEXED' in str(row['coverage_state']))
        blocked = sum(1 for _, row in df.iterrows() if 'BLOCKED' in str(row['robots_txt_state']))
        
        fetch_errors = 0
        for _, row in df.iterrows():
            if 'SUCCESSFUL' not in str(row['page_fetch_state']) and 'UNKNOWN' not in str(row['page_fetch_state']):
                fetch_errors += 1
        
        return {
            'urls_checked': len(df),
            'urls_indexed': int(indexed),
            'urls_not_indexed': int(not_indexed),
            'urls_blocked_by_robots': int(blocked),
            'urls_with_fetch_errors': int(fetch_errors)
        }