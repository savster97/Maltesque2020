import pandas as pd
import os
import glob
import xml.etree.cElementTree as et
import csv

# Returns language of the file
def extractLanguage(fileName):
    className = fileName.split("/")[-1]
    language = className.split(".")[-1]

    return language

# Returns string of the package name
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

    return packageName

# Returns string of the class name
def extractClass (fileName):
    onlyMethod = False
    className = ""

    if (fileName.find('$') != -1) and (fileName.find('/') != -1):
        onlyMethod = True

    if onlyMethod == False:
        className = fileName.split("/")[-1]
        className = className.split(".")[0]

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

mainDirectory = "/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/PMD_Raw_Data"
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

    projectName = file.split("_PMD")[0]
    tool = "PMD"

    try:
        tree = et.parse(file)
        root = tree.getroot()

        print("This is the root tag: " + root.tag)
        print("This is the root attrib: " + root.attrib)
    except:
        missingFiles.append(str(file))
        processedFiles.remove(str(file))
        pass

    for child in root:
        print("This is the child tag: " + str(child.tag))
        print("This is the child attrib: " + str(child.attrib))

        if str(child.tag) == "{http://pmd.sourceforge.net/report/2.0.0}file":

            language = extractLanguage(str(child.attrib['name']))

            for subChild in child:

                try:
                    issue = str(subChild.text)
                    startLine = str(subChild.get('beginline'))
                    endLine = str(subChild.get('endline'))
                    type = str(subChild.get('ruleset'))
                    package = str(subChild.get('package'))
                    className = str(subChild.get('class'))
                    method = str(subChild.get('method'))
                    severity = str(subChild.get('priority'))

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

print("before dictionary")
dict = {'projectName': projectNames, 'tool': tools, 'language': languages, 'package': packages, 'class': classNames,
                'method': methods, 'issue': issues, 'startLine': startLines, 'endLine': endLines, 'severity': severities, 'type': types}

table = pd.DataFrame(dict)
table = table[['projectName', 'tool', 'language', 'package', 'class', 'method', 'issue', 'startLine','endLine', 'severity', 'type']]
table.sort_values("class", axis = 0, ascending = True, inplace = True, na_position ='last')

print("changing directory")
os.chdir("/Users/lujan/Desktop/thesis_work/Maltesque2020_code-smell-prediction/PMD_Parsing_File_Outputs")

print("creating csv file")
table.to_csv("monsterFilePMD.csv")
table.to_csv("monsterFilePMD.csv", quoting=csv.QUOTE_NONNUMERIC, index=False)

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

