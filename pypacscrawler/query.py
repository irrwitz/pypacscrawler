# Finds out the time ranges for a given day
import sys
import logging
import datetime as datetime
import pandas as pd

from typing import List, Dict
from pypacscrawler.command import basic_query, add_time, add_day, \
    add_modality, year_start_end, add_accession_number, MODALITIES, INITIAL_TIME_RANGE
from pypacscrawler.time import split
from pypacscrawler.executor import run


def query_accession_number(config, accession_number):
    query = basic_query(config)
    query = add_accession_number(query, accession_number)
    result, _ = run(query)
    return [result]


def get_months_of_year(year: str) -> List[Dict[str, str]]:
    start, end = year_start_end(year)
    # MS is month start frequency
    return [d.strftime('%Y-%m') for d in pd.date_range(start, end, freq='MS')]


def query_month(config, year_month: str) -> List[Dict[str, str]]:
    start = datetime.datetime.strptime(year_month, '%Y-%m')
    end = start + pd.tseries.offsets.MonthEnd()
    results = []
    for day in pd.date_range(start, end):
        for mod in MODALITIES:
            results.extend(query_day_extended(config, mod, day, INITIAL_TIME_RANGE))
    return results


def query_day(config, day: str) -> List[Dict[str, str]]:
    query_date = datetime.datetime.strptime(day, '%Y-%m-%d')
    results = []
    for mod in MODALITIES:
        results.extend(query_day_extended(config, mod, query_date, INITIAL_TIME_RANGE))
    return results


def query_day_extended(config, mod: str, day: datetime.datetime, time_range: str) -> List[Dict[str, str]]:
    query = prepare_query(config, mod, day, time_range)
    result, size = run(query)

    if size < 500:
        sys.stdout.write('.')
        sys.stdout.flush()
        return [result]
    else:
        sys.stdout.write('|')
        sys.stdout.flush()
        logging.debug('results >= 500 for {} {} {}, splitting'
              .format(mod, day, time_range))
        l, r = split(time_range)
        return query_day_extended(config, mod, day, l) + query_day_extended(config, mod, day, r)


def prepare_query(config, mod, day, time_range):
    query = add_day(basic_query(config), day)
    query = add_modality(query, mod)
    query = add_time(query, time_range)
    return query
