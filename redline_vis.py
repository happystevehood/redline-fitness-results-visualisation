# %%
# This module was developed to create visualisation of the results below.
#
# 2023 redline fitness games scraped from - Day 1 results.
# https://runnersunite.racetecresults.com/results.aspx?CId=16634&RId=1216
# 2023 redline fitness games scraped from - Day 2 results.
# https://runnersunite.racetecresults.com/results.aspx?CId=16634&RId=1217
# 
# Results from abvove were cut and paste into excel file and saved as csv files per competition.
#
# This intial development is based on the format for 2023, The events/formats will be different for 2024 so this code will need to be updated.
#

import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime, timedelta

# printout to confirm pkg versions.
import sys; print('python versions ', sys.version)
print('pandas ', pd.__version__)
print('numpy ', np.__version__)
print('matplotlib ', mpl.__version__)
print('seaborn ', sns.__version__)

# developed using the following versions.
#python versions  3.12.2 | packaged by Anaconda, Inc. | (main, Feb 27 2024, 17:28:07) [MSC v.1916 64 bit (AMD64)]
#pandas  2.2.2
#numpy  1.26.4
#matplotlib  3.9.0
#seaborn  0.13.2


#The 2023 Events Lists
EventList =      [         'Run','Bike','Sandbag Gauntlet','Battle Rope Pull','Farmer\'s Carry','Row','Deadball Burpee','Sled Push','Pendulum Shots','Agility Climber','Ski','The Mule']
EventListStart = ['Start', 'Run','Bike','Sandbag Gauntlet','Battle Rope Pull','Farmer\'s Carry','Row','Deadball Burpee','Sled Push','Pendulum Shots','Agility Climber','Ski','The Mule']

#rootfilepath = "C:\\Users\\Steph\\Documents\\py\\redline\\"
rootfilepath = ".\\"
inputfilepath = rootfilepath + "input\\"
outcsvfilepath= rootfilepath + "output\\csv\\"
outpngfilepath= rootfilepath + "output\\png\\"

# filename and description
fileList = [
            ["MensSinglesCompetitive2023","REDLINE Fitness Games \'23 Mens Singles Comp."], 
            #["WomensSinglesCompetitive2023","REDLINE Fitness Games \'23 Womens Singles Comp."], 
            #["MensSinglesOpen2023","REDLINE Fitness Games \'23 Mens Singles Open"],  
            #["WomensSinglesOpen2023","REDLINE Fitness Games \'23 Womens Singles Open"],
            #["MensDoubles2023","REDLINE Fitness Games \'23 Mens Doubles"],
            #["WomensDoubles2023","REDLINE Fitness Games \'23 Womens Doubles"],
            #["MixedDoubles2023","REDLINE Fitness Games \'23 Mixed Doubles"],
            #["TeamRelayMen2023","REDLINE Fitness Games \'23 Mens Team Relay"],
            #["TeamRelayWomen2023","REDLINE Fitness Games \'23 Womens Team Relay"],
            #["TeamRelayMixed2023","REDLINE Fitness Games \'23 Mixed Team Relay"],
            ]

#These variables are not modified progamatically .
#variables to control where output goes during debug/developement.
pltShow=False
pltPngOut=True
cvsOut=False
allScatter=False

#show graphs
showBar=True
showHist=True
showPie=True
showCorr=True
#Only impact if showCorr=True
showHeat=True

