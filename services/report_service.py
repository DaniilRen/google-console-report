import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from config import OUTPUT_DIR, PDF_PAGE_SIZE, PDF_LEFT_MARGIN, PDF_RIGHT_MARGIN, PDF_TOP_MARGIN, PDF_BOTTOM_MARGIN, CURRENT_THEME
from services.sections import (
    TitleSection, MetricsSection, TopQueriesSection,
    TopCountriesSection, DevicesSection, InspectionSection, ChartsSection
)

class ReportService:
    def __init__(self):
        self._register_fonts()
        self.styles = getSampleStyleSheet()
        self.theme = CURRENT_THEME
        self._setup_styles()
        self.page_size = self._get_page_size()
        self.page_width = self.page_size[0]
        self.content_width = self.page_width - PDF_LEFT_MARGIN - PDF_RIGHT_MARGIN
        
        self.title_section = TitleSection(self.styles, self.theme)
        self.metrics_section = MetricsSection(self.styles, self.theme, self._create_full_width_table)
        self.top_queries_section = TopQueriesSection(self.styles, self.theme, self._create_full_width_table)
        self.top_countries_section = TopCountriesSection(self.styles, self.theme, self._create_full_width_table)
        self.devices_section = DevicesSection(self.styles, self.theme, self._create_full_width_table)
        self.inspection_section = InspectionSection(self.styles, self.theme, self._create_full_width_table, self._create_status_badge)
        self.charts_section = ChartsSection(self.styles, self.theme, self.content_width)
    
    def _register_fonts(self):
        regular_font = 'fonts/Roboto-Regular.ttf'
        bold_font = 'fonts/Roboto-Bold.ttf'
        
        if os.path.exists(regular_font):
            pdfmetrics.registerFont(TTFont('Roboto', regular_font))
            pdfmetrics.registerFont(TTFont('Roboto-Bold', bold_font))
            print("Font Roboto loaded successfully")
    
    def _get_font_name(self, bold=False):
        if os.path.exists('fonts/Roboto-Regular.ttf'):
            return 'Roboto-Bold' if bold else 'Roboto'
        return 'Helvetica-Bold' if bold else 'Helvetica'

    def _get_page_size(self):
        return A4 if PDF_PAGE_SIZE.lower() == 'a4' else letter

    def _setup_styles(self):
        self.styles.title_style = ParagraphStyle('CustomTitle', parent=self.styles['Heading1'],
            fontSize=24, textColor=colors.HexColor(self.theme['primary']),
            alignment=TA_CENTER, spaceAfter=30, fontName=self._get_font_name(bold=True))
        
        self.styles.subtitle_style = ParagraphStyle('CustomSubtitle', parent=self.styles['Normal'],
            fontSize=10, textColor=colors.HexColor('#6B7280'), alignment=TA_CENTER,
            spaceAfter=20, fontName=self._get_font_name())
        
        self.styles.section_style = ParagraphStyle('SectionStyle', parent=self.styles['Heading2'],
            fontSize=16, textColor=colors.HexColor(self.theme['primary']),
            spaceAfter=12, fontName=self._get_font_name(bold=True))
        
        self.styles.table_header_style = ParagraphStyle('TableHeader', parent=self.styles['Normal'],
            fontSize=10, textColor=colors.whitesmoke, alignment=TA_CENTER,
            fontName=self._get_font_name(bold=True))
        
        self.styles.table_cell_style = ParagraphStyle('TableCell', parent=self.styles['Normal'],
            fontSize=8, alignment=TA_CENTER, fontName=self._get_font_name())
        
        self.styles.table_cell_left_style = ParagraphStyle('TableCellLeft', parent=self.styles['Normal'],
            fontSize=8, alignment=TA_LEFT, fontName=self._get_font_name())
    
    def _create_status_badge(self, status):
        good_statuses = ['INDEXED', 'SUCCESSFUL', 'ALLOWED', 'INDEXING_ALLOWED', 'PASS']
        is_good = any(good in str(status).upper() for good in good_statuses)
        
        badge_color = '#10B981' if is_good else '#EF4444'
        
        badge_style = ParagraphStyle('Badge', parent=self.styles.table_cell_style,
            textColor=colors.whitesmoke, backColor=colors.HexColor(badge_color),
            fontSize=7, alignment=TA_CENTER)
        
        return Paragraph(str(status).replace('_', ' ').capitalize(), badge_style)
    
    def _create_full_width_table(self, data, col_widths_percent):
        col_widths = [self.content_width * (pct / 100) for pct in col_widths_percent]
        return Table(data, colWidths=col_widths)

    def generate(self, analytics_df, top_queries_df, top_countries_df, devices_df,
                 inspection_df, indexing_summary, charts, start_date, end_date, site_url):
        
        filename = f"{OUTPUT_DIR}/search_console_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=self.page_size,
            rightMargin=PDF_RIGHT_MARGIN, leftMargin=PDF_LEFT_MARGIN,
            topMargin=PDF_TOP_MARGIN, bottomMargin=PDF_BOTTOM_MARGIN)
        
        metrics = {
            'total_clicks': int(analytics_df['clicks'].sum()) if not analytics_df.empty else 0,
            'total_impressions': int(analytics_df['impressions'].sum()) if not analytics_df.empty else 0,
            'avg_ctr': analytics_df['ctr'].mean() if not analytics_df.empty else 0,
            'avg_position': analytics_df['position'].mean() if not analytics_df.empty else 0
        }
        
        story = []
        story.extend(self.title_section.build(start_date, end_date, site_url))
        story.extend(self.metrics_section.build(metrics))
        story.extend(self.top_queries_section.build(top_queries_df))
        story.extend(self.top_countries_section.build(top_countries_df))
        story.extend(self.devices_section.build(devices_df))
        story.extend(self.inspection_section.build(inspection_df, indexing_summary))
        story.extend(self.charts_section.build(charts))
        
        doc.build(story)
        return filename