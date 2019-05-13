# Factorio-Streamlabs-Integration


A Python exe for integrating Streamlabs and Factorio.


Installation
==========
Get the [latest version zip](https://github.com/muppet9010/Factorio-Streamlabs-Integration).
Unzip the files in to the desired folder.
Run the: > Streamlabs Factorio Integration.exe
Click on Settings button and enter your details.
...............


Usage
========

The app takes in Streamlabs OBS events and processes them through configurable reactions to trigger a desired action in a Factorio game. These reactions are grouped togeather as savable profiles.

The Streamlabs OBS events and their contained data can found on the second part of this page.
https://streamlabs.readme.io/docs/socket-api

The app runs a single grouping of reactions at a time, being loaded and saved as a profile. During the process if no suitable option is found it will be shown within the app and that events processing stops. Its assumed you want to handle any event you get. Special options at each level exist for more simple uses cases.

When an OBS event is received it is processed to have additional data items calculated for them:
    [VALUETYPE] = a simplified grouping of events in to either "money", "viewer" or "host".
    [VALUE] = the standardised value of the event. Donations and money amounts are converted to USD. Subscriptions have the USD cost of them. Follows and Hosts ahve the viewer count. This may be a decimal number.
The reactions are reviewed to find the most approperiate one. First the reactions are checked for the first matching platform and type to the event. If no match is found the ValueType of the event is checked for in the reactions for a match.

Assuming a reaction for the event is found the reaction's filters are checked for the first compliance. Filters allow simple math script conditions to be used to select the approperiate action to do for the event. All of the events data items from OBS and this app (generated up to this point) can be used witihn the filter in the format [DATA_ITEM_NAME]. i.e. [VALUE] > 5 or "[name]" == "bob". There is a special "ALL" filter option that will be triggered after all other filters have been checked.

The first complying reaction filter will then run an optional manipulator script if configured. This creates a new data item for the event [MODVALUE] with the scripts simple math script output value. This is used when you want to pass a modified value in to the Factorio game.

The action is when a Lua command is run in the Factorio game as a silent command (/sc) hidden from players view. It can be multiple lines long and utilise any of the events data items in the standard format [DATA_ITEM_NAME]. i.e. game.print("[name] supported with $[VALUE] worth $[MODVALUE]"). There is a special "NOTHING" action that is intended for intentionally ignoring the event.

All data items used in scripts are replaced with their event data values at execution time. The replaced text may require wrapping in quotes if it needs to be treated as a string.

Actions can be a locally defined Lua string or use a shared named Lua string within the profile. This is to allow re-use when its convienent.




Development Building
=============
Uses the python modules and their dependcies:

- Python 3.7 and default install modules
- python-socketio[client]  =  https://python-socketio.readthedocs.io/en/latest/
- PyInstaller  =  https://www.pyinstaller.org/

Build the scripts into an exe using PyInstaller via Build.bat. It will place the exe in the "build\dist" folder.