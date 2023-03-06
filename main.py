# import necessary libraries
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PIL import Image

# set page config for streamlit app

st.set_page_config(page_title="Sachin Tendulkar 100 Centuries", layout="wide")

image = Image.open("sachin.jpg")
st.image(image, caption='Sachin Tendulkar')


# read the dataset
df= pd.read_csv("Sachin Dataset.csv")
# columns for layout
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns( (0.1, 2, 0.2, 1, 0.1))
# title for app
row0_1.title("Visualization of Sachin Tendulakar 100 centuries")
# adding vertical space for aesthetics
with row0_2:
    add_vertical_space()
# adding subheader with my information info
row0_2.subheader(
    "A Streamlit web app by Akash Nilkanth")

# layout for app descriptio
row1_spacer1, row1_1, row1_spacer2 = st.columns((0.1, 3.2, 0.1))

# adding app description to layout
with row1_1:
    st.markdown(
        "Hey there! Welcome to Sachin Tendulakr 100 centuries Visualization App. This app Analyze dataset  of Sachin Tendulkar, It Shows  some nice graphs, it tries to visualize the history of Sachin Tendulkar. One last tip, if you're on a mobile device, switch over to landscape for viewing ease. Give it a go!"
    )
    st.markdown(
        "**Lets Begin** 👇"
    )

# adding header for data analysis and visualization section
st.header("Analyzing & Visualizing the Dataset")
st.write("")

# creating layout for displaying number of rows and columns
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns( (0.1, 1, 0.1, 1, 0.1)
 )
# display number of rows and columns in dataset
with row3_1:
 df.rename(columns={"Test ":"Test","Date ":"Date"},inplace=True)
 df["Date"] = pd.to_datetime(df["Date"])
 df["Date"][0].date().year # Converts into year
# Applying the same to entire column
 df["Year"] = df["Date"].apply(lambda x: x.date().year) # Converts into year
 with st.expander("**See source code**"):
        with st.echo():
         # get number of rows and columns in dataset
         num_rows = df.shape[0]
         num_cols = df.shape[1]
        # Visualizing the number of rows and columns
         figure, ax = plt.subplots()
         ax.bar(['Number of Rows', 'Number of Columns'], [num_rows, num_cols])
         ax.set_title('Sachin Tendulkar 100 Centuries Dataset')
         ax.set_ylabel('Count')
        #displaying on streamlit
 st.subheader("Number of rows and columns")
 st.plotly_chart(figure,theme="streamlit",use_container_width=True)
 st.markdown(
     " The Above chart shows the number of Rows & Columns in the Dataset. The Dataset has 16 rows & 100 columns"
     )
# create layout for displaying missing values and doing imputation
with row3_2:

 st.subheader("Missing Values")

 # checking the missing value
 null = df.isnull().sum()
 # st.bar_chart(null)
# Doing some imputation
 df["Strike Rate"].isnull().sum()
 df["Strike Rate"].fillna(df["Strike Rate"].mean(), inplace=True)
 df["Test"].fillna(df["Test"].mean(), inplace=True)
 not_null = df.isnull().sum()

 # Display the plots side by side
 col1, col2 = st.columns(2)
 with col1:
     with st.expander("**See source code**"):
         with st.echo():
           st.subheader("Missing values")
     st.bar_chart(null, use_container_width=True)

 with col2:
     with st.expander("**See source code**"):
         with st.echo():
           st.subheader("Non Missing values")
     st.bar_chart(not_null, use_container_width=True)
 st.markdown("Looks like the Dataset has some Missing Values So Doing some  Imputation to Fill the Missing Values")

row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.columns(
     (0.1, 1, 0.1, 1, 0.1)
 )

with row4_1:
    with st.expander("**See source code**"):
        with st.echo():

         # Correlation between variables by pairplot
         pair = sns.pairplot(df)
    st.subheader("Correlation Chart")
    st.pyplot(pair)
    st.markdown("The Above plot is shows the relation between all the Columns. Each Columnin the Dataset is Compared with each other")

with row4_2:
           with st.expander("**See source code**"):
             with st.echo():
              st.subheader("HeatMap")
              heatmaps, ax = plt.subplots()
              sns.heatmap(df.corr(), ax=ax, annot=True, cmap="rainbow", linecolor='yellow', linewidths=2)
              ax.set_title("Sachin 100 centuries Heatmap")
           st.write(heatmaps)
           st.markdown(" The Above Chart is HeatMap which shows the relations correlation in Numbers.The value of the correlation coefficient can take any values from -1 to 1.If the value is 1, it is said to be a positive correlation between two variables. This means that when one variable increases, the other variable also increases."
"If the value is -1, it is said to be a negative correlation between the two variables. This means that when one variable increases, the other variable decreases."
"If the value is 0, there is no correlation between the two variables. This means that the variables changes in a random manner with respect to each other."
     )
