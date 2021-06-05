import argparse

msg = """ superpy.py <CLI_command> [Options]\n
    Examples:\n
    \tsuperpy.py buy  --product_name <name> --price <price> --buy_date <date> -- expiration_date <date>
    \tsuperpy.py sell --product_name <name> --price <price> --sell_date <date>\n
    \tsuperpy.py report inventory [report-date]                <--export_csv> <show_graph>
    \t\t\t  revenue   [report-date]/[report-month] <--export_csv>
    \t\t\t  profit    [report-date]/[report-month] <--export_csv>
    \t\t\t  products  [report_date]/[report-month] <--export_csv>
    \t\t\t  bought    [report_date]/[report-month] <--export_csv>
    \t\t\t  sold      [report_date]/[report-month] <--export_csv>\n
    \tsuperpy.py --set_date <date>
    \t\t   --advance_date <days>\n\n
    Valid <date> argument is:
    \t'yyyy-mm-dd'\n
    Valid [report-date] arguments are:
    \t--now
    \t--today
    \t--yesterday
    \t--date 'yyyy-mm-dd'\n
    Valid [report-month] arguments are:
    \t--date 'yyyy-mm'
    """


def get_arguments():

    my_parser = argparse.ArgumentParser(
        description='SuperPy, a supermarkt inventory tracker tool',
        usage=msg,
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog,
            max_help_position=40))

    my_parser.add_argument('CLI_command',
                           nargs='?',
                           default='None',
                           type=str,
                           help='command')

    my_parser.add_argument('report_name',
                           nargs='?',
                           default='None',
                           type=str,
                           help='report name')

    my_parser.add_argument('--product_name',
                           help='product name',
                           action='store',
                           type=str)

    my_parser.add_argument('--price',
                           help='product price',
                           action='store',
                           type=float)

    my_parser.add_argument('--expiration_date',
                           help='product expiration date',
                           action='store',
                           type=str)

    my_parser.add_argument('--buy_date',
                           help='product buy date',
                           action='store',
                           type=str)

    my_parser.add_argument('--sell_date',
                           help='product sell date',
                           action='store',
                           type=str)

    my_parser.add_argument('--date',
                           help='select certain date',
                           action='store',
                           type=str)

    my_parser.add_argument('--now',
                           help='select date from config.sys as current date',
                           action='store_const',
                           const=True)

    my_parser.add_argument('--today',
                           help='select date from config.sys as current date',
                           action='store_const',
                           const=True)

    my_parser.add_argument(
        '--yesterday',
        help='select date from config.sys -1 as current date',
        action='store_const',
        const=True)

    my_parser.add_argument('--set_date',
                           help='set current date in config.txt',
                           action='store',
                           type=str)

    my_parser.add_argument(
        '--advance_date',
        help='advance current date in config.sys with xx days',
        action='store',
        type=int)

    my_parser.add_argument('--export_csv',
                           help='export data to data file REPORT.CSV',
                           action='store_const',
                           const=True)

    my_parser.add_argument('--export_pdf',
                           help='export data to REPORT.PDF',
                           action='store_const',
                           const=True)

    my_parser.add_argument('--show_graph',
                           help='show bar graph of data',
                           action='store_const',
                           const=True)

    return my_parser.parse_args()
