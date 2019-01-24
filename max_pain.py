import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import sys
from playsound import playsound

from utilities import *
import argparse
parser =argparse.ArgumentParser(description = 'Get Live bar graph data of Option Chain')
parser.add_argument('-l','--link',type=str,metavar='',default = 'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=-9999&symbol=BANKNIFTY&symbol=BANKNIFTY&instrument=OPTIDX&date=-&segmentLink=17&segmentLink=17',help = 'Link of the required Derivative')
parser.add_argument('-p','--pointsnum',type=int,default=7,metavar='',help='Number of points required on either side')
##parser.add_argument('-q','--quantity',type=str,default='OI', metavar='',help='What you want to plot')
args = parser.parse_args()
##style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
data1 = np.zeros(1)
def animate(i):
    web_data = nse_data(args.link)
    ##Get Data
    global data1
    data = np.asarray(web_data["Data"])
    if not np.array_equal(data1,data):
        playsound('notification.wav')
    ##Total Size of Chart
    ##mid_value = data.shape[0]
    values_from_mid = args.pointsnum
    spot_price = web_data["Price"]
    mid_value =  np.argmin(np.abs(data[:,10]-spot_price))
    ##Number of prices you want
    index_start = int(mid_value - values_from_mid)
    index_end = int(mid_value + values_from_mid)
    bar_width = 0.35
    ## Annotations we need
    strike_prices = data[index_start:index_end,10]
    #for index in range(len(web_data["Headers"])):
    #    if web_data["Headers"][index] == args.quantity :
    #        break
    index = 0
    indices = np.arange(index_end-index_start)
    y1 = data[index_start:index_end,index].astype(float)
    y2 = data[index_start:index_end,-1-index].astype(float)
    z = []
    for element in strike_prices:
        ans = 0
        diff_in_strike  = strike_prices-element
        for i in range(len(diff_in_strike)):
            ans = ans + np.max([diff_in_strike[i]*-1*y1[i],diff_in_strike[i]*y2[i]])
        z.append(ans)
            
    ax1.clear()
    ax1.bar(indices,z,bar_width,color='b',label = '')
    ax1.set_xlabel('Strike Prices')
    ax1.set_ylabel('Pain')
    ax1.set_title('Max Pain Chart'+  ' with Spot Price : '+ str(web_data["Price"]))
    ax1.set_xticks(indices +bar_width/ 2)
    ax1.set_xticklabels(strike_prices,rotation=90)
    ax1.legend()
    ax1.grid()
    data1 = data

ani = animation.FuncAnimation(fig,animate,interval=10000)
plt.show()

