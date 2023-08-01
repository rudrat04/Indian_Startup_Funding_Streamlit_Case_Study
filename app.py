import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='StartUp Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total',str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')

    with col3:
        st.metric('Avg',str(round(avg_funding)) + ' Cr')

    with col4:
        st.metric('Funded Startups',num_startups)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])

    st.pyplot(fig3)

def load_startup_details(startup):
    st.title(startup)
    last5_df = df[df['startup']==startup].head()[['date', 'investors', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    
    col1,col2 = st.columns(2)
    with col1:
        # st.subheader('Total Amount invested')
        total_amount_df = df[df['startup']==startup]['amount']
        total_amount_invested = round(total_amount_df.sum(), ndigits=2)
        st.metric('Total Amount invested', str(total_amount_invested) + ' Cr')

    with col2:
        list_of_investors = df[df['startup'] == startup]['investors'].reset_index().drop(columns=['index']).count()
        st.metric('Total Investors Involved', str(list_of_investors[0]) + ' Investors')

    col3,col4 = st.columns(2)
    with col3:
        startup_cities = df[df['startup'] == startup].groupby('startup')['city'].value_counts()
        st.subheader('Startup Cities')
        fig1, ax1 = plt.subplots()
        ax1.pie(startup_cities,labels = startup_cities.index, autopct="%0.01f%%")

        st.pyplot(fig1)

    with col4:
        #Lsit of Investors
        list_of_investors = df[df['startup'] == startup]['investors'].reset_index().drop(columns=['index'])
        st.subheader('List of Investors')
        st.dataframe(list_of_investors)

    col5, col6 = st.columns(2)
    with col5:
        vertical_series = df[df['startup'] == startup].groupby('startup')['vertical'].value_counts()
        st.subheader('Vertical')
        fig2, ax2 = plt.subplots()
        ax2.pie(vertical_series,labels = vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig2)

    with col6:
        round_series = df[df['startup'] == startup].groupby('startup')['round'].value_counts()
        st.subheader('Round')
        fig3, ax3 = plt.subplots()
        ax3.pie(round_series,labels = round_series.index, autopct="%0.01f%%")
        st.pyplot(fig3)



def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)

    with col2:
        verical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(verical_series,labels=verical_series.index,autopct="%0.01f%%")

        st.pyplot(fig1)

    col3, col4 = st.columns(2)

    with col3:
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()

        st.subheader('Rounds invested in')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series,labels=round_series.index,autopct="%0.01f%%")

        st.pyplot(fig2)

    with col4:
        cities_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()

        st.subheader('Cities invested in')
        fig3, ax3 = plt.subplots()
        ax3.pie(cities_series,labels=cities_series.index,autopct="%0.01f%%")

        st.pyplot(fig3)


    print(df.info())

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)

    st.pyplot(fig2)

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    if btn1:
        load_startup_details(selected_startup)
else:
    selected_investor = st.sidebar.selectbox('Select StartUp',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)

