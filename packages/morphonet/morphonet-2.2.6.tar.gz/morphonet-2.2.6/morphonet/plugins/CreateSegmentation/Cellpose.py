# -*- coding: latin-1 -*-
import logging

from morphonet.plugins import MorphoPlugin
import numpy as np
from ...tools import printv


class Cellpose(MorphoPlugin):
    """ This plugin uses an intensity image of the membranes from a local dataset at a specific time point, to compute a segmentation of the membranes,
    using the 3D Cellpose deep learning algorithm.

    Parameters
    ----------
    downsampling : int, default :2
        The resolution reduction applied to each axis of the input image before performing segmentation, 1 meaning that
        no reduction is applied. Increasing the reduction factor may reduce segmentation quality

    model type : list of models
        The model used to compute segmentations. A detailed documentation on models can be found https://cellpose.readthedocs.io/en/latest/models.html

    Reference : Stringer, C., Wang, T., Michaelos, M. et al. Cellpose: a generalist algorithm for cellular segmentation.
    Nat Methods 18, 100?106 (2021). https://doi.org/10.1038/s41592-020-01018-x
    https://www.cellpose.org
    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Cellpose.png")
        self.set_image_name("Cellpose.png")
        self.set_name("CellPose : Perform membrane segmentation on intensity images")
        self.add_inputfield("downsampling", default=2)
        self.add_inputfield("diameter", default=30)
        self.add_dropdown("model type",['cyto','nuclei','tissuenet','livecell', 'cyto2', 'general','CP', 'CPx', 'TN1', 'TN2', 'TN3', 'LC1', 'LC2', 'LC3', 'LC4'])
        self.add_dropdown("time points", ["Current time", "All times"])
        self.set_parent("Create Segmentation")
        self.set_description( "This plugin uses an intensity image of the membranes from a local dataset at a specific "
                              "time point, to compute a segmentation of the membranes,using the 3D Cellpose deep learning "
                              "algorithm.\n \n"
                             "Parameters : \n \n "
                             "- downsampling (numeric,default:2) : he resolution reduction applied to each axis of the "
                              "input image before performing segmentation, 1 meaning that no reduction is applied. "
                              "Increasing the reduction factor may reduce segmentation quality \n"
                             "- diameter: (float, default 30.) : the average cell size diameter. \n" 
                             "- model type : The model used to compute segmentations. A detailed documentation on models"
                              " can be found https://cellpose.readthedocs.io/en/latest/models.html \n"
                            "- time points : Launch Stardist at all times points or the current one")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None

        from cellpose import models, core
        from skimage.transform import resize
        import logging
        logging.basicConfig(level=logging.INFO) #To have cellpose log feedback on the terminalk

        which = "GPU" if core.use_gpu() else "CPU"
        printv("CellPose  will run on " + which, 1)

        downsampling = int(self.get_inputfield("downsampling"))
        diameter = int(self.get_inputfield("diameter"))
        model_type = self.get_dropdown("model type")

        times=[t]
        if str(self.get_dropdown("time points")) == "All times":  # should we process at current time or all times
            times=range(self.dataset.begin, self.dataset.end + 1)

        cancel=True
        for t in  times:
            rawdata = dataset.get_raw(t)
            if rawdata is None:
                printv("please specify the rawdata at "+str(t),0)
            else:
                voxel_size=dataset.get_voxel_size(t)
                anisotropy=voxel_size[2]/voxel_size[1]
                printv("found anisotropy at "+ str(anisotropy),1)
                init_shape = rawdata.shape
                if downsampling>1: rawdata=rawdata[::downsampling,::downsampling,::downsampling]
                printv("load the pretrained model "+model_type,0)
                model = models.Cellpose(gpu=True,  model_type=model_type)
                printv("predict the segmentation masks with diameter "+str(diameter), 0)
                masks = model.eval(rawdata,diameter=int(diameter / downsampling),anisotropy=anisotropy,  do_3D=True)
                data=masks[0]
                if downsampling > 1:data = resize(data,init_shape,preserve_range=True,order=0)
                dataset.set_seg(t, data)
                cancel=False

        logging.basicConfig(level=logging.WARNING)
        self.restart(cancel=cancel)




