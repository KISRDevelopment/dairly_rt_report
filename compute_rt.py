#
# compute_rt.py - Computes Time Dependent Reproductive Number
# Mohammad M Khajah <mmkhajah@kisr.edu.kw>
#
# provides a wrapper interface over the R script that computes R(t).
#
import numpy as np 
import subprocess 
import json 
import pandas as pd 
import uuid 
import os 
import scipy.stats as stats

def main():

    df = pd.read_excel('data/allcases.xlsx')
    days = 7
    gt_distrib_mean = 4.7 # in days
    gt_distrib_std = 2.9 # in days

    mu_x, std_x = adjust_lognormal_params(gt_distrib_mean, gt_distrib_std, 7)
    
    agg_df = aggregate_df(df, days, date_col='Date', case_col='Positives Kuwait', swabs_col='Swabs Kuwait')
    
    
    r = compute_rt(agg_df, case_col='Positives Kuwait', swabs_col='Swabs Kuwait', adjust_for_swabs=False,
        gt_distrib_mean = mu_x,
        gt_distrib_std = std_x
    )

    print(r)
    
def adjust_lognormal_params(mu_x, std_x, days):

    logmean = np.log(np.power(mu_x,2) / np.sqrt(np.power(mu_x,2) + np.power(std_x, 2)))
    logstd = np.sqrt(np.log(1+np.power(std_x / mu_x, 2)))

    adj_logmean = logmean + np.log(1/days)

    new_mu_x = np.exp(adj_logmean + np.power(logstd, 2) / 2)

    return (new_mu_x, std_x)

def aggregate_df(df, days, date_col, case_col, swabs_col):

    agg_rows = []
    curr_day = 0
    for i, r in df.iterrows():

        # create new row 
        if curr_day % days == 0:
            row = {}
            row[date_col] = r[date_col]
            row[case_col] = r[case_col]
            row[swabs_col] = r[swabs_col]
            agg_rows.append(row)
        else:
            row = agg_rows[-1]
            row[case_col] += r[case_col]
            row[swabs_col] += r[swabs_col]
        
        curr_day += 1
    
    # drop incomplete data
    if curr_day % days != 0:
        agg_rows = agg_rows[:-1]
    
    agg_df = pd.DataFrame(agg_rows)

    return agg_df

def compute_rt( df, 
                date_col = 'Date', 
                case_col = 'CaseCounter', 
                swabs_col = 'CaseCounter',
                adjust_for_swabs = False,
                gt_distrib = 'lognormal',
                gt_distrib_mean = 4.7,
                gt_distrib_std = 2.9, **kwargs):

    orig_case_counts = np.array(df[case_col])
    
    case_counts = np.array(df[case_col])
    
    swabs = np.array(df[swabs_col])
    
    if adjust_for_swabs:
        
        ix_not_nan = ~np.isnan(swabs)
        baseline_swabs = swabs[np.where(ix_not_nan)[0][0]]
        case_counts[ix_not_nan] = (case_counts[ix_not_nan] / swabs[ix_not_nan]) * baseline_swabs
        case_counts = case_counts.astype(int)
    else:
        ix_not_nan = np.zeros(df.shape[0]).astype(bool)
    
    case_counts[case_counts == 0] = 1

    input_df = pd.DataFrame({ "CaseCounter" : case_counts })

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
    result_df['date'] = np.array(df[date_col])
    result_df['adjusted'] = ix_not_nan
    result_df['orig_y'] = orig_case_counts
    result_df['swabs'] = swabs
    
    return result_df
    
if __name__ == "__main__":
    main()
