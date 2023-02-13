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

# @st.cache  # No need for TTL this time. It's static data :)
# def get_data_by_state():
# 	return pd.read_csv("100 centuries of Sachin.csv")

df = pd.read_csv("100 centuries of Sachin.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
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

def alpha3code(column):
    CODE=[]
    for Against in column:
        try:
            code=pycountry.countries.get(name=Against).alpha_3
           # .alpha_3 means 3-letter country code
           # .alpha_2 means 2-letter country code
            CODE.append(code)
        except:
            if(Against=="England"):
                CODE.append('GB')
            else:
                CODE.append('aqo')



    return CODE
# create a column for code
df['CODE']=alpha3code(df.Against)







#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
#df.head(5)

#Correlation between variables by pairplot
pair=sns.pairplot(df)

#correlation between variables by heatmap
fig, ax = plt.subplots()
sns.heatmap(df.corr(), ax=ax,annot = True,cmap = "rainbow")

# plt.figure(figsize = (10, 10))
# heatmap =sns.heatmap(df.corr(), annot = True, cmap="rainbow")
# plt.savefig('Correlation')




#bARPLOT
BARPLOT = px.bar(df.sort_values(['Score'],ascending=False),x='Year',y="Score",color='Year',
      title='How many centuries did Sachin score year-wise?',text_auto=True)
#LINEPLOT
lineplot = px.line(df.groupby(["Year"]).Score.sum())

#Animated bar_chart

# fig = px.bar(df, x='Date', y='Centuries', animation_frame='Date', animation_group='Match',
#              range_x=['1989-12-08', '2012-03-18'], range_y=[0, 100],
#              color='Country', labels={'Date': 'Date of Century', 'Centuries': 'Centuries Scored'}, height=600)
#
# st.plotly_chart(fig)

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

#MAPs
maps = px.choropleth(df, locations="Against", color="Against", hover_name="Venue", animation_frame="Year", range_color=[20,80])
#fig.show()
#scatter = px.scatter(df, x="Year", y="Score", animation_frame="Year", animation_group="Against",
           ## log_x=True, size_max=45, range_x=[100,100000], range_y=[25,90])
#scatter= px.scatter(df, x="Year", y="Score", color="Score", marginal_y="violin",
           #marginal_x="box", trendline="ols", template="simple_white")

# df["e"] = df["Year"]/100
# scatter= px.scatter(df, x="Year", y="Score", color="Score", error_x="e", error_y="e")
#fig.show()

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
  st.write(df)


  # visualize my dataframe in the Streamlit app
elif a=="Show Visualization":

    st.text(null)
    st.write(scatter)
    st.write(sp)
    st.header("Missing Values")
    st.bar_chart(null)
    st.bar_chart(not_null)
    st.text("Coreelation between the columns")
    st.pyplot(pair)
    st.subheader("Heatmap")
    st.write(fig)
    st.subheader("Bar plot")
    st.plotly_chart(BARPLOT)
    st.subheader("Line plot")
    st.plotly_chart(lineplot)
    st.plotly_chart(fig_top_10_scores)
    st.plotly_chart(avg_score)
    st.plotly_chart(fig_top_5_scores_years)
    st.plotly_chart(strike_rate)
    st.plotly_chart(performance)
    st.plotly_chart(per)
    st.plotly_chart(ground)
    #st.plotly_chart(maps)
    st.subheader("Animated barplt")
    st.plotly_chart(anim_bar)

    st.title("Sachin Tendulkar's 100 Centuries Map Visualization")

    st.write("This is a map visualization of Sachin Tendulkar's 100 international cricket centuries.")
    #st.write(m)
elif a=="Welcome" :
    st.header("Hello shashank")
    st.header("Data Visualization Assignment")





#heat map
# plt.figure(figsize = (10, 10))
# sns.heatmap(df.corr(), annot = True, cmap="rainbow")
# plt.savefig('Correlation')
# plt.show()


# Displot
# plt.figure(figsize = (30,10))
# features=[ 'Mat', 'Inns', 'NO', 'Runs', 'HS', 'Ave', 'BF', 'SR', '100','50', '0', 'Exp']
# for i in enumerate(features):
#     plt.subplot(3,4,i[0]+1)
#     sns.distplot(df[i[1]])

#ridges plot
