import pandas as pd 
import numpy as np 
import requests
import io 

GROUPS = {
    'all' : ('swabs', 'pos'),
    'kw' : ('swabs_kw_citizens', 'pos_kw_citizens'),
    'nonkw' : ('swabs_nonkw_citizens', 'pos_nonkw_citizens'),
}
class KuwaitDataLoader:

    def __init__(self, base_path, swabs_path):

        base_df = pd.read_excel(base_path)
        base_df['date'] = pd.to_datetime(base_df['date'])

        swabs_df = pd.read_excel(swabs_path, header=2)
        swabs_df = swabs_df[:-1]
        
        top = base_df
        bottom = pd.DataFrame({ "date" : swabs_df["Case_Date"], 
                                "swabs" : swabs_df["Swabs Processed"],
                                "pos" : swabs_df["TotalPositive"],
                                "swabs_kw_citizens" : swabs_df["Total Kuwaiti"],
                                "pos_kw_citizens" : swabs_df["TotalKuwaiti"],
                                "swabs_nonkw_citizens" : swabs_df["Total NonKuwaiti"],
                                "pos_nonkw_citizens" : swabs_df["Total Non-Kuwaiti"]
        })
        
        self.df = top.append(bottom, ignore_index=True)
        self.df.sort_values(by='date', inplace=True)
        self.df.index = np.arange(self.df.shape[0])

    def load(self, group):
        swabs_col, cases_col = GROUPS[group]

        sdf = self.df[['date', cases_col, swabs_col]].copy()
        sdf.columns = ['date', 'cases', 'swabs']
        
        return sdf

class JohnsHopkinsDataLoader:

    def __init__(self, url):

        r = requests.get(url)
        if r.ok:
            data = r.content.decode('utf8')
            global_df = pd.read_csv(io.StringIO(data))
        else:
            raise Exception("Couldn't fetch data")

        #global_df = pd.read_csv('data/glob.csv')

        cols = global_df.columns[4:]
        self.df = global_df
        self.cols = cols 
        self.dates = pd.to_datetime(cols)
        

    def load(self, country):
        
        df = self.df 
        cols = self.cols 
        
        ix = df['Country/Region'] == country
    
        cum_cases = np.array(df[ix][cols])[0]
        
        first_nonzero_ix = np.argmax(cum_cases > 0)
        
        cum_cases = cum_cases[first_nonzero_ix:]
        dates = self.dates[first_nonzero_ix:]
        cases = np.diff(cum_cases, n=1, prepend=0)
        
        country_df = pd.DataFrame({ "date" : dates,  "cases" : cases, "swabs" : np.nan })

        return country_df

    def store(self, path):
        self.df.to_csv(path, index=False)
def main():

    loader = KuwaitDataLoader('base_kuwait_data.xlsx', 'data/Swabs Processed.xlsx')
    df = loader.load('all')
    print(df)

    # df = loader.load('kw')
    # print(df)

    # df = loader.load('nonkw')
    # print(df)

    # loader = JohnsHopkinsDataLoader("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    # df = loader.load('Germany')
    # print(df)

    # df = loader.load('US')
    # print(df)
    # loader.store('data/global.csv')

if __name__ == "__main__":
    main()
