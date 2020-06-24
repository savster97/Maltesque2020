"""
The code in this file elaborates the analysis results from monsterFilePMD.csv.
It prints the total issues from the projects, the number of issues under each severity,
the number of rules under each category, and the number of issues under each rule. In addition,
output CSV files for each of these are exported.
"""

import pandas as pd
import os
import glob
import sys

def exportDict (dict, nameOfFile):
    """
    Exports a csv file from the dictionary.
    :param dict: Dictionary for exporting. (dict)
    :param nameOfFile: Name of the exported CSV file. (string)
    :return: none
     """
    dictTable = pd.DataFrame(dict)
    dictTable.to_csv(nameOfFile)

mainPath = "/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction" \
           "/PMD_Parsing_File_Outputs/monsterFilePMD.csv" # Read the analysis results

# Collecting all relevant information
issues = []
severities = []
categories = []
rules = []

# Information stored in dictionaries to keep track
severityToIssue = {}
ruleToIssue = {}
categoryToRule = {}


data = pd.read_csv(mainPath)
numRows = len(data['issue'])
index = 0

while index < numRows:

    # Adding issues that have not been found
    issue = data['issue'][index]
    if issue not in issues:
        issues.append(issue)

    # Adding severities that have not been found and then adding to dict
    severity = data['severity'][index]
    if severity not in severities:
        severities.append(severity)
        severityToIssue[severity] = [issue]

    # If severity is found then check if the issue has been added to the dict
    elif severity in severities:
        if issue not in severityToIssue[severity]: # Add issue if ít hasn't been added under severity
            severityToIssue[severity].append(issue)

    # Adding rules that have not been found and then adding to dict
    rule = data['rule'][index]
    if rule not in rules:
        rules.append(rule)
        ruleToIssue[rule] = [issue]

    # If rule is found then check if the issue has been added to the dict
    elif rule in rules:
        if issue not in ruleToIssue[rule]: # Add issue if ít hasn't been added under rule
            ruleToIssue[rule].append(issue)

    # Adding categories that have not been found and then adding to dict
    category = data['category'][index]
    if category not in categories:
        categories.append(category)
        categoryToRule[category] = [rule]

    # If category is found then check if the rule has been added to the dict
    elif category in categories:
        if rule not in categoryToRule[category]: # Add rule if ít hasn't been added under category
            categoryToRule[category].append(rule)

    index += 1


print("The  total number of issues is: " + str(len(issues)))
print("The  total number of severities is: " + str(len(severities)))
print("The total number of categories is: " + str(len(categories)))
print("The total number of rules is: " + str(len(rules)))

for key in severityToIssue.keys():
    print("The  number of issues under " + str(key) + " severity is: " + str(len(severityToIssue[key])))

for key in ruleToIssue.keys():
    print("The  number of issues under " + str(key) + " rule is: " + str(len(ruleToIssue[key])))

for key in categoryToRule.keys():
    print("The  number of rules under " + str(key) + " category is: " + str(len(categoryToRule[key])))

os.chdir("/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/PMD_Parsing_File_Outputs")

# To make the CSV files to see all the unique issues, severities, categories, and rules.
issueDict = {'issues': issues}
severitiesDict = {'severities': severities}
categoriesDict = {'categories': categories}
rulesDict = {'rules': rules}

# Export all the information into separate CSV files.
exportDict(issueDict, 'allIssuesPMD.csv')
exportDict(severitiesDict, 'allSeveritiesPMD.csv')
exportDict(categoriesDict, 'allCategoriesPMD.csv')
exportDict(rulesDict, 'allRulesPMD.csv')

# For each of the severities, export a CSV file containing all issues under that severity.
for key in severityToIssue.keys():
    fileName = str(key) + 'IssuesPMD.csv'

    severityIssueDict = {str(key): severityToIssue[key]}
    exportDict(severityIssueDict, fileName)

# For each of the rules, export a CSV file containing all issues under that rule.
for key in ruleToIssue.keys():
    fileName = str(key) + 'IssuesPMD.csv'

    ruleIssueDict = {str(key): ruleToIssue[key]}
    exportDict(ruleIssueDict, fileName)

# For each of the categories, export a CSV file containing all rules under that category.
for key in categoryToRule.keys():
    fileName = str(key) + 'RulesPMD.csv'

    categoryRuleDict = {str(key): categoryToRule[key]}
    exportDict(categoryRuleDict, fileName)
