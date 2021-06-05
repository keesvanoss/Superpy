# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

# ---------------------------------------------------------------------------------------------
# Declare import modules
# ---------------------------------------------------------------------------------------------

import report
from datetime import timedelta, datetime
from arguments import get_arguments
from buy import buy
from sell import sell
from utils import get_current_date
from utils import advance_date, set_date

# Your code below this line.

# ---------------------------------------------------------------------------------------------
# Main routine
# ---------------------------------------------------------------------------------------------


def main():

    # Read config file for date
    current_date = get_current_date()

    # Get command line arguments
    args = get_arguments()

    # Check date handling commands and execute the corresponding routine
    if args.advance_date is not None:
        current_date = print(advance_date(args.advance_date))
        return current_date
    if args.set_date is not None:
        current_date = print(set_date(args.set_date))
        return current_date

    # Check commands and execute the corresponding routine
    if args.CLI_command.lower() == 'buy':
        print(
            buy(args.product_name, args.buy_date, args.price,
                args.expiration_date))
    elif args.CLI_command.lower() == 'sell':
        print(sell(args.product_name, args.sell_date, args.price))
    elif args.CLI_command.lower() == 'report':

        # Convert yesterday, now, today or date to date
        report_date = None
        if args.yesterday is not None:
            report_date = (datetime.strptime(current_date, '%Y-%m-%d') -
                           timedelta(days=1)).strftime('%Y-%m-%d')
        if args.now is not None:
            report_date = current_date
        if args.today is not None:
            report_date = current_date
        if args.date is not None:
            report_date = args.date
        if report_date is not None:
            print(
                report.show_report(args.report_name, report_date,
                                   args.export_csv, args.show_graph, args.export_pdf))
        else:
            print(f"ERROR: missing <date>")

    # Unknown command
    else:
        print(
            f"ERROR: unknown command '{args.CLI_command}' <buy, sell, report>")
    return


if __name__ == '__main__':
    main()
