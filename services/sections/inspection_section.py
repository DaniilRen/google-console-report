from reportlab.platypus import Paragraph, Spacer, TableStyle
from reportlab.lib import colors

class InspectionSection:
    def __init__(self, styles, theme, create_full_width_table, create_status_badge):
        self.styles = styles
        self.theme = theme
        self._create_full_width_table = create_full_width_table
        self._create_status_badge = create_status_badge
    
    def build(self, inspection_df, indexing_summary):
        story = []
        
        story.append(Paragraph("Проверка индексации страниц", self.styles.section_style))
        story.append(Spacer(1, 10))
        
        if indexing_summary and indexing_summary.get('urls_checked', 0) > 0:
            inspection_metrics = [
                [Paragraph('Показатель', self.styles.table_header_style), Paragraph('Значение', self.styles.table_header_style)],
                [Paragraph('Проверено URL', self.styles.table_cell_style), Paragraph(str(indexing_summary['urls_checked']), self.styles.table_cell_style)],
                [Paragraph('Проиндексировано', self.styles.table_cell_style), Paragraph(f"{indexing_summary['urls_indexed']} / {indexing_summary['urls_checked']}", self.styles.table_cell_style)],
                [Paragraph('Не индексируется', self.styles.table_cell_style), Paragraph(str(indexing_summary['urls_not_indexed']), self.styles.table_cell_style)],
                [Paragraph('Заблокировано robots.txt', self.styles.table_cell_style), Paragraph(str(indexing_summary['urls_blocked_by_robots']), self.styles.table_cell_style)],
                [Paragraph('Ошибки загрузки', self.styles.table_cell_style), Paragraph(str(indexing_summary['urls_with_fetch_errors']), self.styles.table_cell_style)]
            ]
            
            table = self._create_full_width_table(inspection_metrics, [50, 50])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (1, 0), colors.HexColor(self.theme['secondary'])),
                ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(self.theme['light_bg'])),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(self.theme['grid'])),
            ]))
            story.append(table)
            
            if not inspection_df.empty:
                story.append(Spacer(1, 15))
                inspection_data = [[Paragraph('URL', self.styles.table_header_style), 
                                   Paragraph('Статус', self.styles.table_header_style),
                                   Paragraph('Покрытие', self.styles.table_header_style), 
                                   Paragraph('Robots.txt', self.styles.table_header_style),
                                   Paragraph('Последний обход', self.styles.table_header_style)]]
                
                for _, row in inspection_df.iterrows():
                    url_text = row['url'][:40] + '...' if len(row['url']) > 40 else row['url']
                    inspection_data.append([Paragraph(url_text, self.styles.table_cell_left_style),
                        self._create_status_badge(row['indexing_state']),
                        Paragraph(str(row['coverage_state']).replace('_', ' '), self.styles.table_cell_style),
                        Paragraph(str(row['robots_txt_state']).replace('_', ' ').capitalize(), self.styles.table_cell_style),
                        Paragraph(str(row['last_crawl_time'])[:10] if row['last_crawl_time'] else 'Никогда', self.styles.table_cell_style)])
                
                detail_table = self._create_full_width_table(inspection_data, [30, 15, 20, 15, 20])
                detail_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.theme['tertiary'])),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(self.theme['grid'])),
                ]))
                story.append(detail_table)
        else:
            story.append(Paragraph("Нет данных проверки индексации. Добавьте URL для проверки в .env файле", self.styles.table_cell_style))
        
        story.append(Spacer(1, 20))
        return story