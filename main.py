from inputhandler import key_presses, load_macro, save_macro
import os
import yaml
from sys import platform

def key_as_string(key):
    return str(key).replace("'", "")

#directory where macros and keybins are stored. initialized with illegial characters to stop accidental macros being stored in root...
def _get_os_config_directory() -> str:
    #directory where macros and keybins are stored. initialized with illegial characters to stop accidental macros being stored in root...
    set_os_macroconfig_store = "!?[]{]\""

    if platform == "linux" or platform == "linux2":
        #swap when testing
        set_os_macroconfig_store = os.environ['HOME'] + "/.local/pymacromaker/"
        #set_os_macroconfig_store = os.getcwd() + "/pymacromaker/"
        pass
        # linux
    elif platform == "darwin":
        raise Exception("No keybind/macro directory set for this OS X. Fix that then remove this exception")
        pass
        # OS X
    elif platform == "win32":
        raise Exception("No keybind/macro directory set for windows. Fix that then remove this exception.")
        pass
    else:
        raise Exception("Huh, what OS is this? Anyway, no keybind/macro directory set for this OS. ")
        # Windows...
    return set_os_macroconfig_store

if platform == "linux" or platform == "linux2":
    #set_os_macroconfig_store = os.environ['HOME'] + "/.local/pymacromaker"
    pass
    # linux
elif platform == "darwin":
    raise Exception("No keybind/macro directory set for this OS X. Fix that then remove this exception")
    pass
    # OS X
elif platform == "win32":
    raise Exception("No keybind/macro directory set for windows. Fix that then remove this exception.")
    pass
else:
    raise Exception("Huh, what OS is this? Anyway, no keybind/macro directory set for this OS. ")
    # Windows...

#default keybinds
Keybinds = {
    "start|stop_recording": "Key.ctrl",
    "continue|pause_recording": "*"

}

#Get keybinds from yaml, otherwise, make new file in .local, /appdata, what ever the os config folder is.
def _retrieve_keybinds():
    global Keybinds
    keybinds_directory = _get_os_config_directory()

    #print(_get_os_config_directory() + "keybinds.yaml")
    if(os.path.exists(keybinds_directory + "keybinds.yaml")):     
        with open(keybinds_directory + "keybinds.yaml") as file:
            keybinds_to_load = yaml.load(file, Loader=yaml.FullLoader)
            Keybinds = keybinds_to_load
    else:
        print("keybind config folder not found, attempting to create new one at: " + keybinds_directory + ", attempting to create")
        try:
            os.makedirs(keybinds_directory)
        except:
            pass
        with open(keybinds_directory + 'keybinds.yaml', 'w') as out:
            yaml.dump(Keybinds, out, default_flow_style=False)
            
def save_keybinds():
    global Keybinds
    keybinds_directory = _get_os_config_directory()

    #print(_get_os_config_directory() + "keybinds.yaml")
    if(os.path.exists(keybinds_directory + "keybinds.yaml")):
        os.remove(keybinds_directory + "keybinds.yaml")     
        with open(keybinds_directory + 'keybinds.yaml', 'w') as out:
            yaml.dump(Keybinds, out, default_flow_style=False)
    else:
        print("keybind config folder not found, attempting to create new one at: " + keybinds_directory + ", attempting to create")
        try:
            os.makedirs(keybinds_directory)
        except:
            pass
        with open(keybinds_directory + 'keybinds.yaml', 'w') as out:
            yaml.dump(Keybinds, out, default_flow_style=False)
def change_keybinds():
    global Keybinds
    print("Press the keybind once first, then press a different key to change it to that key. Press shift + q or caps lock q to exit")
    print("Note: if you have multiple keybinds with the same key, only the keybind closest to the top will be changed")

    while True:
        print("")
        print("press a known keybind from the dict list to set a key")
        #print(Keybinds)
        key = key_presses()
        key.listen_start()
        pressed_key = key_as_string(key.keys)

        if pressed_key == "Q":
            print("quiting setting keybind")
            break
        
        #get number of dict key entries, if the first key in that dict entry is a key(I.E, if the key matches a keybind correlated to a command), it will confirm the key was pressed.
        for i in range(list(Keybinds.keys()).__len__() - 1):
            #Put the dict entry keys into a list, index each of them with a forloop, and take the first entry of the list(The keypress) as the comparison between the pressed_key and the keybind being changed
            if pressed_key == Keybinds[list(Keybinds.keys())[i]][0]:
                print(list(Keybinds.keys())[i] + " keybind pressed, press new key to set keybind. shift + q or caps lock q to exit")
                confirmation_key = key_presses()
                confirmation_key.listen_start()
                confirmation_pressed_key = key_as_string(confirmation_key.keys)

                if pressed_key == "Q":
                    continue
                else:
                    Keybinds[list(Keybinds.keys())[i]] = confirmation_pressed_key
                    print("Keybind now set to " + confirmation_pressed_key)





def make_macro(macro_name):
    key_list = []
    recording_paused = False
    print("Macro recording started, check keybinds for what does what. ")
    while True:
        key = key_presses()
        key.listen_start()
        pressed_key = key_as_string(key.keys)
        print(pressed_key)
        
        
        if pressed_key == Keybinds["start|stop_recording"]:
            print('macro recording stopped')
            break
        if(recording_paused):
            if pressed_key == Keybinds["continue|pause_recording"]:
                print("macro recording unpaused")
                recording_paused = False
        else:
            if pressed_key == Keybinds["continue|pause_recording"]:
                print("macro recording paused")
                recording_paused = True
                continue    
            key_list.append(key)
        #key.key

    save_macro(macro_name, key_list)

def play_macro(macro_name):
    previous_key_time = 0
    for key in load_macro(macro_name):
        print(key)
        key.press_stored_key(epoch_time_to_wait_before_press=previous_key_time)
        previous_key_time = key.press_end_time_at_epoch

def start_pymacromaker():
    #_retrieve_keybinds()
    #print(Keybinds)
    #Keybinds can be changed without saving them. So saving them after changing them is required. 
    #change_keybinds()
    #save_keybinds()
    #print(Keybinds)
    #make_macro("test_macro")
    play_macro("test_macro")
start_pymacromaker()

#make_macro("Taweawe")

#print(os.environ['HOME'] + "/.local/pymacromaker")
