# Streamlabs-Rcon-Integration

A tool that allows you to do actions in games based on Streamlabs events. Current usage focuses around Twitch events via Streamlabs triggering actions within Factorio. The tool is written in Python for cross platform usage and runs fully on your pc to remove any risk of sharing access keys or donators details on the internet.

The tool receives events from Streamlabs and uses configurable logic to send RCON commands to the game server to do actions.
The integration should support any game that allows for RCON and is coded to support multiple streaming platforms connected via Streamlabs; youtube, mixer and twitch.

This tool's setup is a little technical at present, but is fully functional and used by a few Factorio Twitch streamers. Any usage questions or issues grab me on discord: muppet9010#2645



Installation & Usage
==========
1. Install Python 3.7.3 32bit with default options: https://www.python.org/downloads/release/python-373/
2. Get the files from the [latest release zip](https://github.com/muppet9010/Streamlabs-Rcon-Integration/releases).
3. Create a free account at [Currency Layer website](https://currencylayer.com) and make a note of the API access key as needs to be entered into the program's config later on.
4. Unzip the files into the desired folder.
5. Rename `config.sample.json` to be just `config.json`. This is so that future updates don't overwrite your config files.
6. Open `config.json` in a text editor and add in your details - see later in readme for details
7. Run the program: Streamlabs Rcon Integration.exe
8. Select the desired profile from the dropdown. Suggested are the `Print All` and `Print Most Fancy`.
9. Click the Start button to connect the integration between Streamlabs and Factorio.
10. The integration is now running between the Streamlabs account and the game using the selected profile. Test events from streamlabs or from within the integration tool will now trigger activity within Factorio.

Should a critical error occur the program may fail to load or close. Details can be found in the most recent log file within the Logs folder.

Note: on clicking `Start` the program checks the RCON connection. If a Factorio server has been paused by a player then the RCON command will never respond and the application will freeze. Make sure that Factorio hasn't been paused by a player when clicking to `Start`. A server with 0 players on is not in this state.



Program Files
========

The app takes in Streamlabs events and processes them through configurable profiles to trigger the desired action via Rcon in game.

Streamlab Events
--------------

The complete list of Streamlabs events and their contained data attributes can be found in the [eventDefinitions.json file](https://github.com/muppet9010/Streamlabs-Rcon-Integration/blob/master/Source/eventDefinitions.json). The top section under `[ALL]` are generated and normalised by the program to provide some standard entries across all event types. The list of platform and event specific attributes are what Streamlabs is currently sending. These often vary from their platform documentation and change periodically, so please refer to this tools definition.

Profile
---------

The app loads and runs a single profile at a time, with a profile being stored as a single JSON file. At present a profile file must be manually made by someone familiar with JSON syntax.
Example profiles can be found here: [example profiles folder](https://github.com/muppet9010/Streamlabs-Rcon-Integration/blob/master/Source/Profiles)
Profiles are structured as the below:

- Profile file (.json):
    - "name" - the name of the profile as seen within the application
    - "description" - a short description shown within the application for this profile
    - "reactions" - an array [] of unique reactions stored as dictionaries {} of attributes in key, value pairs.
        - "platform" - the event platform identifier string for this reaction
        - "type" - the event type identifier string for this reaction
        - "filteredActions" - an array [] of unique filteredActions stored as dictionaries {} of attributes in key, value pairs.
            - "condition" - a condition for this filteredAction being done as a string
            - "manipulator" - an optional value change script
            - "action" - the text string that will be sent via RCON after being processed, or the name of a profile "actions" to call.
    - "actions" - an array [] of unique actions stored as dictionaries {} of attributes in key, value pairs.
            - "name" - the name of the action as called from filteredActions.
            - "description" - a description just used within the JSON for documentation purposes
            - "effect": - the text string that will be sent via RCON after being processed
    - "options" - a dictionary {} of profile wide options, as key, value pairs.



Event Handling via Profile
==========

When a Streamlabs event is received by the app it reviews the reactions within the current profile to work out what actions to take.

Event Attributes
-----------

When a Streamlabs event is initially received it will have its unique event attributes pre-populated, i.e. a Twitch subscription will have its subscriber level and viewer username. The event is processed to have the `[ALL]` event attributes generated for it. This includes calculating the events `VALUETYPE` of either money, follow, viewer. These attributes are used during the processing logic for the event.

All built in event attributes are wrapped in square brackets when used as values, i.e. `[VALUE]`

Reactions
------------

The reactions for the profile are reviewed to find the most appropriate single one. Firstly, each reactions `platform` and `type` attributes are compared against the events `platform` and `type`, i.e. `twitch_account-subscription`. If no reaction is found, then the `ValueType` of each reaction is compared to the `ValueType` of the event for a match, i.e. `money`. This enables you to be very specific on platform and event match, generic on ValueType, or a mix of the two.

If no suitable reaction is found for the event, the app will show a warning. It's assumed you want to explicitly handle all events you get. Use of the `ValueType` to react to undesired event types is advised. As reactions can have an explicit do nothing action.

Assuming a reaction for the event is found, the reaction's `filteredActions` are then reviewed for this event.

Filtered Actions
--------------

Each `filteredActions` list will have one or more filteredAction entries in it. Each of these entries is reviewed and its action carried out if appropriate.

### Condition

The `condition` script in each filteredAction is evaluated and those that are met (resolves to True) will have their action executed for this event. All of the events data attributes from Streamlabs and this app can be used within the `condition` script in the format `[DATA_ITEM_NAME]`. i.e. `[VALUE] >= 5 and [VALUE] < 10`. The conditions within a reaction are order specific (excluding `[ALL]` condition) and can overlap each other's conditions if you wish both to be executed in those circumstances.

There is a special `[ALL]` condition script value that will be triggered after all other suitable conditions have been triggered in all cases.

If a condition for a filtered action is met then the manipulator script and action are carried out

### Manipulator Script

Each filteredActions can have an optional manipulator script configured. If configured this will create a new event attribute called `[CALCVALUE]` containing the scripts output value. This is used when you want to pass a modified value into the game, i.e. action twice the dollar value of a viewers support event. Note that the values are treated as doubles and so rounding of the output to the desired accuracy is advised.

### Action

The action tied to the filteredAction is the Rcon command string that is run in the game. Actions can be either a specific Lua command string or the name of a shared Lua Action string defined within the `Actions` list in the profile.

Action command strings can utilise any of the events data attributes in the standard format `[DATA_ITEM_NAME]`. i.e. `[name] supported with $[VALUE] worth $[CALCVALUE]` or `/promote [name]`. There is a special `[NOTHING]` action that is intended for intentionally ignoring the event. This avoids any warnings about unhandled events.

Should an Rcon command get a response from the server it will be shown in the Activity Log as is likely an error from the game.

Actions
--------

The Actions list is a collection of named action command strings to enable their re-use when it's convenient. Their `effect` is identification to a filteredAction action.

Options
-----------

A number of profile wide options exist to allow further configuration of specific behaviour.

- twitchMysterSubGiftMode - When Twitch Subscription Mystery Gifts are given out by a viewer to random other viewers the event can either be reacted to for the donator or receiver. The program's default is the `donator` value if the setting isn't specified in the profile's options. If the Streamlabs event is reacted to by a `money` valueType reaction, rather than a twitch subscriber specified reaction, it will obey this setting so only 1 reaction is triggered. Meaning the other event type won't be triggered for Twitch Subscription Mystery Gifts to avoid duplicate reactions.
    - `donator` - React to it as one large donation using the `subMysteryGift` event reaction.
    - `receiver` - React to each viewer getting the gifted subscription using the `subscriptionGift` event reaction.
YES this setting has a typo in it.


Profile Creation Notes
--------------------

### Profile attribute values, quotes and quote escaping

All data attributes used in scripts are replaced with their event data values at execution time. The replaced text may require wrapping in quotes if it needs to be treated as a string when it is received by the game through the RCON command.

However, the profile file is defined using JSON syntax and so all text strings must be wrapped in double quotes `"` within the profile. Single quotes can be used within a JSON string without the need to escape them, and are advised for this reason where possible. If you need to use a double quote within a text string it must be escaped with a backslash `\`. In some cases single quotes may not be accepted by the game/mod receiving the RCON command, and so escaped double quotes would have to be used, i.e. a mod expects a JSON string as an argument.

Data attribute values will be made safe by the program; with any single or double quotes either being removed by Python automatically or escaped with a backslash before being used as part of a Rcon command. If you require a single or double quote to be received by Rcon escaped then you must escape it with 2 backslashes `\\'`. See the `Factorio - Advanced Usage Example.json` for examples of the some of these combinations.

### Condition & Manipulator Scripts

Manipulator scripts are special in that they support raw python code that will be executed.

The event handler will first try to eval() the manipulator script first. This is used for simple condition logic and simple value manipulation activities. The result of the eval() will be passed out as an event attribute `CALCVALUE`.

If the eval() fails (errors) then the script will be executed with exec(). In this case the script must be in a single line format with `\n` for the line breaks as its is supplied via the profile JSON file it. The Python maths module is included in this execution environment. The local script variable `calcValue` must be specified and is passed out of the exec() environment as the event attribute `CALCVALUE`.

See the `Factorio - Advanced Usage Example.json` for examples of the some of these combinations. Note that the values are treated as doubles when being manipulated and so rounding of the output to the desired accuracy is advised.

### Valid JSON Check At Startup

When the application starts up all profiles in the profile folder are checked for their compliance with the event handler types and their attributes. All conditions and manipulators will be tested with a value of "1" for all attributes to confirm they are valid python scripts. Any issues cause the program to stop loading and the issue is recorded to the log file. This is to avoid failure from misconfiguration at run time.
Additional profiles can be created within the Profiles folder following the sample profile syntax and the eventDefinitions.json events and attributes.



Testing Notes
=============

After configuring the application it is advised to run it and use the Streamlabs Test Widget option to send test events and confirm it behaves as you expect.

Built in Testing
-----------------

There is a crude event testing option at the bottom of the app. It will fake Streamlabs events to the program, allowing testing of reactions. It is often useful to enable the `Rcon No Commands` config option to allow testing by printing the Rcon commands rather than running them.

Each platform and event type will dictate if the input fields are enabled/utilised or not. These fields control specific attributes of the faked events.

- Event Value: The raw value passed into the event. This can be a whole number (int) or decimal (float) and used by most events. For donations and pledges it will be the USD value, the number of bits or the type of twitch subscription (1000, 2000, 3000).
- Quantity: The quantity of the event. This must be a whole positive number when used. For Mystery Gift Subscriptions this is how many subscriptions are being gifted.
- Payload Count: The number of viewers events contained within this Streamlabs API call. This is to simulate Streamlabs habit of bundling multiple events of the same type together if they happen at the same time. i.e. if 2 viewers both follow at once you will get 1 Streamlabs API call with 2 payloads (events) within it. This is invisible from the reactions as each event is handled separately, but included for developer testing, so leave as the default value of `1`.



Program Config Notes
============

The program has a `config.json` that stores its global configuration. The settings in here that require additional details are:

- Logging DaysLogsToKeep - How many days back of logs the program will keep. -1 keeps logs indefinitely.
- Logging DebugLogging - If enhanced Debug logs are generated. true/false
- Currency ApiLayerAccessKey - The Currency API key generated when signing up to the free currency API website.
- Streamlabs SocketApiToken - Your streamlabs API key. This can be found on the streamlabs website under your account:
    1. login to streamlabs website.
    1. "Settings" on left hand menu.
    1. "API Settings" tab.
    1. "API Token" on inner tab.
    1. There's then the "Your Socket API Token".
- Profile Default - The name of the profile json file that will be selected on loading the application. Profile can be reselected once loaded.
- Rcon Server Address - The URL/IP address of your game server. Must be reachable from where you are running this application.
- Rcon Server Port - The port that RCON is running on, on your game server. Must be reachable from where you are running this application.
- Rcon Server Password - The password you set in your game, or can be blank if no password was set (not advised).
- Rcon Test Command - The command the application will send to check RCON is working on clicking `Start`. For Factorio a safe (default) value is `/version`.
- Rcon No Commands - When enabled it prints the RCON commands to the activity window rather than sending them. It also skips the RCON connection test which the Start button is clicked within the app. In effect not doing any RCON commands.



Development Building
=============
Uses the python modules and their dependencies. Built and tested against these old versions:

- Python 3.7.3 32bit - default install modules  =  https://www.python.org/downloads/release/python-373
- python-engineio 3.5.1  (pre-requisite of socketio, but if not done first the wrong dependant version gets installed by socketio) =  pip install python-engineio==3.5.1
- python-socketio[client] 4.0.1  =  https://python-socketio.readthedocs.io/en/latest  =  pip install python-socketio[client]==4.0.1
- PyInstaller 3.4  =  https://www.pyinstaller.org  =  pip install -U pyinstaller==3.4
- MCRcon 0.5.2 =  https://github.com/uncaught-exceptions/mcrcon  =  pip install mcrcon==0.5.2

It can either be built or run directly from a Python environment via the `Streamlabs Rcon Integration.py`.

To build the scripts into an exe use PyInstaller via `Build.bat`. It will place the exe and other config files in the `build\dist` folder. This `dist` folder is the program and can be shared via zip.

Note: I have only ever built this under Windows, however I haven't seen any of the dependencies or my code being listed as not linux compatible.