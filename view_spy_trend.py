import web_scraping_yield_curve
import compile_yc_data
import sample_data
import visualize_data
import fit_data
import sys
import pandas as pd

if __name__ == '__main__':
    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])

    web_scraping_yield_curve.get_data(start_year, end_year)
    compiled_data, name = compile_yc_data.compile_data(start_year,end_year)
    print('Compiled Data in:', name)

    df_stats = fit_data.fit_data(compiled_data, degree = 1)
    df_stats.drop(compiled_data.columns.difference(['slope']), 1, inplace=True)
    df_stats.to_csv('Data/all_slopes.csv')

    spy_yc_file = compile_yc_data.add_spy_data()

    visualize_data.visualize_trends(spy_yc_file)