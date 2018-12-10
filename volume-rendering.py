
# coding: utf-8

# In[ ]:


import vtk
import vtk.util.numpy_support as VN
import numpy as np
import json
from pprint import pprint

# This template is going to show a slice of the data

# the data used in this example can be download from
# http://oceans11.lanl.gov/deepwaterimpact/yA31/300x300x300-FourScalars_resolution/pv_insitu_300x300x300_49275.vti 

#setup the dataset filepath (change this file path to where you store the dataset)
filename = '/Volumes/My Passport/迅雷下载/yc31/pv_insitu_300x300x300_09113.vti'
json_data=open('/Users/yijiang/Documents/GitHub/Final/yc31color.json')
data = json.load(json_data)
json_data.close()

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
aRenderer.SetBackground(0.6, 0.6, 0.6)
renWin.SetSize(1600, 1200)

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
print(sum(dary))


########## setup color map ###########
# Now create a lookup table that consists of the full hue circle
# (from HSV).
hueLut = vtk.vtkLookupTable()
hueLut.SetTableRange(dMin, dMax)

hueLut.Build()  # effective built

# An outline provides context around the data.
outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(reader.GetOutputPort())
outlineData.Update()

mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())

outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(colors.GetColor3d("Black"))

volumeMapper = vtk.vtkGPUVolumeRayCastMapper();
volumeMapper.SetInputConnection(reader.GetOutputPort())

    # The color transfer function maps voxel intensities to colors.
    # It is modality-specific, and often anatomy-specific as well.
    # The goal is to one color for flesh (between 500 and 1000)
    # and another color for bone (1150 and over).
volumeScalarOpacity = vtk.vtkPiecewiseFunction()
nOpaPoint = int( len( data[0]['Points'])/4 ) # number of opacity function control point
for i in range( nOpaPoint ):
    dtValue = data[0]['Points'][i*4]
    opaValue = data[0]['Points'][i*4+1]*0.3
    volumeScalarOpacity.AddPoint(dtValue, opaValue)
    print('opacity control point: ', i, ': ', dtValue, opaValue)
volumeColor = vtk.vtkColorTransferFunction()
nRgbPoint= int( len( data[0]['RGBPoints'] ) / 4 ) # number of the color map control point
for i in range( nRgbPoint ):
    dtValue = data[0]['RGBPoints'][i*4]
    r = data[0]['RGBPoints'][i*4+1]
    g = data[0]['RGBPoints'][i*4+2]
    b = data[0]['RGBPoints'][i*4+3]
    volumeColor.AddRGBPoint(dtValue, r, g, b)
    print('rgb control point: ', i, ': ', dtValue, r, g, b)
# volumeColor = vtk.vtkColorTransferFunction()
# volumeColor.AddRGBPoint(dMin, 1.0, 1.0, 1.0)
# # volumeColor.AddRGBPoint((dMax-dMin)/4+dMin,0.0, 1.0, 0.0)
# # volumeColor.AddRGBPoint((dMax-dMin)*2/4+dMin, 0.0, 0.0, 1.0)
# # volumeColor.AddRGBPoint((dMax-dMin)*3/4+dMin, 1.0, 1.0, 0.0)
# volumeColor.AddRGBPoint(dMax, 0.0, 0.0, 1.0)

    # The opacity transfer function is used to control the opacity
    # of different tissue types.
# volumeScalarOpacity = vtk.vtkPiecewiseFunction()
# volumeScalarOpacity.AddPoint(dMin, 0.0)
# volumeScalarOpacity.AddPoint(dMin+(dMax-dMin)*1/5 ,0.0)
# volumeScalarOpacity.AddPoint(dMax, 0.01)


volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(volumeColor)
volumeProperty.SetScalarOpacity(volumeScalarOpacity)
volumeProperty.SetInterpolationTypeToLinear()
volumeProperty.ShadeOn()
volumeProperty.SetAmbient(0.4)
volumeProperty.SetDiffuse(0.6)
volumeProperty.SetSpecular(0.2)
volumeProperty.SetScalarOpacityUnitDistance(8000)


volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)


    # Finally, add the volume to the renderer
aRenderer.AddVolume(volume)

text = vtk.vtkTextActor()
text.SetInput("Scalar Value(v02)")
tprop = text.GetTextProperty()
tprop.SetFontFamilyToArial()
tprop.ShadowOff()
tprop.SetLineSpacing(1.0)
tprop.SetFontSize(36)
text.SetDisplayPosition(0, 0)
aRenderer.AddActor2D(text)

scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetOrientationToVertical()
scalar_bar.SetLookupTable(volumeColor)

# create the scalar_bar_widget
scalar_bar_widget = vtk.vtkScalarBarWidget()
scalar_bar_widget.SetInteractor(iren)
scalar_bar_widget.SetScalarBarActor(scalar_bar)

scalar_bar_widget.On()


# It is convenient to create an initial view of the data. The
# FocalPoint and Position form a vector direction. Later on
# (ResetCamera() method) this vector is used to position the camera
# to look at the data in this direction.
aCamera = vtk.vtkCamera()
aCamera.SetViewUp(0, 0, -1)
aCamera.SetPosition(0, -1, 0)
aCamera.SetFocalPoint(0, 0, 0)
aCamera.SetViewAngle(120)
aCamera.ComputeViewPlaneNormal()
aCamera.Azimuth(180.0)
aCamera.Elevation(-20.0)

# Actors are added to the renderer.

# An initial camera view is created.  The Dolly() method moves
# the camera towards the FocalPoint, thereby enlarging the image.
aRenderer.SetActiveCamera(aCamera)

# Calling Render() directly on a vtkRenderer is strictly forbidden.
# Only calling Render() on the vtkRenderWindow is a valid call.
renWin.Render()

aRenderer.ResetCamera()
aCamera.Dolly(1.5)

# Note that when camera movement occurs (as it does in the Dolly()
# method), the clipping planes often need adjusting. Clipping planes
# consist of two planes: near and far along the view direction. The
# near plane clips out objects in front of the plane; the far plane
# clips out objects behind the plane. This way only what is drawn
# between the planes is actually rendered.
aRenderer.ResetCameraClippingRange()

# Interact with the data.
renWin.Render()
iren.Initialize()
iren.Start()

