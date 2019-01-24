import requests
import lxml.html as lh
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from functools import partial
from matplotlib import style
def nse_data(url):

    url = url
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    ##final output dictionary
    output  = {}
    ##0. Help
    output['Help'] = {1 : "Name",2:"Price",3 : "Time",4: "Expiry",5: "Headers",6: "Data",7: "Total_C_and_P"}
    ##1.Name,2.Price,3.Time,4.Expiry
    string1 = doc.xpath('//*[@id="wrapper_btm"]/table[1]')[0].text_content()
    string1  = string1.replace('\r','')
    string1  = string1.replace('\n','')
    string1  = string1.replace('\t','')
    string1  = string1.replace('Option Chain (Equity Derivatives)Underlying Index: ','')
    data1 = string1.split(' ')
    output["Name"] = data1[0]
    output["Price"] = float(data1[1].replace('\xa0As',''))
    output["Time"] = data1[6]
    output["Expiry"] = data1[4].replace(',','') + ' ' +data1[3] + ' '+ data1[5]
    ##5. Headers
    string2 = doc.xpath('//*[@id="octable"]/thead/tr[2]')[0].text_content()
    string2 = string2.replace('\t','')
    data2 = string2.split('\r\n')
    data2 = data2[3:len(data2)-2]
    data2.remove('')
    data2.remove('')
    output["Headers"] = data2
    ##6. Data and 7. Total Cand P
    string3 =doc.xpath('//*[@id="octable"]')[0].text_content()
    string3 = string3.replace('\t','')
    data3 = string3.split('\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n')
    for i in range(len(data3)):
        data3[i]  = data3[i].replace(',','')
        data3[i] = data3[i].split('\r\n')
        data3[i] = [e for e in data3[i] if e not in ('',' ')]
    data3[0] = data3[0][26:]
    output["Total_C_and_P"] = [float(e) for e in data3[-1][1:len(data3[-1])-1]]
    data3 = data3[:len(data3)-1]
    for i in range(len(data3)):
        for j in range(len(data3[i])):
            if data3[i][j]=='-':
                data3[i][j]=None
            else :
                data3[i][j]= float(data3[i][j][0:])
    output["Data"] = data3



    return output

def bar_graph(url,c_p_or_both='both',values_from_mid = 7,quantity='OI'):
    ##Get URL
    web_data = nse_data(url)
    ##Get Data
    data = np.asarray(web_data["Data"])
    ##Total Size of Chart
    ##mid_value = data.shape[0]
    
    spot_price = web_data["Price"]
    mid_value =  np.argmin(np.abs(data[:,10]-spot_price))
    ##Number of prices you want
    index_start = int(mid_value - values_from_mid)
    print(index_start)
    index_end = int(mid_value + values_from_mid)
    print(index_end)
    ## Annotations we need
    strike_prices = data[index_start:index_end,10]
    for index in range(len(web_data["Headers"])):
        if web_data["Headers"][index] == quantity :
            break
    
    fix ,ax = plt.subplots()
    indices = np.arange(index_end-index_start)
    bar_width = 0.35
    opacity = 0.8
    if c_p_or_both == 'c':
        y1 = data[index_start:index_end,index].astype(float)
        rects1 = plt.bar(indices,y1,bar_width,alpha=opacity,color = 'g',label='Calls')
        plt.xticks(indices + bar_width/2,strike_prices,rotation=90)
    elif c_p_or_both == 'p':
        y2 = data[index_start:index_end,-1-index].astype(float)
        rects2 = plt.bar(indices,y2,bar_width,alpha=opacity,color = 'r',label='Puts')
        plt.xticks(indices + bar_width/2,strike_prices,rotation=90)
    else : 
        y1 = data[index_start:index_end,index].astype(float)
        rects1 = plt.bar(indices,y1,bar_width,alpha=opacity,color = 'g',label='Calls')
        y2 = data[index_start:index_end,-1-index].astype(float)
        rects2 = plt.bar(indices+bar_width,y2,bar_width,alpha=opacity,color = 'r',label='Puts')
        plt.xticks(indices + bar_width,strike_prices,rotation=90)
    plt.xlabel(web_data["Headers"][10] + ' Spot Price : ' + str(web_data["Price"]))
    plt.ylabel(web_data["Headers"][index])
    plt.title('Bar Graph for '+ web_data["Headers"][index])
    plt.legend()
    plt.grid()
    plt.plot(web_data["Price"])
    plt.tight_layout()

    plt.show()
    return


def save_bar_graph(url,name='Option Chain Data',values_from_mid = 7,quantity='OI'):
    ##Get URL
    web_data = nse_data(url)
    ##Get Data
    data = np.asarray(web_data["Data"])
    ##Total Size of Chart
    ##mid_value = data.shape[0]
    
    spot_price = web_data["Price"]
    mid_value =  np.argmin(np.abs(data[:,10]-spot_price))
    ##Number of prices you want
    index_start = int(mid_value - values_from_mid)
    print(index_start)
    index_end = int(mid_value + values_from_mid)
    print(index_end)
    ## Annotations we need
    strike_prices = data[index_start:index_end,10]
    for index in range(len(web_data["Headers"])):
        if web_data["Headers"][index] == quantity :
            break


    y1 = data[index_start:index_end,index].astype(float)
    y2 = data[index_start:index_end,-1-index].astype(float)
    print(np.asarray([strike_prices,y1,y2]).shape)
    np.save('./temperory_saves_while_plotting/'+name+quantity+'.npy',np.asarray([strike_prices,y1,y2]))
    return


