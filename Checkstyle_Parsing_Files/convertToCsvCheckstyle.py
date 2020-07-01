"""
The code in this file converts the XML files from Checkstyle
into one summary CSV file. The CSV file contains all the
relevant information from all the project analysis results.
"""

import pandas as pd
import os
import glob
import xml.etree.cElementTree as et
import csv

DOMAIN_NAMES = ['com/', 'org/', 'edu/', 'gov/', 'net/', 'nl/'] # used for extracting the package

def extractProjectName (fileName):
    """
    Returns the project name where the error occurs.
    :param fileName: File path (string)
    :return: projectName (string)
     """
    projectName = fileName.split("/Users/lujan/Desktop/thesis_work/cloned_repos/")[1]
    projectName = projectName.split("/")[0]

    return projectName


def checkForExistingDomain (fileName):
    """
    Returns the domain name in the package if found.
    Otherwise returns empty string.
    :param fileName: File path (string)
    :return: domainFound (string)
     """
    domainFound = ""

    for domain in DOMAIN_NAMES:

        if domain in fileName:
            domainFound = domain

            break

    return domainFound


def extractLanguage (fileName):
    """
    Returns the language the code is written in concerning the violation.
    :param fileName: File path (string)
    :return: language (string)
    """
    language = str(fileName.split(".")[-1])

    return language


def extractPackage (fileName):
    """
    Returns the package name where the violation occurs if it exists.
    Otherwise returns an empty string.
    :param fileName: File path (string)
    :return: package (string)
    """
    packageName = ""

    domain = checkForExistingDomain(fileName)

    if domain != "":
        splitFileName = fileName.split(domain)
        packageName = domain.replace("/", ".") + splitFileName[-1].replace("/", ".")

    elif "src/main/java/" in fileName:
        splitFileName = fileName.split("src/main/java/")
        packageName = splitFileName[-1].replace("/", ".")
        print("First if ")

    elif "src/test/java/" in fileName:
        splitFileName = fileName.split("src/test/java/")
        packageName = splitFileName[-1].replace("/", ".")
        print("Second if ")

    elif "src/tests/junit/" in fileName:
        splitFileName = fileName.split("src/tests/junit/")
        packageName = splitFileName[-1].replace("/", ".")
        print("Third if")

    elif "src/main/test/" in fileName:
        splitFileName = fileName.split("src/main/test/")
        packageName = splitFileName[-1].replace("/", ".")
        print("Fourth if")

    elif "src/test/inputs/" in fileName:
        splitFileName = fileName.split("src/test/inputs/")
        packageName = splitFileName[-1].replace("/", ".")
        print("Fifth if")

    elif "src/test/" in fileName:
        splitFileName = fileName.split("src/test/")
        packageName = splitFileName[-1].replace("/", ".")
        print("Sixth if")

    elif "src/trunk/" in fileName:
        splitFileName = fileName.split("src/trunk/")
        packageName = splitFileName[-1].replace("/", ".")
        print("Seventh if")

    elif "src/main/" in fileName:
        splitFileName = fileName.split("src/main/")
        packageName = splitFileName[-1].replace("/", ".")
        print("Eighth if")

    elif "src/test/" in fileName:
        splitFileName = fileName.split("src/test/")
        packageName = splitFileName[-1].replace("/", ".")
        print("Ninth if")

    elif "src/" in fileName:
        splitFileName = fileName.split("src/")
        packageName = splitFileName[-1].replace("/", ".")
        print("Tenth if")

    elif "*source*/" in fileName:
        splitFileName = fileName.split("*source*/")
        packageName = splitFileName[-1].replace("/", ".")
        print("Eleventh if")

    elif "java/" in fileName:
        splitFileName = fileName.split("java/")
        packageName = splitFileName[-1].replace("/", ".")
        print("Twelveth if")

    packageName = packageName.rsplit(".", 2)[0]
    print(packageName)

    return packageName


def extractClass (fileName):
    """
    Returns the class name where the violation occurs if it exists.
    Otherwise returns an empty string.
    :param fileName: File path (string)
    :return: className (string)
    """
    className = ""

    if fileName.find("$assert") == -1:

        className = fileName.split("/")[-1]
        className = className.split(".")[0]

    return className


def extractMethod (name):
    """
    Returns the method name where the violation occurs if it exists.
    Otherwise returns an empty string.
    :param fileName: File path (string)
    :return: methodName (string)
    """
    methodName = "" # Checkstyle only provides the class name. This is set as empty string for consistency to combine
                    # with the other tools.

    return methodName


def extractCategory (source):
    """
   Returns the category name where the violation occurs.
   :param source: source path (string)
   :return: category (string)
   """
    category = source.split(".")[-2]

    return category


def extractRule(source):
    """
   Returns the rule where the violation occurs.
   :param source: source path (string)
   :return: rule (string)
   """
    rule = source.split(".")[-1]

    return rule

mainDirectory = "/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/Checkstyle_Raw_Data"
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

testError = []

for file in glob.glob("*.xml"):
    print(file)
    processedFiles.append(str(file))

    tool = "Checkstyle"

    # This is implace to catch any files that were not in
    # the proper XML format imported from Checkstyle.
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

        if child.findall('error'): # Here the violation is named as "error"
            fileName = str(child.attrib['name'])

            projectName = extractProjectName(fileName)
            language = extractLanguage(fileName)
            package = extractPackage(fileName)
            className = extractClass(fileName)

            if className == "AbstractCompletionTest":
                if projectName not in testError:
                    testError.append(projectName)

            method = extractMethod(fileName)

            for subChild in child:

                try:
                    category = extractCategory(subChild.get('source'))
                    rule = extractRule(subChild.get('source'))
                    issue = str(subChild.get('message'))
                    line = str(subChild.get('line'))
                    severity = str(subChild.get('severity'))

                    # This was added to remove the anomaly case "$assert" which was neither a method or class
                    if ((className == "") and (method == "")) or ((className == "assert") or (method == "assert")):
                        pass
                    else:

                        # Add all the values to the CSV file
                        projectNames.append(projectName)
                        tools.append(tool)
                        languages.append(language)
                        packages.append(package)
                        classNames.append(className)
                        methods.append(method)
                        categories.append(category)
                        rules.append(rule)
                        issues.append(issue)
                        startLines.append(line)
                        endLines.append(line)
                        severities.append(severity)
                        types.append(type)
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
os.chdir("/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/Checkstyle_Parsing_File_Outputs")

print("creating csv file")
output.to_csv("monsterFileCheckstyle.csv")
output.to_csv("monsterFileCheckstyle.csv", quoting=csv.QUOTE_NONNUMERIC, index=False)

for project in testError:
    print(project)
