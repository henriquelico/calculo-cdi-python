import requests
from math import prod

def fetch_daily_cdi():
    """
    Fetch the latest daily CDI value from the BCB open data endpoint.
    Returns a dictionary with 'data' and 'valor' (annualized %).
    """
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1178/dados/ultimos/1?formato=json"
    response = requests.get(url)
    if response.status_code == 400:
        raise ValueError(f"Invalid request. Please check the API parameters: {url}")
    response.raise_for_status()  # Raise an error if the request failed
    return response.json()[0]  # Get the latest value (single dictionary)

def calculate_monthly_gain(initial_investment, latest_cdi, cdi_usage_percentage, months=1):
    """
    Given a initial_investment and the latest CDI value (annualized rate),
    calculate the estimated gain over the specified number of months assuming consistent daily growth.
    Returns a tuple (final_amount, total_return_percentage).
    
    :param initial_investment: Initial investment amount.
    :param latest_cdi: Latest CDI data containing the annualized rate.
    :param cdi_usage_percentage: The percentage of the CDI to be applied.
    :param months: The number of months to keep the money invested (default is 1).
    """
    # 'valor' is the annualized CDI percentage
    try:
        annual_rate_percent = float(latest_cdi["valor"])  # e.g., 13.65
    except KeyError as e:
        raise KeyError(f"Missing expected key in API response: {e}")
    
    # Adjust the annual rate based on the usage percentage
    adjusted_annual_rate_percent = annual_rate_percent * (cdi_usage_percentage / 100.0)
    
    # Convert to decimal (e.g., 0.1365 for 13.65%)
    annual_rate_decimal = adjusted_annual_rate_percent / 100.0
    
    # Approximate daily effective rate (assuming 252 business days in a year)
    daily_effective_rate = (1 + annual_rate_decimal) ** (1/252) - 1
    
    # Calculate total growth factor for the specified number of months
    business_days = months * 21  # Assuming 21 business days per month
    total_growth_factor = (1 + daily_effective_rate) ** business_days
    
    # The final return over the period
    total_return_decimal = total_growth_factor - 1
    
    final_amount = initial_investment * (1 + total_return_decimal)
    return final_amount, total_return_decimal * 100.0  # return % as well


def main():
    # Example: Calculate the monthly gain using the latest CDI value
    initial_investment = 150000.00  # let's say we invest R$ 30,000
    cdi_usage_percentage = 100.0  # Use the % of the CDI value
    months = 6
    
    try:
        # 1) Fetch the latest CDI data
        latest_cdi = fetch_daily_cdi()
        
        # 2) Calculate gains
        final_amount, monthly_return_percent = calculate_monthly_gain(initial_investment, latest_cdi, cdi_usage_percentage, months)
        
        print(f"Inicial investment: R$ {initial_investment:,.2f}")
        print(f"Final amount after ~{months * 21} business days ( or {months} month(s) ): R$ {final_amount:,.2f}")
        print(f"Approx. return: {monthly_return_percent:.2f}%")
        print(f"CDI Usage: {cdi_usage_percentage:.1f}%")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except KeyError as ke:
        print(f"KeyError: {ke}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
