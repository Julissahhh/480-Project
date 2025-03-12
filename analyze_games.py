import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the simulation results
file_path = "strat_comparisons.csv"  # Ensure this matches where `game.py` saves results
df = pd.read_csv(file_path)

# Compute win, loss, and push percentages
df["Win %"] = df["Wins"] / (df["Wins"] + df["Losses"] + df["Pushes"])
df["Loss %"] = df["Losses"] / (df["Wins"] + df["Losses"] + df["Pushes"])
df["Push %"] = df["Pushes"] / (df["Wins"] + df["Losses"] + df["Pushes"])

# Compute statistics per strategy
grouped = df.groupby("Strategy").agg(
    Mean_Total_Profit=("Total Profit", "mean"),
#    Median_Total_Profit=("Total Profit", "median"),
#    Std_Total_Profit=("Total Profit", "std"),
#    Min_Total_Profit=("Total Profit", "min"),
#    Max_Total_Profit=("Total Profit", "max"),
    Mean_Final_Bankroll=("Final Bankroll", "mean"),
#    Median_Final_Bankroll=("Final Bankroll", "median"),
#   Std_Final_Bankroll=("Final Bankroll", "std"),
#    Min_Final_Bankroll=("Final Bankroll", "min"),
#    Max_Final_Bankroll=("Final Bankroll", "max"),
    Mean_Profit_Per_Round=("Avg Profit/Round", "mean"),
#    Std_Profit_Per_Round=("Avg Profit/Round", "std")
)

# Compute probability of ruin (final bankroll < $1,000)
broke_agents_count = df[df["Final Bankroll"] < 1000].groupby("Strategy").size()
broke_agents_proportion = (broke_agents_count / df.groupby("Strategy").size()).round(3)
# Compute net profit/loss per strategy (total money won/lost by the casino)
net_profit_loss = df.groupby("Strategy")["Total Profit"].sum().round(2)

broke_stats = pd.DataFrame(
    {"Broke Agents Count": broke_agents_count, "Broke Agents Proportion": broke_agents_proportion, "Net Profit/Loss": net_profit_loss})

# Save statistics to CSV for reference
grouped.to_csv("Blackjack_strategy_stats.csv")
broke_stats.to_csv("Broke_agents_stats.csv")

# Display stats in console
print("Blackjack Strategy Statistics:\n", grouped)
print("\nAgents Who Went Broke:\n", broke_stats)

# Generate histograms and box plots
metrics = {
    "Win %": df["Win %"],
    "Push %": df["Push %"],
#    "Loss %": df["Loss %"],
    "Profit per Hand": df["Avg Profit/Round"],
#    "Final Bankroll": df["Final Bankroll"],
}

def get_plot_limits(data, low=0.05, high=99.9):
    """Returns x-axis limits based on percentiles to filter out extreme outliers."""
    return data.quantile(low / 100), data.quantile(high / 100)

fig, axes = plt.subplots(len(metrics), 2, figsize=(14, 20))
fig.suptitle("Blackjack Strategy Performance Metrics", fontsize=16)

for i, (title, data) in enumerate(metrics.items()):
    x_min, x_max = get_plot_limits(data)
    # Histogram
    sns.histplot(data=df, x=data, hue="Strategy", bins=30, kde=True, ax=axes[i, 0])
    axes[i, 0].set_xlim(x_min, x_max)  # Apply the adjusted scale
    axes[i, 0].set_title(f"{title} Histogram")

    # Box plot
    sns.boxplot(data=df, x="Strategy", y=data, ax=axes[i, 1])
    axes[i, 1].set_ylim(x_min, x_max)  # Apply the adjusted scale
    axes[i, 1].set_title(f"{title} Box Plot")

plt.tight_layout(rect=(0, 0, 1, 0.96))
plt.show()
