# google-console-report

Automatic PDF report generator based on Google Search Console data with professional visualizations.

## Features

- Automatic data collection from Google Search Console API
- Data visualization with charts and diagrams
- Professional PDF report generation
- Support for multiple metrics:
- Top 10 search queries
- Top 10 countries by clicks
- Device breakdown (desktop, mobile, tablet)
- CTR and position distribution
- Secure credential storage via .env file
- Handles zero data scenarios gracefully

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

3. Copy .env.example to .env and configure parameters:
```env
GOOGLE_CLIENT_SECRETS_FILE=client_secrets.json
GOOGLE_TOKEN_FILE=token.json
SITE_URL=https://your-website.com/
REPORT_DAYS_BACK=28
REPORT_TITLE=Search Console Report
COMPANY_NAME=Your Company Name
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