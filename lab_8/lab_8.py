import geopandas as gpd
import os
import ast
import pandas as pd
import matplotlib.pyplot as plt

wd = os.getcwd()
counties_path = "gz_2010_us_050_00_20m.geojson"
fips_path = "fipsToState.json"
data_dir = os.path.join(wd, "data")

gdf_counties = gpd.read_file(os.path.join(data_dir, counties_path))

fips_file = open(os.path.join(data_dir, fips_path), "r")
fips_string = fips_file.read().replace("\n", "")
state_code_dict = ast.literal_eval(fips_string)

df_state_codes = pd.DataFrame(
    {"STATE": state_code_dict.keys(), "state_name": state_code_dict.values()}
)

gdf_counties = pd.merge(gdf_counties, df_state_codes, how="left", on="STATE")


def counts(df, col):
    """Returns a dataframe with counts for each value of col."""
    first_col_name = df.columns[0]
    counts = df.groupby(by=col).count()[first_col_name].rename("Counts")
    return counts


def n_most_frequent(df, col, n):
    """Returns a dict of the n largest values of n in the dataframe df."""
    top_n = counts(df, col).nlargest(n)
    return top_n


def summarize_df(df, group_col, val_col):
    """"""
    groups = df.groupby(group_col)
    summary = pd.DataFrame(
        {
            # "state": groups.any("state_name"),
            "max": groups.max(val_col)[val_col],
            "min": groups.min(val_col)[val_col],
            "mean": groups.mean(val_col)[val_col],
            "sum": groups.sum(val_col)[val_col],
            "count": groups.count()[val_col],
        }
    )
    return summary


county_areas_by_state = summarize_df(gdf_counties, "state_name", "CENSUSAREA")

print(n_most_frequent(gdf_counties, "NAME", 5))
print(gdf_counties.groupby("STATE").mean("CENSUSAREA"))

fig, ax = plt.subplots()
ax.set_aspect("equal")

frequent_counties = n_most_frequent(gdf_counties, "NAME", 5)

# Drop Hawaii, Alaska, and Puerto Rico to facilitate plotting
df_plot = gdf_counties[
    (gdf_counties["state_name"] != "Hawaii")
    & (gdf_counties["state_name"] != "Alaska")
    & (gdf_counties["STATE"] != "72")
]

# Plot base layer
df_plot.plot(ax=ax, color="white", edgecolor="black", linewidth=0.1)

# Build query string
query_string = " | ".join(
    ["NAME == " + f"'{county}'" for county in frequent_counties.index]
)

# Filter GeoDataFrame to counties of interest with query string
df_plot = gdf_counties.query(query_string)

# Merge counts into plotting GeoDataFrame
df_plot = pd.merge(
    df_plot, pd.DataFrame(frequent_counties), how="left", on="NAME", copy=False
)
# Convert Counts column to string
df_plot.Counts = df_plot.Counts.astype(str)
# Create new column for legend labels that includes counts
df_plot = df_plot.assign(legend_labels=lambda df: df.NAME + " (" + df.Counts + ")")
# Plot GeoDataFrame and color by county name
df_plot.plot(ax=ax, column="legend_labels", legend=True)

plt.show()
plt.close()
