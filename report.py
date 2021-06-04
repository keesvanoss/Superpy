import csv
import matplotlib.pyplot as plt
from sell import read_sold
from buy import read_bought
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------------------------
# Class which calculates the sum of a column in a dictionary
# ---------------------------------------------------------------------------------------------


class Finance:
    def __init__(self, header, amount, column):
        self.header = header
        self.amount = sum(item[1][column] for item in amount.items())


# ---------------------------------------------------------------------------------------------
# Report inventory on certain date and return products in store and expired products in a list
# ---------------------------------------------------------------------------------------------


def report_inventory(report_date, exportcsv, showgraph):

    # Convert report date to date object
    try:
        rep_date = datetime.strptime(report_date.strip("'"), '%Y-%m-%d')
    except BaseException:
        return 'ERROR, Wrong date format'

    # Read products bought and create list with all products
    bought = read_bought(report_date)
    productlist = []
    productlist = set([item[1][0] for item in bought.items()])

    # Read products sold and remove sold products from bought list
    sold = read_sold(report_date)
    for item in sold.items():
        sell_date = datetime.strptime(item[1][1].strip("'"), '%Y-%m-%d')

        # If sell_date is before report_date, remove item from bought list
        if sell_date <= rep_date:
            if item[1][0] in bought:
                del bought[item[1][0]]

    # Crystalize inventory from bought
    products_stock = {}
    products_expired = {}
    for key in bought:

        # Convert dates to date objects for comparing
        exp_date = datetime.strptime(bought[key][3].strip("'"), '%Y-%m-%d')
        buy_date = datetime.strptime(bought[key][1].strip("'"), '%Y-%m-%d')

        # Summarize products and expired products compared to report date
        if buy_date <= rep_date:
            if rep_date < exp_date:
                if bought[key][0] in products_stock.keys():
                    products_stock[bought[key][0]] += 1
                else:
                    products_stock[bought[key][0]] = 1
            else:
                if bought[key][0] in products_expired.keys():
                    products_expired[bought[key][0]] += 1
                else:
                    products_expired[bought[key][0]] = 1

    # Create list with reporting data
    outputlist = []
    for item in productlist:
        stock_out = products_stock[item] if item in products_stock else 0
        expired_out = products_expired[item] if item in products_expired else 0
        if (stock_out != 0) or (expired_out != 0):
            outputlist.append([item, stock_out, expired_out])

    # Check if output data available
    if len(outputlist) != 0:

        # Export inventory to REPORT.CSV
        if exportcsv:
            try:
                file = open('report.csv', 'w+', newline='')
                with file:
                    write = csv.writer(file)
                    write.writerows(outputlist)
                return 'Report exported to REPORT.CSV'
            except BaseException:
                return 'ERROR, in creating datafile REPORT.CSV'

        # Show bar graph for inventory
        if showgraph:

            # Set values X/Y axis
            x = [item[0] for item in outputlist]
            y1 = [item[1] for item in outputlist]
            y2 = [item[2] for item in outputlist]

            # Define graph + labels
            plt.bar(x, y1, color='g')
            plt.bar(x, y2, bottom=y1, color='r')
            plt.title(f'Inventory on {report_date}')
            plt.xlabel('Products')
            plt.ylabel('Number')
            plt.legend(["In stock", "Expired"])

            # Show graph
            plt.show()

            return 'Inventory bar-graph showed'

        # Create inventory text report
        else:

           # Header
            report_out = f'\n********** INVENTORY REPORT ON {report_date} **********'
            report_out += '\n+=============================+==========+=========+'
            report_out += '\n| Product Name                | In stock | Expired |'
            report_out += '\n+-----------------------------+----------+---------+'

            # Data
            for item in outputlist:
                report_out += "\n| " + item[0].ljust(28) + "|"
                report_out += str(item[1]).center(10) + "|"
                report_out += str(item[2]).center(9) + "|"

            # Footer
            report_out += '\n+=============================+==========+=========+'

            return report_out
    else:
        return 'No data available'

# ---------------------------------------------------------------------------------------------
# Report all products bought before report-date
# --------------------------------------------------------------------------------------------


def report_products(report_date, exportcsv):

    # Check if report for date or month
    month_flag = False if len(report_date) > 7 else True

    # Read products bought and create list with all products
    bought = read_bought(report_date)
    productlist = []
    productlist = set([item[1][0] for item in bought.items()])

    # Check if output data available
    if len(productlist) != 0:

        # Export inventory to REPORT.CSV
        if exportcsv:
            try:
                with open('report.csv', 'w') as export:
                    export_writer = csv.writer(export, lineterminator='\n')
                    for item in productlist:
                        export_writer.writerow([item])
                return 'Data exported to REPORT.CSV'
            except BaseException:
                return 'ERROR, in creating datafile REPORT.CSV'

        # Create text report
        else:
            if month_flag:
                reportdate = datetime.strptime(report_date + '-01'.strip("'"),
                                               '%Y-%m-%d')
                report_date = reportdate.strftime("%B %Y")

            report_out = f'\nProducts bought until {report_date}: '
            for item in productlist:
                report_out += item + ", "
            return report_out[:-2]

    else:
        return 'No data available'

