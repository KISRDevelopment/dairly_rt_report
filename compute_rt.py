import numpy as np 
import subprocess 
import json 
import pandas as pd 
import uuid 
import os 
import scipy.stats as stats

def main():
    
    df = pd.read_excel('data/allcases.xlsx')

    rdf = compute_rt(df, date_col='Date', case_col='Positives Kuwait')
    rdf.to_csv('data/tmp.csv',index=False)
    
def adjust_lognormal_params(mu_x, std_x, days):

    logmean = np.log(np.power(mu_x,2) / np.sqrt(np.power(mu_x,2) + np.power(std_x, 2)))
    logstd = np.sqrt(np.log(1+np.power(std_x / mu_x, 2)))

    adj_logmean = logmean + np.log(1/days)

    new_mu_x = np.exp(adj_logmean + np.power(logstd, 2) / 2)

    return (new_mu_x, std_x)

def compute_rt( df, 
                date_col = 'date', 
                case_col = 'cases',
                gt_distrib = 'lognormal',
                gt_distrib_mean = 4.7,
                gt_distrib_std = 2.9, **kwargs):

    
    cases = np.array(df[case_col])
    
    input_df = pd.DataFrame({ "cases" : cases })

    input_path = str(uuid.uuid4())
    output_path = input_path + "_result"

    input_df.to_csv(input_path, index=False)

    r = subprocess.call(["Rscript", "compute_rt.r", 
        input_path, gt_distrib, 
        str(gt_distrib_mean), str(gt_distrib_std),
        output_path
    ])

    if r != 0:
        return None 
    
    result_df = pd.read_csv(output_path)
    os.remove(input_path)
    os.remove(output_path)

    result_df.columns = ["id", "y", "yhat", "r", "r_lower", "r_upper", "mean_r0", "mean_r0_lower", "mean_r0_upper"]
    result_df = pd.concat([result_df, df], axis=1)
    
    return result_df
    
if __name__ == "__main__":
    main()
