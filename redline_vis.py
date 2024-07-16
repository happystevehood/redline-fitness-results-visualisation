# This module was developed to create visualisation of the results below.
#
# 2023 Results
# 2023 redline fitness games scraped from - Day 1 results.
# https://runnersunite.racetecresults.com/results.aspx?CId=16634&RId=1216
# 2023 redline fitness games scraped from - Day 2 results.
# https://runnersunite.racetecresults.com/results.aspx?CId=16634&RId=1217
# 
# 2024
# 2024 redline fitness games scraped from - Day 1 results.
# https://runnersunite.racetecresults.com/results.aspx?CId=16634&RId=1251
# 2024 redline fitness games scraped from - Day 2 results.
# https://runnersunite.racetecresults.com/results.aspx?CId=16634&RId=1252
#
# Results from abvove were cut and paste into excel file and saved as csv files per competition.
#
# This intial development is based on the format for 2023, then 2024 format added
#

import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
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
EventList23 =      [         'Run','Bike','Sandbag Gauntlet','Battle Rope Pull','Farmer\'s Carry','Row','Deadball Burpee','Sled Push','Pendulum Shots','Agility Climber','Ski','The Mule']
EventListStart23 = ['Start', 'Run','Bike','Sandbag Gauntlet','Battle Rope Pull','Farmer\'s Carry','Row','Deadball Burpee','Sled Push','Pendulum Shots','Agility Climber','Ski','The Mule']

#The 2024 Events Lists
EventList24 =      [         'Run', 'Row', 'Deadball Burpee', 'Pendulum Shots', 'Bike', 'Sandbag Gauntlet', 'Battle Whip', 'Farmer\'s Carry', 'Agility Chamber', 'Ski', 'Mule', 'Sled Push Pull']
EventListStart24 = ['Start', 'Run', 'Row', 'Deadball Burpee', 'Pendulum Shots', 'Bike', 'Sandbag Gauntlet', 'Battle Whip', 'Farmer\'s Carry', 'Agility Chamber', 'Ski', 'Mule', 'Sled Push Pull']

#Count number of partipants who reach 7 minutes per event.
EventCutOffCount = [             0,     0,                 0,                0,         0,                  0,             0,                0,                 0,      0,      0,                0]

#filepath hardcoded for now, I guess I should pass in as commandline...
filepath23 = r"C:\Users\Steph\Documents\py\redline"
filepath24 = r"C:\Users\Steph\Documents\py\redline"

# filename and description
fileList23 = [
            ["MensSinglesCompetitive2023","REDLINE Fitness Games \'23 Mens Singles Comp."], 
            ["WomensSinglesCompetitive2023","REDLINE Fitness Games \'23 Womens Singles Comp."], 
            ["MensSinglesOpen2023","REDLINE Fitness Games \'23 Mens Singles Open"],  
            ["WomensSinglesOpen2023","REDLINE Fitness Games \'23 Womens Singles Open"],
            ["MensDoubles2023","REDLINE Fitness Games \'23 Mens Doubles"],
            ["WomensDoubles2023","REDLINE Fitness Games \'23 Womens Doubles"],
            ["MixedDoubles2023","REDLINE Fitness Games \'23 Mixed Doubles"],
            ["TeamRelayMen2023","REDLINE Fitness Games \'23 Mens Team Relay"],
            ["TeamRelayWomen2023","REDLINE Fitness Games \'23 Womens Team Relay"],
            ["TeamRelayMixed2023","REDLINE Fitness Games \'23 Mixed Team Relay"],
            ]

# filename and description
fileList24 = [
            ["MensSinglesCompetitive2024","REDLINE Fitness Games \'24 Mens Singles Comp."], 
            ["WomensSinglesCompetitive2024","REDLINE Fitness Games \'24 Womens Singles Comp."], 
            ["MensSinglesOpen2024","REDLINE Fitness Games \'24 Mens Singles Open"],  
            ["WomensSinglesOpen2024","REDLINE Fitness Games \'24 Womens Singles Open"],
            ["MensDoubles2024","REDLINE Fitness Games \'24 Mens Doubles"],
            ["WomensDoubles2024","REDLINE Fitness Games \'24 Womens Doubles"],
            ["MixedDoubles2024","REDLINE Fitness Games \'24 Mixed Doubles"],
            ["TeamRelayMen2024","REDLINE Fitness Games \'24 Mens Team Relay"],
            ["TeamRelayWomen2024","REDLINE Fitness Games \'24 Womens Team Relay"],
            ["TeamRelayMixed2024","REDLINE Fitness Games \'24 Mixed Team Relay"],
            ]

