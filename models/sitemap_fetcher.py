import pandas as pd

class SitemapFetcher:
    def __init__(self, service, site_url):
        self.service = service
        self.site_url = site_url
    
    def fetch(self):
        try:
            request = self.service.sitemaps().list(siteUrl=self.site_url)
            response = request.execute()
            return response.get('sitemap', [])
        except Exception as e:
            print(f"Warning: Could not fetch sitemaps: {e}")
            return []
    
    def process(self, sitemaps):
        if not sitemaps:
            return pd.DataFrame()
        
        data = []
        for sitemap in sitemaps:
            contents = sitemap.get('contents', [])
            submitted = 0
            indexed = 0
            
            if contents and len(contents) > 0:
                submitted_val = contents[0].get('submitted', 0)
                indexed_val = contents[0].get('indexed', 0)
                
                if isinstance(submitted_val, (int, float)):
                    submitted = int(submitted_val)
                if isinstance(indexed_val, (int, float)):
                    indexed = int(indexed_val)
            
            warnings_val = sitemap.get('warnings', 0)
            if not isinstance(warnings_val, (int, float)):
                warnings_val = 0
            
            data.append({
                'path': sitemap.get('path', ''),
                'type': sitemap.get('type', ''),
                'last_submitted': sitemap.get('lastSubmitted', ''),
                'last_downloaded': sitemap.get('lastDownloaded', ''),
                'is_pending': sitemap.get('isPending', False),
                'is_sitemaps_index': sitemap.get('isSitemapsIndex', False),
                'warnings': int(warnings_val),
                'contents_submitted': submitted,
                'contents_indexed': indexed
            })
        
        return pd.DataFrame(data)
    
    def get_summary(self, df):
        if df.empty:
            return {
                'total_sitemaps': 0,
                'total_submitted_urls': 0,
                'total_indexed_urls': 0,
                'sitemaps_with_warnings': 0,
                'avg_index_rate': 0
            }
        
        total_submitted = int(df['contents_submitted'].sum())
        total_indexed = int(df['contents_indexed'].sum())
        
        return {
            'total_sitemaps': len(df),
            'total_submitted_urls': total_submitted,
            'total_indexed_urls': total_indexed,
            'sitemaps_with_warnings': int((df['warnings'] > 0).sum()),
            'avg_index_rate': (total_indexed / total_submitted * 100) if total_submitted > 0 else 0
        }