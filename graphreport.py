import matplotlib.pyplot as plt


def report_graph(outputlist, report_date):
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


def main():

    # Check reports
    print(
        report_graph([['Orange', 2, 1], ['Apple', 0, 1], ['Banana', 1, 0]],
                     '2021-01-01'))
    return


if __name__ == '__main__':
    main()
