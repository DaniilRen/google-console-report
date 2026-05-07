import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from config import OUTPUT_DIR, REPORT_TITLE, COMPANY_NAME, PDF_PAGE_SIZE, PDF_LEFT_MARGIN, PDF_RIGHT_MARGIN, PDF_TOP_MARGIN, PDF_BOTTOM_MARGIN

class PDFReportGenerator:
    def __init__(self):
        self._register_fonts()
        self.styles = getSampleStyleSheet()
        self._setup_styles()
        self.page_size = self._get_page_size()
    
    def _register_fonts(self):
        regular_font = 'fonts/Roboto-Regular.ttf'
        bold_font = 'fonts/Roboto-Bold.ttf'
        
        if os.path.exists(regular_font):
            pdfmetrics.registerFont(TTFont('Roboto', regular_font))
            pdfmetrics.registerFont(TTFont('Roboto-Bold', bold_font))
            print("Шрифт Roboto успешно загружен")
        else:
            print(f"Предупреждение: Файл шрифта не найден: {regular_font}")
    
    def _get_font_name(self, bold=False):
        if os.path.exists('fonts/Roboto-Regular.ttf'):
            return 'Roboto-Bold' if bold else 'Roboto'
        return 'Helvetica-Bold' if bold else 'Helvetica'

    def _get_page_size(self):
        if PDF_PAGE_SIZE.lower() == 'a4':
            return A4
        return letter

    def _setup_styles(self):
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            alignment=TA_CENTER,
            spaceAfter=30,
            fontName=self._get_font_name(bold=True)
        )
        
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7F8C8D'),
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName=self._get_font_name()
        )
        
        self.section_style = ParagraphStyle(
            'SectionStyle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12,
            fontName=self._get_font_name(bold=True)
        )
        
        self.table_header_style = ParagraphStyle(
            'TableHeader',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.whitesmoke,
            alignment=TA_CENTER,
            fontName=self._get_font_name(bold=True)
        )
        
        self.table_cell_style = ParagraphStyle(
            'TableCell',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            fontName=self._get_font_name()
        )

    def generate(self, metrics, top_queries_df, top_countries_df, devices_df, charts, start_date, end_date, site_url):
        filename = f"{OUTPUT_DIR}/search_console_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        doc = SimpleDocTemplate(
            filename, 
            pagesize=self.page_size,
            rightMargin=PDF_RIGHT_MARGIN, 
            leftMargin=PDF_LEFT_MARGIN,
            topMargin=PDF_TOP_MARGIN, 
            bottomMargin=PDF_BOTTOM_MARGIN
        )
        
        story = []
        
        title = Paragraph(REPORT_TITLE, self.title_style)
        story.append(title)
        
        subtitle_text = f"Период отчёта: {start_date} - {end_date}<br/>"
        subtitle_text += f"Дата генерации: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}<br/>"
        subtitle_text += f"Сайт: {site_url}<br/>"
        subtitle_text += f"Компания: {COMPANY_NAME}"
        
        subtitle = Paragraph(subtitle_text, self.subtitle_style)
        story.append(subtitle)
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Ключевые показатели эффективности", self.section_style))
        story.append(Spacer(1, 10))
        
        metrics_data = [
            [Paragraph('Показатель', self.table_header_style), Paragraph('Значение', self.table_header_style)],
            [Paragraph('Всего кликов', self.table_cell_style), Paragraph(f"{metrics['total_clicks']:,.0f}", self.table_cell_style)],
            [Paragraph('Всего показов', self.table_cell_style), Paragraph(f"{metrics['total_impressions']:,.0f}", self.table_cell_style)],
            [Paragraph('Средний CTR', self.table_cell_style), Paragraph(f"{metrics['avg_ctr']:.2f}%", self.table_cell_style)],
            [Paragraph('Средняя позиция', self.table_cell_style), Paragraph(f"{metrics['avg_position']:.1f}", self.table_cell_style)]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[200, 150])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        story.append(metrics_table)
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Топ-10 поисковых запросов", self.section_style))
        story.append(Spacer(1, 10))
        
        table_data = [
            [Paragraph('Запрос', self.table_header_style), 
             Paragraph('Клики', self.table_header_style), 
             Paragraph('Показы', self.table_header_style), 
             Paragraph('CTR (%)', self.table_header_style), 
             Paragraph('Позиция', self.table_header_style)]
        ]
        
        for _, row in top_queries_df.head(10).iterrows():
            query_text = row['query'][:40] + '...' if len(row['query']) > 40 else row['query']
            table_data.append([
                Paragraph(query_text, self.table_cell_style),
                Paragraph(f"{row['clicks']:,.0f}", self.table_cell_style),
                Paragraph(f"{row['impressions']:,.0f}", self.table_cell_style),
                Paragraph(f"{row['ctr']:.1f}", self.table_cell_style),
                Paragraph(f"{row['position']:.1f}", self.table_cell_style)
            ])
        
        top_table = Table(table_data, colWidths=[140, 70, 80, 60, 60])
        top_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ECC71')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        
        story.append(top_table)
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Топ-10 стран", self.section_style))
        story.append(Spacer(1, 10))
        
        if not top_countries_df.empty:
            countries_table_data = [
                [Paragraph('Страна', self.table_header_style), 
                 Paragraph('Клики', self.table_header_style), 
                 Paragraph('Показы', self.table_header_style), 
                 Paragraph('CTR (%)', self.table_header_style), 
                 Paragraph('Позиция', self.table_header_style)]
            ]
            
            for _, row in top_countries_df.head(10).iterrows():
                countries_table_data.append([
                    Paragraph(str(row['country']), self.table_cell_style),
                    Paragraph(f"{row['clicks']:,.0f}", self.table_cell_style),
                    Paragraph(f"{row['impressions']:,.0f}", self.table_cell_style),
                    Paragraph(f"{row['ctr']:.1f}", self.table_cell_style),
                    Paragraph(f"{row['position']:.1f}", self.table_cell_style)
                ])
            
            countries_table = Table(countries_table_data, colWidths=[100, 70, 80, 60, 60])
            countries_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E67E22')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            
            story.append(countries_table)
        else:
            no_data = Paragraph("Нет данных по странам за выбранный период", self.table_cell_style)
            story.append(no_data)
        
        story.append(Spacer(1, 20))
        story.append(Paragraph("Устройства", self.section_style))
        story.append(Spacer(1, 10))
        
        if not devices_df.empty:
            devices_table_data = [
                [Paragraph('Устройство', self.table_header_style), 
                 Paragraph('Клики', self.table_header_style), 
                 Paragraph('Показы', self.table_header_style), 
                 Paragraph('CTR (%)', self.table_header_style), 
                 Paragraph('Позиция', self.table_header_style)]
            ]
            
            for _, row in devices_df.iterrows():
                devices_table_data.append([
                    Paragraph(str(row['device']), self.table_cell_style),
                    Paragraph(f"{row['clicks']:,.0f}", self.table_cell_style),
                    Paragraph(f"{row['impressions']:,.0f}", self.table_cell_style),
                    Paragraph(f"{row['ctr']:.1f}", self.table_cell_style),
                    Paragraph(f"{row['position']:.1f}", self.table_cell_style)
                ])
            
            devices_table = Table(devices_table_data, colWidths=[100, 70, 80, 60, 60])
            devices_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9B59B6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            
            story.append(devices_table)
        else:
            no_data = Paragraph("Нет данных по устройствам за выбранный период", self.table_cell_style)
            story.append(no_data)
        
        story.append(Spacer(1, 20))
        story.append(Paragraph("Визуализация данных", self.section_style))
        story.append(Spacer(1, 10))
        
        for i, chart_path in enumerate(charts):
            if os.path.exists(chart_path):
                img = Image(chart_path, width=400, height=250)
                story.append(img)
                story.append(Spacer(1, 20))
        
        doc.build(story)
        return filename