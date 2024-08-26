# %%
import pandas as pd

import geopandas as gpd
from geopandas import points_from_xy

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap

import mapclassify
import pygeoda

# %%
# Read geospatial data
geo_municipalities = gpd.read_file("adm2/map_files/adm2_shp.shp")
# sez_data = pd.read_csv("aggregated_data/provinces/01_exports/sez_province_map.csv")
sez_location = gpd.read_file("aggregated_data/provinces/01_exports/sez_gdf.shp")

sez_location_2000 = gpd.read_file("sez_location/sez_2000/sez_2000.shp")
sez_location_2005 = gpd.read_file("sez_location/sez_2005/sez_2005.shp")
sez_location_2010 = gpd.read_file("sez_location/sez_2010/sez_2010.shp")
sez_location_2015 = gpd.read_file("sez_location/sez_2015/sez_2015.shp")
sez_location_2020 = gpd.read_file("sez_location/sez_2020/sez_2020.shp")

# %%
# Read and manipulation of the population data/
# pop = pd.read_csv("/Users/hendrixperalta/Desktop/Research Data Manipulation/research_data/adm1/population/p_landscan_pop.csv")
# pop.rename(columns = {"asdf_id" : "id"}, inplace=True)
# column_filter = pop[pop.columns[pop.columns.str.contains("land")]]

# for col in column_filter:
#     new_name = "pop" + col.split(".", 1)[1]
#     pop.rename(columns = {col : new_name}, inplace = True)

# pop_sum = pop[pop.columns[pop.columns.str.contains("sum|id")]]
# pop_sum.columns = pop_sum.columns.str.replace(".sum$", "", regex=True)

#pop_sum.dtypes

# %%
# Read and manipulation of the temperature data
# temp = pd.read_csv("/Users/hendrixperalta/Desktop/Research Data Manipulation/research_data/adm1/temperature/p_landsurface_temp.csv")
# temp.rename(columns = {"asdf_id" : "id"}, inplace=True)
# temp_filter = temp[temp.columns[temp.columns.str.contains("mod11c3_061")]]
# temp_filter = temp_filter[temp_filter.columns[temp_filter.columns.str.contains(".mean.1")]]

# for col in temp_filter: 
#     new_name = "temp" + col.split(".", 1)[1]
#     temp.rename(columns = {col : new_name}, inplace=True)

# temp.columns = temp.columns.str.replace(".mean.1", "", regex=True)
# temp = temp[temp.columns[temp.columns.str.contains("temp|id")]]
# temp.columns

# %%
# Read and manipulation of the Agriculture land cover data
# agri = pd.read_csv("/Users/hendrixperalta/Desktop/Research Data Manipulation/research_data/adm1/landcover/agriculture_land_wide_adm1.csv")
# agri.rename(columns = {"provinceCode" : "id"}, inplace=True)
# agri = agri[agri.columns[agri.columns.str.contains("agr|id")]]
# agri.columns

# %%
# Read and manupulation of the Urban land cover data
# urba = pd.read_csv("/Users/hendrixperalta/Desktop/Research Data Manipulation/research_data/adm1/landcover/urban_land_wide_adm1.csv")
# urba.rename(columns = {"provinceCode" : "id"}, inplace=True)
# urba = urba[urba.columns[urba.columns.str.contains("urb|id")]]
# urba.columns

# %%
# Read and manipulation of the NPP NTL data 
ntl = pd.read_csv("adm2/ntl/ntl_sum_wide_00-22.csv")
ntl = ntl[ntl.columns[ntl.columns.str.contains("ntl|id")]]
ntl.columns

# %%
# Read and manipulation of the Electricity consumption revised GDP 
# egdp = pd.read_csv("/Users/hendrixperalta/Desktop/Research Data Manipulation/research_data/adm1/ntl/egdp_sum_wide_00-16.csv")
# egdp = egdp[egdp.columns[egdp.columns.str.contains("egdp|id")]]
#egdp.columns


# %%
# Unifies the different datasets 
# datasets = [temp, agri, urba, ntl, egdp, edu, health, soci]
# municipality_data = pd.merge(sez_data, pop_sum[pop_sum.columns[pop_sum.columns.str.contains("pop|id")]], on="id", how="outer")

# for dataset in datasets: 
#     municipality_data = pd.merge(municipality_data, dataset, on="id", how= "outer")


# # Filters out the years from 2017 to 2022

# filter_year = ["2017", "2018", "2018", "2019", "2020", "2021", "2022", "2023",
#                "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008",]

