import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SCOPES = [os.getenv('GOOGLE_SCOPES', 'https://www.googleapis.com/auth/webmasters.readonly')]
CREDENTIALS_FILE = os.getenv('GOOGLE_CLIENT_SECRETS_FILE', 'client_secrets.json')
TOKEN_FILE = os.getenv('GOOGLE_TOKEN_FILE', 'token.json')

DEFAULT_DAYS_BACK = int(os.getenv('REPORT_DAYS_BACK', '28'))
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
THEME = os.getenv('THEME', 'GRAY').upper()

SECTION_METRICS = os.getenv('SECTION_METRICS', 'true').lower() == 'true'
SECTION_TOP_QUERIES = os.getenv('SECTION_TOP_QUERIES', 'true').lower() == 'true'
SECTION_TOP_COUNTRIES = os.getenv('SECTION_TOP_COUNTRIES', 'true').lower() == 'true'
SECTION_DEVICES = os.getenv('SECTION_DEVICES', 'true').lower() == 'true'
SECTION_INSPECTION = os.getenv('SECTION_INSPECTION', 'true').lower() == 'true'
SECTION_CHARTS = os.getenv('SECTION_CHARTS', 'true').lower() == 'true'

raw_urls = os.getenv('URLS_TO_INSPECT', '')
if raw_urls.strip():
    URLS_TO_INSPECT = ['/'] + [url.strip() for url in raw_urls.split(',') if url.strip()]
else:
    URLS_TO_INSPECT = ['/']

URLS_TO_INSPECT = list(dict.fromkeys(URLS_TO_INSPECT))

THEMES = {
    'GRAY': {
        'primary': '#374151',
        'secondary': '#4B5563',
        'tertiary': '#6B7280',
        'quaternary': '#9CA3AF',
        'light_bg': '#F3F4F6',
        'grid': '#D1D5DB',
        'text_dark': '#1F2937',
        'text_light': '#FFFFFF',
    },
    'BLUE': {
        'primary': '#1E3A8A',
        'secondary': '#2563EB',
        'tertiary': '#3B82F6',
        'quaternary': '#60A5FA',
        'light_bg': '#EFF6FF',
        'grid': '#93C5FD',
        'text_dark': '#1E3A8A',
        'text_light': '#FFFFFF',
    },
    'RED': {
        'primary': '#7F1D1D',
        'secondary': '#DC2626',
        'tertiary': '#EF4444',
        'quaternary': '#F87171',
        'light_bg': '#FEF2F2',
        'grid': '#FCA5A5',
        'text_dark': '#7F1D1D',
        'text_light': '#FFFFFF',
    },
    'GREEN': {
        'primary': '#14532D',
        'secondary': '#16A34A',
        'tertiary': '#22C55E',
        'quaternary': '#4ADE80',
        'light_bg': '#F0FDF4',
        'grid': '#86EFAC',
        'text_dark': '#14532D',
        'text_light': '#FFFFFF',
    },
    'PURPLE': {
        'primary': '#4C1D95',
        'secondary': '#7C3AED',
        'tertiary': '#8B5CF6',
        'quaternary': '#A78BFA',
        'light_bg': '#F5F3FF',
        'grid': '#C4B5FD',
        'text_dark': '#4C1D95',
        'text_light': '#FFFFFF',
    },
}

CURRENT_THEME = THEMES.get(THEME, THEMES['GRAY'])

CHART_COLORS = [
    CURRENT_THEME['primary'],
    CURRENT_THEME['secondary'],
    CURRENT_THEME['tertiary'],
    CURRENT_THEME['quaternary'],
    CURRENT_THEME['grid'],
]

def get_date_range(days_back=DEFAULT_DAYS_BACK):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_back)
    return start_date, end_date

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
if not os.path.exists(CHARTS_DIR):
    os.makedirs(CHARTS_DIR)