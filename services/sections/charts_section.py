from reportlab.platypus import Paragraph, Spacer, Image, PageBreak

class ChartsSection:
    def __init__(self, styles, theme, content_width):
        self.styles = styles
        self.theme = theme
        self.content_width = content_width
    
    def build(self, charts):
        story = []
        
        story.append(PageBreak())
        story.append(Paragraph("Визуализация данных", self.styles.section_style))
        story.append(Spacer(1, 10))
        
        for chart_path in charts:
            img = Image(chart_path, width=self.content_width, height=300)
            story.append(img)
            story.append(Spacer(1, 20))
        
        return story