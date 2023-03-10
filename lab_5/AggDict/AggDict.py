import matplotlib.pyplot as plt
import plotly.express as plex
from typing import Any
from typing import Callable

def aggDict(dict_list, common_key):
    # Aggregate a list of dictionaries by one of their common keys.

    # Arguments:
    # 
    # dict_list -- A list of dicts; all dicts must include
    # at least one common key.
    # 
    # commmon_key -- The key by which to aggregate the list of
    # dictionaries; all dicts in dict_list must contain common_key.

    # Returns: dict: {each unique value corresponding to common_key :
    # [matching dicts from list_dict]} -- Aggregated dictionary. Keys
    # are the set of unique values of common_key. Values are lists of
    # all the dicts in list_dict that match each value of common_key.

    agg_dict = {}

    # create a set of all the unique values corresponding to common_key
    common_key_values = {listed_dict[common_key] for listed_dict in dict_list}

    # initialize dictionary with unique values as keys and empty lists as values
    agg_dict = {common_key_value: [] for common_key_value in common_key_values}

    # update the values for each key in the dict
    for listed_dict in dict_list:
        # append the properties dict of the current county to the value of the appropriate agg_dict key
        agg_dict[listed_dict[common_key]].append(listed_dict)

    return agg_dict

def frequentValues(agg_dict, n):
    # Returns a sorted list of the n keys in an aggregated dictionary
    # that correspond to the largest values.

    # Arguments:
    # agg_dict -- An aggregated dictionary; see aggDict().
    # n -- number of keys to return; -1 returns all keys

    # Returns: list[n keys of agg_dict corresponding to the longest
    # values]: A list of keys sorted in descending order by length of
    # value list corresponding to each key.

    # cap n at the length of the dictionary, and set to full length if n=-1
    if n > len(agg_dict) or n == -1:
        n = len(agg_dict)

    # Make a 2D array holding the n most common values and the number
    # of counties for each value This array will update as we search
    # the dict
    frequent_values = [[None, 0] for i in range(n)]

    for key in agg_dict:
        # calculate the number of counties in the current key of the aggregated dictionary
        value_count = len(agg_dict[key])

        frequent_values_counts = [
            frequent_value[1] for frequent_value in frequent_values
        ]

        if value_count > min(frequent_values_counts):
            index = frequent_values_counts.index(min(frequent_values_counts))
            frequent_values[index] = [key, value_count]

    sorted_frequent_values = sorted(
        frequent_values, key=lambda row: row[1], reverse=True
    )
    sorted_frequent_values_keys = [key[0] for key in sorted_frequent_values]

    return sorted_frequent_values_keys

def aggDictPlot(agg_dict, x_title, n=10, save=False, xAlias=lambda x: x):
    # Shows (and optionally saves) the frequency of occurences in an aggregated dict.

    # Arguments:
    # agg_dict: The aggregated dictionary to plot (see aggDict())
    # x_title: The title of the x-axis.
    # n: The number of keys of the aggregated dictionary to plot; the
    # top n most frequent keys will be plotted.
    # save: If true, plot will be saved to .png file.
    # xAlias: Optional function for providing alternate names for the
    # x labels (e.g. state names instead of state codes)

    plt.close()  # closes previous figures if any are open; avoids
    # data from multiple function calls being combined into single
    # figure, but maybe there's a better way

    # isSubset is true if n is set to plot only a subset of the key
    # values in agg_dict
    isSubset = n < len(agg_dict)

    if isSubset:
        keys_to_plot = frequentValues(agg_dict, n)
    else:
        # returns all keys sorted by frequency
        keys_to_plot = frequentValues(agg_dict, -1)

    frequencies = [len(agg_dict[key]) for key in keys_to_plot]

    # set title of plot
    if isSubset:
        title = f"Top {n} Most Frequent Values of {titleLabelStyle(x_title)}"
    else:
        title = f"Frequency of All Unique Values of {titleLabelStyle(x_title)}"

    keys_to_plot_alias = [xAlias(key) for key in keys_to_plot]

    # make plot
    plt.bar(keys_to_plot_alias, frequencies)
    plt.title(title)
    plt.xlabel(x_title.title())  # Title case for x title
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Frequency")

    # save or show plot
    if save:
        # replace spaces and slashes for filename
        filename = filenameStyle(title)
        plt.savefig(f"{filename}.png", bbox_inches="tight", pad_inches=0.5)
    else:
        plt.show()
        
def aggDictPie(agg_dict: dict, nameAlias: Callable[[Any], Any] = lambda x: x):
    """Pie chart of aggDict using plotly."""

    pie_data: dict = {nameAlias(k): len(v) for (k, v) in agg_dict.items()}
    plot_dict = {"names": pie_data.keys(), "quantity": pie_data.values()}
    pie = plex.pie(plot_dict, names="names", values="quantity", hole=0.2, labels=False)
    return pie
        
# Capitalization rules for the plot title
def titleLabelStyle(title_label):
    if title_label.isupper():
        return title_label
    else:
        return title_label.title()


# Formatting rules for filename
def filenameStyle(title_label):
    return title_label.title().replace(" ", "_").replace("/", "-").replace("\\", "-")
