import json
import numpy as np 
import pandas as pd
import data_loaders
import data_processors
import compute_rt 
import figures 
def main():

    with open('report_config.json', 'r') as f:
        cfg = json.load(f)
    
    
    for name in cfg['dfs'].keys():
        final_props = cfg['props'].copy()
        final_props.update(cfg['dfs'][name])
        cfg['dfs'][name] = final_props
    
    # kw_loader = data_loaders.KuwaitDataLoader('base_kuwait_data.xlsx', 'data/Swabs Processed.xlsx')
    # glob_loader = data_loaders.JohnsHopkinsDataLoader("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    # aggregator = data_processors.Aggregator()
    # sample_corrector = data_processors.SamplingCorrector()

    # for name, final_props in cfg['dfs'].items():
    #     loader = kw_loader if final_props['source'] == 'kw' else glob_loader
    #     df = loader.load(final_props['group'])

    #     df = aggregator.run(df, final_props['aggregate'])
    #     df = sample_corrector.run(df, final_props['adjust_for_swabs'])
        
    #     mu_x, std_x = final_props['mean'], final_props['std']
    #     if final_props['aggregate'] != 1:
    #         if final_props['distrib'] == 'lognormal':
    #             mu_x, std_x = compute_rt.adjust_lognormal_params(mu_x, std_x, final_props['aggregate'])
    #         else:
    #             raise Exception("Cannot aggregate with distributions other than lognormal")
        
    #     rdf = compute_rt.compute_rt(df, date_col='date', cases_col='cases', 
    #         gt_distrib=final_props['distrib'], 
    #         gt_distrib_mean=mu_x, gt_distrib_std=std_x)
    #     rdf.to_csv('tmp/%s.csv' % name, index=False)
    

    for name, props in cfg['dfs'].items():

        rdf = pd.read_csv('tmp/%s.csv' % name)

        figures.tdr(rdf, props['title'], 'tmp/%s.png' % name, show_swabs=props['show_swabs'])
    

if __name__ == "__main__":
    main()
