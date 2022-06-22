import time
import os
import sys
from win32com.client import Dispatch
import json
from enum import Enum, auto

projectFile = "D:\\VVT\\LightControl_Arbitration_Demo_BackUp_04_12\\LightControl_Arbitration_Demo_BackUp\ssssssssss\LightControl_Arbitration_Demo\\LightControl.vttproj"

vvtApp = Dispatch("Vector.VTT.ComServer.ComApplicationImpl")
vvtApp.OpenProject(projectFile)
project = vvtApp.Project()
ecuInstance = project.GetEcuInstanceCollection()
#add_source_file = ecuInstance[0].AddSourceFile("E:\\Pranav\\LightControl_Arbitration_Demo_BackUp_04_12\\LightControl_Arbitration_Demo_BackUp\\LightControl_Arbitration_Demo\\Arbitration_Code\\rtwtypes.h")
"""target = project.GeneralPcTargetSettings()
target.TargetPlatform = 0
target.CompilerVersion = "Visual Studio 2017"
target.GenerateCsvFile = True
target.GenerateSolution = True
target.VerboseLevel = 0
target.ValidateSourceFiles = True
target.CreateDebugVersion = True
target.BuildSolution = True"""
build = vvtApp.Build()
startBuild = build.StartBuild(False)
print(vvtApp.GetLastError())
