import logging
logging.basicConfig(level=logging.WARNING)

#This filter applies a no slip boundary condition to a velocity profile. 
#Inputs needed are a volume mesh with the velocity profile and a surface mesh that you would like to set the surface to zero
#It is required that the mesh points on the surface of the volume mesh line up exactly with the points of the surface mesh.
from vtkmodules.vtkCommonDataModel import vtkDataSet
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.numpy_interface import dataset_adapter as dsa
from paraview.util.vtkAlgorithm import smproxy, smproperty, smdomain
import numpy as np


@smproxy.filter(label="No-Slip Filter")
@smproperty.input(name="Wall Mesh", port_index=1)
@smproperty.input(name="Volume Mesh", port_index=0)
class NoSlipFilter(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self, nInputPorts=2, nOutputPorts=1,outputType='vtkUnstructuredGrid')


    def RequestData(self, request, inInfo, outInfo):
        # get the input data
        Volume_Input =  dsa.WrapDataObject(vtkDataSet.GetData(inInfo[0]))
        Wall_Input = dsa.WrapDataObject(vtkDataSet.GetData(inInfo[1]))
        
        # Find all of the points in the volume mesh that are on the surface mesh by first finding all of the
        # Points in the Volume_Input that are also in Wall_Input. This will create a mask vector that is the 
        # same number of rows as the Volume input. If that point is on the surface it will be True, else false
        maskX = np.in1d(Volume_Input.Points[:,0], Wall_Input.Points[:,0])
        maskY = np.in1d(Volume_Input.Points[:,1], Wall_Input.Points[:,1])
        maskZ = np.in1d(Volume_Input.Points[:,2], Wall_Input.Points[:,2])
        mask = maskX & maskY & maskZ

        #Get the velocity from the volume input mesh
        velocity = Volume_Input.PointData['Velocity']
        velocity[np.where(mask),:] = 0 #For rows that are on the surface, set all of the velocity columns to zero
        
        logging.debug(f'Input Velocity Shape {np.shape(velocity)}')
        logging.debug(f'Mask Shape {np.shape(mask)}')

        # add to output
        output = dsa.WrapDataObject(vtkDataSet.GetData(outInfo, 0))
        output.ShallowCopy(Volume_Input.VTKObject)
        output.PointData.append(velocity, "Velocity_No_Slip");
        return 1
