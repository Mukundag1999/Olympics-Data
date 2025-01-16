def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Bronze', 'Silver']]
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally = medal_tally.sort_values('Gold', ascending=False)
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, "Overall")
    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, "Overall")

    return years,country

def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if year=='Overall' and country=='Overall' :
        temp_df = medal_df
    if year=='Overall' and country!="Overall" :
        temp_df = medal_df[medal_df['region']==country]
        flag = 1
    if year!='Overall' and country=="Overall" :
        temp_df = medal_df[medal_df['Year']==int(year)]
    if year!='Overall' and country!="Overall" :
         temp_df = medal_df[(medal_df['Year']==int(year)) & (medal_df['region']==country)]

    if flag==1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def data_overtime(df,col):
    nations_overtime = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_overtime.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)

    return nations_overtime

def most_successful(df, sport):
    # Filter rows with medals
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if specified
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Get the top 15 most successful athletes
    top_athletes = temp_df['Name'].value_counts().reset_index().head(15)
    top_athletes.columns = ['Name', 'Medals']

    # Correcting the merge: assuming you want to join back on 'Name' to get more info from df
    # It's important that both 'left_on' and 'right_on' refer to 'Name'
    top_athletes = top_athletes.merge(df[['Name', 'Sport', 'region']], on='Name', how='left').drop_duplicates('Name')
    top_athletes.rename(columns={'region':'Region'},inplace=True)
    return top_athletes

def country_wise_medals(df,country):
    temp_df = df.dropna(subset='Medal')
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    x = new_df.groupby('Year').count()['Medal'].reset_index()
    return x

def country_wise_excel(df,country):
    temp_df = df.dropna(subset='Medal')
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]

    return new_df

def most_successful_country(df, country):
    # Filter rows with medals
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if specified

    temp_df = temp_df[temp_df['region'] == country]

    # Get the top 15 most successful athletes
    top_athletes = temp_df['Name'].value_counts().reset_index().head(15)
    top_athletes.columns = ['Name', 'Medals']

    # Correcting the merge: assuming you want to join back on 'Name' to get more info from df
    # It's important that both 'left_on' and 'right_on' refer to 'Name'
    top_athletes = top_athletes.merge(df[['Name', 'Sport']], on='Name', how='left').drop_duplicates('Name')

    return top_athletes.head(10)

def height_weight(df,sport):
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    temp_df = athelete_df[athelete_df['Sport'] == sport]
    temp_df['Medal'].fillna('No medal', inplace=True)
    return temp_df
def M_F(df):
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    M = athelete_df[athelete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    F = athelete_df[athelete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = M.merge(F, on='Year', how='left')
    final.fillna(0, inplace=True)
    final.columns = ['Year', 'Male', 'Female']
    return final