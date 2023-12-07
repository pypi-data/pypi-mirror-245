"""a python script which runs Applescript which will take the frontmost application and get all of its menus, and make them keys in a dictionary, that point to arrays of all their items, and if they have sub items, please make those dictionaries with one key which poitns to an array of sub items"""

import os
import subprocess

def get_menus():
    script = """
    tell application "System Events"
        tell process (name of frontmost application)
            set menu_names to name of every menu bar item of menu bar 1
            set menu_dict to {}
            repeat with menu_name in menu_names
                set menu_items to name of every menu item of menu 1 of menu bar item menu_name of menu bar 1
                set menu_dict to menu_dict & {menu_name:menu_items}
            end repeat
            return menu_dict
        end tell
    end tell
    """
    osa_command = ['osascript', '-e', script]
    menu_dict_str = subprocess.check_output(osa_command).decode('utf-8')
    menu_dict = eval(menu_dict_str)
    return menu_dict
get_menus()