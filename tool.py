from langchain.tools import tool
#python library to interact with yahoo finance data
import yfinance as yf
import json


@tool
def simple_screener(screen_type: str , offset: int) -> str:
    """Returns screened assets (stocks, funds, bonds) given popular criteria.

    Args:
        screen_type: One of a default set of stock screener queries from yahoo finance. 
        aggressive_small_caps
        day_gainers
        day_losers
        growth_technology_stocks
        most_actives
        most_shorted_stocks
        small_cap_gainers
        undervalued_growth_stocks
        undervalued_large_caps
        conservative_foreign_funds
        high_yield_bond
        portfolio_anchors
        solid_large_growth_funds
        solid_midcap_growth_funds
        top_mutual_funds
        offset: the pagination start point

    Returns:
        The a JSON output of assets that meet the criteria
    """
    #this inbuilt fxn of yf helps us to make a simple query based on the screen type and not a complex query
    query = yf.PREDEFINED_SCREENER_QUERIES[screen_type]['query']
    #this is the actual retreival of data using the query
    #setting size=5 means request 5 results from the screening query
    result = yf.screen(query , offset=offset , size=5)

    #storing the result in a json file
    with open('output.json' , 'w') as f:
        json.dump(result , f)

    #predifined list of fields for which we want the data
    fields = ["shortName","bid","ask","exchange", "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "averageAnalystRating", "dividendYield", "symbol"]

    output_data = []

    #looping through each stock
    #yf has a quotes section containing the assests
    for stock_detail in result['quotes']:

        #creating a dictionary for each stock
        details = {}

        for key , val in stock_detail.items():
            if key in fields:
                details[key] = val

        output_data.append(details)


    return f"Stock screener Results: {output_data}"
