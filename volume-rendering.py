
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
filename = '/Volumes/My Passport/迅雷下载/任务组_20181203_1501/pv_insitu_300x300x300_08948.vti'
json_data1=open('/Users/yijiang/Documents/GitHub/Final/ya31v03color.json')
data1 = json.load(json_data1)
json_data1.close()
json_data2=open('/Users/yijiang/Documents/GitHub/Final/ya31v03color.json')
data2 = json.load(json_data2)
json_data2.close()

#the name of data array which is used in this example
daryName1 = 'v03' #'v03' 'prs' 'tev'
daryName2 = 'v02'
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
reader.GetOutput().GetPointData().SetActiveAttribute(daryName1, 0)
reader.GetOutput().GetPointData().SetActiveAttribute(daryName2, 0)

# convert the data array to numpy array and get the min and maximum valule
dary1 = VN.vtk_to_numpy(reader.GetOutput().GetPointData().GetScalars(daryName1))
dMax1 = np.amax(dary1)
dMin1 = np.amin(dary1)
dRange1 = dMax1 - dMin1
dary2 = VN.vtk_to_numpy(reader.GetOutput().GetPointData().GetScalars(daryName2))
dMax2 = np.amax(dary2)
dMin2= np.amin(dary2)
dRange2 = dMax2- dMin2


########## setup color map ###########
# Now create a lookup table that consists of the full hue circle
# (from HSV).
 # effective built

# An outline provides context around the data.
outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(reader.GetOutputPort())
outlineData.Update()

mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())

outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(colors.GetColor3d("Black"))

volumeMapper1 = vtk.vtkGPUVolumeRayCastMapper();
volumeMapper1.SetInputConnection(reader.GetOutputPort())
volumeMapper2 = vtk.vtkGPUVolumeRayCastMapper();
volumeMapper2.SetInputConnection(reader.GetOutputPort())
    # The color transfer function maps voxel intensities to colors.
    # It is modality-specific, and often anatomy-specific as well.
    # The goal is to one color for flesh (between 500 and 1000)
    # and another color for bone (1150 and over).
volumeScalarOpacity1 = vtk.vtkPiecewiseFunction()
volumeScalarOpacity2 = vtk.vtkPiecewiseFunction()
nOpaPoint1 = int( len( data1[0]['Points'])/4 )
nOpaPoint2 = int( len( data2[0]['Points'])/4 ) # number of opacity function control point
for i in range( nOpaPoint1 ):
    dtValue1 = data1[0]['Points'][i*4]
    opaValue1 = data1[0]['Points'][i*4+1]*0.3
    volumeScalarOpacity1.AddPoint(dtValue1, opaValue1)
volumeColor1 = vtk.vtkColorTransferFunction()
for i in range( nOpaPoint2 ):
    dtValue2 = data2[0]['Points'][i*4]
    opaValue2= data2[0]['Points'][i*4+1]*0.3
    volumeScalarOpacity2.AddPoint(dtValue2, opaValue2)
volumeColor2 = vtk.vtkColorTransferFunction()
nRgbPoint1= int( len( data1[0]['RGBPoints'] ) / 4 )
nRgbPoint2= int( len( data2[0]['RGBPoints'] ) / 4 )  # number of the color map control point
for i in range( nRgbPoint1 ):
    dtValue1 = data1[0]['RGBPoints'][i*4]
    r1 = data1[0]['RGBPoints'][i*4+1]
    g1 = data1[0]['RGBPoints'][i*4+2]
    b1 = data1[0]['RGBPoints'][i*4+3]
    volumeColor1.AddRGBPoint(dtValue1, r1, g1, b1)
for i in range( nRgbPoint2 ):
    dtValue2 = data2[0]['RGBPoints'][i*4]
    r2 = data2[0]['RGBPoints'][i*4+1]
    g2 = data2[0]['RGBPoints'][i*4+2]
    b2 = data2[0]['RGBPoints'][i*4+3]
    volumeColor2.AddRGBPoint(dtValue2, r2, g2, b2)

volumeProperty1 = vtk.vtkVolumeProperty()
volumeProperty1.SetColor(volumeColor1)
volumeProperty1.SetScalarOpacity(volumeScalarOpacity1)
volumeProperty1.SetInterpolationTypeToLinear()
volumeProperty1.ShadeOn()
volumeProperty1.SetAmbient(0.4)
volumeProperty1.SetDiffuse(0.6)
volumeProperty1.SetSpecular(0.2)
volumeProperty1.SetScalarOpacityUnitDistance(8000)
volumeProperty2 = vtk.vtkVolumeProperty()
volumeProperty2.SetColor(volumeColor2)
volumeProperty2.SetScalarOpacity(volumeScalarOpacity2)
volumeProperty2.SetInterpolationTypeToLinear()
volumeProperty2.ShadeOn()
volumeProperty2.SetAmbient(0.4)
volumeProperty2.SetDiffuse(0.6)
volumeProperty2.SetSpecular(0.2)
volumeProperty2.SetScalarOpacityUnitDistance(8000)

volume1 = vtk.vtkVolume()
volume1.SetMapper(volumeMapper1)
volume1.SetProperty(volumeProperty1)
volume2 = vtk.vtkVolume()
volume2.SetMapper(volumeMapper2)
volume2.SetProperty(volumeProperty2)

    # Finally, add the volume to the renderer
aRenderer.AddVolume(volume1)
aRenderer.AddVolume(volume2)
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
scalar_bar.SetLookupTable(volumeColor1)

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

