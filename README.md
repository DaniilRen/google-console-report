# google-console-report

Automatic PDF report generator based on Google Search Console data with professional visualizations.

## Features

- Automatic data collection from Google Search Console API
- Data visualization with charts and diagrams
- PDF report generation
- Support for multiple metrics:
	- Top search queries
	- Top countries by clicks
	- Device breakdown (desktop, mobile, tablet)
	- CTR and position distribution
- Secure credential storage via .env file

## Requirements

- Python 3.8 or higher
- Google account with access to Google Search Console
- Website verified in Google Search Console

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/search-console-reporter.git
cd search-console-reporter
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # For Linux/Mac
.venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Google Cloud Console Setup
* Go to Google Cloud Console

* Create a new project or select existing one

* Enable Google Search Console API

* Go to APIs & Services > OAuth consent screen

* Choose External and fill the form:

* App name: Search Console Reporter

* User support email: your email

* Developer contact: your email

* Add scope: .../auth/webmasters.readonly

* Add your email to Test users

* Go to Credentials and create OAuth Client ID of type Desktop app

* Download the client_secrets.json file

### 5. Project Configuration
1. Place client_secrets.json in the project root folder.
2. Create fonts folder and add fonts (if not installed by default):

* Roboto-Regular.ttf

* Roboto-Bold.ttf

3. Copy env_example to .env and configure parameters:
```env
# Website Configuration
SITE_URL=https://domen.com/ - your website working URL
URLS_TO_INSPECT=/home,/about,/contacts - pages on website which will be inspected (only for INSPECTION report section)

# Report Configuration
REPORT_DAYS_BACK=30 - days from current date that will be analyzed
REPORT_TITLE=New report - title of report
COMPANY_NAME=Best Company - title of company in report
REPORT_OUTPUT_DIR=reports - dir for generated reports
CHARTS_OUTPUT_DIR=charts - dir for generated charts

# report sectiona to include. 'true' - section included in report, 'false' - not included
SECTION_METRICS=true
SECTION_TOP_QUERIES=true
SECTION_TOP_COUNTRIES=true
SECTION_DEVICES=true
SECTION_INSPECTION=true
SECTION_CHARTS=true

# Theme settings (GRAY, BLUE, RED, GREEN, PURPLE)
THEME=GRAY

# PDF Settings. Report page style
PDF_PAGE_SIZE=letter
PDF_LEFT_MARGIN=72
PDF_RIGHT_MARGIN=72
PDF_TOP_MARGIN=72
PDF_BOTTOM_MARGIN=72
```

## Usage
Run Application:
```bash
python main.py
```

## Report Structure
PDF report includes:
*  Title page with period and site information

* KPI dashboard: total clicks, impressions, average CTR, position

* Top search queries with metrics

* Top countries with click breakdown

* Device distribution

* Visualizations:

	* CTR distribution histogram

	* Position distribution histogram

	* Top countries chart

	* Top queries chart

	* Device click distribution

## Font Configuration
For proper Cyrillic support in PDF and charts:
### PDF (ReportLab)
```python
# Place fonts in fonts/ folder
regular_font = 'fonts/Roboto-Regular.ttf'
bold_font = 'fonts/Roboto-Bold.ttf'
```
### Charts (Matplotlib)
```python
# Configured in visualizer.py
plt.rcParams['font.sans-serif'] = ['Roboto', 'Arial', 'DejaVu Sans']
```

## Troubleshooting
### Error 403: access_denied
Solution: Add your email to test users in Google Cloud Console:
1. Go to APIs & Services > OAuth consent screen

2. Click Test users > Add Users

3. Enter your email address

### Squares Instead of Cyrillic Text
Solution:
1. Ensure fonts with Cyrillic support are in fonts/ folder

2. Check font file permissions

3. Use recommended fonts: Roboto, Arial, Noto Sans