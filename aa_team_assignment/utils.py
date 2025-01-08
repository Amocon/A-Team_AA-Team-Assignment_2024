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


def plot_hist_per_year(df: pd.DataFrame, title: str = "") -> None:
    """
    Plots a histogram for either multiple years (dfs_by_year) or a single year's data (season_df).
    """
    dfs_by_year = {year: df[df["connectionYear"] == year] for year in sorted(df["connectionYear"].unique())}
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


def plot_monthly_hist(season_df: pd.DataFrame = None, title: str = "") -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_histogram(ax, season_df)
    plt.title(title)
    plt.tight_layout()
    plt.show()


seasons = pd.read_feather("../data/burbank_seasons.feather")


def get_season_year(date: Timestamp) -> Optional[int]:
    """
    This ensures that the season 'Winter' the year is correctly assigned. By adding the Winter months late in a year to the next year.
    """
    year = date.year
    # Filter the DataFrame for the desired year
    year_row = seasons[seasons['Year'] == year]

    # Check if the year exists in the DataFrame
    if year_row.empty:
        return None

    if date >= year_row['Winter Start'].iloc[0]:
        return year + 1
    else:
        return year


def get_season(date: Timestamp) -> Optional[str]:
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
                # Set end date for winter to the next year's Spring Start
                end_date = seasons[seasons['Year'] == year + 1].iloc[0][end_col]
            else:
                # Set start date for winter to the previous year's Winter Start
                start_date = seasons[seasons['Year'] == year - 1].iloc[0][start_col]

        if start_date <= date < end_date:
            return season
    raise ValueError(f"Date {date} does not fall into any season range")


def calculate_seasonal_factors(df, year):
    if 'season' not in df.columns:
        raise ValueError("Das DataFrame muss eine Spalte 'season' enthalten.")

    season_order = ['Winter', 'Spring', 'Summer', 'Autumn']
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
    }).sort_values('season')
    result['season'] = pd.Categorical(result['season'], categories=season_order, ordered=True)
    return result


def calculate_weekday_season_factors(df, weekday_column, year):
    if weekday_column not in df.columns:
        raise ValueError(f"The DataFrame must contain the column '{weekday_column}'.")

    # Calculate the value counts for each weekday
    weekday_counts = df[weekday_column].value_counts()

    # Calculate the total records and the average records per weekday
    total_records = weekday_counts.sum()
    average_records = total_records / len(weekday_counts)

    # Calculate seasonal factors (relative occurrence to the average)
    seasonal_factors = weekday_counts / average_records

    # Create a DataFrame with the results
    result = pd.DataFrame({
        'weekday': weekday_counts.index,
        'record_count': weekday_counts.values,
        'seasonal_factor': seasonal_factors.values,
        'year': year
    })

    # Sort by weekday name (Monday to Sunday)
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    result['weekday'] = pd.Categorical(result['weekday'], categories=weekday_order, ordered=True)
    result = result.sort_values('weekday')

    return result


def calculate_range(user_inputs, column, date_format="%a, %d %b %Y %H:%M:%S GMT"):
    """
    Calculate the range (max - min) of values for a specified column from a list of user inputs.

    Parameters:
        user_inputs (list of dict): A list of dictionaries where the values are the inputs provided by the user.
        column (str): The key for which the range is to be calculated.
        date_format (str, optional): The date format string for the column if the column contains date strings.

    Returns:
        float: The range (max - min) of the values in the specified column.
    """
    values = [input_data[column] for input_data in user_inputs if column in input_data]
    if len(values) > 1:
        # If numeric, calculate range as max - min
        if isinstance(values[0], (int, float)):
            return max(values) - min(values)
        # If string, attempt to convert to datetime and calculate the range
        elif isinstance(values[0], str):
            values = pd.to_datetime(values, format=date_format, errors='coerce')
            values = values.dropna()
            if len(values) > 1:
                return values.max() - values.min()
            else:
                return pd.Timedelta(0)
    return 0


def plot_top_n_distribution(df, input_count, column_for_distribution, top_n=10):
    """
    Filters the DataFrame based on input_count and plots the top n categories of the specified column.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        input_count (int): The value of 'inputCount' to filter rows.
        column_for_distribution (str): The column to calculate and plot the distribution.
        top_n (int): Number of top categories to display.

    Returns:
        pd.Series: The top N distribution of the specified column, sorted by index.
    """

    # Filter the DataFrame
    filtered_df = df[df["inputCount"] == input_count]

    # Calculate the distribution and get the top N categories
    distribution = filtered_df[column_for_distribution].value_counts().nlargest(top_n).sort_index()

    # Plot the distribution
    plt.figure(figsize=(10, 6))
    distribution.plot(kind="bar")
    plt.title(f"Top {top_n} {column_for_distribution} for inputCount = {input_count}")
    plt.xlabel(column_for_distribution)
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()