#Adding a subheader and scatterplot
add_vertical_space()
row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.columns(
     (0.1, 1, 0.1, 1, 0.1) )
#
with row5_1:
 with st.expander("**See source code**"):
             with st.echo():
                 st.subheader("Scatterplot Year vs Runs")
                # scatterplot
                 scatter = px.scatter(df, x="Year",y="Runs",size="Position",color="Year",title="Scatterplot Year vs Runs")

 st.plotly_chart(scatter)
 st.markdown("The  above fig  shows the Scatterplot of Runs Scored by Sachin Tendulkar each year. A scatter plot is a popular visualization tool for examining the relationship between two variables. It is a two-dimensional plot in which each data point is represented by a dot. Each dot represents the Year of the century, runs score by Sachin and the position at which Sachin played. The light blue dot represents the lowest runs scored by whereas Dark blue dot represents the highest runs scored by Sachin Tendulkar."
"As seen in Figure4 Sachin's first century came in 1990, when he scored 120 runs; his second century came three years later, in 1993, when he hit 105 runs. Sachin's highest career runs were 204 in year 2004, which was his first double century. Figure 4 further illustrates that Sachin performed very well when batting at position 4, whereas when batting at position 2 he scored less runs compared to batting at position 4. Sachin scored the fewest runs from 2000 to 2005, when he hit the century with a strike rate of 60. [3]"
)
#     )
#
#
with row5_2:
 with st.expander("**See source code**"):
             with st.echo():
                 st.subheader("3D Scatter plot")
                 sp = px.scatter_3d(df, x="Year", y="Runs", z="Opponent", color="City", size="Year", hover_name="City",
                                   symbol="Opponent", color_discrete_map={"Year": "blue", "Runs": "green", "Opponent": "red"})

 st.write(sp)
 st.markdown("The fig5 shows the 3D plot in 3D plane which compares the 3 variables which is Team against Century scored, city where the century is Scored & year in which century is Scored. The right-hand side symbols represent he the city and the opposite team The same colour Symbol represent the Same city but different opponent team. As seen in fig the at Nagpur city Sachin Tendulkar played against West Indies in Year 1994 & Scored 179 runs. Most Number of centuries scored by Sachin was I at Sharjah & Nagpur where he scored. Where has he scored one one century in Manchester Against England, Sydney Against Australia, Perth, Against Australia, & Johannesburg, South Africa. [4]")
#aadding sub header and Bar plot
add_vertical_space()
row6_space1, row6_1, row6_space2, row6_2, row6_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row6_1:
    with st.expander("**See source code**"):
        with st.echo():
    # Displaying the barplot of centiry Runs of sachin tendulkar year wise
            BARPLOT = px.bar(df.sort_values(['Runs'], ascending=False), x='Year', y="Runs", color="Opponent",
                             title='Number of centuries Sachine Tendulkar Runs each year', text_auto=True)
            BARPLOT.update_layout(
                width=600,
                height=600)
    st.subheader("Bar plot of century score by sachin year wise")
    st.plotly_chart(BARPLOT)

with row6_2:
 with st.expander("**See source code**"):
             with st.echo():
                 #Animated bar_chart
                    anim_bar = px.bar(df, x='Year', y='Runs', animation_frame='Year', animation_group='Venue',
                                      range_x=['1990', '2012'], range_y=[0, 200],
                                      color='Opponent', labels={'Year': 'Year of century', 'Runs': 'Runs Runs'}, height=900)
                    anim_bar.update_layout(
                        width=600,
                        height=600)

 st.subheader("Animated barplot")
 st.plotly_chart(anim_bar)
 st.markdown("Here you can see the Animated Graph")


add_vertical_space()
row7_space1, row7_1, row7_space2, row7_2, row7_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)
#
with row7_1:
    with st.expander("**See source code**"):
        with st.echo():
            # Pichart
             top_score = df.sort_values(["Runs"], ascending=False)[["Runs", "Year"]][:10]
             top_score = top_score.groupby(["Year"]).Year.sum()
             piechart = px.pie(top_score, names=top_score.index, values=top_score.values,
                              hole=.5,
                              title="Sachin's top centuries & year")
             piechart.update_traces(textposition='inside', textinfo='percent+label')
             piechart.update_layout(
                width=600,
                height=600)
    st.subheader("Donut chart of Sachin top centuries & year")
    st.plotly_chart(piechart)
    st.markdown("The above chart is the Donut chart which shows the  top most centuries of Sachin Tendulkar")

