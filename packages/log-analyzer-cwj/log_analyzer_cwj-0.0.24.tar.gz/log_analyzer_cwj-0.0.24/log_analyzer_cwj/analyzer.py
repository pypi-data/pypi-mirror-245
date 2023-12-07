from log_analyzer_cwj import logAnalyzer
from log_analyzer_cwj import innerRule


def start(_ruleFile, _fastMode):
    print('------------start---------------')
    logAnalyzer.log_analyze(_ruleFile, _fastMode)


def json_all_to_dict(jsonString):
    return logAnalyzer.json_all_to_dict(jsonString)


def prepare(eventDict, startFlag):
    return innerRule.prepare(eventDict, startFlag)