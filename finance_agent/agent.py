import requests
from google.adk.agents import Agent
import yfinance as yf
import json

# def get_market_screener() -> dict:
#     # """Fetches the Market data.  
#     # """
#     try:
#         url = f"https://jsonplaceholder.typicode.com/posts/1"

#         # querystring = {"list":"day_gainers"}

#         # headers = {
#         # "x-rapidapi-key": "67eec20f09msh8006b65c054ee0ap16f1bbjsn6c698c90c5d8",
#         # "x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
#         # }
        
#         # response = requests.get(url, headers=headers, params=querystring)
#         response = requests.get(url)

#         if response.status_code == 200:
#             data = response.json()           
#             # return {
#             #     "status": "success",
#             #     "report": f"The current price of {coin.capitalize()} is {price} {currency.upper()}."
#             # }       
#             return {
#                 "status":"success",
#                 "report":f"Details are {data}"
#             }     
               
#         else:
#             return {
#                 "status": "error",
#                 "error_message": f"API error with status code {response.status_code}."
#             }
#     except Exception as e:
#         return {
#             "status": "error",
#             "error_message": f"Exception occurred: {str(e)}"
#         }



# def get_ticker_name(name:str)->dict:
#     """
#     Converts a company name to its ticker symbol.

#     Args:
#         name (str): Company name (e.g., "apple")

#     Returns:
#         dict: {'ticker_symbol': 'AAPL'} or {'status': 'error', ...}
#     """


    

def get_finance_data(ticker_symbol:str): 

    try:
        ticker = yf.Ticker(ticker_symbol)
        historical_data = ticker.history(period="1y")
        financials = ticker.financials

        historical_dict = {
            str(k): v for k, v in historical_data.tail(5)["Close"].to_dict().items()
        }

        financials_dict = {
            str(row): {str(k): v for k, v in financials.loc[row].to_dict().items()}
            for row in financials.index
        }

        report = {
            "last_5_days_close_prices": historical_dict,
            "financials": financials_dict
        }

        report_str = json.dumps(report, indent=4)
        return {
            "status": "success",
            "report": report_str
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to fetch data for {ticker_symbol}: {str(e)}"
        }
    

# Define the root agent
root_agent = Agent(
    name="finance_agent",
    model="gemini-1.5-flash",
    description="Agent to fetch data.",
    instruction="You are a helpful agent that fetches financial data about a company. When given a company name (e.g., Apple), infer its ticker symbol (e.g., AAPL), and use `get_finance_data` with that ticker.",
    tools=[get_finance_data]
)
