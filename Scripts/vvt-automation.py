import time
import os
import sys
from win32com.client import Dispatch
import json
from enum import Enum, auto

vvtApp = None

curr_dir = os.getcwd()
json_ = open("Scripts\\vvtconfig.json", "r")

path_details = json.load(json_)

src_file_bool = path_details.get("additional_file")

debug_version_enable = path_details.get("debug_version")

projectfile = path_details.get("vvt_project_path")
projectFile = curr_dir+'\\'+projectfile

sourceFiles_path = path_details.get("additional_files_path")
sourceFiles_full = [curr_dir + '\\' + n if n.find("C:") else n for n in sourceFiles_path]

dll_path = path_details.get("dll_path")
dll_path_full = curr_dir+'\\'+dll_path

sln_path = path_details.get("sln_path")
sln_path_full = curr_dir+'\\'+sln_path

targetPlatform = path_details.get("target_platform")

verboseLevel = path_details.get("verbose_level")

complierVersion = path_details.get("compiler_version")

generateCSV = path_details.get("generate_csv")

generateSolution = path_details.get("generate_solution")

validateSource = path_details.get("validate_source_files")

class BuildResult:
    class Success:
        value__ = 0
    class Failed:
        value__ = 1
    class InProcess:
        value__ = 2

def startVVT():
    print("Open COM connection with vVirtualTarget")
    try:
        vvtApp = Dispatch("Vector.VTT.ComServer.ComApplicationImpl")
        
        print("COM connection Successful")
    except:
        sys.exit("Unable to connect to vVirtual Target please check the license or close the running instance")
    if vvtApp == None:
        sys.exit("Could not establish COM communication with vVirtualTarget")
    vvtApp.BringToFront()
    return vvtApp
    
def openProject(vvtApp):
    print("Opening vVirtualTarget (.vvtproj) project")
    try:
        vvtApp.OpenProject(projectFile)
        print("vVirtualTarget (.vvtproj) project is Opened")
    except:
        sys.exit("Unable to Open the vVirtualTarget (.vvtproj) project")
    project = vvtApp.Project()
    
    return project
    
def addSourceFiles(vvtApp,project):
    print("Adding Source files to the vVirtualTarget (.vvtproj) project")
    ecuInstance = project.GetEcuInstanceCollection()
    for i in sourceFiles_full:
        if os.path.exists(i):
            print("Source file present at "+i)
        else:
            sys.exit("Source file not present at "+i)
  
        add_source_file = ecuInstance[0].AddSourceFile(i)
        if add_source_file:
            print("Added Source file in the vVirtualTarget (.vvtproj) project "+i)
        else:
            sys.exit("Failed to add Source File in the vVirtualTarget (.vvtproj) project "+i)
    sourceFiles = ecuInstance[0].GetSourceFileCollection()
    for i in sourceFiles:
        print(i)
   
def generalPCsettings(vvtApp,project):
    print("Configuraing PC settigns for the BUILD")
    target = project.GeneralPcTargetSettings()
    
    try:
        target.TargetPlatform = targetPlatform
        print("Target Platform set to")
        if target.TargetPlatform == 0:
            print("Windows_x86")
        elif target.TargetPlatform == 1:
            print("Windows_x64")
        elif target.TargetPlatform == 2:
            print("Linux_x64")
        else:
            sys.exit("Please enter the valid platform number 1. Windows_x86 = 0, 2. Windows_x64 = 1, 3. Linux_x64 = 2")
    except:
        sys.exit("Failed to set the Target Platform please check the data type in configuration file")
        
    try:
        target.CompilerVersion = complierVersion
        print("Compiler Version set to " + target.CompilerVersion)
    except:
        sys.exit("Failed to set the Compiler Version please check the data type in configuration file")
        
    try:
        target.GenerateCsvFile = generateCSV
        print("Generate CSV file: " + str(target.GenerateCsvFile))
    except:
        sys.exit("Failed to set the Generate CSV please check the data type in configuration file")
        
    try:
        target.GenerateSolution = generateSolution
        print("Generate Solution file: " + str(target.GenerateSolution))
    except:
        sys.exit("Failed to set the Generate Solution please check the data type in configuration file")
        
    try:
        target.VerboseLevel = verboseLevel
        if target.VerboseLevel == 0:
            print("Verbose Level: Low")
        elif target.VerboseLevel == 1:
            print("Verbose Level: Medium")
        elif target.VerboseLevel == 2:
            print("Verbose Level: High")
        else:
            sys.exit("Please enter the valid Verbose Level 1. Low = 0, 2. Medium = 1, 3. High = 2")
    except:
        sys.exit("Failed to set the Verbose Level please check the data type in configuration file")
        
    try:
        target.ValidateSourceFiles = validateSource
        print("Validate Source Files: " + str(target.ValidateSourceFiles))
    except:
        sys.exit("Failed to set the Validate Source Files please check the data type in configuration file")
    try:
        target.CreateDebugVersion = debug_version_enable
        print("Build fors DLL file will be in debug: " + str(target.CreateDebugVersion))
    except:
        sys.exit("Failed to set the Debug Version please check the data type in configuration file")
    target.BuildSolution = True
    print("Generate DLL is set to True")
    

def solutionAbsPath(vvtApp,project):
    print("Setting absolute file path of the Visual Studio solution")
    
    project.SolutionFileAbsolutePath = sln_path_full

def quitAPP(vvtApp):
    print("Closing the COM connection with VVT")
    print("Exited due to the Error Code: "+str(vvtApp.GetLastError()))
    try:
        if vvtApp == None:
            sys.exit("Could not locate the VVT application or Application closed already")
        else:
            vvtApp.Exit()
            print("VVT app closed succesfully")
    except:
        sys.exit("An error occured while closing the VVT instance")
    

def buildVVT(vvtApp):
    try:
        print("Started build for vVirtualTarget (.vvtproj) project")
        build = vvtApp.Build()
        if not build.StartBuild(True):
            sys.exit(1)
        if vvtApp.GetLastError() != 0:
            print("Build did not start due to Error: "+str(vvtApp.GetLastError()))
            sys.exit(1)
        startTime = time.time()
        while 1:
            if build.GetResult() != BuildResult.Success.value__ or build.GetResult() != BuildResult.Failed.value__:
                pass
            else:
                break
        endTime = time.time()
        print("Total Time taken for build: "+str(endTime-startTime))
        if build.GetResult() == 0:
            print("Build is Successful")
        elif build.GetResult() == 1:
            print("Build is Failed")
        else:
            sys.exit(1)
    except:
        print("Build did not succeded due to Error: "+str(vvtApp.GetLastError())) 

def saveProject(vvtApp):
    try:
        vvtApp.SaveProject(projectFile)
        print("Save the vVirtualTarget (.vvtproj) project")
        if vvtApp.GetLastError() != 0:
            print("Unable to save the project due to Error: "+str(vvtApp.GetLastError()))
            sys.exit(1)
    except:
        print("Failed to save the project closing the COM connection")
        return 0
    return 1
    
if __name__ == "__main__":
    vvtApp = startVVT()
    project = openProject(vvtApp)
    solutionAbsPath(vvtApp,project)
    if src_file_bool:
        addSourceFiles(vvtApp,project)
    else:
        print("No Source files to be added as parameter is set to: " +str(src_file_bool))
    generalPCsettings(vvtApp,project)
    saved = saveProject(vvtApp)
    if saved:
        buildVVT(vvtApp)
    quitAPP(vvtApp)