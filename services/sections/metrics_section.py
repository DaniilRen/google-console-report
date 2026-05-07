from reportlab.platypus import Paragraph, Spacer, TableStyle
from reportlab.lib import colors

class MetricsSection:
    def __init__(self, styles, theme, create_full_width_table):
        self.styles = styles
        self.theme = theme
        self._create_full_width_table = create_full_width_table
    
    def build(self, metrics):
        story = []
        
        story.append(Paragraph("Ключевые показатели эффективности", self.styles.section_style))
        story.append(Spacer(1, 10))
        
        metrics_data = [
            [Paragraph('Показатель', self.styles.table_header_style), Paragraph('Значение', self.styles.table_header_style)],
            [Paragraph('Всего кликов', self.styles.table_cell_style), Paragraph(f"{metrics['total_clicks']:,.0f}", self.styles.table_cell_style)],
            [Paragraph('Всего показов', self.styles.table_cell_style), Paragraph(f"{metrics['total_impressions']:,.0f}", self.styles.table_cell_style)],
            [Paragraph('Средний CTR', self.styles.table_cell_style), Paragraph(f"{metrics['avg_ctr']:.2f}%", self.styles.table_cell_style)],
            [Paragraph('Средняя позиция', self.styles.table_cell_style), Paragraph(f"{metrics['avg_position']:.1f}", self.styles.table_cell_style)]
        ]
        
        table = self._create_full_width_table(metrics_data, [50, 50])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor(self.theme['primary'])),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(self.theme['light_bg'])),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(self.theme['grid'])),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        return story