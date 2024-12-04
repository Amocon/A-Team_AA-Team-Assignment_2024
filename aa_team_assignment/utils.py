from typing import Optional

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import Timestamp, DataFrame


def plot_histogram(ax, season_df: pd.DataFrame, year: str = None) -> None:
    """
    Helper function to plot a histogram for a single year's data on a given axis.
    """
    # Determine the minimum and maximum month numbers present in the DataFrame
    min_month = season_df['connectionMonth'].min()
    max_month = season_df['connectionMonth'].max()

    # Calculate the number of bins dynamically based on the range of months
    month_bins = max_month - min_month + 1

    # Plotting histogram
    counts, bins, patches = ax.hist(
        season_df['connectionMonth'], bins=month_bins, edgecolor='black',
        rwidth=0.8, range=(min_month - 0.5, max_month + 0.5)
    )

    # Configure the plot
    if year:
        ax.set_title(f"Year {year}")
    ax.set_xlabel('Month')
    ax.set_ylabel('Frequency')

    # Set x-ticks centered under each bar
    ax.set_xticks(np.arange(min_month, max_month + 1))
    ax.set_xticklabels(
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][min_month - 1:max_month]
    )

    ax.grid(axis='y', linestyle='--', alpha=0.7)


def plot_hist(dfs_by_year: dict = None, season_df: pd.DataFrame = None, title: str = "") -> None:
    """
    Plots a histogram for either multiple years (dfs_by_year) or a single year's data (season_df).
    """
    if dfs_by_year:
        num_years = len(dfs_by_year)
        fig, axes = plt.subplots(1, num_years, figsize=(15, 5), sharey=True)
        fig.suptitle(title)

        # Ensure axes is iterable for single subplot case
        if num_years == 1:
            axes = [axes]

        for i, (year, df) in enumerate(dfs_by_year.items()):
            plot_histogram(axes[i], df, year)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout to fit title
        plt.show()
    elif season_df is not None:
        fig, ax = plt.subplots(figsize=(10, 6))
        plot_histogram(ax, season_df)
        plt.title(title)
        plt.tight_layout()
        plt.show()
    else:
        raise ValueError("Provide either 'dfs_by_year' or 'season_df' to plot.")


seasons = pd.read_feather("../data/burbank_seasons.feather")

def get_season(date: Timestamp):

    year = date.year
    # Filter the DataFrame for the desired year
    year_row = seasons[seasons['Year'] == year]

    # Check if the year exists in the DataFrame
    if year_row.empty:
        return None

    # Iterate through each season and check if the date falls in its range
    for season, (start_col, end_col) in {
        'Spring': ('Spring Start', 'Summer Start'),
        'Summer': ('Summer Start', 'Autumn Start'),
        'Autumn': ('Autumn Start', 'Winter Start'),
        'Winter': ('Winter Start', 'Spring Start')  # Handle wrap-around
    }.items():
        start_date = year_row[start_col].iloc[0]
        end_date = year_row[end_col].iloc[0]

        if season == 'Winter':
            if year == 2018 and date < end_date:
                return season
            if year == 2022 and date >= start_date:
                return season
            if date.month == 12:
                # Set start date for winter to the previous year's Winter Start
                end_date = seasons[seasons['Year'] == year + 1].iloc[0][end_col]
            else:
                # Set end date for winter to the next year's Spring Start
                start_date = seasons[seasons['Year'] == year - 1].iloc[0][start_col]

        if start_date <= date < end_date:
            return season
    raise ValueError(f"Date {date} does not fall into any season range")


import pandas as pd

def calculate_seasonal_factors(df, year):
    if 'season' not in df.columns:
        raise ValueError("Das DataFrame muss eine Spalte 'season' enthalten.")

    season_stats = df['season'].value_counts()
    total_records = season_stats.sum()
    average_records = total_records / len(season_stats)
    seasonal_factors = season_stats / average_records

    # Ergebnis in einem DataFrame zusammenfassen
    result = pd.DataFrame({
        'year': year,
        'season': season_stats.index,
        'record_count': season_stats.values,
        'seasonal_factor': seasonal_factors.values
    })

    return result