import vtk
import vtk.util.numpy_support as VN
import numpy as np
import json
from pprint import pprint

g= open("./ya31.txt",'w') 
f=open("test_name.txt","r")
lines=f.readlines()
f.close()
g.write("timestamp,dMax,dMin,dRange"+"\n")
for i in range(0,2):
	filename=lines[i].split('\n')[0]
#the name of data array which is used in this example
	daryName = 'v03' #'v03' 'prs' 'tev'

# for accessing build-in color access
	colors = vtk.vtkNamedColors() 

# Create the renderer, the render window, and the interactor. The
# renderer draws into the render window, the interactor enables
# mouse- and keyboard-based interaction with the data within the
# render window.
	aRenderer = vtk.vtkRenderer()
	renWin = vtk.vtkRenderWindow()
	renWin.AddRenderer(aRenderer)
	iren = vtk.vtkRenderWindowInteractor()
	iren.SetRenderWindow(renWin)

# Set a background color for the renderer and set the size of the
# render window.
	aRenderer.SetBackground(100/255, 77/255, 102/255)
	renWin.SetSize(600, 600)

# data reader
	reader = vtk.vtkXMLImageDataReader()
	reader.SetFileName(filename)
	reader.Update()

# specify the data array in the file to process
	reader.GetOutput().GetPointData().SetActiveAttribute(daryName, 0)
# convert the data array to numpy array and get the min and maximum valule
	dary = VN.vtk_to_numpy(reader.GetOutput().GetPointData().GetScalars(daryName))
	dMax = np.amax(dary)
	dMin = np.amin(dary)
	dRange = dMax - dMin
	g.write(filename[66:71]+","+str(dMax)+","+str(dMin)+","+str(dRange)+"\n")
g.close()