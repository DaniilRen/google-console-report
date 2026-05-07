from .analytics_fetcher import AnalyticsFetcher
from .sitemap_fetcher import SitemapFetcher
from .inspection_fetcher import InspectionFetcher

class DataFetcher:
    def __init__(self, service, site_url):
        self.service = service
        self.site_url = site_url
        self.analytics = AnalyticsFetcher(service, site_url)
        self.sitemaps = SitemapFetcher(service, site_url)
        self.inspection = InspectionFetcher(service, site_url)