#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas
import companion_functions

# variables
dca_filename = 'LB_DCAs.csv'
template_scene = 9
start_scene = 10
dca_range = range(1, 9)

# make console 
console = companion_functions.yamahaQLCL(port = 16759, ip = '127.0.0.1')


# load in file
dca_file = pandas.read_csv(dca_filename, keep_default_na=False)



for index, row in dca_file.iterrows():
    pass
    #print(row.Scene_Name)
    
    # Recall template
    console.scene_recall(template_scene)
    
    
    # for each DCA
    for dca in dca_range:
        # Read in channels from file as a list of ints
        dca_channels_raw = getattr(row, "DCA%d_Channels"%dca)
        if len(dca_channels_raw) == 0:
            dca_channels = []
        elif type(dca_channels_raw) == int or type(dca_channels_raw) == float:
            dca_channels = [int(dca_channels_raw)]
        elif type(dca_channels_raw) == str:
            dca_channels = [int(x) for x in dca_channels_raw.split(',')]
        
        
               
    
        # assign DCAs to channels / enable channels
        for channel in dca_channels:
            console.dca_set(dca, channel, True)
            console.channel_enable(channel, True)
            
            
        
        # name DCAs
        dca_name = getattr(row, "DCA%d_Name"%dca)
        console.dca_name(dca, dca_name)
        
        # color DCAs
        dca_color = getattr(row, "DCA%d_Color"%dca)
        console.dca_color(dca, dca_color)
        
        # Clear 'channel' value if empty for debug print
        if len(dca_channels) == 0:
            channel = 0 
        print('CH%d > DCA%d (%s / %s)'%(channel, dca, dca_name, dca_color))

    
    # Save scene
    console.scene_store(start_scene + index)
    
    # name scene
    console.scene_name(start_scene + index, row.Scene_Name)
    
    print("%d: %s"%(start_scene + index, row.Scene_Name))
    