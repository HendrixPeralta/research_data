# %%
import pandas as pd
import geopandas as gpd
from geopandas import points_from_xy
import matplotlib as plt
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap

# %%
provinces = gpd.read_file("/Users/hendrixperalta/Desktop/Research Data Manipulation/research_data/adm1/adm1_map/untitled.shp")

# %%
sez = pd.read_csv("/Users/hendrixperalta/Desktop/Research Data Manipulation/research_data/aggregated _data/municipalities/sez_aggregated.csv")

# %%
filtered_sez = sez[sez['latitude'] != 0]


# %%
filtered_sez

# %%
filtered_sez.plot(
    kind='scatter', x="longitude", y="latitude"
)


# %%
provinces.crs

# %%
sez_gdf = gpd.GeoDataFrame(
    filtered_sez, crs = provinces.crs,
    geometry = points_from_xy(
        filtered_sez["longitude"], filtered_sez["latitude"]
    )
)

# %%
sez_gdf.isna().sum()

# %%
#sez_gdf.to_csv("sez_gdf.csv")

# %%
sez_gdf.explore(
    titles = "CartoDB positron",
    cmap = "plasma", 
    style_kwds=dict(color = "black")
)

# %%
#%%timeit
joined = gpd.sjoin(
    sez_gdf,
    provinces,
    how="right",
    predicate="within"
)

# %%
joined.fillna(0, inplace = True)

# %%


# %%
agg_func = {col: "sum" for col in joined.columns}
del agg_func['geometry']

# %%
joined["id"] = pd.to_numeric(joined["id"], errors = "coerce")

# %%
mean_columns = joined.columns[joined.columns.str.contains('sal|id', regex=True)]


# %%
for col in mean_columns:
    if col in agg_func:
        agg_func[col] = "mean"

# %%
types = joined[joined.columns[joined.columns.str.contains('sal|id')]].dtypes

# %%
types.to_csv("types.csv")

# %%


# %%
res_dissolve = joined.dissolve(by="id", aggfunc=agg_func)

# %%
res_dissolve

# %%
provinces.info()

# %%
import matplotlib.pyplot as plt

cmap = LinearSegmentedColormap.from_list("custom_blue_red", ["blue", "red"])

fig, ax = plt.subplots(figsize=(20, 8))

joined.plot(ax=ax, color="lightgrey", alpha=0.5)
            
joined.plot(ax=ax, alpha=0.5, markersize=2, column="ent2015", 
            legend=True, vmin=1, vmax=30)
plt.title("Pickups Colored by Neighborhood", fontsize=20);


# %%
joined.drop(columns = 'geometry').to_csv("joined.csv", index = False)

# %%
res_nogeo = res_dissolve.drop(columns = "geometry")
res_nogeo.to_csv("joined_sez_map.csv", index = False)

# %%


# %%



