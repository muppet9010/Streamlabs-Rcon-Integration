import json as Json
import os as Os
from StreamlabsEvent import StreamlabsEvent


class Profiles:
    def __init__(self, state):
        self.State = state
        self.profileFolder = "Profiles"
        self.profiles = {}
        self.currentProfile = None
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

    def SetCurrentProfile(self, profileName):
        self.currentProfile = self.profiles[profileName]


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
        elif "valueType" in reactionData:
            self.reactionPriorities[2].append(reaction)

    def GetActionTextForEvent(self, event):
        for reaction in self.reactionPriorities[1]:
            if reaction.handlerName == event.handlerName:
                result = reaction.GetActionTextForEvent(event)
                if result != None:
                    return result
        for reaction in self.reactionPriorities[2]:
            if reaction.valueType == event.valueType:
                result = reaction.GetActionTextForEvent(event)
                if result != None:
                    return result
        return None


class Reaction:
    def __init__(self, reactionData, profile):
        # TODO validate these values are accepted and throw error if not
        if "platform" in reactionData:
            self.platform = reactionData["platform"]
            self.type = reactionData["type"]
            self.handlerName = StreamlabsEvent.MakeHandlerString(
                self.platform, self.type)
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

    def GetActionTextForEvent(self, event):
        # TODO HERE - Parse over the filterPriorities and filteredActions to find the approperiate one. If nothing found return None
        print(self.handlerName)
        return "found " + self.handlerName


class FilteredAction:
    def __init__(self, filteredActionData, profile):
        # TODO Validate the condition and manipulator text strings
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
