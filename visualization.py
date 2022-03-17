import re
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
sns.set_theme()

proj_dir = os.getcwd()
data_dir = os.path.join(proj_dir, 'data')
jhu_dir = os.path.join(data_dir, 'jhu')
data_output_dir = os.path.join(data_dir, 'output')

latest_csv = [c for c in sorted(os.listdir(data_output_dir)) if re.search(
    'cnty_total_confirmed_cases_\d{8}-\d{6}\.csv', c)][-1]

df_full_data = pd.read_csv(os.path.join(
    data_output_dir, latest_csv), index_col='iso3')

df_cnty_info = df_full_data.iloc[:, :4]

df_total_cases = df_full_data.iloc[:, 4:]
df_total_cases = df_total_cases.T
df_total_cases.index.name = 'Date'
df_total_cases.index = pd.to_datetime(df_total_cases.index)


def showCntyForDays(cnty, history=30):
    """Show the data of a selected country/region

    Parameters
    ----------
    cnty : str
        The ```iso3``` of the selected country/region
    history : int, default ```30```
        The number of days that the chart shows

    Returns
    -------
    None
    """
    cnty = cntyValidation(cnty)[0]
    history = historyValidation(history)

    df_selected = df_total_cases[[cnty]].copy()
    df_selected['new'] = df_selected.diff(1)
    df_selected['rolling7'] = df_selected['new'].rolling(7).mean()
    df_selected['pop_pct'] = df_selected.iloc[:, 0] / \
        df_cnty_info.at[cnty, 'Population']
    df_selected['per_1m'] = df_selected.iloc[:, 0] / \
        df_cnty_info.at[cnty, 'Population'] * 1000000
    df_selected = df_selected[-history:]

    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(
        getFigWidth(df_selected.shape[0]), 15), sharex=True)
    axs[0].bar(df_selected.index, df_selected.iloc[:, 0], label='Total Cases')
    axs[0].set_title(
        'Total COVID-19 Cases in {}'.format(df_cnty_info.at[cnty, 'Country/Region']))
    axs[0].legend()

    axs[1].bar(df_selected.index, df_selected['new'], label='New Cases')
    axs[1].plot(df_selected.index, df_selected['rolling7'],
                color='orange', label='Average Number of New Cases in Past 7 Days')
    axs[1].set_title(
        'Daily New COVID-19 Cases in {}'.format(df_cnty_info.at[cnty, 'Country/Region']))
    handles, labels = axs[1].get_legend_handles_labels()
    order = [1, 0]
    axs[1].legend([handles[i] for i in order], [labels[i] for i in order])

    # axs[2].bar(df_selected.index, df_selected['per_1m'], label='Total Cases per million people')
    # axs[2].set_title('Total covid-19 Cases per million people in {}'.format(df_cnty_info.at[cnty, 'Country/Region']))
    # axs[2].legend()

    for i in range(len(axs)):
        axs[i].set_xlabel('Date')
        axs[i].xaxis.set_major_locator(
            mdates.WeekdayLocator(byweekday=mdates.SU))
        axs[i].xaxis.set_minor_locator(mdates.DayLocator(interval=1))
        axs[i].grid(visible=True, axis='x', which='minor', lw=0.5)
        axs[i].set_xlim(left=(df_selected.index[0] + datetime.timedelta(days=-1)),
                        right=(df_selected.index[-1] + datetime.timedelta(days=1)))

    fig.autofmt_xdate()

    plt.show()


def showSelectedCntyWithPerMillionForDays(cnty, history=30, title=False):
    """Show the data of a list of selected countries/regions

    Parameters
    ----------
    cnty : str or list
        The ```iso3``` of the selected country/region
    history : int, default ```30```
        The number of days that the chart shows
    title : list, default ```None```
        The custom tiltes

    Returns
    -------
    None
    """
    cnty = sorted(cntyValidation(cnty))
    df_new = getDFCasesWithPerMillion(cnty)[-history:]

    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(
        getFigWidth(df_new.shape[0]), 15), sharex=True)

    if not title:
        title_ax0 = 'Number of Daily New COVID-19 Cases'
        title_ax1 = 'Number of Daily New COVID-19 Cases per 1 Million People'
    else:
        title_ax0 = title[0]
        title_ax1 = title[1]

    df_new.iloc[:, :len(cnty)].plot(ax=axs[0], x_compat=True, title=title_ax0)
    df_new.iloc[:, len(cnty):].plot(ax=axs[1], x_compat=True, title=title_ax1)

    for i in range(len(axs)):
        axs[i].xaxis.set_major_locator(
            mdates.WeekdayLocator(byweekday=mdates.SU))
        axs[i].xaxis.set_minor_locator(mdates.DayLocator(interval=1))
        axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        axs[i].set_xlim(left=df_new.index[0], right=df_new.index[-1])
        axs[i].grid(visible=True, axis='x', which='minor', lw=0.5)
        axs[i].legend(labels=list(
            df_cnty_info[df_cnty_info.index.isin(cnty)]['Country/Region']))

    fig.autofmt_xdate()

    plt.show()


