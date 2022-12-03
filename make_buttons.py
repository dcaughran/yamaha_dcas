
import json
import secrets

start_filename = "start_full.companionconfig"
out_filename = "out_full.companionconfig"
channels = range(1, 33)

# Pages
page_names = ["scratch1", # 1
                "scratch2", # 2
                "Channel Select", # 3
                "Channel ON", # 4
                "Channel OFF", # 5
                "Labels", # 6
                "DCA1 ON", # 7
                "DCA1 OFF", # 8
                "DCA2 ON", # 9
                "DCA2 OFF", # 10
                "DCA3 ON", # 11
                "DCA3 OFF", # 12
                "DCA4 ON", # 13
                "DCA4 OFF", # 14
                "DCA5 ON", # 15
                "DCA5 OFF", # 16
                "DCA6 ON", # 17
                "DCA6 OFF", # 18
                "DCA7 ON", # 19
                "DCA7 OFF", # 20
                "DCA8 ON", # 21
                "DCA8 OFF", # 22
                "Store 0", # 23
                "Store 1", # 24
                "Store 2", # 25
                "Store 3", # 26
                "Store 4", # 27
                "Store 5", # 28
                "Store 6", # 29
                "Store 7", # 30
                "Store 8", # 31
                "Store 9", # 32
                "Load 0", # 33
                "Load 1", # 34
                "Load 2", # 35
                "Load 3", # 36
                "Load 4", # 37
                "Load 5", # 38
                "Load 6", # 39
                "Load 7", # 40
                "Load 8", # 41
                "Load 9", # 42
                "DCA1 Color", # 43
                "DCA2 Color", # 44
                "DCA3 Color", # 45
                "DCA4 Color", # 46
                "DCA5 Color", # 47
                "DCA6 Color", # 48
                "DCA7 Color", # 49
                "DCA8 Color"] # 50

dca_colors = ['Blue', 
              'Orange',
              'Yellow',
              'Purple',
              'Cyan',
              'Magenta',
              'Red',
              'Green',
              'Off']

name_base = {'style': 'png',
            'text': '',
             'size': 'auto',
             'alignment': 'center:center',
             'pngalignment': 'center:center',
             'color': 16777215,
             'bgcolor': 0,
             'latch': False,
             'relative_delay': False,
             'show_topbar': 'default'}

f = open(start_filename, 'r')
config = json.load(f)
f.close()

####################
# Custom Variables #
####################

# DCA Names
for idca in range(1,9):
    var_dict = {"dca%d_name"%idca: {'defaultValue': '', 'description': 'DCA%d Name'%idca}}
    config['custom_variables'].update(var_dict)

# Scene Name
var_dict = {"scene_name": {'defaultValue': '', 'description': 'Scene Name'}}
config['custom_variables'].update(var_dict)


# Get instance ID for yamaha-MIDI module
for instance in config['instances']:
    if config['instances'][instance]['label'] == 'yamaha-MIDI':
        print("Yamaha-MIDI instance is '%s'"%instance)
        break

for ipage, page in enumerate(page_names):
    
    # Set page name
    config['page'][str(ipage + 1)]['name'] = page
    
    
    for ibutton, button in enumerate(channels):

        
        ########################
        # Set Name and Actions #
        ########################
        if "Select" in page:
            button_name = "SEL %d"%button
            action = "0103000012"
            options = {"yamMIDIval": button - 1}
        elif "Channel ON" in page or "Channel OFF" in page:
            button_name = "CH %d"%button
            action = "0100350000"
            options = {"yamMIDIch": button - 1}
            if "ON" in page:
                options.update({"yamMIDIval": True})
            else:
                options.update({"yamMIDIval": False})
        elif "DCA" in page and ("ON" in page or "OFF" in page):
            dca_num = int(page[3])
            button_name = "CH %d"%button
            action = "010046000%d"%(dca_num-1) # last digit is DCA number
            options = {"yamMIDIch": button - 1}
            if "ON" in page:
                options.update({"yamMIDIval": True})
            else:
                options.update({"yamMIDIval": False})
        elif "Store" in page:
            scene = int(page[-1])*32 + ibutton + 1
            if scene > 300:
                continue
            button_name = "Store %d"%scene
            action = "LibStr__SCENE___"
            options = {"yamMIDIval": scene}
        elif "Load" in page:
            scene = int(page[-1])*32 + ibutton + 1
            if scene > 300:
                continue
            button_name = "Load %d"%scene
            action = "LibRcl__SCENE___"
            options = {"yamMIDIval": scene}
        elif "Labels" in page:
            if button <= 8:
                button_name = "DCA %d Name"%button
                action = "0101020000"
                options = {"yamMIDIch": button - 1, 
                           "yamMIDIval": "$(internal:custom_dca%d_name)"%button}
            elif (button >8) & (button <=16):
                button_name = "$(internal:custom_dca%d_name)"%(button-8)
                action = ''
                options = {}
            elif button == 17:
                button_name = "Scene Name"
                # TBD: Action and options to save scene name
                action = ''
                options = {}
            elif button == 25:
                button_name = "$(internal:custom_scene_name)"
                action = ''
                options = {}
            else:
                continue
        elif "DCA" in page and "Color" in page:
            dca_num = int(page[3])
            if button <= 9:
                button_name = dca_colors[ibutton]
                action = "otherYamParamMsg"
                options = {"yamMIDIcmd": "0101030001",
                          "yamMIDIch": dca_num - 1,
                          "yamMIDIval": button - 1
                        }
            else:
                continue
        else:
            continue
            
            
        # Set template and re-name
        config['config'][str(ipage+1)][str(ibutton+1)].update(name_base)
        config['config'][str(ipage+1)][str(ibutton+1)]['text'] = button_name
        
        # set action
        delay = 0
        action_label = ("%s CH%d"%(page, button)).replace(' ', '_')
        action_dict = {'label': action_label,
                       'id': secrets.token_urlsafe(8),
                       'instance': instance,
                       'action': action,
                       'options': options,
                       'delay': delay}
        
        config['actions'][str(ipage+1)][str(ibutton+1)] = [action_dict]
    
    
with open(out_filename, 'w') as f:
    json.dump(config, f)   