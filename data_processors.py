import pandas as pd 
import numpy as np 

class Aggregator:

    def __init__(self):
        pass
    def run(self, df, n_days):

        if n_days == 1:
            return df 

        agg_rows = []
        curr_day = 0
        for i, r in df.iterrows():

            # create new row 
            if curr_day % n_days == 0:
                row = {}
                row['date'] = r['date']
                row['cases'] = r['cases']
                row['swabs'] = r['swabs']
                agg_rows.append(row)
            else:
                row = agg_rows[-1]
                row['cases'] += r['cases']
                row['swabs'] += r['swabs']
            
            curr_day += 1
        
        # drop incomplete data
        if curr_day % n_days != 0:
            agg_rows = agg_rows[:-1]
        
        agg_df = pd.DataFrame(agg_rows)

        return agg_df

class SamplingCorrector:

    def __init__(self):
        pass
    def run(self, df, adjust_for_swabs):
        orig_case_counts = np.array(df['cases'])
    
        case_counts = np.array(df['cases'])
        
        swabs = np.array(df['swabs'])
        
        ix_not_nan = ~np.isnan(swabs)

        if adjust_for_swabs and np.sum(ix_not_nan) > 0:
            baseline_swabs = swabs[np.where(ix_not_nan)[0][0]]
            case_counts[ix_not_nan] = (case_counts[ix_not_nan] / swabs[ix_not_nan]) * baseline_swabs
            case_counts = case_counts.astype(int)
    
        case_counts[case_counts == 0] = 1

        df['orig_cases'] = orig_case_counts
        df['ppos'] = orig_case_counts / swabs
        df['adjusted'] = ix_not_nan
        df['cases'] = case_counts
    
        return df

def main():

    import data_loaders
    loader = data_loaders.KuwaitDataLoader('base_kuwait_data.xlsx', 'data/Swabs Processed.xlsx')
    df = loader.load('all')
    
    proc_agg = Aggregator()
    df = proc_agg.run(df, 7)
    print(df)
    
    proc_corr = SamplingCorrector()
    print(proc_corr.run(df, True))

if __name__ == "__main__":
    main()
