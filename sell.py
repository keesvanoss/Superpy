import csv
import pathlib
from utils import check_date, clearfile
from buy import read_bought
from datetime import datetime, timedelta

csv_outputfile = 'sold.csv'

# ---------------------------------------------------------------------------------------------
# Syntax: sell product_name, sell_date, price
# Data will be added to the sold.csv file with an ID
# ---------------------------------------------------------------------------------------------


def sell(product_name, sell_date, price):

    # Convert report date to date object
    try:
        sold_date = datetime.strptime(sell_date.strip("'"), '%Y-%m-%d')
    except BaseException:
        return 'ERROR, Wrong date format'

    # Check if routine is called with the right parameters
    error_message = ''
    if product_name is None:
        error_message += "ERROR: missing argument --product_name\n"
    if check_date(sell_date) is None:
        error_message += "ERROR: missing argument --sell_date or wrong format <YYYY-MM-DD>\n"
    if price is None:
        error_message += "ERROR: missing argument --price\n"

    # If parameters ok, add data to sold.csv file
    if error_message == '':

        # If sold.csv exists, read last id nr else id = 0
        file = pathlib.Path(csv_outputfile)
        if file.exists():
            with open(csv_outputfile, 'r') as f:
                opened_file = f.readlines()
                id = int(opened_file[-1].split(',')[0])
                id = id + 1
        else:
            id = 0

        # Get bought list
        bought = read_bought(sell_date)

        if id > 0:

            # Read products sold and remove sold products from bought list
            sold = read_sold(sell_date)
            for item in sold.items():
                product_sell_date = datetime.strptime(item[1][1].strip("'"),
                                                      '%Y-%m-%d')

                # If sell_date is before report_date, remove item from bought
                # list
                if product_sell_date <= sold_date:
                    if item[1][0] in bought:
                        del bought[item[1][0]]

        # Check if product available
        product_id = -1
        for item in bought.items():
            if item[1][0] == product_name:
                product_id = item[0]
                break

        if product_id != -1:
            # Write data row with id to csv file
            with open(csv_outputfile, mode='a', newline='',
                      encoding='utf-8') as f:
                product_writer = csv.writer(f,
                                            delimiter=',',
                                            quotechar="'",
                                            quoting=csv.QUOTE_NONNUMERIC)
                product_writer.writerow(
                    [id, int(product_id), sell_date, price])

            # Action finished without problems, return 'Ok'
            return 'Ok'
        else:
            return 'ERROR: Product not in stock'
    else:

        # Error occured, return error
        return error_message


# ---------------------------------------------------------------------------------------------
# Read products sold until report_date and return list
# ---------------------------------------------------------------------------------------------


def read_sold(report_date):

    # Check if report until date or report for a month
    month_flag = False if len(report_date) > 7 else True
    start_date = report_date if month_flag == False else report_date + '-01'

    # Calculate start- end enddate for report
    try:
        startdate = datetime.strptime(start_date.strip("'"), '%Y-%m-%d')
        enddate = startdate if month_flag == False else (startdate.replace(
            day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    except BaseException:
        return 'ERROR, Wrong date format'

    # Read data from csv file into list
    filename = 'sold.csv'
    sold = {}

    f = pathlib.Path(filename)
    if f.exists():
        f = open(filename)
        reader = csv.reader(f)
        with f:
            for row in reader:

                # Read one line from csv file and convert dates
                product_id, bought_id, sold_date, price = row
                solddate = datetime.strptime(sold_date.strip("'"), '%Y-%m-%d')
                add_flag = False

                # If month report, check for buydate in month
                if month_flag:
                    if (solddate >= startdate) and (solddate <= enddate):
                        add_flag = True

                # If date report, check if buydate before reportdate
                else:
                    if solddate <= startdate:
                        add_flag = True

                # If buydate ok, add item to list
                if add_flag:
                    sold[product_id] = [bought_id, sold_date, float(price)]
    else:
        return {}

    return sold


# Test routine


def main():

    # Delete bought.csv file
    print(clearfile('sold.csv'))

    # Add items to sell.csv
    print('\nBanana sold:', sell('Banana', '2021-02-04', 3))
    print('Orange sold:', sell('Orange', '2021-01-02', 2))
    print('Peer   sold:', sell('Peer', '2021-02-04', 4))

    # Check sold with dates
    print('\nSold before 2021-01-03:\n', read_sold('2021-01-05'))
    print('\nSold in February:\n', read_sold('2021-02'))

    return


if __name__ == '__main__':
    main()
