import json
import os


def get_data_in_range(ticker, start_date, end_date, data_type, data_dir, period=None):
    """
    Gets finnhub data saved and processed on disk.
    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        data_type (str): Type of data from finnhub to fetch. Can be insider_trans, SEC_filings, news_data, insider_senti, or fin_as_reported.
        data_dir (str): Directory where the data is saved.
        period (str): Default to none, if there is a period specified, should be annual or quarterly.
    """

    if period:
        data_path = os.path.join(
            data_dir,
            "finnhub_data",
            data_type,
            f"{ticker}_{period}_data_formatted.json",
        )
    else:
        data_path = os.path.join(
            data_dir, "finnhub_data", data_type, f"{ticker}_data_formatted.json"
        )

    data = open(data_path, "r")
    data = json.load(data)

    # filter keys (date, str in format YYYY-MM-DD) by the date range (str, str in format YYYY-MM-DD)
    filtered_data = {}
    for key, value in data.items():
        if start_date <= key <= end_date and len(value) > 0:
            filtered_data[key] = value
    return filtered_data


def get_finnhub_etf_news(ticker, start_date, end_date, data_dir):
    """Stub helper to fetch ETF-level news from Finnhub cached files.

    The current project stores finnhub data by ticker. ETFs may not be present; this
    helper returns an empty list if no cached file exists. Replace with a live Finnhub
    API call if you have an API key and want real-time ETF data.
    """
    import os

    data_path = os.path.join(data_dir, "finnhub_data", "news_data", f"{ticker}_data_formatted.json")
    if not os.path.exists(data_path):
        return []

    with open(data_path, "r") as fh:
        data = json.load(fh)

    filtered = {k: v for k, v in data.items() if start_date <= k <= end_date}
    return filtered
