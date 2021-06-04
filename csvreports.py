import csv


#==========================================================================================
# Create csv report with seperate items in a row for outputlist
#==========================================================================================

def report_csvitems(outputlist):
    try:
        file = open('report.csv', 'w+', newline='')
        with file:
            write = csv.writer(file)
            write.writerows(outputlist)
        return 'Data exported to REPORT.CSV'
    except BaseException:
        return 'ERROR, in creating datafile REPORT.CSV'

#==========================================================================================
# Create csv report with rows for outputlist
#==========================================================================================

def report_csvrow(outputlist):
    try:
        with open('report.csv', 'w') as export:
            export_writer = csv.writer(export, lineterminator='\n')
            for item in outputlist:
                export_writer.writerow([item])
        return 'Data exported to REPORT.CSV'
    except BaseException:
        return 'ERROR, in creating datafile REPORT.CSV'

def report_csvbought(outputlist):
    pass


def main():

    # Check reports
    print(report_csvitems([['Orange', 2, 1], ['Apple', 0, 1]]))
    print(report_csvrow({'Orange','Apple'}))
    print(report_csvrow([7.00]))
    print(report_csvrow([-14.0]))
    return


if __name__ == '__main__':
    main()
