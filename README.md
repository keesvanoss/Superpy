# Superpy.py

* ## Highlight 1): Date calculation
To make calculations with dates is difficult in Python. You do need the Datetime library to convert ASCII dates into date objects. This way you can make calculations with dates in an easy way. So first convert dates into dates objects before doing any calculations. To be sure that dates are converted without quotes, these quotes are stripped from the date.

Example:

        # Convert dates to date objects for comparing
        exp_date = datetime.strptime(bought[key][3].strip("'"), '%Y-%m-%d')
        buy_date = datetime.strptime(bought[key][1].strip("'"), '%Y-%m-%d')

	if buy_date <= exp_date:

* ## Highlight 2): Parameter check
When entering routines, parameters are required. If you are missing parameters or having parameters in the wrong format, the program ends with an error. When entering a routine, I check if the right parameters are given and if dates are in the right format. If not, a decent message is displayed.

Example:

    # Check if routine is called with the right parameters
    error_message = ''
    if product_name is None:
        error_message += "ERROR: missing argument --product_name\n"
    if check_date(sell_date) is None:
        error_message += "ERROR: missing argument --sell_date or wrong format <YYYY-MM-DD>\n"
    if price is None:
        error_message += "ERROR: missing argument --price\n"

* ## Highlight 3): Report output
When a report is required, the right data is filtered, adjusted and put in a list. This list is the base for creating reports because the same list is used to generate a bar-graphic, csv-file or a text report. This way you only have to generate the datalist once which means that if the output has to be changed, you only have to change it in one place.

Example:

    # Create list with reporting data
    outputlist = []
    for item in productlist:
        stock_out = products_stock[item] if item in products_stock else 0
        expired_out = products_expired[item] if item in products_expired else 0
        if (stock_out != 0) or (expired_out != 0):
            outputlist.append([item, stock_out, expired_out])

        # Export inventory to REPORT.CSV
        if exportcsv:
            ...........

        # Show bar graph for inventory
        elif showgraph:
            ...........
	    
        # Create inventory text report
        else:

