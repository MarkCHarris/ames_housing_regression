############# DEPENDENCIES ##############

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

############# SHORTCUTS FOR VERY COMMON GRAPHS ##############

def quick_hist(data, bins=None):
    
    """
    Accepts an np.series and a number of bins, then graphs a histogram with title based on the name of the series.
    bins (default == None) sets the number of bins as per plt.hist.
    """
    
    plt.figure(figsize=(20,5))
    plt.hist(data, bins=bins)
    plt.title(f'Histogram of {data.name}', fontsize='x-large');

def quick_scatter(x_col, y_col):
    
    """
    Accepts two np.series and then graphs a scatterplot with x_col on the x-axis and y_col on the y-axis.
    Axis labels are automatically generated based on the names of the input series.
    """
    
    plt.figure(figsize=(20,5))
    plt.scatter(x_col, y_col)
    plt.xlabel(f'{x_col.name}', fontsize='x-large')
    plt.ylabel(f'{y_col.name}', fontsize='x-large')
    plt.title(f'{y_col.name} vs {x_col.name}', fontsize='x-large');

def quick_bar(target_col, group_col):
    
    """
    Accepts two np.series.  Data will be split into a group for each value in group_col.
    The mean of target_col is calculated for each group, and the mean for each group is plotted on a bar graph.
    Axis labels are automatically generated based on the names of the input series.
    """
    
    target_by_group = target_col.groupby(group_col).mean()
    plt.figure(figsize=(20,5))
    plt.bar(target_by_group.index, target_by_group)
    plt.xlabel(f'{group_col.name}', fontsize='x-large')
    plt.ylabel(f'{target_col.name}', fontsize='x-large')
    plt.title(f'mean {target_col.name} by {group_col.name}', fontsize='x-large');
    
############# TOOLS FOR MULTIPLE QUICK GRAPHS ##############

def multi_scatter(df, y_axis, row_size=2, width=16, height=None):

    """
    This function accepts a dataframe, then sets up a grid and plots scatter plots of every numeric column vs. the y-axis.
    
    df = dataframe for which each numeric feature will be plotted.
    y_axis (string) = name of the column that will be on the y-axis of each plot.
    row_size (default == 2) = number of subplots to display on each row.
    width (default == 16) = total width of the figure.
    height = (default ==  None) = total height of the figure.
    If height == None, height will be set to 4 times the number of rows needed to display all graphs.
    """
    
    # Select only numeric features and leave out the feature that will be on the y-axis of each plot.
    df_num = df._get_numeric_data()
    df_num.drop(y_axis, axis=1, inplace=True)

    # Determine number of rows needed to accommodate all numeric columns in the grid.
    col_size = (len(df_num.columns) // row_size)
    if len(df_num.columns) % row_size != 0:
        col_size += 1

    # Set the default height based on number of rows that will be needed.
    if height == None:
        height = col_size * 4
    
    # Create the grid using the height and width parameters.
    fig, axs = plt.subplots(col_size, row_size, figsize = (width, height))
    # Flatten the grid into a single array for easier iteration.
    ax = axs.flatten()

    # Keep track of position in the grid as plots are filled.
    plot_count = 0

    # Increment through each numeric column except y-axis.
    for col in df_num.columns:
        
        # Fill the graph and create axis labels and title.
        ax[plot_count].scatter(df[col], df[y_axis])
        ax[plot_count].set_title(f'{y_axis} vs. {col}', fontsize='x-large');

        # Increments position in the grid once graph is complete.
        plot_count += 1

def multi_bar_target_mean(df, target_col, row_size=2, width=16, height=None):
    
    """
    This function accepts a dataframe, then sets up a grid and plots bar graphs of every column vs. the target column.
    For each bar graph, the target column is grouped by each value in the non-target column and then the mean is calculated to determine bar heights.
    The number of values that were averaged to the find the height of each bar is displayed as a number above the bar.
    
    df = dataframe for which each feature will be plotted.
    target_col (string) = name of the column that will be grouped and averaged to determine the height of each bar.
    row_size (default == 2) = number of subplots to display on each row.
    width (default == 16) = total width of the figure.
    height = (default == None) = total height of the figure.
    If height == None, height will be set to 6 times the number of rows needed to display all graphs.
    
    I learned about .groupby().size() here:
    https://datascienceparichay.com/article/pandas-groupby-count-of-rows-in-each-group/
    
    I learned about the bar_label() function from the following sources:
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_label_demo.html
    https://discourse.matplotlib.org/t/axessubplot-object-has-no-attribute-bar-label/21985
    """
    
    # Determine number of rows needed to accommodate all numeric columns in the grid.
    col_size = ((len(df.columns)-1) // row_size )
    if (len(df.columns)-1) % row_size != 0:
        col_size += 1
        
    # Set the default height based on number of rows that will be needed.
    if height == None:
        height = col_size * 6
    
    # Create the grid using the height and width parameters.
    fig, axs = plt.subplots(col_size, row_size, figsize = (width, height))
    # Flatten the grid into a single array for easier iteration.
    ax = axs.flatten()

    # Keep track of position in the grid as plots are filled.
    plot_count = 0
    # List of all columns except the target.
    cols = df.columns.drop(target_col)
    
    # Increment through each columns except the target.
    for col in cols:
        
        # Fill the graph and create axis labels and title.
        target_by_group = df[target_col].groupby(df[col]).mean()
        plot = ax[plot_count].bar(target_by_group.index, target_by_group)
        ax[plot_count].set_title(f'mean {target_col} by {col}', fontsize='x-large')
        ax[plot_count].bar_label(plot, df[col].groupby(df[col]).size());
        
        # Increments position in the grid once graph is complete.
        plot_count += 1
