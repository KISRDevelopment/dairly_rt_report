import json
import numpy as np 
import pandas as pd
import data_loaders
import data_processors
import compute_rt 
import figures
from string import Template
import datetime 
import sys 
import os 
def main():
    path = sys.argv[1]

    with open(path, 'r') as f:
        cfg = json.load(f)
    
    if not os.path.isdir('./tmp/%s' % cfg['name']):
        os.mkdir('./tmp/%s' % cfg['name'])
    
    cfg = finalize_props(cfg)
    
    compute_tdr(cfg)
    compute_overview(cfg)
    make_tdr_figures(cfg)
    make_overview_figures(cfg)
    make_report(cfg)

def finalize_props(cfg):

    for name in cfg['dfs'].keys():
        final_props = cfg['props'].copy()
        final_props.update(cfg['dfs'][name])
        cfg['dfs'][name] = final_props
    
    return cfg 

def compute_tdr(cfg):

    kw_loader = data_loaders.KuwaitDataLoader('base_kuwait_data.xlsx', 'data/Swabs Processed.xlsx')
    glob_loader = data_loaders.JohnsHopkinsDataLoader("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    aggregator = data_processors.Aggregator()
    sample_corrector = data_processors.SamplingCorrector()

    
    for name, final_props in cfg['dfs'].items():
        loader = kw_loader if final_props['source'] == 'kw' else glob_loader
        df = loader.load(final_props['group'])

        df = aggregator.run(df, final_props['aggregate'])
        df = sample_corrector.run(df, final_props['adjust_for_swabs'])
        
        mu_x, std_x = final_props['mean'], final_props['std']
        if final_props['aggregate'] != 1:
            if final_props['distrib'] == 'lognormal':
                mu_x, std_x = compute_rt.adjust_lognormal_params(mu_x, std_x, final_props['aggregate'])
            else:
                raise Exception("Cannot aggregate with distributions other than lognormal")
        
        rdf = compute_rt.compute_rt(df, date_col='date', cases_col='cases', 
            gt_distrib=final_props['distrib'], 
            gt_distrib_mean=mu_x, gt_distrib_std=std_x)
        rdf.to_csv('tmp/%s/%s.csv' % (cfg['name'], name), index=False)

        

def compute_overview(cfg):
    rows = []

    for name, props in cfg['dfs'].items():
        if not props['in_overview']:
            continue 
        
        rdf = pd.read_csv('tmp/%s/%s.csv' % (cfg['name'], name))

        rows.append({
            "name" : name, 
            "color" : props['color'],
            "title" : props['title'],
            "cumcases" : np.sum(rdf['cases']),
            "rt" : rdf['r'].iloc[-2],
            "rt_lower" : rdf['r_lower'].iloc[-2],
            "rt_upper" : rdf['r_upper'].iloc[-2],
            "mean_r0" : rdf['mean_r0'].iloc[0],
            "mean_r0_lower" : rdf['mean_r0_lower'].iloc[-1],
            "mean_r0_upper" : rdf['mean_r0_upper'].iloc[-1]
        })

    overview_df = pd.DataFrame(rows)
    overview_df.to_csv('tmp/%s/overview.csv' % cfg['name'], index=False)

def make_tdr_figures(cfg):
    for name, props in cfg['dfs'].items():
        rdf = pd.read_csv('tmp/%s/%s.csv' % (cfg['name'], name))
        figures.tdr(rdf, props['title'], 'tmp/%s/%s.png' % (cfg['name'], name), show_swabs=props['show_swabs'], show_ppos=props['show_ppos'])

def make_overview_figures(cfg):
    overview_df = pd.read_csv('tmp/%s/overview.csv' % cfg['name'])
    figures.overview_stats(overview_df, 'tmp/%s/overview.png' % cfg['name'])

def make_report(cfg):

    today_date = datetime.datetime.now()

    template_html = """
<section class="sheet padding-10mm">
    <article>
    <h1>%s</h1>
    <h2>As of %s</h2>
    <br>
    <img src="./overview.png" style="height: 768px; margin: auto; display: block" />
    </article>
    </section>
    """ % (cfg['title'], today_date.strftime("%d %B %Y"))

    for name, props in cfg['dfs'].items():
        template_html += """
    <section class="sheet padding-10mm">
    <article>
    <img src="./%s.png" style="width:100%%"/>
    </article>
    </section>
    """ % name

    with open('r0_td_template.html', 'r') as f:
        html = f.read()
    
    t = Template(html)

    result = t.substitute(body=template_html)
    
    with open('tmp/%s/r0td_report.html' % cfg['name'], 'w') as f:
        f.write(result)
if __name__ == "__main__":
    main()
