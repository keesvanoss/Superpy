import csv
import pathlib
from utils import check_date, clearfile
from datetime import datetime, timedelta

csv_filename = 'bought.csv'

# ---------------------------------------------------------------------------------------------
# Syntax: buy product_name, price, expiration_date
# Data will be added to the bought.csv file with an ID
# ---------------------------------------------------------------------------------------------


def buy(product_name, buy_date, price, expiration_date):

    # Check if routine is called with the right parameters
    error_message = ''
    if product_name is None:
        error_message += "ERROR: missing argument --product_name\n"
    if price is None:
        error_message += "ERROR: missing argument --price\n"
    if check_date(expiration_date) is None:
        error_message += "ERROR: missing argument --expiration_date or wrong format <YYYY-MM-DD>\n"
    if check_date(buy_date) is None:
        error_message += "ERROR: missing argument --buy_date or wrong format <YYYY-MM-DD>"

    # If parameters ok, add data to bought.csv file
    if error_message == '':

        # If bought.csv exists, read last ID else id = 0
        file = pathlib.Path(csv_filename)
        if file.exists():
            with open(csv_filename, 'r') as f:
                opened_file = f.readlines()
                id = int(opened_file[-1].split(',')[0])
                id = id + 1
        else:
            id = 0

        # Write data row with ID to csv file
        with open(csv_filename, mode='a', newline='', encoding='utf-8') as f:
            product_writer = csv.writer(f,
                                        delimiter=',',
                                        quotechar="'",
                                        quoting=csv.QUOTE_NONNUMERIC)
            product_writer.writerow(
                [id, product_name, buy_date, price, expiration_date])

        # Action finished without problems, return 'Ok'
        return 'Ok'

    else:

        # Error occured, return error
        return error_message


# ---------------------------------------------------------------------------------------------
# Read products bought until report_date and return list
# ---------------------------------------------------------------------------------------------


def read_bought(report_date):

    if report_date != 'All':

        # Check if report until date or report for a month
        month_flag = False if len(report_date) > 7 else True
        start_date = report_date if month_flag == False else report_date + '-01'

        # Calculate start- and enddate for report
        try:
            startdate = datetime.strptime(start_date.strip("'"), '%Y-%m-%d')
            enddate = startdate if month_flag == False else (startdate.replace(
                day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        except BaseException:
            return 'ERROR, Wrong date format'

    # Read data from csv file into list
    filename = 'bought.csv'
    bought = {}

    f = pathlib.Path(filename)
    if f.exists():
        f = open(filename)
        reader = csv.reader(f)
        with f:
            for row in reader:

                # Read one line from csv file and convert dates
                product_id, product_name, buy_date, price, exp_date = row
                buydate = datetime.strptime(buy_date.strip("'"), '%Y-%m-%d')

                # Read all records
                if report_date == 'All':
                    add_flag = True

                # Read records defined by dates
                else:
                    add_flag = False

                    # If month report, check for buydate in month
                    if month_flag:
                        if (buydate >= startdate) and (buydate <= enddate):
                            add_flag = True

                    # If date report, check if buydate before reportdate
                    else:
                        if (buydate <= startdate):
                            add_flag = True

                # If buydate ok, add item to list
                if add_flag:
                    bought[product_id] = [
                        product_name.replace("'", ""), buy_date,
                        float(price), exp_date
                    ]
    else:
        return {}

    return bought


# ---------------------------------------------------------------------------------------------
# Test routines
# ---------------------------------------------------------------------------------------------


def main():

    # Delete bought.csv file
    print(clearfile('bought.csv'))

    # Add items to bought.csv
    print('\nBanana added:', buy('Banana', '2021-01-08', 3, '2021-01-15'))
    print('Orange added:', buy('Orange', '2021-01-01', 3, '2021-01-10'))
    print('Apple  added:', buy('Apple', '2021-01-01', 2, '2021-01-10'))
    print('Peer   added:', buy('Peer', '2021-01-01', 4, '2021-01-12'))
    print('Peer   added:', buy('Peer', '2021-01-03', 4, '2021-02-15'))

    # Check bought with dates
    print('\nBought before 2021-01-03:\n', read_bought('2021-01-03'))
    print('\nBought in January:\n', read_bought('2021-01'))

    return


if __name__ == '__main__':
    main()
