import pandas as pd
import os
import glob

def exportDict (dict, nameOfFile):
    dictTable = pd.DataFrame(dict)
    dictTable.to_csv(nameOfFile)

mainPath = "/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/PMD_Parsing_File_Outputs/monsterFilePMD.csv"

# Collecting all information
issues = []
severities = []
types = []

severityToIssue = {}
typeToIssue = {}

data = pd.read_csv(mainPath)
numRows = len(data['issue'])
index = 0

while index < numRows:

    issue = data['issue'][index]
    if issue not in issues:
        issues.append(issue)

    severity = data['severity'][index]
    if severity not in severities:
        severities.append(severity)
        severityToIssue[severity] = [issue]

    elif severity in severities:
        if issue not in severityToIssue[severity]:
            severityToIssue[severity].append(issue)

    type = data['type'][index]
    if type not in types:
        types.append(type)
        typeToIssue[type] = [issue]

    elif type in types:
        if issue not in typeToIssue[type]:
            typeToIssue[type].append(issue)

    index += 1

print("The  number of issues is " + str(len(issues)))
print("The  number of severities is " + str(len(severities)))
print("The  number of types is " + str(len(types)))

for key in severityToIssue.keys():
    print("The  number of issues under " + str(key) + " severity is: " + str(len(severityToIssue[key])))

for key in typeToIssue.keys():
    print("The  number of issues under " + str(key) + " type is: " + str(len(typeToIssue[key])))

os.chdir("/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/PMD_Parsing_File_Outputs")

issueDict = {'issues': issues}
severitiesDict = {'severities': severities}
typesDict = {'types': types}

exportDict(issueDict, 'issuesPMD.csv')
exportDict(severitiesDict, 'severitiesPMD.csv')
exportDict(typesDict, 'typesPMD.csv')

for key in severityToIssue.keys():
    fileName = str(key) + 'IssuesPMD.csv'

    severityIssueDict = {str(key): severityToIssue[key]}
    exportDict(severityIssueDict, fileName)

for key in typeToIssue.keys():
    fileName = str(key) + 'IssuesPMD.csv'

    typeIssueDict = {str(key): typeToIssue[key]}
    exportDict(typeIssueDict, fileName)