# ---------------------------------------------------------------------------------------------
# Revenue report, print revenue on a given date.
# ---------------------------------------------------------------------------------------------


def report_revenue(report_date, exportcsv):

    # Check if report for date or month
    month_flag = False if len(report_date) > 7 else True

    # Read products sold
    sold = read_sold(report_date)

    # Sumarize all prices in sold
    revenue = sum(item[1][2] for item in sold.items())

    # Check if output data available
    if len(sold) != 0:

        # Export inventory to REPORT.CSV
        if exportcsv:
            try:
                with open('report.csv', 'w') as export:
                    export_writer = csv.writer(export, lineterminator='\n')
                    export_writer.writerow([revenue])
                return 'Data exported to REPORT.CSV'
            except BaseException:
                return 'ERROR, in creating datafile REPORT.CSV'

        # Create text report
        else:
            if month_flag:
                reportdate = datetime.strptime(report_date + '-01'.strip("'"),
                                               '%Y-%m-%d')
                report_date = reportdate.strftime("%B %Y")
            return '\nRevenu on ' + report_date + \
                ': EUR {:.2f}'.format(revenue)
    else:
        return 'No data available'

# ---------------------------------------------------------------------------------------------
# Report profit on report-date
# ---------------------------------------------------------------------------------------------


def report_profit(report_date, exportcsv):

    # Check if report for date or month
    month_flag = False if len(report_date) > 7 else True

    # Read products bought and sold
    bought = read_bought(report_date)
    sold = read_sold(report_date)

    # Sumarize all prices in bought column 2
    total_bought = Finance('bought', bought, 2)

    # Sumarize all prices in sold column 2
    total_sold = Finance('sold', sold, 2)

    # Check if output data available
    if (len(bought) != 0) or (len(sold) != 0):

        # Export inventory to REPORT.CSV
        if exportcsv:
            try:
                with open('report.csv', 'w') as export:
                    export_writer = csv.writer(export, lineterminator='\n')
                    export_writer.writerow(
                        [round(total_sold.amount - total_bought.amount, 2)])
                return 'Data exported to REPORT.CSV'
            except BaseException:
                return 'ERROR, in creating datafile REPORT.CSV'

        # Create text report
        else:
            if month_flag:
                reportdate = datetime.strptime(report_date + '-01'.strip("'"),
                                               '%Y-%m-%d')
                report_date = reportdate.strftime("%B %Y")

            return '\nProfit on ' + report_date + \
                ': EUR {:.2f}'.format(total_sold.amount - total_bought.amount)
    else:
        return 'No data available'

# ---------------------------------------------------------------------------------------------
# Report products + info bought before report-date
# ---------------------------------------------------------------------------------------------


def report_bought(report_date, exportcsv):

    # Check if report for date or month
    month_flag = False if len(report_date) > 7 else True

    # Read bought products
    bought = read_bought(report_date)

    # Check if output data available
    if len(bought) != 0:

        # Export inventory to REPORT.CSV
        if exportcsv:
            try:
                with open('report.csv', 'w') as export:
                    export_writer = csv.writer(export, lineterminator='\n')
                    for key in bought:
                        name_out = bought[key][0]
                        buydate_out = bought[key][1]
                        price_out = bought[key][2]
                        expdate_out = bought[key][3]
                        export_writer.writerow(
                            [name_out, buydate_out, price_out, expdate_out])
                return 'Data exported to REPORT.CSV'
            except BaseException:
                return 'ERROR, in creating datafile REPORT.CSV'

        # Create text report
        else:

            # Check if data has to be reported
            if len(bought) != 0:

                # Header
                if month_flag:
                    reportdate = datetime.strptime(
                        report_date + '-01'.strip("'"), '%Y-%m-%d')
                    report_date = reportdate.strftime("%B %Y")

                report_out = f'\n************ BOUGHT REPORT ON {report_date} ***********'
                report_out += '\n+==============+============+=========+============+'
                report_out += '\n| Product Name |  Buy date  |  Price  |  Exp.date  |'
                report_out += '\n+--------------+------------+---------+------------+'

                # Data
                for key in bought:
                    report_out += "\n| " + bought[key][0].ljust(13) + "|"
                    report_out += bought[key][1].replace(
                        "'", "").center(12) + "|"
                    report_out += "{:.2f}".format(
                        bought[key][2]).center(9) + "|"
                    report_out += bought[key][3].replace(
                        "'", "").center(12) + "|"

                # Footer
                report_out += '\n+==============+============+=========+============+'

            else:
                report_out = 'No data available.'

            return report_out

    else:
        return 'No data available'

# ---------------------------------------------------------------------------------------------
# Report products + info sold or expired on report-date
# ---------------------------------------------------------------------------------------------


