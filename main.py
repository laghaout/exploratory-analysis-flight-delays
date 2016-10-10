# -*- coding: utf-8 -*-
"""
Created on Thu Oct 6 12:01:26 2016

@author: Amine Laghaout
"""

import module as md
import pandas as pd
import numpy as np

#%% SETTINGS

# Data files
dataDir = './data/'                                     # Data directory
dataFile = 'On_Time_On_Time_Performance_2016_1.csv'     # Data file
carriersLookup = 'carriers.csv'                         # Carrier abbreviations
airportsLookup = 'airports new.csv'                     # Airport abbreviations
outDir = './writeup/'                                   # Output directory

numTrainData = None     # Number of data points to extract (None for all)
showSynopsis = False    # Take a peek at the data?
topNum = 10             # Select the `topNum' busiest airports/carriers

featureList = ['Carrier', 'Origin', 'DepDelay', 'DepTimeBlk', 'TaxiOut', 'Dest', 'ArrDelay', 'ArrTimeBlk', 'TaxiIn']

#%% LOAD DATA

trainData = pd.read_csv(dataDir+dataFile, usecols = featureList).dropna()[:numTrainData]
carriersLookup = pd.read_csv(dataDir+carriersLookup, index_col = 'Code', usecols = ['Code', 'Description']).dropna()
airportsLookup = pd.read_csv(dataDir+airportsLookup, index_col = 'iata', usecols = ['iata', 'airport']).dropna()

md.dataSynopsis(trainData, showSynopsis)

#%% FEATURE ENGINEERING

# Extract the set of airports that serve both as departures and arrivals. 
# Record the taxi times, their mean, and the number of flights.
airportList = set(trainData['Dest']).intersection(set(trainData['Origin']))
airports = pd.DataFrame(index = airportList, columns = ['TaxiTimes', 'TaxiTimeMean', 'NumFlights'])

# Extract the set of cariers and record their arrival delays, the mean arrival
# delay, and the number of flights.
carrierList = set(trainData['Carrier'])
carriers = pd.DataFrame(index = carrierList, columns = ['ArrDelay', 'ArrDelayMean', 'NumFlights'])

#%% TAXI TIME BY TOP-BUSIEST AIRPORT

# For each airport among the set of airports that serve both as departures and
# arrivals...
for elem in airportList: 

    # gather a list of both taxi-in and taxi-out times.
    taxiTimes = np.array(trainData[trainData['Dest'] == elem]['TaxiIn'].append(trainData[trainData['Origin'] == elem]['TaxiOut']))  
    airports['TaxiTimes'].loc[elem] = taxiTimes
    airports['TaxiTimeMean'].loc[elem] = np.mean(taxiTimes) # Mean taxi time
    airports['NumFlights'].loc[elem] = len(taxiTimes)       # Number of flights

# Select the `topNum' busiest airports by number of flights and sort them by
# mean taxi time.
topAirports = airports.sort_values('NumFlights')[-topNum:].sort_values('TaxiTimeMean')

md.boxPlot(topAirports, 'TaxiTimes', airportsLookup['airport'], 
           xLabel = 'Taxi time [min]', saveAs = outDir+'TaxiTimesBoxPlot.pdf')

#%% DELAY TIME BY TOP-BUSIEST CARRIER

# For each carrier...
for elem in carrierList: 
    
    # record the list of arrival delay times.
    delayTimes = np.array(trainData[trainData['Carrier'] == elem]['ArrDelay'])
    carriers['ArrDelay'].loc[elem] = delayTimes
    carriers['ArrDelayMean'].loc[elem] = np.mean(delayTimes)# Mean delay time
    carriers['NumFlights'].loc[elem] = len(delayTimes)      # Number of flights

# Select the top `topNum' busiest carriers by number of flights and sort them
# by arrival delay time.
topCarriers = carriers.sort_values('NumFlights')[-topNum:].sort_values('ArrDelayMean')

md.boxPlot(topCarriers, 'ArrDelay', carriersLookup['Description'],  
           xLabel = 'Arrival delay [min]', saveAs = outDir+'CarrierDelayBoxPlot.pdf')

#%% BEST CARRIER BETWEEN TOP-BUSIEST AIRPORTS

bestConnections = md.bestCarriersFromA2B(topAirports, trainData, carriersLookup)
connectionTable = bestConnections.to_latex(bold_rows = True)

#%% DELAY BY TIME BLOCK

md.delayByTimeOfDay(trainData, xLabel = 'Time of day', yLabel = 'Delay [min]',
                    saveAs = outDir+'DelayByTimeOfDay.pdf')


