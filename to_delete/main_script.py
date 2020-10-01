import web_scraping_yield_curve
import compile_yc_data
import sample_data
import visualize_data
from to_delete import stats_funcs
import sys
import pandas as pd

if __name__ == '__main__':
    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])

    web_scraping_yield_curve.get_data(start_year, end_year)
    compiled_data_name = compile_yc_data.compile_data(start_year,end_year)
    compiled_data = pd.read_csv('Data/{}.csv'.format(compiled_data_name))
    compiled_data.set_index('Date', inplace=True)
    print('Compiled Data in:', compiled_data_name)

    sampled_data = sample_data.sample_data(compiled_data_name)
    visualize_data.visualize_data(sampled_data)

    df_stats = stats_funcs.get_stats(compiled_data_name)
    df_stats.drop(compiled_data.columns.difference(['log_slope']), 1, inplace=True)
    df_stats.to_csv('Data/all_slopes.csv')

    spy_yc_file = web_scraping_yield_curve.add_spy_data()

    visualize_data.visualize_trends(spy_yc_file)

