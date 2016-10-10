# -*- coding: utf-8 -*-
"""
Created on Thu Oct 6 12:51:02 2016

@author: Amine Laghaout
"""

def delayByTimeOfDay(df, xLabel = '', yLabel = '', fontSize = 14, 
                     saveAs = None):
    
    '''
    This function plots the mean arrival and departure delays over the 
    time blocks of the day. Note that all time blocks are one-hour long, except 
    for the midnight-to-6:00 am interval which is collapsed into one time 
    block.
    '''    
    
    import matplotlib.pyplot as plt
    from pandas import concat    

    # Get the mean arrival and departure delays for every corresponding time 
    # block.
    ArrDelay = df.groupby(['ArrTimeBlk'])['ArrDelay'].mean()  
    DepDelay = df.groupby(['DepTimeBlk'])['DepDelay'].mean()  
    delay = concat([ArrDelay, DepDelay], axis=1)
    
    # Rename the indices (time of day) to 'hh:mm' and columns to 'Arrival' and 
    # 'Departure'.
    delay.index = [elem[0:2]+':'+elem[2:4] for elem in delay.index]
    delay.columns = ['Arrival', 'Departure']
    
    plt.figure()
    delay.plot.area(stacked = False, legend = True)
    plt.xlabel(r'%s' % xLabel, fontsize = fontSize)
    plt.ylabel(r'%s' % yLabel, fontsize = fontSize)
    plt.grid(True)
    plt.tight_layout()    
    
    if saveAs != None:
        plt.savefig(saveAs, bbox_inches='tight')
        
    plt.show()

def bestCarriersFromA2B(topAirports, df, carriersLookup):
    
    '''
    This function generates a table linking the top-busiest airports where each
    entry at the intersection of airport A and airport B recommends the airline
    with the smallest arrival delay.
    '''
    
    from pandas import DataFrame
    from numpy import argmin
    
    # For each pair of departure-arrival airports, determine the mean arrival
    # dealy for all airlines that service those two airports.
    meanDelay = df.groupby(['Origin', 'Dest', 'Carrier'])['ArrDelay'].mean()
    
    # Create the empty table as a dataframe where the columns and rows are
    # restricted to the top-busiest airports.
    topAirports = sorted(topAirports.index.values)
    bestConnections = DataFrame(index = topAirports, columns = topAirports)
    
    # For each pair of distinct top-busiest airports, record the carrier that
    # has the smallest arrival delay.
    for airportA in topAirports:
        for airportB in [x for x in topAirports if x != airportA]:
            bestConnections[airportA][airportB] = argmin(meanDelay[(airportA, airportB)])
    
    return bestConnections.fillna('n/a')

def boxPlot(df, value, lookupTable, xLabel = '', yLabel = '', fontSize = 14,
            saveAs = None):

    '''
    This function generates a box plot of the list `df[value]' and labels each
    box via the lookup table `lookupTable' linking the indices of `df' to a new
    value.
    '''

    import matplotlib.pyplot as plt

    plt.figure()
    plt.boxplot(df[value].values, showmeans = True, whis = [15, 85], sym = '', 
                labels=lookupTable.loc[list(df[value].index)].values, vert = False)
    plt.xlabel(r'%s' % xLabel, fontsize = fontSize)
    plt.ylabel(r'%s' % yLabel, fontsize = fontSize)
    plt.grid(True)
    plt.tight_layout()
    
    if saveAs != None:
        plt.savefig(saveAs, bbox_inches='tight')   
        
    plt.show()

def dataSynopsis(df, showSynopsis = True):
    
    '''
    This function prints to the screen a brief synopsis of the data in the 
    data frame `df' provided that `showSynopsis' is True.
    '''
    
    if showSynopsis:    
        print(df.head(5))
        print(df.describe())

