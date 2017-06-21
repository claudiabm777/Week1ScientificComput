# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 11:31:38 2017

@author: Asus
"""

################################################
# CHALLENGE 1
################################################
import vtk

rectGridReader = vtk.vtkRectilinearGridReader()
rectGridReader.SetFileName("../data/jet4_0.500.vtk")
# do not forget to call "Update()" at the end of the reader
rectGridReader.Update()

#filter
rectGridOutline = vtk.vtkRectilinearGridOutlineFilter()
rectGridOutline.SetInputData(rectGridReader.GetOutput())

#mapper
rectGridOutlineMapper = vtk.vtkPolyDataMapper()
rectGridOutlineMapper.SetInputConnection(rectGridOutline.GetOutputPort())

#actor
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(rectGridOutlineMapper)
outlineActor.GetProperty().SetColor(0, 0, 0)

#filter2
plane = vtk.vtkRectilinearGridGeometryFilter()
plane.SetInputData(rectGridReader.GetOutput())

#mapper2
rgridMapper = vtk.vtkPolyDataMapper()
rgridMapper.SetInputConnection(plane.GetOutputPort())

#actor2
wireActor = vtk.vtkActor()
wireActor.SetMapper(rgridMapper)
wireActor.GetProperty().SetRepresentationToWireframe()
wireActor.GetProperty().SetColor(0, 0, 0)

################################################
# CHALLENGE 2
################################################

magnitudeCalcFilter = vtk.vtkArrayCalculator()
magnitudeCalcFilter.SetInputConnection(rectGridReader.GetOutputPort())
magnitudeCalcFilter.AddVectorArrayName('vectors')
# Set up here the array that is going to be used for the computation ('vectors')
magnitudeCalcFilter.SetResultArrayName('magnitude')
#se agrega una lista
magnitudeCalcFilter.SetFunction("mag(vectors)")
# Set up here the function that calculates the magnitude of a vector
magnitudeCalcFilter.Update()


################################################
# CHALLENGE 3
################################################
points = vtk.vtkPoints()
grid = magnitudeCalcFilter.GetOutput()
grid.GetPoints(points)
scalars = grid.GetPointData().GetArray('magnitude')

#Create an unstructured grid that will contain the points and scalars data
ugrid = vtk.vtkUnstructuredGrid()
ugrid.SetPoints(points)
ugrid.GetPointData().SetScalars(scalars)

#Populate the cells in the unstructured grid using the output of the vtkCalculator
for i in range (0, grid.GetNumberOfCells()):
    cell = grid.GetCell(i)
    ugrid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

#There are too many points, let's filter the points
subset = vtk.vtkMaskPoints()
subset.SetOnRatio(50)
subset.RandomModeOn()
subset.SetInputData(ugrid)

#filter3
#Make a vtkPolyData with a vertex on each point.
pointsGlyph = vtk.vtkVertexGlyphFilter()
pointsGlyph.SetInputConnection(subset.GetOutputPort())
#pointsGlyph.SetInputData(ugrid)
pointsGlyph.Update()

#mapper3
pointsMapper = vtk.vtkPolyDataMapper()
pointsMapper.SetInputConnection(pointsGlyph.GetOutputPort())
pointsMapper.SetScalarModeToUsePointData()

#actor3
pointsActor = vtk.vtkActor()
pointsActor.SetMapper(pointsMapper)



################################################
# CHALLENGE 4
################################################
scalarRange = ugrid.GetPointData().GetScalars().GetRange()

#filter4
isoFilter = vtk.vtkContourFilter()
isoFilter.SetInputData(ugrid)
isoFilter.GenerateValues(50, scalarRange)

#mapper4
isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInputConnection(isoFilter.GetOutputPort())

#actor4
isoActor = vtk.vtkActor()
isoActor.SetMapper(isoMapper)
isoActor.GetProperty().SetOpacity(0.5)


# Find out how to visualize this as a wireframe 
# Play with the options you get for setting up actor properties (color, opacity, etc.)
renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
 
renderer.AddActor(outlineActor)
#renderer.AddActor(wireActor)
renderer.AddActor(pointsActor)
#renderer.AddActor(isoActor)
renderer.SetBackground(1,1,1)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(60.0)
renderer.GetActiveCamera().Azimuth(30.0)
renderer.GetActiveCamera().Zoom(1.0)
 
renWin.SetSize(300, 300)
 
# interact with data
renWin.Render()
iren.Start()