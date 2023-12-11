import requests

def getStatement(ttName, stmtType):
    """Returns records of the requested statement"""
    ttID = ttName.split("-")[-1]
    stmt = dict()
    url_string = "https://api.tickertape.in/stocks/financials/{}/{}/annual/normal?count=10"
    url = url_string.format(stmtType, ttID)
    print(url)
    records = json.loads(requests.get(url).content)["data"]
    for record in records:
        if record["displayPeriod"] == "TTM":
            continue
        
        for key in record:
            try:
                record[key] = round(record[key], 2)
            except:
                pass
        stmt[record["displayPeriod"].split("FY")[1].strip()] = record
    return stmt