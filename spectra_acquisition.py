# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 21:41:35 2016

@author: fedel_000
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm # Colour Map
import numpy as np
import os

Path = r"C:\Users\fedel_000\Documents\Measurements\stefano\02_25_Angle_resolved_Raman_TMPyP_HClpH1_AuNC"
#Path = r"C:\Users\fedel_000\Documents\Measurements\stefano\02_26_Angle_resolved_Fluorescence_TMPyP_HClpH1_AuNC\0_5mWatt" 
s = '\\'
Path = Path + "\ASCII" +  s
files = os.listdir(Path)

#pathCal = Path + files[0]
pathCal = Path + files[-1]

names = []
data = {}
index = 0
#pixel_first = 270 #Fluorescence range
#pixel_last = 300
pixel_first = 200  #Raman range
pixel_last = 220
dfCal = pd.read_csv(pathCal, sep=',', header=None).astype(float) # x axis from toluene spectrum
wl_shift = dfCal.loc[:][0] # x axis
data['wavenumber shift (cm^-1)'] = wl_shift
# first and last element of each axis
wl_first = wl_shift[0]
wl_last = wl_shift[len(wl_shift) - 1]
fGsize = 4 # First Figure Size
sGsize = 1 # Second Figure Size

for k in range(0, len(files)): #7):#
    #j = 2
    path = Path + files[k]

    #---------------------------------------------------------
    """
    a = files[k].find('expTime') + 7 # first index
    b = files[k].find('NAcc') - 1 # second index
    expTime = float( files[k][a:b].replace('_', '.') )
    """    
    df = pd.read_csv(path, sep=',', header=None).astype(float)#/expTime # renormalizzation
    
    #---------------------------------------------------------    
    
    #df = pd.read_csv(path, sep=',', header=None).astype(float)
    pixel = df.loc[0][:] # y axis
    
    #pixel_first = pixel[0]
    #pixel_last = pixel[len(pixel) - 2]
    #
    
    df = df.set_index(0) # set the first column as index
    df.index.name= None # remove first column index
    df = df.set_index(wl_shift) # set calibration as index (generate a new column index)
    df.index.name= None # remove the name from the index columnl
    df = df.transpose() 
    
    j = 1
    
    spectrum = []
    #for j in range(len(pixel) - 2): # sum of the spectra
    for j in range(len(wl_shift)): # sum of the spectra
        spectrum = spectrum + [ df.loc[pixel_first : pixel_last][ wl_shift[j] ].sum()]
    
    Min = np.min(spectrum[0:len(spectrum) - 1] )
    Max = np.max(spectrum)
    #Max = np.max(spectrum)
    #Max = 60000
    #Max = 800000
    size = len(spectrum)
    
    names = names + [ files[k][6:22] ] #+ str(k)
    data[ names[ index ] ] = spectrum # dictionary of all the data
    index = index + 1

    
    fig = plt.figure(figsize=(20,10))
    ax1 = plt.subplot2grid((fGsize,sGsize), (0,0), rowspan=fGsize - 1) # first braket is the figure size, the second one is the on-going plot position
    plt.axis([wl_first, wl_last, Min, Max])    

    line1, = ax1.plot(wl_shift, spectrum, label = files[k][6:15])    
    #fucking legend!
    handles, labels = ax1.get_legend_handles_labels() # http://matplotlib.org/1.3.1/users/legend_guide.html
    ax1.legend(handles[::-1], labels[::-1])
    # plt.plot(x, y, label = "plot label") # the easiest way to get a legend
    # plt.legend()
    #fucking legend!
    ax1.grid()
    
    #ax2 = fig.add_subplot(212)
    ax2 = plt.subplot2grid((fGsize,sGsize), (fGsize - 1,0), rowspan=1)
    ax2.imshow(df.ix[:][pixel_first:pixel_last], cmap=cm.gray, extent=[wl_first,wl_last,pixel_last,pixel_first])

    #plt.plot(df[ wl_shift[j] ], 'r+') # wl_shift[j] is the index of the pixel
    #j = 500
    #plt.plot(df[ wl_shift[j] ], 'k+')
    #plt.grid(True)
    
    #df[ wl_shift[j] ][1:100].mean()
    #plt.figure()



dF = pd.DataFrame(data) # convert the dictionary of different Raman into a DataFrame
#pathExFl =r"C:\Users\fedel_000\Documents\Measurements\stefano\02_26_Angle_resolved_Fluorescence_TMPyP_HClpH1_AuNC\0_5mWatt" # Path Excel File
#pathExFl = pathExFl + s
writer = pd.ExcelWriter( Path[:-6] + 'Fluorescence TMPyP jAgg on AuNC.xlsx', engine='xlsxwriter')
dF.to_excel(writer, sheet_name='Fluorescence TMPyP jAgg on AuNC')
writer.save()
writer.close()

#df_to_excel = pd.DataFrame(data, axis = wl_shift, axis = 1)   