with row7_2:
    with st.expander("**See source code**"):
        with st.echo():
            avg = df.groupby(["Year"]).Runs.mean()
            avg_Runs = px.bar(avg, x=avg.index, y=avg.values,
                              title="strike rate of sachin Tendukar each year",

                              text_auto=True,
                              color_discrete_sequence=[px.colors.qualitative.Alphabet],
                              labels={"x": "Year", "y": "Strike rate"})
            avg_Runs.update_layout(
                width=600,
                height=600)
    st.subheader("Barplot year wise average Runs of sachin?")
    st.plotly_chart(avg_Runs)
    st.markdown("The Bar chart shoes the average runs of sachin Tendulakar each year")

add_vertical_space()
row8_space1, row8_1, row8_space2, row8_2, row8_space3 = st.columns((0.1, 1, 0.1, 1, 0.1)  )

with row8_1:
    with st.expander("**See source code**"):
        with st.echo():
            # Calculate the percentage of centuries scored in each location
            location_counts = df["Opponent"].value_counts()
            location_percents = location_counts / location_counts.sum() * 100
            pie_chart, ax = plt.subplots()
            ax.pie(location_percents, labels=location_percents.index, autopct="%1.1f%%")
    ax.set_title("Percentage of centuries Score against each team")
    st.pyplot(pie_chart)
    st.markdown("The Pie chart above shows the percentage of centuries Scored by Sachin Tendulkar against each team. The different colors in the pie chart shows the different teams. As seen most number of centuries were score against Australia i.e., 20%. Whereas least number of centuries were score against Namibia.")


# Sachine year wise strike rate
with row8_2:
 with st.expander("**See source code**"):
             with st.echo():
                 year_wise_strike_rate = df.groupby(["Year"])["Strike Rate"].mean()
                 strike_rate = px.bar(year_wise_strike_rate, x=year_wise_strike_rate.values, y=year_wise_strike_rate.index,
                                     title="What was Sachin's year-wise average strike rate?",
                                      orientation="h",
                                     text_auto=True,
                                     color_discrete_sequence=[px.colors.qualitative.Alphabet],
                                     labels={"x": "Year", "y": "Average century strike rate"})
                 strike_rate.update_layout(width=600,
                                  height=500,
                                  )
 st.subheader("Sachin year wise strike rate")
 st.plotly_chart(strike_rate)

#displaying the barplot
 add_vertical_space()
row9_space1, row9_1, row9_space2, row9_2, row9_space3 = st.columns( (0.1, 1, 0.1, 1, 0.1))
with row9_1:
    with st.expander("**See source code**"):
        with st.echo():

            performance = px.bar(df.groupby(["Opponent"]).Runs.mean().sort_values(ascending=False),
                                         title="Sachin's average Runs against each team",
                                         text_auto=True,
                                         color_discrete_sequence=[px.colors.qualitative.Alphabet],
                                         labels={"x": "Country", "y": "Average Runs"})

    st.subheader("Sachin performance")
    st.plotly_chart(performance)
#displaying the  esachin performanace home vs away
with row9_2:
    with st.expander("**See source code**"):
        with st.echo():
            performance_against_each_team_home_vs_away = df.groupby(["Opponent", "H/A"]).Runs.mean()
            performance_against_each_team_home_vs_away = performance_against_each_team_home_vs_away.reset_index()
            performance_against_each_team_home_vs_away.Runs = performance_against_each_team_home_vs_away.Runs.map(
                lambda x: round(x))
            performance_against_each_team_home_vs_away_df = performance_against_each_team_home_vs_away.index

            per = px.bar(performance_against_each_team_home_vs_away,
                         x='Opponent',
                         y='Runs',
                         color='H/A',
                         text='Runs',
                         labels={"x": "Country", "y": "Average Runs"},
                         title="Sachin's performance against each team (home vs away)"
                         )
        st.subheader("Sachin performance home vs away")
    st.plotly_chart(per)
#showing the horizontal bar chart of top grounds
add_vertical_space()
row10_space1, row10_1, row10_space2, row10_2, row10_space3 = st.columns(
        (0.1, 1, 0.1, 1, 0.1)
    )
