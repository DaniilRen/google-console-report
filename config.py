import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SCOPES = [os.getenv('GOOGLE_SCOPES', 'https://www.googleapis.com/auth/webmasters.readonly')]
CREDENTIALS_FILE = os.getenv('GOOGLE_CLIENT_SECRETS_FILE', 'client_secrets.json')
TOKEN_FILE = os.getenv('GOOGLE_TOKEN_FILE', 'token.json')

DEFAULT_DAYS_BACK = int(os.getenv('REPORT_DAYS_BACK', '28'))
CHART_COLORS = os.getenv('CHART_COLORS', '#3498DB,#2ECC71,#E74C3C,#F39C12,#9B59B6').split(',')
OUTPUT_DIR = os.getenv('REPORT_OUTPUT_DIR', 'reports')
CHARTS_DIR = os.getenv('CHARTS_OUTPUT_DIR', 'charts')

REPORT_TITLE = os.getenv('REPORT_TITLE', 'Отчёт Google Search Console')
COMPANY_NAME = os.getenv('COMPANY_NAME', 'Ваша Компания')

PDF_PAGE_SIZE = os.getenv('PDF_PAGE_SIZE', 'letter')
PDF_LEFT_MARGIN = int(os.getenv('PDF_LEFT_MARGIN', '72'))
PDF_RIGHT_MARGIN = int(os.getenv('PDF_RIGHT_MARGIN', '72'))
PDF_TOP_MARGIN = int(os.getenv('PDF_TOP_MARGIN', '72'))
PDF_BOTTOM_MARGIN = int(os.getenv('PDF_BOTTOM_MARGIN', '72'))

SITE_URL = os.getenv('SITE_URL', '')

def get_date_range(days_back=DEFAULT_DAYS_BACK):
	end_date = datetime.now().date()
	start_date = end_date - timedelta(days=days_back)
	return start_date, end_date

if not os.path.exists(OUTPUT_DIR):
	os.makedirs(OUTPUT_DIR)
if not os.path.exists(CHARTS_DIR):
	os.makedirs(CHARTS_DIR)