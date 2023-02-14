import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import datetime
import streamlit as st
import pycountry
import plotly.graph_objects as go
import folium
import time
import requests

import altair as alt




@st.cache(allow_output_mutation=True)
def load_data():
    return pd.read_csv("sachin_100_centuries_lat_long.csv")

df = load_data()

# Define a function to get the latitude and longitude for a given location
# def get_lat_long(location):
#     url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
#     response = requests.get(url)
#     data = response.json()
#     if len(data) > 0:
#         lat = data[0]['lat']
#         lon = data[0]['lon']
#         return lat, lon
#     else:
#         return None, None
#
# # Get the latitude and longitude for each location in the dataset
# latitude = []
# longitude = []
# for index, row in df.iterrows():
#     lat, lon = get_lat_long(row['Against'])
#     latitude.append(lat)
#     longitude.append(lon)
#
# # Add the latitude and longitude columns to the data frame
# df['Latitude'] = latitude
# df['Longitude'] = longitude
#
# # Save the updated data frame to a new CSV file
# df.to_csv("sachin_100_centuries_lat_long.csv", index=False)
# print(df.head)









null = df.isnull().sum()

df.rename(columns={"Test ":"Test","Date ":"Date"},inplace=True)
df["Strike Rate"].isnull().sum()
df["Strike Rate"].fillna(df["Strike Rate"].mean(),inplace=True)
df["Test"].fillna(df["Test"].mean(),inplace=True)
not_null = df.isnull().sum()
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].apply(lambda x : x.date().year)

#++++++++++++++++++++++++++++++++++++++++
#Maps








#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
#df.head(5)

#Correlation between variables by pairplot
pair=sns.pairplot(df)

#correlation between variables by heatmap
heatmaps, ax = plt.subplots()
sns.heatmap(df.corr(), ax=ax,annot = True,cmap = "rainbow")






#bARPLOT
BARPLOT = px.bar(df.sort_values(['Score'],ascending=False),x='Year',y="Score",color='Year',
      title='How many centuries did Sachin score year-wise?',text_auto=True)

#LINEPLOT
lineplot = px.line(df.groupby(["Year"]).Score.sum())


#Animated bar_chart

anim_bar= px.bar(df, x='Year', y='Score', animation_frame='Year', animation_group='Venue',
             range_x=['1990', '2012'], range_y=[0, 200],
             color='Against', labels={'Year': 'Year of century', 'Score': 'Runs Score'}, height=900)


#Pichart
top_10_scores = df.sort_values(["Score"],ascending=False)[["Score","Year"]][:10]
top_10_scores = top_10_scores.groupby(["Year"]).Year.sum()
fig_top_10_scores = px.pie(top_10_scores, names=top_10_scores.index,values=top_10_scores.values,
       hole=.5,
       title="What were Sachin's top 10 centuries & in which year?")
fig_top_10_scores.update_traces(textposition='inside', textinfo='percent+label')


#barplot
year_wise_average_score = df.groupby(["Year"]).Score.mean()
avg_score=px.bar(year_wise_average_score, x=year_wise_average_score.index, y=year_wise_average_score.values,
           title="What was Sachin's year-wise average score?",
           text_auto=True,
           color_discrete_sequence=[px.colors.qualitative.Alphabet],
           labels={"x": "Year", "y": "Average score"})


#scatterplot
plt.figure(figsize=(24,12))
#scatter = sns.scatterplot(x= df['Year'] , y = df['Score'] , data = df)
scatter = px.scatter(df, x="Year", y="Score", color="Score")

#3d Scatter plot
sp = px.scatter_3d(df, x="Year", y="Score", z="Against", color="City", size="Year", hover_name="City",
                  symbol="Against", color_discrete_map = {"Year": "blue", "Score": "green", "Against":"red"})



#piplot #top 5 years of sachin

top_5_scores_years = df.groupby(["Year"]).Score.sum().sort_values(ascending=False)[:5]
fig_top_5_scores_years = px.pie(top_5_scores_years, names=top_5_scores_years.index,
       values=top_5_scores_years.values,hole=.5,
       title='Top 5 years in which Sachin scored the most number of runs?')
fig_top_5_scores_years.update_traces(textposition='inside', textinfo='percent+label')



#Sachine year wise strike rate
year_wise_strike_rate = df.groupby(["Year"])["Strike Rate"].mean()
strike_rate=px.bar(year_wise_strike_rate,x=year_wise_strike_rate.index,y=year_wise_strike_rate.values,
       title="What was Sachin's year-wise average strike rate?",
       text_auto=True,
       color_discrete_sequence=[px.colors.qualitative.Alphabet],
       labels={"x":"Year","y":"Average century strike rate"})


#Sachin performance against each team ( home vs away )

