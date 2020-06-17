import pandas as pd
import os
import glob
import xml.etree.cElementTree as et
import csv

DOMAIN_NAMES = ['com/', 'org/', 'edu/', 'gov/', 'net/', 'nl/']

# Returns language of the file
def extractLanguage(sourceFile):

    language = sourceFile.split(".")[1]

    return language

# Returns string of the package name
def extractPackage (className):

    packageName = className.rsplit(".", 1)[0]

    return packageName

# Returns string of the class name
def extractClass (className):

    className = className.rsplit(".", 1)[1]

    return className

# Returns string of the method name
def extractMethod (name):
    onlyClass = False
    methodName = ""

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

# Returns string of the type
def extractType (className):
    type = className.split(".")[-1]

    return type

mainDirectory = "/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/FindBugs_Raw_Data"
os.chdir(mainDirectory)

# Creating the output csv file structure
projectNames = []
tools = []
languages = []
filePaths = []
packages = []
classNames = []
methods = []
issues = []
startLines = []
endLines = []
severities = []
types = []

missingFiles = []
processedFiles = []


for file in glob.glob("*.xml"):
    print("This is the file: " + file)
    processedFiles.append(str(file))

    projectName = file.split(".xml")[0]
    tool = "FindBugs"

    try:
        tree = et.parse(file)
        root = tree.getroot()

    except:
        missingFiles.append(str(file))
        processedFiles.remove(str(file))
        pass

    for child in root:

        if str(child.tag) == "BugInstance":

            issue = child.attrib['type']
            severity = child.attrib['priority']
            type = child.attrib['category']

        for subChild in child:

            if str(subChild.tag) == "Class" or "Method" or "Field" or "Type":

                for subSubChild in subChild:

                    if str(subSubChild.tag) == "SourceLine":

                        try:
                            package = extractPackage(subSubChild.attrib['classname'])
                            print("Package went through")

                            try:
                                method = subChild.attrib['name']

                            except:
                                method = ""

                            startLine = subSubChild.attrib['start']
                            endLine = subSubChild.attrib['end']
                            language = extractLanguage(subSubChild.attrib['sourcefile'])
                            className = extractClass(subSubChild.attrib['classname'])

                            # Skipping instances of "$assert"
                            if ((className.find("$assert") != -1) or (method.find("$assert") != -1)):
                                pass
                            else:
                                projectNames.append(projectName)
                                tools.append(tool)
                                languages.append(language)
                                packages.append(package)
                                classNames.append(className)
                                methods.append(method)
                                issues.append(issue)
                                startLines.append(startLine)
                                endLines.append(endLine)
                                severities.append(severity)
                                types.append(type)

                        except:
                            pass

dict = {'projectName': projectNames, 'tool': tools, 'language': languages, 'package': packages, 'class': classNames,
                'method': methods, 'issue': issues, 'startLine': startLines, 'endLine': endLines, 'severity': severities, 'type': types}

print(len(projectNames))
print(len(tools))
print(len(languages))
print(len(packages))
print(len(classNames))
print(len(methods))
print(len(issues))
print(len(startLines))
print(len(endLines))
print(len(severities))
print(len(types))

table = pd.DataFrame(dict)
table = table[['projectName', 'tool', 'language', 'package', 'class', 'method', 'issue', 'startLine','endLine', 'severity', 'type']]
table.sort_values("class", axis = 0, ascending = True, inplace = True, na_position ='last')

print("changing directory")
os.chdir("/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/FindBugs_Parsing_File_Outputs")

print("creating csv file")
table.to_csv("monsterFileFindBugs.csv")
table.to_csv("monsterFileFindBugs.csv", quoting=csv.QUOTE_NONNUMERIC, index=False)

classesOkay = True
methodsOkay = True

for className in classNames:

    if className != "":

        if (className.find("$") != -1) or (className.find(".") != -1) or (className.find("/") != -1):
            classesOkay = False
            print("The class with error is: " + className)
for method in methods:

    if method != "":

        if (method.find("$") != -1) or (method.find(".") != -1) or (method.find("/") != -1):
            methodOkay = False

print("Classes okay?: " + str(classesOkay))
print("Methods okay?: "+ str(methodsOkay))