#These variables are not modified progamatically .
#variables to control where output goes during debug/developement.
pltShow=True
pltPngOut=False
cvsOut=False
allScatter=False

#show graphs
showBar=True
showCutOffBar=False   
showHist=True
showPie=True
showCorr=True
#Only impact if showCorr=True
showHeat=True

#programatically for now
do2023input=True


#############################
# Tidy the data/data frame
#############################
def tidyTheData(df):

    #Remove boring columns
    df.drop(columns=['Race No','Name', 'Gender', 'Wave'], inplace=True)

    if 'Fav' in df.columns:
        df.drop('Fav', axis=1, inplace = True)

    if 'Share' in df.columns:
        df.drop('Share', axis=1, inplace = True)

    if 'Team' in df.columns:
        df.drop('Team', axis=1, inplace = True)

    if 'Member1' in df.columns:
        df.drop('Member1', axis=1, inplace = True)
        df.drop('Member2', axis=1, inplace = True)
        df.drop('Member3', axis=1, inplace = True)
        df.drop('Member4', axis=1, inplace = True)

    if 'Cat Pos' in df.columns:
        df.drop('Cat Pos', axis=1, inplace = True)

    if 'Net Cat Pos' in df.columns:
        df.drop('Net Cat Pos', axis=1, inplace = True)

    if 'Net Gender Pos' in df.columns:
        df.drop('Net Gender Pos', axis=1, inplace = True)

    if 'Time Adj' in df.columns:
        df.drop('Time Adj', axis=1, inplace = True)

    #Rename Columns so consistent across years....etc
    df.rename(columns={'Net Pos':'Pos'},inplace=True)
    df.rename(columns={'Sled Push & Pull':'Sled Push Pull'},inplace=True)
    df.rename(columns={'Ski Erg':'Ski'},inplace=True)
    df.rename(columns={'Row Erg':'Row'},inplace=True)
    df.rename(columns={'Bike Erg':'Bike'},inplace=True)
    df.rename(columns={'Battle Rope Whips':'Battle Whip'},inplace=True)
    df.rename(columns={'SandbagGauntlet':'Sandbag Gauntlet'},inplace=True)
    df.rename(columns={'Deadball Burpee Over Target':'Deadball Burpee'},inplace=True)

    #in 2023 doubles "The Mule" Column is called "Finish Column"
    df.rename(columns={'Finish':'The Mule'},inplace=True)

    #drop and rows with empty data including DNF
    df.dropna(inplace = True)

    #add a  column to calculate the times based on sum of each event.
    df.insert(0, 'Calc Time', 0.0)

    #Reset the CutOffEvent count value to 0
    EventCutOffCount[:] = [0 for _ in EventCutOffCount]

    # Index to last item
    MyIndex = len(EventListStart) - 1

    #iterate the event list in reverse order
    for event in EventListStart[::-1]:

        #Note Event = EventListStart[MyIndex] below, may be tidier ways to write

        #reorganise data such that each event a duration in reverse format
        for x in df.index:

            # do not write to start time
            if MyIndex != 0:

                #2023 does not have decimal places
                if (do2023input == True):
                    #write Duration @Position(X) = Time @Position(X) - Time @Position(X-1)
                    df.loc[x,event] =  timedelta.total_seconds(datetime.strptime(df.loc[x,event],"%H:%M:%S") - datetime.strptime(df.loc[x,EventListStart[MyIndex-1]] ,"%H:%M:%S"))
                #2024 time has decimal places
                else:
                    #write Duration @Position(X) = Time @Position(X) - Time @Position(X-1)
                    
                    df.loc[x,event] = timedelta.total_seconds(datetime.strptime(df.loc[x,event],"%H:%M:%S.%f") - datetime.strptime(df.loc[x,EventListStart[MyIndex-1]] ,"%H:%M:%S.%f"))
                    
                #if value less than 10 seconds, then somthing wrong.
                if df.loc[x,event] < 10.0:
                    #print data...
                    print ('Removed Low value', x, event, df.loc[x,event], df.loc[x,'Pos'])
                    
                    #drop the row
                    df.drop(x, inplace = True)

                # else if event is greater than 7 minutes
                elif (df.loc[x,event] > 420.0):
                    
                    #Increment the CutOff event counter (minus 1 due the diff in lists EventListStart and EventCutOffCount)
                    EventCutOffCount[MyIndex-1] = EventCutOffCount[MyIndex-1] + 1

        MyIndex = MyIndex - 1


    # conver Net Time Column to float in seconds.
    for x in df.index:
        #2023 does not have decimal places
        if (do2023input == True):
            df.loc[x,'Net Time'] =  timedelta.total_seconds(datetime.strptime(df.loc[x,'Net Time'],"%H:%M:%S") - datetime.strptime("00:00:00","%H:%M:%S"))
        else:
            df.loc[x,'Net Time'] =  timedelta.total_seconds(datetime.strptime(df.loc[x,'Net Time'],"%H:%M:%S.%f") - datetime.strptime("00:00:00.0","%H:%M:%S.%f"))

        #if net time less than 6 minutes
        if ((df.loc[x,'Net Time']) < 360.0):
           #print data...
           print ('Removed Low NetTime', x, df.loc[x,'Net Time'], df.loc[x,'Pos'])
           #drop the row
           df.drop(x, inplace = True)

        #Reset Calculated time for this index
        calculatedNetTime = 0.0

        #iterate the event list in reverse order
        for event in EventList:
            #add each event time.
            calculatedNetTime = calculatedNetTime + df.loc[x,event] 

        #Store the event time.
        df.loc[x,'Calc Time'] = calculatedNetTime    

        #if NetTime - Calculated time is less than 12 seconds
        #if (abs(df.loc[x,'Net Time'] - calculatedNetTime) > 12):
                            
            #print ('NetTime Mismatch ', df.loc[x,'Net Time'], calculatedNetTime, abs(df.loc[x,'Net Time'] - calculatedNetTime), x  )

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

    #get rid of this in place of 'Calc Time'
    if 'Net Time' in dfcorr.columns:
        dfcorr.drop('Net Time', axis=1, inplace = True)

    #get corrolation info
    corr_matrix = dfcorr.corr()
    
    if( showHeat ):
        plt.figure(figsize=(10, 10))
        heatmap = sns.heatmap(corr_matrix, vmin=-0, vmax=1, annot=True, cmap='BrBG')
        heatmap.set_title('Correlation Heatmap ' + file[1], fontdict={'fontsize':12}, pad=12);

        # Output/Show depending of global variable setting with pad inches
        if ( pltPngOut ): plt.savefig(filepath + '\\output\\png\\' + file[0] + 'CorrHeat' + '.png', bbox_inches='tight', pad_inches = 0.5)
        if ( pltShow ):   plt.show()
        if ( pltPngOut or  pltShow):   plt.close()

    plt.figure(figsize=(10, 10))
    
    #Drop the Calctime column so dont see in later grapicds.
    corr_matrix.drop('Calc Time', axis=0, inplace = True)
    
    # Shows a nice correlation barchar
    heatmap = sns.barplot( data=corr_matrix['Calc Time'])
    
    for i in heatmap.containers:
        heatmap.bar_label(i,fmt='%.2f')
    
    plt.xticks(rotation=70)
    plt.ylabel('Total Time')

    heatmap.set_title('Event Correlation V Total Time ' + file[1], fontdict={'fontsize':12}, pad=10);

    # Output/Show depending of global variable setting with pad inches
    if ( pltPngOut ): plt.savefig(filepath + '\\output\\png\\' + file[0] + 'Corr' + '.png', bbox_inches='tight', pad_inches = 0.5)
    if ( pltShow ):   plt.show()
    if ( pltPngOut or  pltShow):   plt.close()
    
    #get the highest and lowest correlation events
    #Correction works better with Calculated time compared with Net Time compared with 
    corr_matrix = corr_matrix[['Calc Time']].sort_values(by='Calc Time', ascending=False)

    if (allScatter == False):
        #Show scatter chart with higest correlation.
        ShowScatterPlot(df, corr_matrix.index[0], corr=corr_matrix.at[corr_matrix.index[0],'Calc Time'])

        #Show scatter chart with lowest correlation.
        ShowScatterPlot(df, corr_matrix.index[-1], corr=corr_matrix.at[corr_matrix.index[-1],'Calc Time'])

    else:
        for event in corr_matrix.index:
            #skip next time scatter plot
            if (event != 'Calc Time'):
                #Show scatter Plot
                ShowScatterPlot(df, event, corr=corr_matrix.at[event,'Calc Time'] )

