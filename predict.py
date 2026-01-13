from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df=pd.read_csv("C:/Users/ranab/OneDrive/Desktop/Arbitrage Hunter/cleaned_laptop_data.csv")
regressor=LinearRegression()

X=df[["Ram(GBs)"]]

y=df["Price"]

regressor.fit(X,y)

print(f"Regresson Score:{regressor.score(X,y)}")

df['Predicted_Price'] = regressor.predict(X)

df['Arbitrage'] = df['Predicted_Price'] - df['Price']

deals = df[ (df['Arbitrage'] > 10000) & (df['Arbitrage'] < 100000) ]
deals = deals.sort_values(by='Arbitrage', ascending=False)

print(f"Found {len(deals)} potential arbitrage opportunities.\n")
print(deals[['Title', 'Price', 'Predicted_Price', 'Arbitrage']].head(10).to_string(index=False))

deals[['Title', 'Price', 'Predicted_Price', 'Arbitrage']].to_csv("final_arbitrage_list.csv", index=False)

plt.figure(figsize=(12, 8))

# 1. Create the Regression Plot
# sns.regplot fits a linear model and plots it with a confidence interval
sns.regplot(x=df['Price'], y=df['Predicted_Price'], 
            scatter_kws={'alpha': 0.5, 's': 60, 'color': '#1f77b4'}, 
            line_kws={'color': '#d62728', 'linewidth': 2, 'label': 'Market Trend'})

# 2. Add the "Perfect Value" Reference Line (x=y)
# This helps your eye instantly spot the "Above Average" deals
min_val = min(df['Price'].min(), df['Predicted_Price'].min())
max_val = max(df['Price'].max(), df['Predicted_Price'].max())
plt.plot([min_val, max_val], [min_val, max_val], 
         color='green', linestyle='--', linewidth=2, label='Fair Value (x=y)')

# 3. Labeling
plt.title('Arbitrage Hunter: Actual vs. Predicted Price', fontsize=18, fontweight='bold')
plt.xlabel('Listing Price (What you Pay) ₹', fontsize=14)
plt.ylabel('Predicted Value (What you Get) ₹', fontsize=14)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)

# 4. Show the plot
plt.show()