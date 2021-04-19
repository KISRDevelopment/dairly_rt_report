import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
from matplotlib import gridspec
from matplotlib.dates import DateFormatter

plt.rcParams["font.family"] = "Liberation Serif"
plt.rcParams["font.weight"] = "bold"

plot_cfg = {
    "tick_label_size" : 32,
    "axis_label_size" : 38,
    "capthick" : 5,
    "capsize" : 10,
    "elinewidth" : 5,
    "markersize" : 10,
    "annot_size" : 28,
    "title_size" : 38,
    "suptitle_size" : 42,
    "legend_size" : 24
}
def overview_stats(overview_df, output_path):
    
    f, axes = plt.subplots(2, 1, figsize=(10, 20))

    errors = np.array(overview_df[['rt_lower', 'rt_upper']]).T
    errors[0,:] = overview_df['rt'] - errors[0,:]
    errors[1,:] = errors[1,:] - overview_df['rt']

    ax = axes[0]
    ax.plot([1.0, 1.0], [-0.5, overview_df.shape[0]-0.5], linewidth=5, color='magenta', linestyle='--')
    for i in range(overview_df.shape[0]):
        ax.errorbar(y = [i], x = [overview_df.iloc[i]['rt']], 
            xerr=errors[:,i][:,np.newaxis], 
            fmt='o',
            color=overview_df.iloc[i]['color'], 
            capthick=plot_cfg['capthick'], 
            capsize=plot_cfg['capsize'], 
            elinewidth=plot_cfg['elinewidth'], 
            markersize=plot_cfg['markersize'])
    ax.set_yticks(np.arange(overview_df.shape[0]))
    ax.set_yticklabels(overview_df['title'])
    ax.tick_params(axis='x', labelsize=plot_cfg['tick_label_size'])
    ax.tick_params(axis='y', labelsize=plot_cfg['tick_label_size'])
    ax.set_xlabel('Latest R(t)', fontsize=plot_cfg['axis_label_size'], fontweight='bold')
    ax.set_ylabel('')
    ax.set_xlim([0, 3])
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    xlims = ax.get_xlim()
    ax.grid(linestyle='-.', which='both')

    ax = axes[1]
    errors = np.array(overview_df[['mean_r0_lower', 'mean_r0_upper']]).T
    errors[0,:] = overview_df['mean_r0'] - errors[0,:]
    errors[1,:] = errors[1,:] - overview_df['mean_r0']
    ax.plot([1.0, 1.0], [-0.5, overview_df.shape[0]-0.5], linewidth=5, color='magenta', linestyle='--')
    for i in range(overview_df.shape[0]):
        ax.errorbar(y = [i], x = [overview_df.iloc[i]['mean_r0']], 
            xerr=errors[:,i][:,np.newaxis], 
            fmt='o',
            color=overview_df.iloc[i]['color'], 
            capthick=plot_cfg['capthick'], 
            capsize=plot_cfg['capsize'], 
            elinewidth=plot_cfg['elinewidth'], 
            markersize=plot_cfg['markersize'])
    ax.set_yticks(np.arange(overview_df.shape[0]))
    ax.set_yticklabels(overview_df['title'])
    ax.tick_params(axis='x', labelsize=plot_cfg['tick_label_size'])
    ax.tick_params(axis='y', labelsize=plot_cfg['tick_label_size'])
    ax.set_xlabel('Average R0', fontsize=plot_cfg['axis_label_size'], fontweight='bold')
    ax.set_ylabel('')
    ax.set_xlim(xlims)
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    ax.grid(linestyle='-.', which='both')

    plt.savefig(output_path,  pad_inches=0.1,bbox_inches='tight')

