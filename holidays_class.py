import pandas as pd
import datetime
import holidays

import logging
logger = logging.getLogger(__name__)

class SpecialEvents(object):
    """
    Holidays and Special Events aka Covid
    """
    cybermonday_nov = [
        datetime.datetime(2021, 11, 29).date(), datetime.datetime(2021, 11, 30).date(),
        datetime.datetime(2021, 12, 1).date(),
    ]
    blackfriday = [
        datetime.datetime(2021, 11, 26).date(), datetime.datetime(2021, 11, 27).date(),
        datetime.datetime(2021, 11, 28).date(),

    ]
    easter = [
        datetime.datetime(2021, 5, 2).date()
    ]
    EXTRA_HOLIDAYS = {
        '09-01': 'День знаний',
        '10-31': 'Helloween',
    }

    cybermonday_nov = dict.fromkeys(cybermonday_nov, 'Cybermonday_Nov')
    blackfriday = dict.fromkeys(blackfriday, 'BlackFriday')
    easter = dict.fromkeys(easter, 'Easter')
    ADDITIONAL_HOLIDAYS = {**easter, **cybermonday_nov, **blackfriday}


    def __init__(self, df, date_col):
        self.df = df
        self.date_col = date_col
        self.years = self.df[self.date_col].dt.year.unique()
        self.min_year = self.df[self.date_col].dt.year.min()
        self.extra_holidays = self.EXTRA_HOLIDAYS
        self.additional_holidays = self.ADDITIONAL_HOLIDAYS
        self.dummies_prefix = 'HOL'


    def get_holidays(self, max_year):
        """
        get Russian holidays from lib and add extra holidays from custom dict
        :return: DataFrame['date', 'holiday_name']
        """
        holidays_dict = {}
        for year in range(self.min_year, max_year):
            ru_hol_dict = holidays.RU(years=int(year))

            for date, name in self.extra_holidays.items():
                extra_holidays_dict = {datetime.date.fromisoformat(f'{year}-{date}'): name}
                ru_hol_dict.update(extra_holidays_dict)
            holidays_dict.update(ru_hol_dict)

        total_holidays = {**holidays_dict, **self.additional_holidays}
        holidays_df = pd.DataFrame.from_dict(total_holidays, orient='index', columns={'hol_name'})

        logger.info('[get_holidays]: Holidays successfully downloaded')
        return holidays_df


    def holidays_dummies_df(self, max_year):
        """ Make dummies dataframe from <get_holidays> func """
        holidays_series = self.get_holidays(max_year)

        holidays_df = pd.get_dummies(holidays_series, prefix=self.dummies_prefix)
        holidays_df.columns = holidays_df.columns.str.replace(' ', '_', regex=True)
        holidays_df.index = pd.to_datetime(holidays_df.index)

        holidays_df['total_holidays'] = holidays_df.filter(regex=self.dummies_prefix).sum(axis=1)
        holidays_df.reset_index(inplace=True)
        holidays_df.rename(columns={'index': 'date'}, inplace=True)

        logger.info('[holidays_dummies_df]: Holiday dummies created')
        return holidays_df