#############################
# Tidy the data/data frame
#############################
def tidyTheData(df):

    #Remove boring columns
    df.drop(columns=['Fav', 'Race No','Name', 'Share', 'Gender', 'Wave'], inplace=True)

    if 'Team' in df.columns:
        df.drop('Team', axis=1, inplace = True)

    if 'Member1' in df.columns:
        df.drop('Member1', axis=1, inplace = True)
        df.drop('Member2', axis=1, inplace = True)
        df.drop('Member3', axis=1, inplace = True)
        df.drop('Member4', axis=1, inplace = True)

    if 'Cat Pos' in df.columns:
        df.drop('Cat Pos', axis=1, inplace = True)

    #drop and rows with empty data including DNF
    df.dropna(inplace = True)

    #in doubles "The Mule" Column is called "Finish Column"
    df.rename(columns={'Finish':'The Mule'},inplace=True)

    # Index to last item
    MyIndex = len(EventListStart) - 1

    #iterate the event list in reverse order
    for event in EventListStart[::-1]:

        #Note Event = EventListStart[MyIndex] below, may be tidier ways to write

        #reorganise data such that each event a duration in reverse format
        for x in df.index:

            # do not write to start time
            if MyIndex != 0:
                #write Duration @Position(X) = Time @Position(X) - Time @Position(X-1)
                df.loc[x,event] =  timedelta.total_seconds(datetime.strptime(df.loc[x,event],"%H:%M:%S") - datetime.strptime(df.loc[x,EventListStart[MyIndex-1]] ,"%H:%M:%S"))
                #if value less than 10, then somthing wrong.
                if df.loc[x,event] < 10.0:
                    #print data...
                    print ('Removed suspicious value', file[1], event, df.loc[x,event], df.loc[x,'Pos'])
                    #drop the row
                    df.drop(x, inplace = True)

        MyIndex = MyIndex - 1

    # conver Net Time Column to float in seconds.
    for x in df.index:
        df.loc[x,'Net Time'] =  timedelta.total_seconds(datetime.strptime(df.loc[x,'Net Time'],"%H:%M:%S") - datetime.strptime("00:00:00","%H:%M:%S"))

    #Now can remove start colum
    df.drop('Start', axis=1, inplace = True)

#############################
# Correlation
#############################

def ShowCorrInfo(df):
    #remove category for corralation info

    dfcorr = df.copy(deep=True)

    if 'Pos' in dfcorr.columns:
        dfcorr.drop('Pos', axis=1, inplace = True)
    
    if 'Category' in dfcorr.columns:
        dfcorr.drop('Category', axis=1, inplace = True)

    #get corrolation info
    corr_matrix = dfcorr.corr()
    
    if( showHeat ):
        plt.figure(figsize=(10, 10))
        heatmap = sns.heatmap(corr_matrix, vmin=-0, vmax=1, annot=True, cmap='BrBG')
        heatmap.set_title('Correlation Heatmap ' + file[1], fontdict={'fontsize':12}, pad=12);

        # Output/Show depending of global variable setting with pad inches
        if ( pltPngOut ): plt.savefig(outpngfilepath + file[0] + 'CorrHeat' + '.png', bbox_inches='tight', pad_inches = 0.5)
        if ( pltShow ):   plt.show()
        if ( pltPngOut or  pltShow):   plt.close()

    plt.figure(figsize=(10, 10))
    heatmap = sns.heatmap(corr_matrix[['Net Time']].sort_values(by='Net Time', ascending=False), vmin=0, vmax=1, annot=True, cmap='BrBG')
    heatmap.set_title('Event Correlation V Total Time ' + file[1], fontdict={'fontsize':12}, pad=10);

    # Output/Show depending of global variable setting with pad inches
    if ( pltPngOut ): plt.savefig(outpngfilepath + file[0] + 'Corr' + '.png', bbox_inches='tight', pad_inches = 0.5)
    if ( pltShow ):   plt.show()
    if ( pltPngOut or  pltShow):   plt.close()
    
    #get the highest and lowest correlation events
    corr_matrix = corr_matrix[['Net Time']].sort_values(by='Net Time', ascending=False)

    if (allScatter == False):
        #Show scatter chart with higest correlation.
        ShowScatterPlot(df, corr_matrix.index[1], corr=corr_matrix.at[corr_matrix.index[1],'Net Time'])

        #Show scatter chart with lowest correlation.
        ShowScatterPlot(df, corr_matrix.index[-1], corr=corr_matrix.at[corr_matrix.index[-1],'Net Time'])
    else:
        for event in corr_matrix.index:
            #skip next time scatter plot
            if (event != 'Net Time'):
                #Show scatter Plot
                ShowScatterPlot(df, event, corr=corr_matrix.at[event,'Net Time'] )

