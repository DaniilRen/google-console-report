from reportlab.platypus import Paragraph, Spacer, TableStyle
from reportlab.lib import colors

class DevicesSection:
    def __init__(self, styles, theme, create_full_width_table):
        self.styles = styles
        self.theme = theme
        self._create_full_width_table = create_full_width_table
    
    def build(self, devices_df):
        story = []
        
        story.append(Paragraph("Устройства", self.styles.section_style))
        story.append(Spacer(1, 10))
        
        if not devices_df.empty:
            devices_data = [[Paragraph('Устройство', self.styles.table_header_style), 
                            Paragraph('Клики', self.styles.table_header_style),
                            Paragraph('Показы', self.styles.table_header_style), 
                            Paragraph('CTR (%)', self.styles.table_header_style),
                            Paragraph('Позиция', self.styles.table_header_style)]]
            
            for _, row in devices_df.iterrows():
                devices_data.append([Paragraph(str(row['device']), self.styles.table_cell_left_style),
                    Paragraph(f"{row['clicks']:,.0f}", self.styles.table_cell_style),
                    Paragraph(f"{row['impressions']:,.0f}", self.styles.table_cell_style),
                    Paragraph(f"{row['ctr']:.1f}", self.styles.table_cell_style),
                    Paragraph(f"{row['position']:.1f}", self.styles.table_cell_style)])
            
            table = self._create_full_width_table(devices_data, [40, 15, 15, 15, 15])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.theme['quaternary'])),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor(self.theme['text_light'])),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(self.theme['grid'])),
            ]))
            story.append(table)
        else:
            story.append(Paragraph("Нет данных по устройствам за выбранный период", self.styles.table_cell_style))
        
        story.append(Spacer(1, 20))
        return story