"""
The code in this file converts the XML files from FindBugs
into one summary CSV file. The CSV file contains all the
relevant information from all the project analysis results.
"""

import pandas as pd
import os
import glob
import xml.etree.cElementTree as et
import csv


def extractLanguage(sourceFile):
    """
    Returns the language the code is written in concerning the violation.
    :param sourceFile: Name of class (string)
    :return: language (string)
    """

    language = sourceFile.split(".")[1] # Extract the extension

    return language


def extractPackage (className):
    """
    Returns the package name where the violation occurs if it exists.
    :param className: File path (string)
    :return: packageName (string)
    """

    packageName = className.rsplit(".", 1)[0] # Remove the part of the string that contains the class name

    return packageName


def extractClass (className):
    """
    Returns the class name where the violation occurs if it exists.
    :param className: File path (string)
    :return: className (string)
    """

    className = className.rsplit(".", 1)[1]

    return className


def extractMethod (name):
    """
    Returns the method name where the violation occurs if it exists.
    Otherwise returns an empty string.
    :param name: method name (string)
    :return: methodName (string)
    """
    onlyClass = False
    methodName = ""

    # If you can find traces of a method being mentioned, exclude since it means they only provide the class.
    if ((name.find(".") == -1) and (name.find("(") == -1)) or (name.find("$") == -1):
        onlyClass = True

    if onlyClass == False:
        if (name.find('$') != -1) and (name.find('.java') != -1):
            methodName = name.split(".", 1)[0]
            methodName = methodName.replace("$", "")

        else:
            methodName = name.split(".", 1)[-1]
            methodName = methodName.split("(", 1)[0]
            methodName = methodName.replace("$", "")

    return methodName


mainDirectory = "/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/FindBugs_Raw_Data"
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

    projectName = file.split(".xml")[0]
    tool = "FindBugs"

    # This is implace to catch any files that were not in
    # the proper XML format imported from FindBugs.
    try:
        tree = et.parse(file)
        root = tree.getroot()
    # In case some files were not in the right XML format. These are reported in the missingFiles.
    # The code shouldn't enter here preferably (assuming all the XML files are proper).
    except:
        missingFiles.append(str(file))
        processedFiles.remove(str(file))
        pass

    # Iterate through all the violations reported in a class.
    for child in root:

        if str(child.tag) == "BugInstance":

            issue = "" # FindBugs doesn't provide the error message, so this is set as an empty string
            rule = child.attrib['type']
            severity = child.attrib['priority']
            category = child.attrib['category']

        for subChild in child:

            if str(subChild.tag) == "Class" or "Method" or "Field" or "Type": # This instances include the
                                                                            # information we want.

                for subSubChild in subChild:

                    if str(subSubChild.tag) == "SourceLine":

                        try:
                            package = extractPackage(subSubChild.attrib['classname'])

                            # Sometimes the BugInstances do not provide the method, only the class
                            try:
                                method = subChild.attrib['name'] # In the case it provides the method

                            except:
                                method = "" # Otherwise empty string, only class provided

                            startLine = subSubChild.attrib['start']
                            endLine = subSubChild.attrib['end']
                            language = extractLanguage(subSubChild.attrib['sourcefile'])
                            className = extractClass(subSubChild.attrib['classname'])

                            # Skipping instances of "$assert"
                            if ((className.find("$assert") != -1) or (method.find("$assert") != -1)):
                                pass
                            else:
                                # Adding to the arrays
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
os.chdir("/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/FindBugs_Parsing_File_Outputs")

print("creating csv file")
output.to_csv("monsterFileFindBugs.csv")
output.to_csv("monsterFileFindBugs.csv", quoting=csv.QUOTE_NONNUMERIC, index=False)
