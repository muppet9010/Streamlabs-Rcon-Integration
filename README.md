# Streamlabs-Rcon-Integration


A Python exe for integrating Streamlabs and any game supporting Rcon. Its currently being used with Factorio, but should be compatible with any other Rcon interfaced game.
At present only really tested with Twitch, but should work with mixer and youtube based on API spec.


Installation & Usage
==========
Get the [latest version zip](https://github.com/muppet9010/Streamlabs-Rcon-Integration).
Create a free account at [Currency Layer website](https://currencylayer.com) and make a note of the API access key as needs to be entered in to the programs config later on.
Unzip the files in to the desired folder.
Open config.json in a text editor and add in your details.
Run the program: Streamlabs Rcon Integration.exe
Select the desired profile from the dropdown and click Start.
The integration is now running between the Streamlabs account and the game using the selected profile.

Should a critical error occur the program may fail to load or close. Details can be found in the most recent log file within the Logs folder.


Usage Concepts
========

The app takes in Streamlabs events and processes them through configurable reactions to trigger a desired action via Rcon in  game. These reactions are grouped togeather as savable profiles.

The complete list of Streamlabs events and their contained data attributes can be found in the [eventDefinitions.json file](https://github.com/muppet9010/Streamlabs-Rcon-Integration/eventDefinitions.json). The top section under `[ALL]` are generated and normalised by the program to provide some standard entries across all event types. The list of platform and event specific attributes are what streamlabs is currently sending. These often vary from their documentation and change periodically.

The app runs a single grouping of reactions at a time, being loaded and saved as a profile. During the process if no suitable option is found it will be shown within the app and that events processing stops. Its assumed you want to handle any event you get. Special options at each level exist for more simple uses cases.

When an Streamlabs event is received it is processed to have the standard `[ALL]` additional data attributes calculated for them. The reactions are reviewed to find the most approperiate one. First the reactions are checked for the first matching platform and type to the event. If no match is found the ValueType of the event is checked for in the reactions for a match.

Assuming a reaction for the event is found the reaction's filter script is checked for the first that is met (resolves to True). Filters allow a scripts conditions to be used to select the approperiate action to do for the event. All of the events data attributes from Streamlabs and this app can be used witihn the filter in the format `[DATA_ITEM_NAME]`. i.e. `[VALUE] >= 5 and [VALUE] < 10`. There is a special `ALL` filter option that it configured will be triggered after all other filters have been checked. The filters within a reaction are not order specific and so should not overlap each others conditions.

The first complying reaction filter will then run an optional manipulator script if configured. This creates a new data item for the event `[MODVALUE]` with the scripts output value. This is used when you want to pass a modified value in to the game.

The action tied to the filter are the Rcon commands that are run in the game. It can utilise any of the events data attributes in the standard format `[DATA_ITEM_NAME]`. i.e. `[name] supported with $[VALUE] worth $[MODVALUE]` or `/promote [name]`. There is a special `NOTHING` action that is intended for intentionally ignoring the event. This avoids any warnings about unhandled events. Actions can be either a specific Lua command string or the name of a shared Lua command string within the profile. This is to allow re-use of Lua command strings when its convienent. Should an Rcon command get a response from the server it will be shown in the Activity Log as is liekly an error from the game.

All data attributes used in scripts are replaced with their event data values at execution time. The replaced text may require wrapping in quotes if it needs to be treated as a string. A script is a single python expression that can be processed via the Python eval() function.

When the application starts up all profiles in the profile folder are checked for their compliance with the event handler types and their attributes. All conditions and manipulators will be tested with a value of "1" for all attributes to confirm they are valid python scripts. Any issues causes the program to stop loading and the issue is recorded to the log file. This is to avoid failure from mis-configuration at run time.
Additional profiles can be created within the Profiles folder following the sample profile syntax and the eventDefinitions.json events and attributes.

After configuring the application it is advised to run it and use the Streamlabs Test Widget option to send test events and confirm it behaves as you expect.

Profile configuration files must be created with knowledge of quote escaping. The profile file is in the JSON syntax and so all text strings must be wrapped in double quotes `"` within it. If you want to use a duoble quote within a text string it must be escaped with a back slash `\`. Single quotes can be used fine within a JSON string and are advised for this reason. Data attributes will be made safe by the program; with any single or doube quotes either being removed by Python automatically or escaped with a backslash before being used as part of an rcon command. If you require a single or double quote to be recieved by Rcon escaped then you must escape it with 2 back slashes `\\'`. See the `Factorio - Advanced Usage Example.json` for examples of the some of these combinations.


Development Building
=============
Uses the python modules and their dependcies:

- Python 3.7 and default install modules
- python-socketio[client]  =  https://python-socketio.readthedocs.io/en/latest/
- PyInstaller  =  https://www.pyinstaller.org/
- MCRcon  =  https://github.com/uncaught-exceptions/mcrcon

Build the scripts into an exe using PyInstaller via Build.bat. It will place the exe and other files in the `build\dist` folder. This `dist` folder is the program and can be shared via zip.
