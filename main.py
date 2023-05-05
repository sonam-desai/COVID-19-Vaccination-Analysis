import numpy as np
import pandas as pd  #Load Pandas
import seaborn as sns
import matplotlib.pyplot as plt
#%matplotlib inline

pd.set_option('display.max_columns', 30)
pd.set_option('display.float_format', '{:,.2f}'.format)

#Load Dataset for country vaccinations
vaccine_data = pd.read_csv('country_vaccinations.csv')

#data is from kaggle - select top 5 countries
vaccine_data.head(5)
vaccine_data.info()
vaccine_data.shape
vaccine_data.isnull().sum()
vaccine_data.describe()

vaccine_country = vaccine_data.drop(
  ['source_name', 'source_website', 'vaccines'], axis=1)
vaccine_country.head()

vaccine_country["date"] = pd.to_datetime(vaccine_country["date"],
                                         format='%Y-%m-%d')

vaccine_country = vaccine_country.replace([np.inf, -np.inf], np.nan)
vaccine_country = vaccine_country.fillna(0)
vaccine_country.isnull().sum()


#Function to find total, avergae, maximum  and minimum of different vaccinations status by country
def vaccination_country(column_name, function):

  if function == 'sum':

    return (vaccine_country[[
      'country', column_name
    ]].groupby(by='country').sum().sort_values(by=column_name,
                                               ascending=False).reset_index())

  elif function == 'mean':

    return (vaccine_country[[
      'country', column_name
    ]].groupby(by='country').mean().sort_values(by=column_name,
                                                ascending=False).reset_index())
  elif function == 'max':

    return (vaccine_country[[
      'country', column_name
    ]].groupby(by='country').max().sort_values(by=column_name,
                                               ascending=False).reset_index())
  elif function == 'min':
    return (vaccine_country[[
      'country', column_name
    ]].groupby(by='country').min().sort_values(by=column_name,
                                               ascending=False).reset_index())


# Calculating different vaccinations for visualizations
max_vacines_total = vaccination_country('total_vaccinations', 'max')

sum_vaccinated = vaccination_country('people_vaccinated', 'sum')
sum_fully_vaccinated = vaccination_country('people_fully_vaccinated', 'sum')

total_vaccinations_avg = vaccination_country('total_vaccinations_per_hundred',
                                             'mean')
avg_vaccinated = vaccination_country('people_vaccinated_per_hundred', 'mean')
avg_fully_vaccinated = vaccination_country(
  'people_fully_vaccinated_per_hundred', 'mean')
vaccinations_daily_avg = vaccination_country('daily_vaccinations_per_million',
                                             'mean')


#Function for Country with maximum and minimum daily vaccinations
def daily_vaccination_country(column_name, function):
  '''
    A function that requires daily_vaccination column and max/min function name as string arguments.
    '''

  daily_vaccines = (vaccine_country.pivot_table(index='country',
                                                columns='date',
                                                values=column_name))
  if function == 'max':
    daily_vaccines['Highest Daily Vaccination'] = daily_vaccines.max(axis=1)
    daily_vaccines['Date - Highest Daily Vaccination'] = daily_vaccines.idxmax(
      axis=1)
    daily_vaccines.sort_values(by='Highest Daily Vaccination',
                               ascending=False,
                               inplace=True)
    daily_vaccines.rename_axis('', axis=1, inplace=True)

    return daily_vaccines[[
      'Highest Daily Vaccination', 'Date - Highest Daily Vaccination'
    ]].reset_index()

  elif function == 'min':

    daily_vaccines.replace(0.00, np.nan, inplace=True)
    daily_vaccines['Lowest Daily Vaccination'] = daily_vaccines.min(axis=1)
    daily_vaccines['Date - Lowest Daily Vaccination'] = daily_vaccines.idxmin(
      axis=1)
    daily_vaccines.sort_values(by='Lowest Daily Vaccination',
                               ascending=False,
                               inplace=True)
    daily_vaccines.rename_axis('', axis=1, inplace=True)

    return daily_vaccines[[
      'Lowest Daily Vaccination', 'Date - Lowest Daily Vaccination'
    ]].reset_index()


#Calculating highest and lowest daily vaccination and the respective dates.
highest_daily_vaccination = daily_vaccination_country('daily_vaccinations',
                                                      'max')
lowest_daily_vaccination = daily_vaccination_country('daily_vaccinations',
                                                     'min')

#Top 5 and bottom 5 countries (Total Vaccinations).
sns.set_theme(style='darkgrid')
sns.set(rc={'figure.figsize': (12, 5)})

fig, axes = plt.subplots(2, 1)

sns.barplot(x='country',
            y='total_vaccinations',
            data=max_vacines_total.head(),
            ax=axes[0])
axes[0].set(xlabel='',
            ylabel='Total Vaccinations',
            title='Top 5 Countries (Total vaccinations)')

sns.barplot(x='country',
            y='total_vaccinations',
            data=max_vacines_total.tail(),
            ax=axes[1])
axes[1].set(xlabel='',
            ylabel='Total Vaccinations',
            title='Bottom 5 Countries (Total Vaccinations)')

fig.tight_layout()
plt.show()

# Top 5 and bottom 5 countries (People vaccinated)
fig, axes = plt.subplots(2, 1)

sns.barplot(x='country',
            y='people_vaccinated',
            data=sum_vaccinated.head(),
            ax=axes[0])
axes[0].set(xlabel='',
            ylabel='Total People Vaccinated',
            title='Top 5 Countries (People Vaccinated)')

sns.barplot(x='country',
            y='people_vaccinated',
            data=sum_vaccinated.tail(),
            ax=axes[1])
axes[1].set(xlabel='',
            ylabel='Total People Vaccinated',
            title='Bottom 5 Countries (People Vaccinated)')

fig.tight_layout()
plt.show()

# Top and Bottom 5 countries (People fully vaccinated)
fig, axes = plt.subplots(2, 1)

sns.barplot(x='country',
            y='people_fully_vaccinated',
            data=sum_fully_vaccinated.head(),
            ax=axes[0])
axes[0].set(xlabel='',
            ylabel='People Fully Vaccinated',
            title='Top 5 Countries (Fully Vaccinated)')

sns.barplot(x='country',
            y='people_fully_vaccinated',
            data=sum_fully_vaccinated.tail(),
            ax=axes[1])
axes[1].set(xlabel='',
            ylabel='People Fully Vaccinated',
            title='Bottom 5 Countries (Fully Vaccinated)')

fig.tight_layout()
plt.show()
