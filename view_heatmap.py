import web_scraping_yield_curve
import compile_yc_data
import sample_data
import visualize_data
import sys

if __name__ == '__main__':
    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])

    web_scraping_yield_curve.get_data(start_year, end_year)
    compiled_data, name = compile_yc_data.compile_data(start_year,end_year, fillgap = True)
    print('Compiled Data in:', name)

    sampled_data, name = sample_data.sample_data(compiled_data, name)
    visualize_data.visualize_data(name)