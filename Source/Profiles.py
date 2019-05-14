import json as Json
import os as Os


class Profiles:
    def __init__(self, state):
        self.State = state
        self.profileFolder = "Profiles"
        self.profiles = {}
        if not Os.path.isdir(self.profileFolder):
            Os.mkdir(self.profileFolder)
        else:
            self._LoadProfilesFromFolder()

    def _LoadProfilesFromFolder(self):
        for fileName in Os.listdir(self.profileFolder):
            with open(self.profileFolder + "/" + fileName, "r") as file:
                data = Json.load(file)
            file.closed
            self.profiles[data["name"]] = Profile(data)


class Profile:
    def __init__(self, profileData):
        self.name = profileData["name"]
        self.description = profileData["description"]
        self.actions = {}
        if "actions" in profileData:
            for actionData in profileData["actions"]:
                self.actions[actionData["name"]] = Action(actionData)
        self.reactionPriorities = {1: [], 2: []}
        for reactionData in profileData["reactions"]:
            self._AddReaction(reactionData)

    def _AddReaction(self, reactionData):
        reaction = Reaction(reactionData, self)
        if "platform" in reactionData:
            self.reactionPriorities[1].append(reaction)
        elif "valuetype" in reactionData:
            self.reactionPriorities[2].append(reaction)


class Reaction:
    def __init__(self, reactionData, profile):
        if "platform" in reactionData:
            self.platform = reactionData["platform"]
            self.type = reactionData["type"]
        else:
            self.valueType = reactionData["valueType"]
        self.filterPriorities = {1: [], 2: []}
        for filteredActionData in reactionData["filteredActions"]:
            self._AddfilteredActionData(filteredActionData, profile)

    def _AddfilteredActionData(self, filteredActionData, profile):
        filteredAction = FilteredAction(filteredActionData, profile)
        if filteredAction.condition == "[ALL]":
            self.filterPriorities[2].append(filteredAction)
        else:
            self.filterPriorities[1].append(filteredAction)


class FilteredAction:
    def __init__(self, filteredActionData, profile):
        self.condition = filteredActionData["condition"]
        self.manipulator = filteredActionData["manipulator"]
        action = filteredActionData["action"]
        if action[0:8] == "[ACTION_" and action[-1:] == "]":
            self.action = profile.actions[action[8:-1]]
        else:
            self.action = action


class Action:
    def __init__(self, actionData):
        self.name = actionData["name"]
        self.description = actionData["description"]
        self.effect = actionData["effect"]