############################
# Histogram Age Categories
#############################

def ShowHistAgeCat(df):

    # set num of categories to be 3 by default
    num_cat        = 3

    plt.figure(figsize=(10, 10))

    # do for 2023
    if (do2023input==True):

        #Competitive singles Category columns colours
        Category_order = ["18 - 29", "30 - 39", "40+"]
        colors         = ['red'    , 'tan'    , 'lime']
    
    #else for 2024
    else:
        #Competitive singles Category 
        Category_order_single = ["18-24", "25-29", "30-34", "35-39", "40-44",  "45-49", "50+"]
        colors_single =         ['red'  , 'tan'  , 'lime' , 'blue' , 'purple', 'orange', 'grey']

        #Competitive Dobules Mixed Relay Category 
        category_order_team = ["< 30", "30-44", "45+"]
        colors_team =         ['red' , 'tan'  , 'lime']

    #converting from seconds to minutes and making bins dvisible by 5
    binWidth = 5
    binMin = ((int(min(df['Net Time']))//60)//binWidth)*binWidth
    binMax = (((int(max(df['Net Time']))//60)+binWidth)//binWidth)*binWidth
    bins=np.arange(binMin,binMax, binWidth)

    #BinAllWidth
    binAllWidth = 20
    binAllMin = ((int(min(df['Net Time']))//60)//binWidth)*binWidth
    binAllMax = (((int(max(df['Net Time']))//60)+binWidth)//binWidth)*binWidth
    binsAll=np.arange(binAllMin,binAllMax, binAllWidth)


    catAll = list((df['Net Time'])/60.0)

    #if category column exist.
    if 'Category' in df.columns:

        #if 2024 style
        if (do2023input==False):

            #need to setup for singles or teams
            #if single matches exist
            if (Category_order_single[0] in df['Category'].values):
                Category_order = Category_order_single
                colors = colors_single
                num_cat        = 7
            else:
                Category_order = category_order_team
                colors = colors_team
                num_cat        = 3            

        #create list per category
        cat0 = list((df[df['Category'] == Category_order[0]]['Net Time'])/60.0)
        cat1 = list((df[df['Category'] == Category_order[1]]['Net Time'])/60.0)
        cat2 = list((df[df['Category'] == Category_order[2]]['Net Time'])/60.0)

        if (num_cat == 7):
            cat3 = list((df[df['Category'] == Category_order[3]]['Net Time'])/60.0)
            cat4 = list((df[df['Category'] == Category_order[4]]['Net Time'])/60.0)
            cat5 = list((df[df['Category'] == Category_order[5]]['Net Time'])/60.0)
            cat6 = list((df[df['Category'] == Category_order[6]]['Net Time'])/60.0)

        #if cat0 not empty means there are categories.
        if cat0 != []:

            if (num_cat == 3):
                plt.hist([cat0,cat1,cat2], color=colors, label=Category_order, bins=bins)
                plt.legend()
            else:
                plt.hist([cat0,cat1,cat2,cat3,cat4,cat5,cat6], color=colors, label=Category_order, bins=bins)
                plt.legend()

        else:
            plt.hist(catAll,bins=binAllWidth)

    else:
        plt.hist(catAll,bins=binAllWidth)

    plt.xticks(bins)
    plt.xlabel('Time (Minutes)')
    plt.ylabel('Num. Participants')
    plt.title(file[1] + ' Time Distrbution')
    plt.grid(color ='grey', linestyle ='-.', linewidth = 0.5, alpha = 0.4)

    # Output/Show depending of global variable setting.
    if ( pltPngOut ): plt.savefig(filepath + '\\output\\png\\' + file[0] + 'Hist' + '.png', bbox_inches='tight', pad_inches = 0.3)
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

        maxEventList.append(df[event].quantile(0.98))
        q1EventList.append(df[event].quantile(0.75))
        medianEventList.append(df[event].quantile(0.50))
        q3EventList.append(df[event].quantile(0.25))
        minEventList.append(df[event].min())
        

    plt.bar(EventList, maxEventList,       color='grey'   , label='75%-98%')
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
    if ( pltPngOut ): plt.savefig(filepath + '\\output\\png\\' + file[0] + 'Bar' + '.png', bbox_inches='tight', pad_inches = 0.5)
    if ( pltShow ):   plt.show()
    if ( pltPngOut or  pltShow):   plt.close()


#############################
# Bar chart Cut Off Events
#############################

def ShowBarChartCutOffEvent(df):

    fig, ax = plt.subplots(figsize=(10, 10))

    #null list
    cutOffEventList = []
    MyIndex = 0

    for event in EventList[::]:
        #print ('Event CutOff %s %d %d %2.2f' % (event, EventCutOffCount[MyIndex], len(df.index), EventCutOffCount[MyIndex] / len(df.index)))

        #add percentage to list
        cutOffEventList.append((100*EventCutOffCount[MyIndex]) / len(df.index))
        MyIndex = MyIndex + 1

    ax.bar(EventList, cutOffEventList,       color='red'   , label='Partipants > 7min')

    for container in ax.containers:
        ax.bar_label(container,fmt='%.1f%%')

    plt.grid(color ='grey', linestyle ='-.', linewidth = 0.5, alpha = 0.4)
    plt.tick_params(axis='x', labelrotation=90)
    plt.ylabel('Num Participants')
    plt.title(file[1] + ' Station 7 Min Stats')
    plt.legend() 

    # Output/Show depending of global variable setting with some padding
    if ( pltPngOut ): plt.savefig(filepath + '\\output\\png\\' + file[0] + 'CutOffBar' + '.png', bbox_inches='tight', pad_inches = 0.5)
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
    if ( pltPngOut ): plt.savefig(filepath + '\\output\\png\\' + file[0] + 'Pie' + '.png', bbox_inches='tight', pad_inches = 0.3)
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

        elif df[eventName][index] <  df[eventName].quantile(0.98):
            #Add to slowest quartile list
            q4ListX.append(df[eventName][index])
            q4ListY.append(df['Pos'][index])


    plt.figure(figsize=(10, 10))

    plt.scatter(x=q1ListX, y=q1ListY, c ="blue",  label="0%-24%")
    plt.scatter(x=q2ListX, y=q2ListY, c ="brown", label="25%-49%")
    plt.scatter(x=q3ListX, y=q3ListY, c ="green", label="50%-74%")
    plt.scatter(x=q4ListX, y=q4ListY, c ="red",   label="75%-98%")

    #conver corr float to str
    if (corr):
        corrstr = "{:1.2f}".format(corr)
    
    plt.title(file[1] + ' ' + eventName + ' Corr. ' + corrstr)
    plt.ylabel("Ovearll Position")
    plt.xlabel("Station Time")
    plt.legend()
    plt.grid(color ='grey', linestyle ='-.', linewidth = 0.5, alpha = 0.4)
    
    # Output/Show depending of global variable setting. 
    if ( pltPngOut ): plt.savefig(filepath + '\\output\\png\\' + file[0] + eventName + 'Scat' + '.png', bbox_inches='tight', pad_inches = 0.3)
    if ( pltShow ):   plt.show()
    if ( pltPngOut or  pltShow):   plt.close()
  
#############################
# Reading the file
#############################

#configure for 2023 format or 2024 format
if (do2023input==True):
    EventList = EventList23
    EventListStart = EventListStart23
    filepath = filepath23
    fileList =  fileList23
else:
    EventList = EventList24
    EventListStart = EventListStart24
    filepath = filepath24
    fileList =  fileList24

#Loop through each file.
for file in fileList :

    indatafile = filepath + '\\input\\' + file[0] + '.csv'
    #read in the data.
    df = pd.read_csv(indatafile)

    tidyTheData(df=df)

    #Outpuy the tidy data to csv
    if (cvsOut): 
        outdatafile = filepath + '\\output\\csv\\' + file[0] + '.csv'
        df.to_csv(outdatafile)

    #show the plots.
    if(showHist): ShowHistAgeCat(df=df)
    if(showBar): ShowBarChartEvent(df=df)
    if(showCutOffBar): ShowBarChartCutOffEvent(df=df)
    if(showPie): ShowPieChartAverage(df=df)
    
    #Show Correlation Info
    # also calls show Scatter plot in order of correlation
    if(showCorr): ShowCorrInfo(df=df)

#that is the end
