import json
import numpy as np 
import pandas as pd
import data_loaders
import data_processors

def main():

    with open('report_config.json', 'r') as f:
        cfg = json.load(f)
    
    kw_loader = data_loaders.KuwaitDataLoader('base_kuwait_data.xlsx', 'data/Swabs Processed.xlsx')
    glob_loader = data_loaders.JohnsHopkinsDataLoader("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    aggregator = data_processors.Aggregator()
    sample_corrector = data_processors.SamplingCorrector()

    dfs = []
    for name, props in cfg['dfs'].items():
        final_props = cfg['props'].copy()
        final_props.update(props)

        loader = kw_loader if final_props['source'] == 'kw' else glob_loader
        df = loader.load(final_props['group'])

        df = aggregator.run(df, final_props['aggregate'])
        df = sample_corrector.run(df, final_props['adjust_for_swabs'])
        
        final_props['df'] = df
        dfs.append(final_props)
    
    

if __name__ == "__main__":
    main()
