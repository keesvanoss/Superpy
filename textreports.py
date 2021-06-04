from datetime import datetime

# Define constants
footer_inventory  = '\n+=============================+==========+=========+'
header_inventory  = footer_inventory + \
                    '\n| Product Name                | In stock | Expired |' + \
                    '\n+-----------------------------+----------+---------+'

footer_bought = '\n+==============+============+=========+============+'
header_bought = footer_bought + \
                '\n| Product Name |  Buy date  |  Price  |  Exp.date  |' + \
                '\n+--------------+------------+---------+------------+'

footer_sold =   '\n+==============+============+=========+============+'
header_sold =   footer_sold + \
                '\n| Product Name |  Sold date |  Price  |  Exp.date  |' + \
                '\n+--------------+------------+---------+------------+'

#==========================================================================================
# Create text report for inventory
#==========================================================================================

def report_txtinv(reportlist, report_date):

    report_out = f'\n********** INVENTORY REPORT ON {report_date} **********'  + header_inventory

    for item in reportlist:
        report_out += "\n| " + item[0].ljust(28) + "|"
        report_out += str(item[1]).center(10) + "|"
        report_out += str(item[2]).center(9) + "|"

    return report_out + footer_inventory

#==========================================================================================
# Create text report for products
#==========================================================================================

def report_txtprod(productlist, report_date, month_flag):

    if month_flag:
        reportdate = datetime.strptime(report_date + '-01'.strip("'"),
                                        '%Y-%m-%d')
        report_date = reportdate.strftime("%B %Y")

    report_out = f'\nProducts bought until {report_date}: '
    for item in productlist:
        report_out += item + ", "

    return report_out[:-2]

#==========================================================================================
# Create text report for revenue
#==========================================================================================

def report_txtrev(revenue, report_date, month_flag):

    if month_flag:
        reportdate = datetime.strptime(report_date + '-01'.strip("'"), '%Y-%m-%d')
        report_date = reportdate.strftime("%B %Y")

    return '\nRevenu on ' + report_date + ': EUR {:.2f}'.format(revenue)


#==========================================================================================
# Create text report for profit
#==========================================================================================

def report_txtprofit(profit, report_date, month_flag):

    if month_flag:
        reportdate = datetime.strptime(report_date + '-01'.strip("'"), '%Y-%m-%d')
        report_date = reportdate.strftime("%B %Y")

    return '\nProfit on ' + report_date + ': EUR {:.2f}'.format(profit)

#==========================================================================================
# Create text report for bought items
#==========================================================================================

def report_txtbought(outputlist, report_date, month_flag):

    # Check if data has to be reported
    if len(outputlist) != 0:

        if month_flag:
            reportdate = datetime.strptime(report_date + '-01'.strip("'"), '%Y-%m-%d')
            report_date = reportdate.strftime("%B %Y")

        report_out = f'\n************ BOUGHT REPORT ON {report_date} ***********' + header_bought

        for key in outputlist:
            report_out += "\n| " + outputlist[key][0].ljust(13) + "|"
            report_out += outputlist[key][1].replace("'", "").center(12) + "|"
            report_out += "{:.2f}".format(outputlist[key][2]).center(9) + "|"
            report_out += outputlist[key][3].replace("'", "").center(12) + "|"

        report_out += footer_bought

    else:
        report_out = 'No data available.'

    return report_out

#==========================================================================================
# Create text report for sold items
#==========================================================================================

def report_txtsold(outputlist, report_date, month_flag):

    # Check if data has to be reported
    if len(outputlist) != 0:

        if month_flag:
            reportdate = datetime.strptime(report_date + '-01'.strip("'"), '%Y-%m-%d')
            report_date = reportdate.strftime("%B %Y")

        report_out = f'\n******* SOLD + EXPIRED REPORT ON {report_date} ********' + header_sold

        for item in outputlist:
            report_out += "\n| " + item[0].ljust(13) + "|"
            report_out += item[1].replace("'", "").center(12) + "|"
            if item[2] != '-':
                report_out += "{:.2f}".format(item[2]).center(9) + "|"
            else:
                report_out += '-'.center(9) + "|"
            report_out += item[3].replace("'", "").center(12) + "|"

        report_out += footer_sold

    else:
        report_out = 'No data available.'

    return report_out


def main():

    # Check reports
    print(report_txtinv([['Orange', 2, 1], ['Apple', 0, 1]], '2021-01-14'))
    print(report_txtprod({'Orange', 'Apple', 'Banana'}, '2021-01-04', False))
    print(report_txtprod({'Orange', 'Apple', 'Banana'}, '2021-01', True))
    print(report_txtrev(4.5, '2021-01-01', False))
    print(report_txtrev(4.5, '2021-01', True))
    print(report_txtprofit(1.45, '2021-01-01', False))
    print(report_txtprofit(1.45, '2021-06', True))
    print(report_txtbought({'0': ['Orange', "'2021-01-01'", 4, "'2021-02-15'"]}, '2021-01-14', False))
    print(report_txtbought({'0': ['Orange', "'2021-01-01'", 4, "'2021-02-15'"]}, '2021-01', True))
    print(report_txtsold([['Orange', "'2021-01-01'", 4, "'2021-02-15'"]], '2021-01-14', False))
    print(report_txtsold([['Orange', "'2021-01-01'", 4, "'2021-02-15'"]], '2021-01', True))
    print(report_txtsold([], '2021-01', True))
    return


if __name__ == '__main__':
    main()
