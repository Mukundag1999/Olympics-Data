import streamlit as st
import pandas as pd
import Preprocessor, Helper
from Helper import most_successful_country
from Preprocessor import preprocess
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = Preprocessor.preprocess()
st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athelete wise Analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = Helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = Helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year == 'Overall' and selected_country != "Overall":
        st.title(selected_country + " Overall perfomance")
    if selected_year != 'Overall' and selected_country == "Overall":
        st.title('Medal Tally in '+ str(selected_year) + ' Olympics')
    if selected_year != 'Overall' and selected_country != "Overall":
        st.title(selected_country + ' perfomance in ' + str(selected_year))

    st.table(medal_tally.style.format({'Year': "{:.0f}"}))

if user_menu == 'Overall Analysis':
    st.title('Overall Statistics')
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    events= df['Event'].unique().shape[0]

    col1,col2,col3 = st.columns(3)

    with col1:
        st.title('Editions')
        st.header(editions)
    with col2:
        st.title('Hosts')
        st.header(cities)
    with col3:
        st.title('Sports')
        st.header(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.title('Events')
        st.header(events)
    with col2:
        st.title('Nations')
        st.header(nations)
    with col3:
        st.title('Athletes')
        st.header(athletes)



    nations_overtime = Helper.data_overtime(df,'region')
    st.title('Nations over the years')
    fig = px.line(nations_overtime, x='Edition', y='region')
    st.plotly_chart(fig)

    events_overtime = Helper.data_overtime(df, 'Event')
    st.title('Events over the years')
    fig = px.line(events_overtime, x='Edition', y='Event')
    st.plotly_chart(fig)

    athletes_overtime = Helper.data_overtime(df, 'Name')
    st.title('Athletes over the years')
    fig = px.line(athletes_overtime, x='Edition', y='Name')
    st.plotly_chart(fig)

    st.title('No. of events overtime (every sport)')

    # Create a larger Matplotlib figure
    fig, ax = plt.subplots(figsize=(15, 12))  # Adjust the figure size to make the chart larger

    # Prepare the data for the heatmap
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    pivot_table = x.pivot_table(
        index='Sport', columns='Year', values='Event', aggfunc='count'
    ).fillna(0).astype(int)

    # Plot the heatmap with larger annotations
    sns.heatmap(
        pivot_table,
        annot=True,
        annot_kws={"size": 12},  # Increase font size for annotations
        fmt="d",  # Format annotations as integers
        cmap="Blues",  # Optional: Add a color map
        ax=ax  # Use the Matplotlib axis
    )

    # Customize axis labels and tick label sizes
    ax.set_xlabel("Year", fontsize=14)  # Increase X-axis label font size
    ax.set_ylabel("Sport", fontsize=14)  # Increase Y-axis label font size
    ax.tick_params(axis='x', labelsize=12)  # Increase font size of X-axis ticks
    ax.tick_params(axis='y', labelsize=12)  # Increase font size of Y-axis ticks

    # Render the plot in Streamlit
    st.pyplot(fig)

    st.title('Most succesful athletes')
    sports = df['Sport'].unique().tolist()
    sports.sort()
    sports.insert(0,'Overall')
    selected_sport = st.selectbox('Select a sport',sports)
    succesful_athletes = Helper.most_successful(df,selected_sport)
    st.table(succesful_athletes)


if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country Wise Analysis')
    country = df['region'].dropna().unique().tolist()
    country.sort()


    # Create a larger Matplotlib figure
    selected_country = st.sidebar.selectbox('Select a country', country) # Adjust the figure size to make the chart larger
    excel = Helper.country_wise_excel(df,selected_country)
    pivot_table = excel.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int)
    if pivot_table.empty:
        st.header('No Medals')
    else:

        new_df = Helper.country_wise_medals(df, selected_country)
        st.title('Medals won by ' + selected_country)
        fig = px.line(new_df, x='Year', y='Medal')
        st.plotly_chart(fig)

        st.title(selected_country + ' excels in the following sports')

        fig, ax = plt.subplots(figsize=(15, 12))
        sns.heatmap(
            pivot_table,
            annot=True,
            annot_kws={"size": 12},  # Increase font size for annotations
            fmt="d",  # Format annotations as integers
            cmap="Blues",  # Optional: Add a color map
            ax=ax  # Use the Matplotlib axis
        )

        ax.set_xlabel("Year", fontsize=14)  # Increase X-axis label font size
        ax.set_ylabel("Sport", fontsize=14)  # Increase Y-axis label font size
        ax.tick_params(axis='x', labelsize=12)  # Increase font size of X-axis ticks
        ax.tick_params(axis='y', labelsize=12)  # Increase font size of Y-axis ticks

        # Render the plot in Streamlit
        st.pyplot(fig)

    most_successful_country = most_successful_country(df,selected_country)
    if most_successful_country.empty:
        st.header('No Medals')
    else:
        st.title('Top 10 athletes of '+selected_country)
        st.table(most_successful_country)

if user_menu == 'Athelete wise Analysis':
    st.title('Age-wise probability of wining medals')
    st.text('Note - Click on the medal type to show/hide the graphs')
    try:
        athlete_df = df.drop_duplicates(subset=['Name', 'region'])
        x1 = athlete_df['Age'].dropna()
        x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

        fig = ff.create_distplot([x1, x2, x3, x4], ['Age Distribution', 'Gold', 'Silver', 'Bronze'],
                                 show_hist=False, show_rug=False)
        fig.update_layout(autosize=False,width=1000,height=600)
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

    sports = df['Sport'].unique().tolist()
    sports.sort()
    selected_sport = st.selectbox('Select a sport', sports)
    st.title('Height Vs Weight')
    fig,ax= plt.subplots()
    temp_df=Helper.height_weight(df,selected_sport)
    ax = sns.scatterplot(data=temp_df,x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title('Men Vs Women')
    final = Helper.M_F(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
