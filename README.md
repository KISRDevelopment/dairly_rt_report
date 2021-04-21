# Time-Dependent Reproductive Number Reporter

This repository contains Python and R code that KISR and Kuwait University have developed to compute the time-dependent reproductive number R(t). 

## Installation Instructions

1. Install R 
2. Install Python 3.6+
3. Open a Terminal. Clone the repository and move into the application's directory:
```bash
$ git clone https://github.com/KISRDevelopment/dairly_rt_report.git
$ cd daily_rt_report
```
4. Create a virtual environment for Python, activate it, and install the application's dependencies. A virtual environment is an isolated environment where you can install application specific packages without affecting the global Python environment. 
```bash
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

## Running Instructions

1. Place the  `Swabs Processed.xlsx` file in the `daily_rt_report` directory. Make sure it's name is exactly as shown.
2. Open the terminal and navigate to the `daily_rt_report` directory and activate the Python environment.
```bash
$ cd daily_rt_report
$ . venv/bin/activate
```
3. To generate the weekly report:
```bash
$ python reporter.py report_weekly.json
```
For the daily report:
```bash
$ python reporter.py report_daily.json
```
4. This command will create an HTML report page at `daily_rt_report/tmp/report_weekly/r0td_report.html`.
5. Open the HTML page in Google Chrome and print it to PDF.

## Report parameters

The parameters of the generated reports can be adjusted by changing the JSON configuration file. These parameters include the countries that are covered, whether or not adjust for swabs, the number of days to aggregate, the generation time parameters, and so on.