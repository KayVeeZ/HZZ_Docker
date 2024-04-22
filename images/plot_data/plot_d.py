from queue import Queue
import pika
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import os
import json
import pandas as pd
import pickle
import datetime
# import msgpack



samples = {

    'data': {
        'list' : ['data_A','data_B','data_C','data_D'],
    },

    r'Background $Z,t\bar{t}$' : { # Z + ttbar
        'list' : ['Zee','Zmumu','ttbar_lep'],
        'color' : "#6b59d3" # purple
    },

    r'Background $ZZ^*$' : { # ZZ
        'list' : ['llll'],
        'color' : "#ff0000" # red
    },

    r'Signal ($m_H$ = 125 GeV)' : { # H -> ZZ -> llll
        'list' : ['ggH125_ZZ4lep','VBFH125_ZZ4lep','WH125_ZZ4lep','ZH125_ZZ4lep'],
        'color' : "#00cdff" # light blue
    },

}

# import variables
GeV = 1.0
lumi = 10  # fb-1 # data_A,data_B,data_C,data_D
fraction = 1.0  # reduce this is if you want the code to run quicker


def plot_data(df, signal_color, mc_labels):
    # Your plotting code here
    xmin = 80 * GeV
    xmax = 250 * GeV
    step_size = 5 * GeV

    bin_edges = np.arange(start=xmin,  # The interval includes this value
                           stop=xmax + step_size,  # The interval doesn't include this value
                           step=step_size)  # Spacing between values
    bin_centres = np.arange(start=xmin + step_size / 2,  # The interval includes this value
                            stop=xmax + step_size / 2,  # The interval doesn't include this value
                            step=step_size)  # Spacing between values

    # processing dataframe
    # Extract variables from DataFrame
    data_x = df['data_x'].values
    signal_x = df['signal_x'].values
    signal_weights = df['signal_weights'].values
    mc_colors = df['mc_colors'].values
    mc_x_a = df['mc_x_a'].values
    mc_x_b = df['mc_x_b'].values
    mc_weights_a = df['mc_weights_a'].values
    mc_weights_b = df['mc_weights_b'].values

    # functions to perform
    def rem_nan(arr1):
        filtered_iterator = filter(lambda x: x != 'nan', arr1)
        arr1 = list(filtered_iterator)
        return arr1

    def rem_nan1(arr1):
        cleaned_list = [x for x in arr1 if not np.isnan(x)]
        return cleaned_list

    # remove nan types
    data_x = np.array(rem_nan1(data_x)).astype(int)
    signal_x = np.array(rem_nan1(signal_x))
    signal_weights = np.array(rem_nan1(signal_weights))
    mc_x_a = np.array(rem_nan1(mc_x_a))
    mc_x_b = np.array(rem_nan1(mc_x_b))
    mc_weights_a = np.array(rem_nan1(mc_weights_a))
    mc_weights_b = np.array(rem_nan1(mc_weights_b))
    mc_colors = rem_nan(mc_colors)

    data_x_errors = np.sqrt( data_x ) # statistical error on the data

    # merge the separated arrays
    mc_x = [mc_x_a, mc_x_b]
    mc_weights = [mc_weights_a, mc_weights_b]

    # *************
    # Main plot
    # *************
    main_axes = plt.gca()  # get current axes

    # plot the data points
    main_axes.errorbar(x=bin_centres, y=data_x, yerr=data_x_errors,
                        fmt='ko',  # 'k' means black and 'o' is for circles
                        label='Data')

    # plot the Monte Carlo bars
    mc_heights = main_axes.hist(mc_x, bins=bin_edges,
                                 weights=mc_weights, stacked=True,
                                 color=mc_colors, label=mc_labels)

    mc_x_tot = mc_heights[0][-1]  # stacked background MC y-axis value

    # calculate MC statistical uncertainty: sqrt(sum w^2)
    mc_x_err = np.sqrt(np.histogram(np.hstack(mc_x), bins=bin_edges, weights=np.hstack(mc_weights) ** 2)[0])

    # plot the signal bar
    main_axes.hist(signal_x, bins=bin_edges, bottom=mc_x_tot,
                   weights=signal_weights, color=signal_color,
                   label=r'Signal ($m_H$ = 125 GeV)')

    # plot the statistical uncertainty
    main_axes.bar(bin_centres,  # x
                   2 * mc_x_err,  # heights
                   alpha=0.5,  # half transparency
                   bottom=mc_x_tot - mc_x_err, color='none',
                   hatch="////", width=step_size, label='Stat. Unc.')

    # set the x-limit of the main axes
    main_axes.set_xlim(left=xmin, right=xmax)

    # separation of x axis minor ticks
    main_axes.xaxis.set_minor_locator(AutoMinorLocator())

    # set the axis tick parameters for the main axes
    main_axes.tick_params(which='both',  # ticks on both x and y axes
                           direction='in',  # Put ticks inside and outside the axes
                           top=True,  # draw ticks on the top axis
                           right=True)  # draw ticks on right axis

    # x-axis label
    main_axes.set_xlabel(r'4-lepton invariant mass $\mathrm{m_{4l}}$ [GeV]',
                         fontsize=13, x=1, horizontalalignment='right')

    # write y-axis label for main axes
    main_axes.set_ylabel('Events / ' + str(step_size) + ' GeV',
                         y=1, horizontalalignment='right')

    # set y-axis limits for main axes
    main_axes.set_ylim(bottom=0, top=np.amax(data_x) * 1.6)

    # add minor ticks on y-axis for main axes
    main_axes.yaxis.set_minor_locator(AutoMinorLocator())

    # Add text 'ATLAS Open Data' on plot
    plt.text(0.05,  # x
              0.93,  # y
              'ATLAS Open Data',  # text
              transform=main_axes.transAxes,  # coordinate system used is that of main_axes
              fontsize=13)

    # Add text 'for education' on plot
    plt.text(0.05,  # x
              0.88,  # y
              'for education',  # text
              transform=main_axes.transAxes,  # coordinate system used is that of main_axes
              style='italic',
              fontsize=8)

    # Add energy and luminosity
    lumi_used = str(lumi * fraction)  # luminosity to write on the plot
    plt.text(0.05,  # x
              0.82,  # y
              '$\sqrt{s}$=13 TeV,$\int$L dt = ' + lumi_used + ' fb$^{-1}$',  # text
              transform=main_axes.transAxes)  # coordinate system used is that of main_axes

    # Add a label for the analysis carried out
    plt.text(0.05,  # x
              0.76,  # y
              r'$H \rightarrow ZZ^* \rightarrow 4\ell$',  # text
              transform=main_axes.transAxes)  # coordinate system used is that of main_axes

    # draw the legend
    main_axes.legend(frameon=False)  # no box around the legend

    # Create the directory if it doesn't exist
    save_dir = './static/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Save the plot to a file
    plt_path = os.path.join(save_dir, f'plot_{datetime.datetime.now().strftime("%d_%m_%y")}-{datetime.datetime.now().strftime("%H_%M")}.png')
    plt.savefig(plt_path)

    # Close the plot to release resources
    plt.close()

    # Return the path to the saved plot
    return

# Define global variables to store DataFrame, array, and list
df = None
signal_color = None
mc_labels = None

def callback(ch, method, properties, body):
    global df, signal_color, mc_labels

    # Deserialize the message using pickle
    data = pickle.loads(body)

    # Extract data from the message
    df = data['dataframe']
    signal_color = data['array']
    mc_labels = data['list']

    # Print array
    print("Array:")
    print(signal_color)

    # Print list
    print("List:")
    print(mc_labels)
    plot_data(df, signal_color, mc_labels)
    print('done plotting')

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('172.30.160.1'))
channel = connection.channel()

channel.queue_declare(queue='my_queue')

# Set up the callback function for messages
channel.basic_consume(queue='my_queue', on_message_callback=callback)

# Start consuming messages
print("Waiting for messages...")
channel.start_consuming()
print(signal_color)

plot_data(df, signal_color, mc_labels)
print('done plotting')