with row10_1:
    with st.expander("**See source code**"):
        with st.echo():
            # Top 5 ground of sachine scored the most runs
             top_5_grounds = df.groupby(['Venue']).sum()
             top_5_grounds = top_5_grounds.sort_values(['Runs'], ascending=False)
             top_5_grounds["Venue"] = top_5_grounds.index
             ground = px.bar(top_5_grounds[:10],
                                x='Runs',
                                y="Venue",
                                orientation='h',
                                text_auto=True,
                                title="Sachin's top 5 grounds where he scored the most")
             ground.update_layout(
                width=600,
                height=600)
             st.subheader("Top 5 ground sachin Runs the most")
    st.plotly_chart(ground)

with row10_2:
    with st.expander("**See source code**"):
        with st.echo():
            #displaying the top 5 grounds.
                top_5_Runs_years = df.groupby(["Year"]).Runs.sum().sort_values(ascending=False)[:5]
                fig_top_5_Runs_years = px.pie(top_5_Runs_years, names=top_5_Runs_years.index,
                                              values=top_5_Runs_years.values, hole=.5,
                                              title='Top 5 years in which Sachin scored the most number of runs?')
                fig_top_5_Runs_years.update_traces(textposition='inside', textinfo='percent+label')
                fig_top_5_Runs_years.update_layout(width=600,
                                                   height=500,
                                                   )
                st.subheader("Donut chart ")
    st.plotly_chart(fig_top_5_Runs_years)
add_vertical_space()



# Define a function to get the latitude and longitude for a given location
with st.expander("**See source code**"):
    with st.echo():
        @st.cache_data
        def get_lat_long(location):
                url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
                response = requests.get(url)
                data = response.json()
                if len(data) > 0:
                    lat = data[0]['lat']
                    lon = data[0]['lon']
                    return lat, lon
                else:
                    return None, None


        # Get the latitude and longitude for each location in the dataset
        latitude = []
        longitude = []
        for index, row in df.iterrows():
                lat, lon = get_lat_long(row['Opponent'])
                latitude.append(lat)
                longitude.append(lon)

            # Add the latitude and longitude columns to the data frame
        df['Latitude'] = latitude
        df['Longitude'] = longitude

            # Save the updated data frame to a new CSV file
        df.to_csv("100_centuries_of_Sachin.csv", index=False)
        data = pd.read_csv("100_centuries_of_Sachin.csv")
        Map = px.scatter_mapbox(data, lat="Latitude", lon="Longitude", color="Opponent",
                                    size="Runs", hover_name="Runs",
                                    mapbox_style="open-street-map")
        Map.update_layout(width=1200,
                              height=800,
                              mapbox_zoom=-12,
                              # mapbox_center={"lat": 52.5310214, "lon": -1.2649062}
                              )
# Display the map in Streamlit
st.plotly_chart(Map)
st.markdown("The most complex part in Mapping was the Web Scrapping ."
"The longitude and latitude of the location are required to display the mapping."
"To get the longitude and latitude, The function “get_lat_long”  that  is used to obtain the latitude and longitude of a specific location by providing its name as input. When this function is called with a location name, it constructs a URL that contains the location as a query parameter and sends an HTTP GET request to the OpenStreetMap Nominatim API using the requests library. The API then returns a response in JSON format containing the latitude and longitude of the location if it can be found. If the API returns a valid response, the function extracts the latitude and longitude from the JSON data and returns them as a tuple. However, if the API cannot find the location or if the request fails for some reason, the function returns None for both the latitude and longitude values. The code then iterates over each row in a Pandas data frame called df and calls the get_lat_long function to obtain the latitude and longitude for the opponent in each row. It will appends the latitude and longitude to two lists called latitude and longitude, respectively."
"The code creates two new columns in the data frame df called Latitude and Longitude. It uses the latitude and longitude values obtained for each opponent location and add these new columns with the corresponding values. The updated df data frame is then saved as a new CSV file named 100_centuries_of_Sachin.csv.After this the Map is shown using the plotly express library and df data frame is then saved as a new CSV file named 100_centuries_of_Sachin.csv.After this the Map is shown using the plotly express library and visualizing it on streamlit web application.")
# Create a bar chart using Altair
with st.expander("**See source code**"):
    with st.echo():
        chart = alt.Chart(df).mark_bar().encode(
            x='Venue:N',
            y='Runs:Q',
        )
        # Display the chart in Streamlit
        st.subheader("Altair chart")
st.altair_chart(chart)



