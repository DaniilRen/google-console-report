from reportlab.platypus import Paragraph, Spacer
from reportlab.lib import colors
from config import REPORT_TITLE, COMPANY_NAME
from datetime import datetime

class TitleSection:
    def __init__(self, styles, theme):
        self.styles = styles
        self.theme = theme
    
    def build(self, start_date, end_date, site_url):
        story = []
        
        title = Paragraph(REPORT_TITLE, self.styles.title_style)
        story.append(title)
        
        subtitle_text = f"Период отчёта: {start_date} - {end_date}<br/>"
        subtitle_text += f"Дата генерации: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}<br/>"
        subtitle_text += f"Сайт: {site_url}<br/>"
        subtitle_text += f"Компания: {COMPANY_NAME}"
        
        subtitle = Paragraph(subtitle_text, self.styles.subtitle_style)
        story.append(subtitle)
        story.append(Spacer(1, 20))
        
        return story