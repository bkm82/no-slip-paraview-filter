"""


Apply a no slip velocity to a surface mesh in paraview.

# This filter applies a no slip boundary condition to a velocity profile.
# Inputs needed are a volume mesh with the velocity profile and a surface
# mesh that you would like to set the surface to zero. It is required that
# the mesh point on the surface of the volume mesh line up exactly with the
# points of the surface mesh
"""
from vtkmodules.vtkCommonDataModel import vtkDataSet
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.numpy_interface import dataset_adapter as dsa
from paraview.util.vtkAlgorithm import smproxy, smproperty
import numpy as np
import logging

logging.basicConfig(level=logging.WARNING)


def Create_Mask(Volume_Mesh, Wall_Mesh):
    """

    Create a mask vector showing if a volume point is on the wall.

    Requires the volume and wall to have a .Points variable

    Returns an np.array that is True if the volume point is on the wall.
    Else False
    """
    maskX = np.in1d(Volume_Mesh.Points[:, 0], Wall_Mesh.Points[:, 0])
    maskY = np.in1d(Volume_Mesh.Points[:, 1], Wall_Mesh.Points[:, 1])
    maskZ = np.in1d(Volume_Mesh.Points[:, 2], Wall_Mesh.Points[:, 2])
    mask = maskX & maskY & maskZ
    return (mask)


def Set_Velocity(mask, Volume_Mesh, set_velocity=0):
    """

    Set the velocity of the volume mesh to a value.

    Takes a Volume Mesh, mask of points to be modified, and desired velocity
    """
    # Get the velocity from the volume input mesh
    velocity = Volume_Mesh.PointData['Velocity']
    velocity[np.where(mask), :] = set_velocity

    logging.debug(f'Input Velocity Shape {np.shape(velocity)}')
    logging.debug(f'Mask Shape {np.shape(mask)}')
    return(velocity)


@smproxy.filter(label="No-Slip Filter")
@smproperty.input(name="Wall Mesh", port_index=1)
@smproperty.input(name="Volume Mesh", port_index=0)
class NoSlipFilter(VTKPythonAlgorithmBase):
    """

    This is a VTKPythonAlgoritm base class that sets a no slip boundary condition

    """
    def __init__(self):
        """

        Initialize the class.

        This sets up 2 inport ports, 1 output port and set the output type
        Output type is a VTK Unstructured grid
        """
        VTKPythonAlgorithmBase.__init__(
            self,
            nInputPorts=2,
            nOutputPorts=1,
            outputType='vtkUnstructuredGrid'
        )

    def RequestData(self, request, inInfo, outInfo):
        """

        Request the input Volume Mesh and Wall Mesh from user.

        Stores the volume mesh as self.Volume_Input
        Stores the surface mesh as self.Wall_Input
        """
        Volume_Input = dsa.WrapDataObject(vtkDataSet.GetData(inInfo[0]))
        Wall_Input = dsa.WrapDataObject(vtkDataSet.GetData(inInfo[1]))
        mask = Create_Mask(Volume_Input, Wall_Input)
        Set_Velocity(mask, Volume_Input, set_velocity=5)
        # add to output
        output = dsa.WrapDataObject(vtkDataSet.GetData(outInfo, 0))
        output.ShallowCopy(Volume_Input.VTKObject)
        return 1