def report_sold(report_date, exportcsv):

    # Check if report for date or month
    month_flag = False if len(report_date) > 7 else True

    # Read all bought and sold products
    bought = read_bought('All')
    sold = read_sold(report_date)

    # Create reportlist of all records and create list with all sold-ID's
    outputlist = []
    soldlist = []

    # Add sold items before report date to list
    for key in sold:
        name = bought[sold[key][0]][0]
        sold_date = sold[key][1]
        sold_price = sold[key][2]
        exp_date = bought[sold[key][0]][3]
        outputlist.append([name, sold_date, sold_price, exp_date])
        soldlist.append(sold[key][0])

    # Read all bought items until date
    bought = read_bought(report_date)

    try:
        if month_flag:
            report_date += '-01'

        # Convert dates to date objects and calculate end of month date
        startdate = datetime.strptime(report_date.strip("'"), '%Y-%m-%d')
        enddate = (startdate.replace(day=1) +
                   timedelta(days=32)).replace(day=1) - timedelta(days=1)

    except BaseException:
        return 'ERROR, Wrong date format'

    # Add not sold items which are expired to reportlist
    for key in bought:
        if key not in soldlist:
            name = bought[key][0]
            sold_date = 'Expired'
            sold_price = '-'
            expdate = datetime.strptime(bought[key][3].strip("'"), '%Y-%m-%d')
            if month_flag:
                if (expdate >= startdate) and (expdate <= enddate):
                    outputlist.append(
                        [name, sold_date, sold_price, bought[key][3]])
            else:
                if startdate >= expdate:
                    outputlist.append(
                        [name, sold_date, sold_price, bought[key][3]])

    # Check if output data available
    if len(outputlist) != 0:

        # Export inventory to REPORT.CSV
        if exportcsv:
            try:
                file = open('report.csv', 'w+', newline='')
                with file:
                    write = csv.writer(file)
                    write.writerows(outputlist)
                return 'Report exported to REPORT.CSV'
            except BaseException:
                return 'ERROR, in creating datafile REPORT.CSV'

        # Create text report
        else:

            # Header
            if month_flag:
                reportdate = datetime.strptime(
                    report_date.strip("'"), '%Y-%m-%d')
                report_date = reportdate.strftime("%B %Y")

            report_out = f'\n******* SOLD + EXPIRED REPORT ON {report_date} ********'
            report_out += '\n+==============+============+=========+============+'
            report_out += '\n| Product Name |  Sold date |  Price  |  Exp.date  |'
            report_out += '\n+--------------+------------+---------+------------+'

            # Data
            for item in outputlist:
                report_out += "\n| " + item[0].ljust(13) + "|"
                report_out += item[1].replace("'", "").center(12) + "|"
                if item[2] != '-':
                    report_out += "{:.2f}".format(item[2]).center(9) + "|"
                else:
                    report_out += '-'.center(9) + "|"
                report_out += item[3].replace("'", "").center(12) + "|"

            # Footer
            report_out += '\n+==============+============+=========+============+'

            return report_out
    else:
        return 'No data available'

# ---------------------------------------------------------------------------------------------
# Show report:
# ---------------------------------------------------------------------------------------------
# Check which report has to be created:
# - inventory, shows inventory on certain date
# - revenue, shows revenue on certain date
# - profit, shows profit on certain date
# - products, shows which products are available on certain date
# - bought, shows all products + info bought before a certain date
# - sold, shows all products + info sold or expired on a certain date
#
# Reports can be created at a certain date or as a montly overview.
# All reports can be saved as CSV files.
# The inventory report can be shown as a bar-graphic
# ---------------------------------------------------------------------------------------------


def show_report(report_name, report_date, export_csv, show_graph):

    # Check for valid report name typed
    if report_name == 'inventory':
        return (report_inventory(report_date, export_csv, show_graph))
    elif report_name == 'revenue':
        return (report_revenue(report_date, export_csv))
    elif report_name == 'profit':
        return (report_profit(report_date, export_csv))
    elif report_name == 'products':
        return (report_products(report_date, export_csv))
    elif report_name == 'bought':
        return (report_bought(report_date, export_csv))
    elif report_name == 'sold':
        return (report_sold(report_date, export_csv))
    else:
        print(
            f"ERROR: unknown report '{report_name}' <inventory, revenue, profit>"
        )
    return


# ---------------------------------------------------------------------------------------------
# Test routines
# ---------------------------------------------------------------------------------------------


def main():

    # Check reports
    print(report_inventory('2021-01-14', False, False))
    print(report_inventory('2021-01-14', True, False))
    print(report_inventory('2021-01-14', False, True))
    print(report_revenue('2021-02-04', False))
    print(report_revenue('2021-03', False))
    print(report_profit('2021-01-08', False))
    print(report_profit('2021-02', False))
    print(report_products('2021-01-01', False))
    print(report_products('2021-01', False))
    print(report_bought('2021-03-01', False))
    print(report_bought('2021-03', False))
    print(report_sold('2021-01-12', False))
    print(report_sold('2021-01', False))
    return


if __name__ == '__main__':
    main()