def tdr(result_df, title, output_path, 
           show_swabs=True, 
           with_labels=True, 
           labelsize=plot_cfg['tick_label_size'], 
           axis_labelsize=plot_cfg['axis_label_size'], 
           annot_size=plot_cfg['annot_size'], 
           title_size=plot_cfg['title_size'], 
           suptitle_size=plot_cfg['suptitle_size'], 
           markersize=plot_cfg['markersize'], 
           linewidth=plot_cfg['elinewidth'], 
           legend_size=plot_cfg['legend_size'],
           show_ppos=True, **kwargs):

    result_df['date'] = pd.to_datetime(result_df['date'])
    annot_idx = -1
    
    mean_r0 = result_df['mean_r0'].iloc[0]
    mean_r0_lower = result_df['mean_r0_lower'].iloc[0]
    mean_r0_upper = result_df['mean_r0_upper'].iloc[0]
    avgR_str = "Average R0:\n%0.2f (%0.2f - %0.2f)" % (mean_r0, mean_r0_lower, mean_r0_upper)

    if show_swabs:
        fig = plt.figure(figsize=(20,15))
        spec = gridspec.GridSpec(nrows=4, ncols=1, height_ratios=[1, 0.75, 0.5, 0.5])
    else:
        fig = plt.figure(figsize=(20,10))
        spec = gridspec.GridSpec(nrows=2, ncols=1, height_ratios=[1, 0.75])
        
    ax = fig.add_subplot(spec[0])
    
    dates = np.array(result_df['date'][:-1])
    r = np.array(result_df['r'])[:-1]
    r_lower = np.array(result_df['r_lower'])[:-1]
    r_upper = np.array(result_df['r_upper'])[:-1]
    
    ax.plot(dates, r, linewidth=5)

    ax.fill_between(dates, r_lower, r_upper, alpha=0.2)
    ax.plot(dates, np.ones(dates.shape[0]), color='magenta', linestyle='--', linewidth=5)

    ax.tick_params(axis='x', labelsize=labelsize)
    ax.tick_params(axis='y', labelsize=labelsize)
    ax.set_xlabel('', fontsize=axis_labelsize, fontweight='bold')
    ax.set_ylabel('R(t)', fontsize=axis_labelsize, fontweight='bold')
    ax.grid(linestyle='-.', which='both')
    date_form = DateFormatter("%d %b")
    ax.xaxis.set_major_formatter(date_form)
    plt.setp(ax.get_xticklabels(), visible=False)
    
    if with_labels:
        ax.text(0.5, 0.9, avgR_str, color='black', ha="center", va="top", fontweight='bold', fontsize=annot_size, transform=ax.transAxes)

        rtd_str = "Time-Dependent R: \n%0.2f (%0.2f - %0.2f)" % \
            (r[annot_idx], r_lower[annot_idx], r_upper[annot_idx])

        ax.annotate(rtd_str, xy=(dates[annot_idx], r[annot_idx]),  xycoords='data',
                    xytext=(.98, 0.9), textcoords='axes fraction',
                    fontweight='bold',
                    arrowprops=dict(color='grey', shrink=0.05),
                    fontsize=annot_size,
                    horizontalalignment='right', verticalalignment='top',)
    ax.set_title('Time-Dependant Reproductive Number', fontsize=title_size, fontweight='bold')

    ax = fig.add_subplot(spec[1], sharex=ax)
    
    dates = np.array(result_df['date'])
    yhat = np.array(result_df['yhat'])
    y = np.array(result_df['y'])
    
    adjusted_ix = np.array(result_df['adjusted']) == 1
    
    if np.sum(adjusted_ix) == 0:
        ax.plot(dates, y, linestyle='', marker='o', color='black', markersize=markersize, label='Observed Cases')
    else:
        ax.plot(dates[~adjusted_ix], y[~adjusted_ix], linestyle='', marker='o', color='black', markersize=markersize, label='Observed Cases')
        ax.plot(dates[adjusted_ix], y[adjusted_ix], linestyle='', marker='X', color='#ff9500', markeredgecolor='black', markersize=markersize, label='Adjusted Cases')
        
    ax.plot(dates, yhat, linewidth=linewidth, color='red', label='Predicted Cases')
    
    ax.tick_params(axis='x', labelsize=labelsize)
    ax.tick_params(axis='y', labelsize=labelsize)
    ax.set_ylabel('Cases', fontsize=axis_labelsize, fontweight='bold')
    ax.grid(linestyle='-.', which='both')
    ax.legend(fontsize=legend_size, frameon=False, loc='upper left')
    ax.xaxis.set_major_formatter(date_form)
    ax.set_title('Observed and Predicted Cases', fontsize=title_size, fontweight='bold')
    
    if show_swabs:
        plt.setp(ax.get_xticklabels(), visible=False)
    
    pred_str = "Prediction:\n%0.0f Cases" % yhat[-1]

    if with_labels:
        ax.annotate(pred_str, xy=(dates[-1], yhat[-1]),  xycoords='data',
                    xytext=(.98, 0), textcoords='axes fraction',
                    fontweight='bold',
                    arrowprops=dict(color='grey', width=3, shrink=0.05),
                    fontsize=annot_size,
                    horizontalalignment='right', verticalalignment='bottom',)
    
    
    #
    # plot swabs
    # 
    if show_swabs:
        
        ax = fig.add_subplot(spec[2], sharex=ax)
        swabs = np.array(result_df['swabs'])
        
        ax.bar(dates, swabs, color='#ff9500', edgecolor='black')
        
        ax.set_ylabel('Swabs', fontsize=axis_labelsize, fontweight='bold')
        ax.grid(linestyle='-.', which='both')
        ax.xaxis.set_major_formatter(date_form)
        ax.set_title('Daily Swabs', fontsize=title_size, fontweight='bold')
        ax.tick_params(axis='x', labelsize=labelsize)
        ax.tick_params(axis='y', labelsize=labelsize)
        
        if show_ppos:
            plt.setp(ax.get_xticklabels(), visible=False)

            ax = fig.add_subplot(spec[3], sharex=ax)
            ppos = np.array(result_df['ppos']) * 100
            ax.plot(dates, ppos, 'o-', color='#9000ff')
            ax.tick_params(axis='x', labelsize=labelsize)
            ax.tick_params(axis='y', labelsize=labelsize)
            ax.set_ylabel('%', fontsize=axis_labelsize, fontweight='bold')
            ax.grid(linestyle='-.', which='both')
            
            ax.set_title('Percent Positive', fontsize=title_size, fontweight='bold')
        
        ax.xaxis.set_major_formatter(date_form)

    plt.suptitle(title, fontsize=suptitle_size, fontweight='bold')
    
    plt.savefig(output_path,  pad_inches=0.1 ,bbox_inches='tight')
    
    plt.close()