def showAvgHighestCasesForDays(per_1m=True, no_of_cnty=5, avgCases=7, history=30):
    """Show the top n countries/regions with the highest average number of new cases

    Parameters
    ----------
    per_1m : boolean, default ```True```
        In case ```per_1m=True```, the average number of new cases is determined by cases per 1 million people
    no_of_cnty : int, default ```5```
        Number of top countries/regions to be selected
    avgCases : int, default ```7```
        Number of days for computing the average
    history : int, default ```30```
        The number of days that the chart shows

    Returns
    -------
    None
    """
    def getHighestCntyListFromDF(df):
        list_top_cnty = list(df.index)
        list_top_cnty = [x[:3] for x in list_top_cnty]
        list_top_cnty = sorted(list_top_cnty)
        return list_top_cnty

    df_new = getDFCasesWithPerMillion(list(df_cnty_info.index))
    df_new = df_new.rolling(avgCases).mean()
    if per_1m:
        df_top = df_new.iloc[-1, int(len(df_new.columns)/2):]
    else:
        df_top = df_new.iloc[-1, :int(len(df_new.columns)/2)]

    no_of_cnty = nCntyValidation(no_of_cnty)
    df_top = df_top.sort_values(axis=0, ascending=False).head(no_of_cnty)
    list_top_cnty = getHighestCntyListFromDF(df_top)

    if per_1m:
        title_ax0 = 'Number of Daily New COVID-19 Cases of Top {} Countries/Regions with the Highest Average Number of New Cases per 1 Million People in Past {} Days'.format(
            no_of_cnty, avgCases)
        title_ax1 = 'Number of Daily New COVID-19 Cases per 1 Million People of Top {} Countries/Regions with the Highest Average Number of New Cases per 1 Million People in Past {} Days'.format(
            no_of_cnty, avgCases)
    else:
        title_ax0 = 'Number of Daily New COVID-19 Cases of Top {} Countries/Regions with the Highest Average Number of New Cases in Past {} Days'.format(
            no_of_cnty, avgCases)
        title_ax1 = 'Number of Daily New COVID-19 Cases per 1 Million People of Top {} Countries/Regions with the Highest Average Number of New Cases in Past {} Days'.format(
            no_of_cnty, avgCases)

    showSelectedCntyWithPerMillionForDays(
        cnty=list_top_cnty, history=history, title=[title_ax0, title_ax1])


def showHighestCasesInAllTime(no_of_cnty=5, history=30):
    """Show the top n countries/regions with the highest total number of cases in all time

    Parameters
    ----------
    no_of_cnty : int, default ```5```
        Number of top countries/regions to be selected
    history : int, default ```30```
        The number of days that the chart shows

    Returns
    -------
    None
    """
    no_of_cnty = nCntyValidation(no_of_cnty)
    df_highest_total = df_total_cases.tail(1).T
    list_highest_cnty = list(df_highest_total.sort_values(
        list(df_highest_total.columns), ascending=False).index)
    list_highest_cnty = list_highest_cnty[:no_of_cnty]

    df_highest_total = df_highest_total[df_highest_total.index.isin(
        list_highest_cnty)]
    df_highest_total.columns = ['Number of Cases']
    df_highest_total = pd.merge(
        df_highest_total, df_cnty_info, left_index=True, right_index=True)
    df_highest_total['Number of Cases per 1 Million People'] = df_highest_total['Number of Cases'] / \
        df_highest_total['Population'] * 1000000
    df_highest_total = df_highest_total.sort_values('Number of Cases')

    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(20, 5))
    axs[0].barh(df_highest_total['Country/Region'],
                df_highest_total['Number of Cases'])
    axs[0].set_title(
        'Total Number of Cases of Top {} Countries/Regions'.format(no_of_cnty))
    axs[1].barh(df_highest_total['Country/Region'],
                df_highest_total['Number of Cases per 1 Million People'])
    axs[1].set_title(
        'Total Number of Cases Per 1 Million People of Top {} Countries/Regions'.format(no_of_cnty))

    plt.show()

    title_ax0 = 'Number of Daily New COVID-19 Cases of Top {} Countries/Regions with the Highest Total Number of Cases'.format(
        no_of_cnty)
    title_ax1 = 'Number of Daily New COVID-19 Cases per 1 Million People of Top {} Countries/Regions with the Highest Total Number of Cases'.format(
        no_of_cnty)

    showSelectedCntyWithPerMillionForDays(
        list_highest_cnty, history=history, title=[title_ax0, title_ax1])


def getDFCasesWithPerMillion(cnty):
    df_selected = df_total_cases[cnty]
    df_new = df_selected.diff(1)
    df_new = pd.merge(left=df_new, right=df_new, left_index=True,
                      right_index=True, suffixes=('', '_per_1m'))
    df_new = df_new.apply(lambda x: (
        x / df_cnty_info.at[x.name[:3], 'Population'] * 1000000) if x.name.endswith('_per_1m') else x)
    return df_new


def cntyValidation(input):
    cnty = []

    if not isinstance(input, list):
        input = [str(input)]
    else:
        input = [str(x) for x in input]

    cnty = [x.upper() for x in input if x.upper() in list(df_cnty_info.index)]
    if len(cnty) == 0:
        cnty = ['CAN']

    return cnty


def historyValidation(input):
    try:
        history = int(input)
        if history == -1:
            return 0
        elif history > 0:
            return history
        else:
            return 30
    except:
        return 30


def nCntyValidation(input):
    try:
        no_of_cnty = int(input)
        if no_of_cnty > 0 and no_of_cnty <= df_cnty_info.shape[0]:
            return no_of_cnty
        else:
            return 5
    except:
        return 5


def getFigWidth(nrow):
    fig_width = max((nrow/30.0) * 10, 15)
    fig_width = min(fig_width, 50)
    return fig_width
