import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


# ---------------------------------------------------------------------------------------------
# Report Class for generating a PDF report
# You can add a logo, header, paragraph and table before saving the PDF file
# ---------------------------------------------------------------------------------------------

class Report:

    styles = None
    document = None
    elements = []

    # Initialize new PDF document
    def __init__(self, filename):
        self.styles = getSampleStyleSheet()

        # Create new centered BodyText style
        self.styles.add(ParagraphStyle(name = 'BodyText_CENTER',
                parent = self.styles['BodyText'],
                alignment=TA_CENTER,
                leading=20
                        ))

        # Use template
        self.document = SimpleDocTemplate(filename, pagesize=letter)
        return

    # Option to add a logo to the PDF document
    def add_logo(self,logoname, scale):
        I = Image(logoname)
        I.drawHeight = scale * inch * I.drawHeight / I.drawWidth
        I.drawWidth =  scale * inch
        self.elements.append(I)

    # Option to add a header to the PDF document
    def add_header(self, text):
        P = Paragraph(text, self.styles["Title"])
        self.elements.append(P)

    # Option to add a paragraph to the PDF document
    def add_paragraph(self, text, style):
        P = Paragraph(text, self.styles[style])
        self.elements.append(P)

    # Option to add a table to the PDF document
    def add_table(self, data):
        T = Table(data,style=[
        # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),       
            ('BOX',(0,0),(-1,-1),2,colors.black),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('ALIGN',(0,0),(-1,-1),"CENTER")
            ])
        # Set cellwidth
        for i in range(len(data[0])):                           
            T._argW[i] = inch

        self.elements.append(T)

    # Save the PDF document
    def build(self):
        self.document.build(self.elements)


# ---------------------------------------------------------------------------------------------
# Create PDF report
# ---------------------------------------------------------------------------------------------

def report_pdf(bodytext, outputlist):
    try:
        doc = Report('report.pdf')
        doc.add_logo('logo.png', 4)
        doc.add_header('SUPERPY Opdracht ')
        doc.add_paragraph(bodytext, "BodyText_CENTER")
        doc.add_table(outputlist)
        doc.build()
        os.system('report.pdf')
        return 'Data exported to REPORT.PDF'
    except BaseException:
        return 'ERROR, in creating datafile REPORT.PDF'

# ---------------------------------------------------------------------------------------------
# Test routines
# ---------------------------------------------------------------------------------------------


def main():

    data = [['A', 'B', 'C'],
            ['00', '01', '02'],
            ['10', '11', '12'],
            ['20', '21', '22'],
            ['30', '31', '32']]

    report_pdf('Dit is een rapport met 3 kolommen voor Inventory Superpy', data)
    
    data = [['A', 'B', 'C', 'E'],
            ['00', '01', '02', '03'],
            ['10', '11', '12', '13'],
            ['20', '21', '22', '23'],
            ['30', '31', '32', '33']]

    report_pdf('En dit is een test voor een tabel met 4 kolommen', data)
    
    return


if __name__ == '__main__':
    main()


