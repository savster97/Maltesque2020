"""
The code in this file converts the XML files from PMD
into one summary CSV file. The CSV file contains all the
relevant information from all the project analysis results.
"""

import pandas as pd
import os
import glob
import xml.etree.cElementTree as et
import csv


def extractLanguage(fileName):
    """
    Returns the language the code is written in concerning the violation.
    :param fileName: File path (string)
    :return: language (string)
    """
    className = fileName.split("/")[-1]
    language = className.split(".")[-1]

    return language


mainDirectory = "/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/PMD_Raw_Data"
os.chdir(mainDirectory) # Changing directory to iterate through all the raw data from the analysis

# Creating the output csv file structure
projectNames = []
tools = []
languages = []
packages = []
classNames = []
methods = []
categories = []
rules = []
issues = []
startLines = []
endLines = []
severities = []

missingFiles = []
processedFiles = []

for file in glob.glob("*.xml"):
    print("This is the file: " + file)
    processedFiles.append(str(file))

    projectName = file.split("_PMD")[0]
    tool = "PMD"

    # This is implace to catch any files that were not in
    # the proper XML format imported from PMD.
    try:
        tree = et.parse(file)
        root = tree.getroot()

        print("This is the root tag: " + root.tag)
        print("This is the root attrib: " + root.attrib)
    # In case some files were not in the right XML format. These are reported in the missingFiles.
    # The code shouldn't enter here preferably (assuming all the XML files are proper).
    except:
        missingFiles.append(str(file))
        processedFiles.remove(str(file))
        pass

    # Iterate through all the violations reported in a class.
    for child in root:

        if str(child.tag) == "{http://pmd.sourceforge.net/report/2.0.0}file":

            language = extractLanguage(str(child.attrib['name']))

            for subChild in child:

                try:
                    category = str(subChild.get('ruleset'))
                    rule = str(subChild.get('rule'))
                    issue = str(subChild.text)
                    startLine = str(subChild.get('beginline'))
                    endLine = str(subChild.get('endline'))
                    package = str(subChild.get('package'))
                    className = str(subChild.get('class'))
                    method = str(subChild.get('method'))
                    severity = str(subChild.get('priority'))

                    # Skipping instances of "$assert"
                    if ((className.find("$assert") != -1) or (method.find("$assert") != -1)):
                        pass
                    else:
                        # Adding to arrays
                        projectNames.append(projectName)
                        tools.append(tool)
                        languages.append(language)
                        packages.append(package)
                        classNames.append(className)
                        methods.append(method)
                        categories.append(category)
                        rules.append(rule)
                        issues.append(issue)
                        startLines.append(startLine)
                        endLines.append(endLine)
                        severities.append(severity)

                except:
                    pass

print("before dictionary")
test = {"projectName": projectNames, "tool": tools, "language": languages, "package": packages, "class": classNames,
        "method": methods, "category": categories, "rule": rules, "issue": issues, "startLine": startLines, "endLine": endLines,"severity": severities}

# Making sure there are no problems with the length of the arrays for the file
print(len(projectNames))
print(len(tools))
print(len(languages))
print(len(packages))
print(len(classNames))
print(len(methods))
print(len(categories))
print(len(rules))
print(len(issues))
print(len(startLines))
print(len(endLines))
print(len(severities))

print("before dataframe")
output = pd.DataFrame(test)

# To arrange the CSV file to output in the mentioned order. Otherwise the order of the columns is randomly allocated.
output = output[['projectName', 'tool', 'language', 'package', 'class', 'method', 'category', 'rule', 'issue', 'startLine', 'endLine', 'severity']]
output.sort_values("class", axis = 0, ascending = True, inplace = True, na_position ='last')

print("changing directory")
os.chdir("/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/PMD_Parsing_File_Outputs")

print("creating csv file")
output.to_csv("monsterFilePMD.csv")
output.to_csv("monsterFilePMD.csv", quoting=csv.QUOTE_NONNUMERIC, index=False)
