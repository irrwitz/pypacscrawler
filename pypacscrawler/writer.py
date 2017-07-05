import logging
import os
import pandas as pd

OUTPUT_DIR = 'data'


def _get_file_name(month: str, day: str, mod: str):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    file_name = os.path.join(OUTPUT_DIR, 'data-')
    if month:
        return file_name + month
    else:
        return file_name + day + '-' + mod


def write_results(results, month, day, mod):
    # type: (List[Dict[str, str]], str, str, str) -> None
    file_name = _get_file_name(month, day, mod)
    frames = pd.concat([pd.DataFrame(x) for x in results if len(x) > 0])
    logging.info('Writing results to file %s', file_name)
    frames.to_csv(file_name + '.csv', index=False, sep=';')
    frames.to_json(file_name+ '.json', orient='records')
