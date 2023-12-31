import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    average_age_men = df[df['sex'] == 'Male']['age'].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    p = len(df)

    # Filtra las filas donde la columna 'education' es igual a 'Bachelor'
    personas_bachelor = df[df['education'] == 'Bachelors']

    # Calcula el número de personas con 'Bachelor'
    num_bachelor = len(personas_bachelor)

    # Calcula el porcentaje de personas con 'Bachelor'
    percentage_bachelors = round((num_bachelor / p) * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education= df[df['education'].isin(['Bachelors','Masters','Doctorate'])]
    lower_education= df[~df['education'].isin(['Bachelors','Masters','Doctorate'])]

    higher_education_50= higher_education[higher_education['salary'] == '>50K']
    lower_education_50= lower_education[lower_education['salary'] == '>50K']

    # percentage with salary >50K
    p=(higher_education_50['salary'].value_counts() / len(higher_education)) * 100
    l=(lower_education_50['salary'].value_counts() / len(lower_education)) * 100
    higher_education_rich = round(p.sum(),1)
    lower_education_rich = round(l.sum(),1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df.sort_values(by='hours-per-week').head(1)['hours-per-week'].values[0]

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[df['hours-per-week'] == 1]
    num_workers_50 =len(num_min_workers[num_min_workers['salary'] == '>50K'])

    rich_percentage = int((num_workers_50 / len(num_min_workers)) * 100)

    # What country has the highest percentage of people that earn >50K?
    lower= df[df['salary'] == '<=50K'][['native-country','salary']]
    higher= df[df['salary'] == '>50K'][['native-country','salary']]
    lower2 = lower.groupby(['native-country', 'salary']).size().reset_index(name='count') 
    higher2 = higher.groupby(['native-country', 'salary']).size().reset_index(name='count')
    new_df = higher2.merge(lower2, how='inner',on='native-country')
    new_df['count'] = new_df['count_x'] + new_df['count_y']
    new_df['percentil_higher'] = round((new_df['count_x'] / new_df['count'] *100 ),1)
    new=new_df.sort_values(by='percentil_higher',ascending=False)[['native-country','percentil_higher']]
    highest_earning_country = new.head(1).values[0,0]
    highest_earning_country_percentage = new.head(1).values[0,1]

    # Identify the most popular occupation for those who earn >50K in India.
    df_india = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
    df_india.loc[df_india['education'] == 'Prof-school', 'education'] = 'Prof-specialty'
    top_IN_occupation= df_india.groupby(['education']).size().reset_index(name='count').tail(1).values[0,0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
