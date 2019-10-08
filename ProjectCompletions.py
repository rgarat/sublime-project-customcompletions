import sublime_plugin
import re
import pprint

def all_match(view, locs, selector):
    for loc in locs:
        if not view.score_selector(loc, selector):
            return False
    return True

def matchesRule(view, locs, rule):  
    pprint.pprint(rule)
    if 'scopes' in rule:
        scopes = rule["scopes"]
        print("Checking rule scope " + scopes)
        return all_match(view, locs, scopes)

    if 'file_paths' in rule:
        file_regexpList = rule["file_paths"]
        file_name = view.file_name()
        print("Checking rule path " + ", ".join(file_regexpList))
        for file_regexp in file_regexpList:
            if re.match(file_regexp, file_name):
                return True
        return False

    print("Unknown rule match")
    return True

def matchesRules(view, locs, rules):
    for rule in rules:
        print("Rule")
        if not matchesRule(view, locs, rule):
            print("Match Failed")
            return False

    print("Match Success")
    return True

class ProjectCompletions(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        if view.window() and view.window().project_data():
            print("ProjectAutocomplete")
            completions = view.window().project_data().get("completions2")
            result = []
            for item in completions:
                rules  = item.get("rules",[])
                if matchesRules(view, locations, rules):
                    result += item.get("completions")
            return result
        return None

