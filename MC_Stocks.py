import yfinance as yf
import datetime

ticker = 'TSLA'
print(datetime.datetime.now())
def get_stock_prices(ticker_symbol):
    # Get today's date
    end_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')

    # Calculate the date 5 years ago from today
    start_date = (datetime.datetime.now() - datetime.timedelta(days=10*365)).strftime('%Y-%m-%d')

    try:
        # Fetch historical data for stock from Yahoo Finance
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

        # Extract the 'Close' prices from the fetched data
        closing_prices = stock_data['Close'].values
        return closing_prices

    except Exception as e:
        print("Error occurred:", e)
        return None
def get_current_prices(ticker_symbol):
    # Get today's date
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Calculate the date 5 years ago from today
    start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')

    try:
        # Fetch historical data for stock from Yahoo Finance
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

        # Extract the 'Close' prices from the fetched data
        closing_prices = stock_data['Close'].values

        return closing_prices, stock_data.index

    except Exception as e:
        print("Error occurred:", e)
        return None

prices_last_5_years = get_stock_prices(ticker)
current, index_dates = get_current_prices(ticker)

if prices_last_5_years is not None:
    print(f"Number of days of data:")
    print(len(prices_last_5_years))

import numpy as np
import matplotlib.pyplot as plt

# Define historical stock prices
historical_prices = prices_last_5_years

# Define parameters for simulation
num_simulations = 1000
num_days = 252

# Calculate daily returns
returns = np.log(1+np.diff(historical_prices) / historical_prices[:-1])

mu, sigma = returns.mean(), returns.std()

# Generate simulations
simulations = []
for _ in range(num_simulations):
    prices = [historical_prices[-1]]
    mc_returns = np.random.normal(mu, sigma, num_days)
    new_prices = prices * (1 + mc_returns).cumprod()
    simulations.append(new_prices)

# Initialize a counter for the number of simulations where stock price is above 200
count_above = 0

# Define the threshold price
threshold_price = historical_prices[-1]

# Iterate through each simulation
for sim in simulations:
    # Check if the final stock price in the simulation is above 200
    if sim[-1] > threshold_price:
        count_above += 1

# Calculate the probability
probability_above = count_above / num_simulations

simulations_mean = np.mean(simulations, axis=0)

print()
print(f"Probability that {ticker} stock price is above {threshold_price} in Monte Carlo simulation:", probability_above)
print()
print(f"Forecasted today's price: ", simulations_mean[-1])

# Plot simulations

#Adding parameter information as a sidebox
info_text = f"""
Ticker: {ticker}
Actual Annualized Return: {(current[-1]/threshold_price - 1) * 100}%
Expected Annualized Return: {(simulations_mean[-1]/threshold_price - 1) * 100}%
"""
plt.figure(figsize=(20, 10))
plt.text(0.75, 0.95, info_text, transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', alpha=0.5))
for sim in simulations:
    plt.plot(index_dates[0:250], sim[0:250])
plt.plot(index_dates[0:250], simulations_mean[0:250],linewidth=3, label=f'Mean along MC simulations ending {simulations_mean[-1]}', color='red')
plt.plot(index_dates[0:250], current[0:250], linewidth=3, label=f'Actual prices for the last year ending {current[-1]}', color='black')
plt.axhline(y=threshold_price, color='blue', linestyle='--', label=f'Threshold (${threshold_price})')
plt.xlabel('Days')
plt.ylabel('Stock Price')
plt.title(f'Monte Carlo Simulation: {ticker} Stock Price Prediction')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()