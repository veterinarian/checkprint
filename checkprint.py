from fpdf import FPDF #pip install fpdf2
from num2words import num2words

#Quickbooks Check
check_measurements = {
    'date' : { 'x': 6.875, 'y': 0.75, 'w': 1.125, 'h': 0.25 },
    'payee' : { 'x': 1.25, 'y': 1.2, 'w': 5.5, 'h': 0.25 },
    'numeric_amount' : { 'x': 6.875, 'y': 1.2 , 'w': 1.125, 'h': 0.25 },
    'text_amount' : { 'x': 0.375, 'y': 1.575, 'w': 7.125, 'h': 0.25 },
    'memo' : { 'x': 0.875, 'y': 2.75, 'w': 2, 'h': 0.25 }}

def makepdf(payee,amount,date,memo='',address=''):
    def mkcell(m, txt, extend=False, ch='-'):
        pdf.set_xy(m['x'], m['y'])
        tw = pdf.get_string_width(txt)
        cw = m['w']
        if tw > cw:
            pdf.set_stretching(100.0*cw/tw)
        if extend and cw > tw:
            dw = pdf.get_string_width(ch)
            n = int((cw-tw) / dw)
            txt = txt + (ch * n)
        pdf.cell(m['w'], m['h'], txt)
        pdf.set_stretching(100.0)

    pdf = FPDF(orientation = 'P', unit = 'in', format='Letter')
    pdf.add_page()
    pdf.set_font('Courier', size=12)
    pdf.set_margins(0,0,0)
    mkcell(check_measurements['date'], date)
    mkcell(check_measurements['payee'], payee)
    mkcell(check_measurements['numeric_amount'], '{:,}'.format(amount))
    mkcell(check_measurements['text_amount'],
           num2words(amount, to='check').upper(),True)
    pdf.set_font('Courier', size=10)
    mkcell(check_measurements['memo'], memo)

    pdf.set_font('Courier', size=10)
    pdf.set_xy(0.375, 2)
    pdf.cell(4, 0.15, 'AVLC Admin', ln=2)
    pdf.cell(4, 0.15, txt='123 Any Street', ln=2)
    pdf.cell(4, 0.15, txt='Suite 300', ln=2)
    pdf.cell(4, 0.15, txt='Nowhere, TX 13313-1315')

    return pdf

if __name__ == '__main__':
    pdf = makepdf("John Duncan", 12315.33, "12/31/2017")
    pdf.output('check1.pdf', 'F')
