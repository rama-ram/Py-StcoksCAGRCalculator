import pandas
import datetime

if __name__ == '__main__':
    data = pandas.read_csv("SampleCAGR.csv")
    df = pandas.DataFrame(data)
    print(df)

    previous_scrip_name = ""
    current_date = datetime.date.today()
    print(current_date)
    result = {}

    for index, row in data.iterrows():
        if str(row["ScripName"]) == "nan":
            date = str(row["Date"]).replace("Opening as on ", "").strip("  *")
            date_formatted = datetime.datetime.strptime(date, "%d/%m/%Y").date()
            number_of_years = int((current_date - date_formatted).days / 365)
            buy_value = 1 if float(row["BuyValue"]) == 0 else float(row["BuyValue"])
            cagr = round(((((float(row["MarketValue"]) / buy_value) ** (
                    1 / number_of_years)) - 1) * 100), 2) if number_of_years > 0 else 0
            result[previous_scrip_name].append(
                [previous_scrip_name, str(date_formatted), row["BuyValue"], row["MarketValue"], number_of_years, cagr])
        else:
            previous_scrip_name = str(row["ScripName"])
            result[previous_scrip_name] = []
    values_list = result.values()
    flattened_list = [item for list_item in values_list for item in list_item]
    print(flattened_list)
    columns = ["Scrip", "Buy Date", "Buy Value", "Market Value", "Number of Years", "CAGR"]
    df = pandas.DataFrame(flattened_list,columns=columns)
    df.to_excel("cagr_calculated.xlsx",index=False)

#TODO handle initial formatting of the sheet downloaded before parsing data