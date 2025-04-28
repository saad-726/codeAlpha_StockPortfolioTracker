import yfinance as yf

class StockPortfolio:
    def __init__(self):
        self.portfolio = {}  # { 'AAPL': {'shares': 10, 'buy_price': 150} }

    def add_stock(self, symbol, shares, buy_price):
        symbol = symbol.upper()
        if symbol in self.portfolio:
            self.portfolio[symbol]['shares'] += shares
            # Average the buy price
            self.portfolio[symbol]['buy_price'] = (
                (self.portfolio[symbol]['buy_price'] + buy_price) / 2
            )
        else:
            self.portfolio[symbol] = {'shares': shares, 'buy_price': buy_price}
        print(f"Added {shares} shares of {symbol} at ${buy_price} each.")

    def remove_stock(self, symbol):
        symbol = symbol.upper()
        if symbol in self.portfolio:
            del self.portfolio[symbol]
            print(f"Removed {symbol} from portfolio.")
        else:
            print(f"{symbol} not found in portfolio.")

    def get_current_price(self, symbol):
        symbol = symbol.upper()
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")
            if not data.empty:
                return data['Close'].iloc[-1]
            else:
                print(f"No data found for {symbol}")
                return None
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def track_portfolio(self):
        total_investment = 0
        total_current_value = 0

        print("\n--- Portfolio Summary ---")
        for symbol, details in self.portfolio.items():
            shares = details['shares']
            buy_price = details['buy_price']
            current_price = self.get_current_price(symbol)

            if current_price:
                investment = shares * buy_price
                current_value = shares * current_price
                profit_loss = current_value - investment
                profit_loss_percent = (profit_loss / investment) * 100

                total_investment += investment
                total_current_value += current_value

                print(f"\n{symbol}:")
                print(f"  Shares Owned: {shares}")
                print(f"  Buy Price: ${buy_price:.2f}")
                print(f"  Current Price: ${current_price:.2f}")
                print(f"  Investment: ${investment:.2f}")
                print(f"  Current Value: ${current_value:.2f}")
                print(f"  P/L: ${profit_loss:.2f} ({profit_loss_percent:.2f}%)")

        total_profit_loss = total_current_value - total_investment
        total_profit_loss_percent = (total_profit_loss / total_investment) * 100 if total_investment else 0

        print("\n--- Overall Portfolio ---")
        print(f"Total Investment: ${total_investment:.2f}")
        print(f"Total Current Value: ${total_current_value:.2f}")
        print(f"Total P/L: ${total_profit_loss:.2f} ({total_profit_loss_percent:.2f}%)\n")

def main():
    portfolio = StockPortfolio()

    while True:
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Track Portfolio")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol (e.g., AAPL): ")
            shares = int(input("Enter number of shares: "))
            buy_price = float(input("Enter buy price per share: "))
            portfolio.add_stock(symbol, shares, buy_price)

        elif choice == '2':
            symbol = input("Enter stock symbol to remove: ")
            portfolio.remove_stock(symbol)

        elif choice == '3':
            portfolio.track_portfolio()

        elif choice == '4':
            print("Exiting Portfolio Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

