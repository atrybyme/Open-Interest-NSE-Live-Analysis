# Open-Interest-NSE-Live-Analysis
## Contents:
The package contains various analysis tools for live Option Chain Data.

## Following Analysis Methods are present in the package :

1. [Live Prices to Option Data for both Put and Call Option][5]
2. [Live Put Call Ratio and Total Put and Call Contracts for Option Chain][6]
3. [Live Max Pain Analysis for Option Chain][7]
4. [Probability of Change and Swing in Trend][8]
### Images of BANK NIFTY ploted for p=7 over OI Data.
![inr1][1]
_____________________________________
![inr2][2]
____________________________________
![inr3][3]
_____________________________________
![inr4][4]
______________________________________

## Additional Information
1. [notification.wav][9] is the audio file that will notify the user as soon as the data on NSE site and our graphs are updated.
2. To run the code type 
  > python any_analysis_you_want.py -l LINK -p POINT_ON_EITHER_SIDE_YOU_WANT -p QUANTITY
3. LINK - insert the link of the nse option chaing page you want to analysis.
4. POINT_ON_EITHER_SIDE_YOU_WANT - Number of points you want to plot on the graph.
5. QUANTITY - What you want to plot. Default - OI.
6. Use 
  >python any_analysis_you_want.py --help for any help about arguments.


[1]: oispot.png
[2]: pr_ratio.png
[3]: maxpain.png
[4]: change_and_swing_probability.png
[5]: option_data_plotter_live_file1.py
[6]: option_data_put_call_ratio.py
[7]: max_pain.py
[8]: utilities.py
[9]: notification.wav