performance= px.bar(df.groupby(["Against"]).Score.mean().sort_values(ascending=False),
       title="Sachin's average score against each team",
       text_auto=True,
       color_discrete_sequence=[px.colors.qualitative.Alphabet],
       labels={"x":"Country","y":"Average score"})


performance_against_each_team_home_vs_away = df.groupby(["Against","H/A"]).Score.mean()
performance_against_each_team_home_vs_away = performance_against_each_team_home_vs_away.reset_index()
performance_against_each_team_home_vs_away.Score = performance_against_each_team_home_vs_away.Score.map(lambda x: round(x))
performance_against_each_team_home_vs_away_df = performance_against_each_team_home_vs_away.index
per = px.bar(performance_against_each_team_home_vs_away,
       x='Against',
       y='Score',
       color='H/A',
       text='Score',
       labels={"x":"Country","y":"Average score"},
       title="Sachin's performance against each team (home vs away)"
      )

#Top 5 ground of sachine scored the most runs

top_5_grounds = df.groupby(['Venue']).sum()
top_5_grounds = top_5_grounds.sort_values(['Score'],ascending=False)
top_5_grounds["Venue"] = top_5_grounds.index
ground = px.bar(top_5_grounds[:10],
       x='Score',
       y="Venue",
       orientation='h',
       text_auto=True,
      title="Sachin's top 5 grounds where he scored the most?")




#MAp
# m = folium.Map(location=[20, 70], zoom_start=4)
#
# for i, row in df.iterrows():
#     folium.Marker(
#         location=[row["latitude"], row["longitude"]],
#         popup=row["Ground"]
#     ).add_to(m)






a=st.sidebar.radio('Navigation',['Welcome','Show Dataset','Show Visualization'])

if a=='Show Dataset':
  st.text("Dataset")  # add a title
  st.dataframe(df)


  # visualize my dataframe in the Streamlit app
elif a=="Show Visualization":

    st.text(null)


    st.header("Missing Values")
    st.bar_chart(null)
    st.bar_chart(not_null)

    st.subheader("Satter plot")
    st.write(scatter)

    st.subheader("3d scatter plot")
    st.write(sp)

    st.subheader("Coreelation between the columns")
    st.pyplot(pair)

    st.subheader("Heatmap")
    st.write(heatmaps)

    st.subheader("Bar plot of century score by sachin year wise")
    st.plotly_chart(BARPLOT)

    st.subheader("Line plot")
    st.plotly_chart(lineplot)

    st.subheader("Animated barplot")
    st.plotly_chart(anim_bar)

    st.subheader("Donut chart  of top 10 century of sachin & year")
    st.plotly_chart(fig_top_10_scores)

    st.subheader("Barplot year wise average score of sachin?")
    st.plotly_chart(avg_score)

    st.subheader("Donut chart ")
    st.plotly_chart(fig_top_5_scores_years)


    st.subheader("Sachin year wise strike rate")
    st.plotly_chart(strike_rate)

    st.subheader("Sachine perforance")
    st.plotly_chart(performance)

    st.subheader("Sachin performance home vs away")
    st.plotly_chart(per)

    st.subheader("Top 5 ground sachin score the most")
    st.plotly_chart(ground)




    st.title("Sachin Tendulkar's 100 Centuries Map Visualization")

    st.write("This is a map visualization of Sachin Tendulkar's 100 international cricket centuries.")
    fig1 = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="Venue",
                            size="Score", hover_name="Score",

                            mapbox_style="open-street-map")
    fig1.update_layout(
        mapbox_zoom=-18,
        mapbox_center={"lat": 52.5310214, "lon": -1.2649062}
    )

    # Display the map in Streamlit
    st.plotly_chart(fig1)

    # Create a bar chart using Altair
    chart = alt.Chart(df).mark_bar().encode(
    x='Venue:N',
    y='Score:Q',
)

# Display the chart in Streamlit
    st.subheader("Altair chart")
    st.altair_chart(chart)



# Create a radar chart
    radar_chart = px.line_polar(df, r='Score', theta='Against', line_close=True)

# Show the radar chart in Streamlit
    st.subheader("Radar chart")
    st.plotly_chart(radar_chart)

#number of centuris sachine tendulkar score on diffrent grounds
    df_grouped = df.groupby('Venue').agg({'Score': 'count'})

    # Create a pie chart
    pie_chart = px.pie(df_grouped, values='Venue', names='Score')

    # Show the pie chart in Streamlit
    st.subheader("piechart")
    st.plotly_chart(pie_chart)


elif a=="Welcome" :
    st.header("Hello shashank")
    st.header("Data Visualization Assignment")







# Displot
# plt.figure(figsize = (30,10))
# features=[ 'Mat', 'Inns', 'NO', 'Runs', 'HS', 'Ave', 'BF', 'SR', '100','50', '0', 'Exp']
# for i in enumerate(features):
#     plt.subplot(3,4,i[0]+1)
#     sns.distplot(df[i[1]])

#ridges plot

