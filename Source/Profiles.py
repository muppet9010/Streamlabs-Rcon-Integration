import json as Json
import os as Os
from StreamlabsEvent import StreamlabsEventUtils


class Profiles:
    def __init__(self, state):
        self.state = state
        self.profileFolder = "Profiles"
        self.profiles = {}
        self.currentProfile = None
        if not Os.path.isdir(self.profileFolder):
            Os.mkdir(self.profileFolder)
        else:
            for fileName in Os.listdir(self.profileFolder):
                with open(self.profileFolder + "/" + fileName, "r") as file:
                    data = Json.load(file)
                file.closed
                self.profiles[data["name"]] = Profile(data, self)

    def SetCurrentProfile(self, profileName):
        self.currentProfile = self.profiles[profileName]


class Profile:
    def __init__(self, profileData, profiles):
        self.profiles = profiles
        self.name = profileData["name"]
        self.description = profileData["description"]
        self.actions = {}
        if "actions" in profileData:
            for actionData in profileData["actions"]:
                self.actions[actionData["name"]] = Action(actionData)
        self.reactionPriorities = {1: [], 2: []}
        for reactionData in profileData["reactions"]:
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
        self.logging = profile.profiles.state.logging
        self.profile = profile
        self.platform = ""
        self.type = ""
        self.handlerName = ""
        self.valueType = ""
        if "platform" in reactionData:
            self.platform = reactionData["platform"]
            self.type = reactionData["type"]
            self.handlerName = StreamlabsEventUtils.MakeHandlerString(
                self.platform, self.type)
            if self.handlerName not in StreamlabsEventUtils.handledEventTypes.keys():
                self.logging.LogQuit(
                    "invalid event handler type: " + self.handlerName)
        else:
            self.valueType = reactionData["valueType"]
            if self.valueType not in ["money", "follow", "viewer"]:
                self.logging.LogQuit("invalid valueType: " + self.valueType)
        self.filterActionPriorities = {1: [], 2: []}
        for filteredActionData in reactionData["filteredActions"]:
            filteredAction = FilteredAction(filteredActionData, self)
            if filteredAction.condition == "[ALL]":
                self.filterActionPriorities[2].append(filteredAction)
            else:
                self.filterActionPriorities[1].append(filteredAction)

    def GetActionTextForEvent(self, event):
        for filterAction in self.filterActionPriorities[1]:
            if filterAction.DoesEventTriggerAction(event):
                return filterAction.GetActionText(event)
        for filterAction in self.filterActionPriorities[2]:
            if filterAction.DoesEventTriggerAction(event):
                return filterAction.GetActionText(event)
        return None

    def GetPrintHandlerType(self):
        if self.handlerName != "":
            return self.handlerName
        else:
            return self.valueType


class FilteredAction:
    def __init__(self, filteredActionData, reaction):
        self.reaction = reaction
        self.logging = self.reaction.profile.profiles.state.logging

        self.condition = filteredActionData["condition"]
        if self.condition == "":
            self.logging.LogQuit("'" + self.reaction.GetPrintHandlerType() +
                                 "' condition can not be blank")
        eventAttributeCheckResult = StreamlabsEventUtils.IsBadEventAttritubeUsed(
            self.reaction.handlerName, self.condition, False)
        if eventAttributeCheckResult != "":
            self.logging.LogQuit("'" + self.reaction.GetPrintHandlerType() +
                                 "' condition error: " + eventAttributeCheckResult)
        scriptParseCheck = StreamlabsEventUtils.IsScriptValid(self.condition)
        if scriptParseCheck != "":
            self.logging.LogQuit("'" + self.reaction.GetPrintHandlerType() +
                                 "' has an invalid condition script:\n" + scriptParseCheck)

        self.manipulator = filteredActionData["manipulator"]
        eventAttributeCheckResult = StreamlabsEventUtils.IsBadEventAttritubeUsed(
            self.reaction.handlerName, self.manipulator, False)
        if eventAttributeCheckResult != "":
            self.logging.LogQuit("'" + self.reaction.GetPrintHandlerType() +
                                 "' manipulator error: " + eventAttributeCheckResult)
        scriptParseCheck = StreamlabsEventUtils.IsScriptValid(self.manipulator)
        if scriptParseCheck != "":
            self.logging.LogQuit("'" + self.reaction.GetPrintHandlerType() +
                                 "' has an invalid manipulator script:\n" + scriptParseCheck)

        self.actionText = ""
        self.action = None
        action = filteredActionData["action"]
        if action[0:8] == "[ACTION_" and action[-1:] == "]":
            actionName = action[8:-1]
            if actionName in self.reaction.profile.actions.keys():
                self.action = self.reaction.profile.actions[actionName]
                eventAttributeCheckResult = StreamlabsEventUtils.IsBadEventAttritubeUsed(
                    self.reaction.handlerName, self.action.effect, True)
                if eventAttributeCheckResult != "":
                    self.logging.LogQuit("'" + self.reaction.GetPrintHandlerType() + "' referenced action " +
                                         actionName + " which has action text error: " + eventAttributeCheckResult)
            else:
                self.logging.LogQuit("'" + self.reaction.GetPrintHandlerType() +
                                     "' referenced non-existent action : " + actionName)
        else:
            self.actionText = action
            if self.actionText == "":
                self.logging.LogQuit("'" + self.reaction.GetPrintHandlerType() +
                                     "' action can not be blank")
            eventAttributeCheckResult = StreamlabsEventUtils.IsBadEventAttritubeUsed(
                self.reaction.handlerName, self.actionText, True)
            if eventAttributeCheckResult != "":
                self.logging.LogQuit("'" + self.reaction.GetPrintHandlerType() +
                                     "' action text error: " + eventAttributeCheckResult)

    def DoesEventTriggerAction(self, event):
        if self.condition == "[ALL]":
            return True
        conditionStringPopulated = event.SubstituteEventDataIntoString(
            self.condition)
        if eval(conditionStringPopulated) == True:
            return True
        else:
            return False

    def GetActionText(self, event):
        if self.actionText == "[NOTHING]":
            return ""
        actionText = self.actionText
        if self.action != None:
            actionText = self.action.effect
        if self.manipulator != None and self.manipulator != "":
            manipulatorValueString = event.SubstituteEventDataIntoString(
                self.manipulator)
            manipulatorValue = 0
            try:
                manipulatorValue = eval(manipulatorValueString)
            except:
                manipulatorValue = StreamlabsEventUtils.ProcessExecScript(
                    manipulatorValueString)
            return event.SubstituteEventDataIntoString(
                actionText, manipulatorValue)
        return event.SubstituteEventDataIntoString(
            actionText)


class Action:
    def __init__(self, actionData):
        self.name = actionData["name"]
        self.description = actionData["description"]
        self.effect = actionData["effect"]