# pattern = "|".join(filter_year)
# municipality_data = municipality_data.drop(columns = municipality_data.columns[municipality_data.columns.str.contains(pattern)])

# %%
# converts the dataset into a long format dataset 
# var_names = ["inv", "ob_f_","tec_f_","adm_f_","ob_m_","tec_m_","adm_m_",'ent', 'ele', "com", 
#                 "inf", "wat", "tss", "buiilt", "ocu", "sal_op", "sal_tec", "pop", "temp", "agr", 
#                 "urb", "ntl", "egdp",  "medical_checks_", "emergencies_", "deaths_", "births_",
#                 "suicides_", "homicides_", "car_theft_", "drop_m", "scho_count", "class", "stu"]

# pattern2 = "|".join(var_names)

# long_df = pd.wide_to_long(municipality_data, stubnames=var_names, i='id', j='year', sep='')
# long_df = long_df[long_df.columns[long_df.columns.str.contains("shape|id|year")|long_df.columns.str.contains(pattern2)]]
# long_df =  long_df.drop(columns = "sez_id")
# long_df.fillna(0, inplace=True)

# %%
# Exports the data in a long format 
# long_df.to_csv("aggregated_data/provinces/02_exports/long_province_sez_data.csv")

# %%
geo_municipalities["id"] = geo_municipalities["id"].astype(int)
geo_municipalities = geo_municipalities.merge(ntl,
                               left_on="id",
                               right_on="id")
type(geo_municipalities)
# %%
# classifier = mapclassify.NaturalBreaks(geo_municipalities["viirs_ntl_annual_v20_avg_masked.2020.mean"], k=5)
breaks = pygeoda.natural_breaks(6, geo_municipalities["ntl_2020"])
# %%

 # %%
def distributionPlusCoordinationPoints(geo_map, column, breaks, coordinates, title=None, period=None, ax=None):
    # fig, ax = plt.subplots(figsize=(15,15))

    color_list = ["blue", "green", "black", "grey"]

    geo_map.plot(
        column = column,
        scheme="UserDefined",  
        classification_kwds={"bins":breaks},
        cmap="OrRd", # Change the color scheme
        edgecolor="k",
        linewidth=0.2,
        legend=True,
        legend_kwds={"fontsize":18, 
                    "markerscale":1.7}, #Scales the items inside the legend 
        ax=ax
    )

    for coordinate, color in zip(coordinates,color_list):
        coordinate.plot(
            ax=ax,
            color=color,
            marker="o",
            markersize=50,
            # label=
        )

    ax.set_axis_off();
    ax.set_title(title,
             pad=15,
             fontsize=22,
             fontdict={"weight":"bold"})
# %%


fig, axes = plt.subplots(2, 3, figsize=(50, 30))

# Flatten the array of axes
ax1, ax2, ax3, ax4, ax5, ax6 = axes.flat


distributionPlusCoordinationPoints(geo_municipalities, 
                                   "ntl_2000", 
                                   breaks, 
                                   coordinates=[sez_location_2000], 
                                   title="The Location of SEZ is Correlated With High NTL Observations in 2000",
                                   ax=ax1
                                )

distributionPlusCoordinationPoints(geo_municipalities, 
                                   "ntl_2005", 
                                   breaks, 
                                   coordinates=[sez_location_2000, sez_location_2005],
                                   title="The Location of SEZ is Correlated With High NTL Observations in 2005",
                                   ax=ax2
                                   )

distributionPlusCoordinationPoints(geo_municipalities, 
                                   "ntl_2010", 
                                   breaks, 
                                   coordinates=[sez_location_2000, sez_location_2005, sez_location_2010],
                                   title="The Location of SEZ is Correlated With High NTL Observations in 2010",
                                   ax=ax3
                                   )

distributionPlusCoordinationPoints(geo_municipalities, 
                                   "ntl_2015", 
                                   breaks, 
                                   coordinates=[sez_location_2000, sez_location_2005, 
                                                sez_location_2010, sez_location_2015],
                                   title="The Location of SEZ is Correlated With High NTL Observations in 2015",
                                   ax=ax4            
                                    )

distributionPlusCoordinationPoints(geo_municipalities, 
                                   "ntl_2020", 
                                   breaks, 
                                   coordinates=[sez_location_2000, sez_location_2005, 
                                                sez_location_2010, sez_location_2015,
                                                sez_location_2020],
                                    title="The Location of SEZ is Correlated With High NTL Observations in 2020",
                                   ax=ax5
                                    )

fig.delaxes(ax6)
plt.tight_layout()
plt.show()
# %%
