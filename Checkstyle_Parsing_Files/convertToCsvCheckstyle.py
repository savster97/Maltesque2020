import pandas as pd
import os
import glob
import xml.etree.cElementTree as et
import csv

DOMAIN_NAMES = ['com/', 'org/', 'edu/', 'gov/', 'net/', 'nl/']

# Checks for existing domain and returns the domain if found
def checkForExistingDomain (fileName):
    domainFound = ""

    for domain in DOMAIN_NAMES:
        if domain in fileName:
            # splitFileName = fileName.split(domain)
            # packageName = domain + splitFileName[-1].replace("/", ".")
            domainFound = domain
            break
    return domainFound


# Return the language of the file
def extractLanguage (fileName):
    language = fileName.split(".")[-1]

    return language

# Return the package of the file
def extractPackage (fileName):
    packageName = ""

    domain = checkForExistingDomain(fileName)

    if domain != "":
        splitFileName = fileName.split(domain)
        packageName = domain.replace("/", ".") + splitFileName[-1].replace("/", ".")
        print("Domain found is: " + domain)
        print("File path is: " + fileName)

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

# Returns string of the class name
def extractClass (fileName):
    className = ""

    if fileName.find("$assert") == -1:

        className = fileName.split("/")[-1]
        className = className.split(".")[0]

    return className

# Returns string of the method name
def extractMethod (name):
    methodName = ""

    return methodName

mainDirectory = "/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/Checkstyle_Raw_Data"
os.chdir(mainDirectory)

# Creating the output csv file structure
projectNames = []
tools = []
languages = []
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
    print(file)
    processedFiles.append(str(file))

    projectName = file.split("_CS")[0]
    tool = "Checkstyle"

    try:
        tree = et.parse(file)
        root = tree.getroot()
    except:
        missingFiles.append(str(file))
        processedFiles.remove(str(file))
        pass

    for child in root:

        if child.findall('error'):
            fileName = str(child.attrib['name'])

            language = extractLanguage(fileName)
            package = extractPackage(fileName)
            className = extractClass(fileName)
            method = extractMethod(fileName)

            for subChild in child:

                try:
                    issue = str(subChild.get('message'))
                    line = str(subChild.get('line'))
                    severity = str(subChild.get('severity'))
                    type = str(subChild.get('source'))
                    type = type.split(".")[-1]

                    if ((className == "") and (method == "")) or ((className == "assert") or (method == "assert")):
                        pass
                    else:

                        projectNames.append(projectName)
                        tools.append(tool)
                        languages.append(language)
                        packages.append(package)
                        classNames.append(className)
                        methods.append(method)
                        issues.append(issue)
                        startLines.append(line)
                        endLines.append(line)
                        severities.append(severity)
                        types.append(type)
                except:
                    pass

print("before dictionary")
test = {"projectName": projectNames, "tool": tools, "language": languages, "package": packages, "class": classNames,
        "method": methods, "issue": issues, "startLine": startLines, "endLine": endLines,"severity": severities, "type": types}

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

print("before dataframe")
output = pd.DataFrame(test)

output = output[['projectName', 'tool', 'language', 'package', 'class', 'method', 'issue', 'startLine', 'endLine', 'severity', 'type']]
output.sort_values("class", axis = 0, ascending = True, inplace = True, na_position ='last')

print("changing directory")
os.chdir("/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/Checkstyle_Parsing_File_Outputs")

print("creating csv file")
output.to_csv("monsterFileCheckstyle.csv")
output.to_csv("monsterFileCheckstyle.csv", quoting=csv.QUOTE_NONNUMERIC, index=False)

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
            print("The method with error is: " + className)

print("Classes okay?: " + str(classesOkay))
print("Methods okay?: "+ str(methodsOkay))