############################
# Histogram Age Categories
#############################

def ShowHistAgeCat(df):

    plt.figure(figsize=(10, 10))

    #Three Category columns colours
    Category_order = ["18 - 29", "30 - 39", "40+"]
    colors =         ['red'    , 'tan'    , 'lime']

    #converting from seconds to minutes and making bins dvisible by 5
    binWidth = 5
    binMin = ((int(min(df['Net Time']))//60)//5)*5
    binMax = (((int(max(df['Net Time']))//60)+binWidth)//5)*5
    bins=np.arange(binMin,binMax, binWidth)

    catAll = list((df['Net Time'])/60.0)

    #if category column exist.
    if 'Category' in df.columns:

        #create list per category
        cat0 = list((df[df['Category'] == Category_order[0]]['Net Time'])/60.0)
        cat1 = list((df[df['Category'] == Category_order[1]]['Net Time'])/60.0)
        cat2 = list((df[df['Category'] == Category_order[2]]['Net Time'])/60.0)

        #if cat0 not empty means there are categories.
        if cat0 != []:
            plt.hist([cat0,cat1,cat2], color=colors, label=Category_order, bins=bins)
            plt.legend()

        else:
            plt.hist(catAll,bins=bins)

    else:
        plt.hist(catAll,bins=bins)

    plt.xticks(bins)
    plt.xlabel('Time (Minutes)')
    plt.ylabel('Num. Participants')
    plt.title(file[1] + ' Time Distrbution')
    plt.grid(color ='grey', linestyle ='-.', linewidth = 0.5, alpha = 0.4)

    # Output/Show depending of global variable setting.
    if ( pltPngOut ): plt.savefig(outpngfilepath + file[0] + 'Hist' + '.png', bbox_inches='tight', pad_inches = 0.3)
    if ( pltShow ):   plt.show()
    if ( pltPngOut or  pltShow):   plt.close()

#############################
# Bar chart Events
#############################

def ShowBarChartEvent(df):

    plt.figure(figsize=(10, 10))

    maxEventList = []
    q1EventList = []
    medianEventList = []
    q3EventList = []
    minEventList = []

    # get the median time for each event.
    for event in EventList:

        maxEventList.append(df[event].quantile(0.95))
        q1EventList.append(df[event].quantile(0.75))
        medianEventList.append(df[event].quantile(0.50))
        q3EventList.append(df[event].quantile(0.25))
        minEventList.append(df[event].min())
        

    plt.bar(EventList, maxEventList,       color='grey'   , label='75%-95%')
    plt.bar(EventList, q1EventList,        color='red'    , label='50%-74%')
    plt.bar(EventList, medianEventList,    color='orange' , label='25%-49%')
    plt.bar(EventList, q3EventList,        color='green'  , label='0%-24%')
    plt.bar(EventList, minEventList,       color='blue'   , label='fastest')

    #keep the y axis showing multiples of 60
    plt.yticks(range(0,int(max(maxEventList))+30,60))
    plt.grid(color ='grey', linestyle ='-.', linewidth = 0.5, alpha = 0.4)

    plt.tick_params(axis='x', labelrotation=90)
    plt.ylabel('Time in Seconds')
    plt.title(file[1] + ' Station Breakdown')
    plt.legend() 

    # Output/Show depending of global variable setting with some padding
    if ( pltPngOut ): plt.savefig(outpngfilepath + file[0] + 'Bar' + '.png', bbox_inches='tight', pad_inches = 0.5)
    if ( pltShow ):   plt.show()
    if ( pltPngOut or  pltShow):   plt.close()

#############################
# PieChartAverage
#############################
def ShowPieChartAverage(df):

    meanEventList = []
    meanEventListLabel = []
    totalMeanTime = 0.0
    
    plt.figure(figsize=(10, 10))

    # get the median time for each event.
    for event in EventList:
        meanEventList.append(df[event].mean())
        totalMeanTime = totalMeanTime + int(df[event].mean())

        eventLabelString = "{}\n{:1d}m {:2d}s".format(event, int(df[event].mean())//60 ,int(df[event].mean())%60)
        meanEventListLabel.append(eventLabelString)

    totalMeanTimeString = "{:1d}m {:2d}s".format(int(totalMeanTime)//60 ,int(totalMeanTime)%60)
    plt.title(file[1] + ' Average Station Breakdown : ' + totalMeanTimeString )
   
    #create pie chart = Use Seaborn's color palette 'Set2'
    plt.pie(meanEventList, labels = meanEventListLabel, startangle = 0, autopct='%1.1f%%', colors=sns.color_palette('Set2'))
    
    # Output/Show depending of global variable setting. 
    if ( pltPngOut ): plt.savefig(outpngfilepath + file[0] + 'Pie' + '.png', bbox_inches='tight', pad_inches = 0.3)
    if ( pltShow ):   plt.show()
    if ( pltPngOut or  pltShow):   plt.close()

#############################
# Show Scatter Plot
#############################
def ShowScatterPlot(df, eventName, corr):
        
    q1ListX = [] #fastest quatile
    q2ListX = []
    q3ListX = []
    q4ListX = [] #slowest quatile

    q1ListY = [] #fastest quatile
    q2ListY = []
    q3ListY = []
    q4ListY = [] #slowest quatile

     # For each competitor.
    for index in df.index:

        if df[eventName][index] <  df[eventName].quantile(0.25) :
            #Add to fastest quartile list
            q1ListX.append(df[eventName][index])
            q1ListY.append(df['Pos'][index])
        
        elif df[eventName][index] <  df[eventName].quantile(0.50) :
            #Add to q2 list
            q2ListX.append(df[eventName][index])
            q2ListY.append(df['Pos'][index])
            
        elif df[eventName][index] <  df[eventName].quantile(0.75) :
            #Add to q3 list
            q3ListX.append(df[eventName][index])
            q3ListY.append(df['Pos'][index])

        elif df[eventName][index] <  df[eventName].quantile(0.95):
            #Add to slowest quartile list
            q4ListX.append(df[eventName][index])
            q4ListY.append(df['Pos'][index])


    plt.figure(figsize=(10, 10))

    plt.scatter(x=q1ListX, y=q1ListY, c ="blue",  label="0%-24%")
    plt.scatter(x=q2ListX, y=q2ListY, c ="brown", label="25%-49%")
    plt.scatter(x=q3ListX, y=q3ListY, c ="green", label="50%-74%")
    plt.scatter(x=q4ListX, y=q4ListY, c ="red",   label="75%-95%")

    #conver corr float to str
    if (corr):
        corrstr = "{:1.2f}".format(corr)
    
    plt.title(file[1] + ' ' + eventName + ' Corr. ' + corrstr)
    plt.ylabel("Ovearll Position")
    plt.xlabel("Station Time")
    plt.legend()
    plt.grid(color ='grey', linestyle ='-.', linewidth = 0.5, alpha = 0.4)
    
    # Output/Show depending of global variable setting. 
    if ( pltPngOut ): plt.savefig(outpngfilepath + file[0] + eventName + 'Scat' + '.png', bbox_inches='tight', pad_inches = 0.3)
    if ( pltShow ):   plt.show()
    if ( pltPngOut or  pltShow):   plt.close()
  
#############################
# Reading the file
#############################

#Loop through each file.
for file in fileList :

    indatafile = inputfilepath + file[0] + '.csv'
    #read in the data.
    df = pd.read_csv(indatafile)

    tidyTheData(df=df)

    #Outpuy the tidy data to csv
    if (cvsOut): 
        outdatafile = outcsvfilepath + 'out' + file[0] + '.csv'
        df.to_csv(outdatafile)

    #show the plots.
    if(showHist): ShowHistAgeCat(df=df)
    if(showBar): ShowBarChartEvent(df=df)
    if(showPie): ShowPieChartAverage(df=df)
    
    #Show Correlation Info
    # also calls show Scatter plot in order of correlation
    if(showCorr): ShowCorrInfo(df=df)


# %%



