import web_scraping_yield_curve
import compile_yc_data
import fit_data
import visualize_data
import pandas as pd
import sys

if __name__ == '__main__':
    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])
    web_scraping_yield_curve.get_data(start_year, end_year)
    compiled_data, filename = compile_yc_data.compile_data(start_year, end_year, fillgap=True)
    print('Compiled Data in:', filename)

    df_coeffs = fit_data.fit_data(compiled_data, degree=3)
    df_coeffs.to_csv('Data/cubic_fit.csv')

    visualize_data.view_surface(df_coeffs)


