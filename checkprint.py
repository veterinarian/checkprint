from fpdf import FPDF #pip install fpdf2
from num2words import num2words

#Quickbooks Check
check_measurements = {
    'date' : { 'x': 6.875, 'y': 0.75, 'w': 1.125, 'h': 0.25 },
    'payee' : { 'x': 1.25, 'y': 1.2, 'w': 5.5, 'h': 0.25 },
    'numeric_amount' : { 'x': 6.875, 'y': 1.2 , 'w': 1.125, 'h': 0.25 },
    'text_amount' : { 'x': 0.375, 'y': 1.575, 'w': 7.125, 'h': 0.25 },
    'memo' : { 'x': 0.875, 'y': 2.75, 'w': 2, 'h': 0.25 },
    'address': { 'x': 0.375, 'y': 2, 'w': 4, 'h': 0.15 } # h = line leading
}

normal_font = { 'face': 'Helvetica', 'size': 12 }
small_font = { 'face': 'Helvetica', 'size': 10 }

capitalization=str.capitalize

def set_measurements(m):
    """Sets check measurements to m, returns the old measurements"""
    global check_measurements
    old = check_measurements
    check_measurements = m
    return old

def set_fonts(normal,small):
    """Sets fonts to normal and small, returns the old fonts as a tuple"""
    global normal_font, small_font
    old = (normal_font, small_font)
    normal_font, small_font = normal, small
    return old
    
def set_capitalization(f):
    """sets capitalization to the function f, returns the old function"""
    global capitalization
    old = capitalization
    capitaliztion = f
    return old
    
def makepdf(payee,amount,date,memo='',address=''):
    """Return an FPDF object that fills out a pre-printed check.

Output is based on the measurements in the check_measurements global,
normal_font and small_font, and using the capitalization function.
"""

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

    def small():
        pdf.set_font(small_font['face'], size=small_font['size'])
        
    def normal():
        pdf.set_font(normal_font['face'], size=normal_font['size'])
        
    pdf = FPDF(orientation = 'P', unit = 'in', format='Letter')
    pdf.add_page()
    normal()
    pdf.set_margins(0,0,0)
    mkcell(check_measurements['date'], date)
    mkcell(check_measurements['payee'], payee)
    mkcell(check_measurements['numeric_amount'], '{:,}'.format(amount))
    mkcell(check_measurements['text_amount'],
           capitalization(num2words(amount, to='check')),True)
    small()
    mkcell(check_measurements['memo'], memo)

    small()
    alines = address.split('\n')

    am = check_measurements['address']
    pdf.set_xy(am['x'],am['y'])
    for txt in alines:
        pdf.cell(am['w'], am['h'], txt, ln=2)

    return pdf

if __name__ == '__main__':
    import argparse
    import datetime

    parser = argparse.ArgumentParser(description="Create a PDF file that " +
                                     "fills in a pre-printed check.",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog='''
Example: 

python checkprint.py Veterinarian 2133.43 12/23/2017 Surgery 
    "Veterinary Clinic" "ATTN: Receptionist" "123 Main St" "Anywhere, US 99999"
''')
    today = datetime.date.today().strftime('%m/%d/%Y')
    parser.add_argument('payee', help="Payee name as string.")
    parser.add_argument('amount', type=float, help="Amount as decimal.")
    parser.add_argument('date',nargs='?', default=today,
                        help='Any string.  Default "today", currently '
                        + today + '.')
    parser.add_argument('memo',nargs='?', default='',
                        help="Any string for the memo line.")
    parser.add_argument('address',nargs='*', 
                        help="Lines for the address window.")
    parser.add_argument('-o', '--output', metavar='FILE',
                        help='Output to FILE instead of stdout')
    args = parser.parse_args()
    print(args)
    d = args.date.lower()
    if d == 'today':
        args.date = today
    address = '\n'.join(args.address)
    pdf = makepdf(args.payee,args.amount,args.date,args.memo,address)
    if args.output:
        pdf.output(args.output,'F')
    else:
        pdf.output()
