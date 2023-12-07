# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv


class Seedax(MorphoPlugin):
    """This plugin generates seeds that can be used in other plugins (mainly watershed segmentation).
    The longest axis of the segmentation shape is computed, and then split in 2. At ?  and ? of the axis,  2 seeds are
    created inside the selected objects.


    Parameters
    ----------
    The selected or labeled objects on MorphoNet
    elongation factor : int, default :8
        The elongation factor applied to the objects different axis to compute the distance (>=0)

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_parent("Create Seeds")
        self.set_icon_name("Seedax.png")
        self.set_image_name("Seedax.png")
        self.set_name("Seedax : Create Seeds on the long axis of the selected objects (without intensity images)")
        self.add_inputfield("elongation factor", default=8)
        self.set_description( "This plugin generates seeds that can be used in other plugins (mainly watershed segmentation).\n "
                              "The longest axis of the segmentation shape is computed, and then split in 2. At 1/3  and 2/3 of the axis,  "
                              "2 seeds are created inside the selected objects. \n \n"
                              "Parameters : \n \n"
                              "- elongation factor (numeric,default:8) : The elongation factor applied to the objects "
                              "different axis to compute the distance (>=0)")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, backup=False):
            return None
        #Get user elongation factor for the long axis found, for the seed positioning
        factor = int(self.get_inputfield("elongation factor"))
        import numpy as np
        from scipy.spatial.distance import cdist
        nbc = 0
        # For each time point in cells labeled
        for t in dataset.get_times(objects):
            #Forces to load the segmentation in memory
            data = dataset.get_seg(t)
            # For each cell to this time point
            for o in dataset.get_objects_at(objects, t):
                #Get the cell coordinates
                coords =dataset.np_where(o)
                printv('ook for object ' + str(o.get_name()) + " with " + str(factor*len(coords[0])) + " voxels ",0)
                vT = np.zeros([len(coords[0]), len(coords)])
                #Create distance matrix for each axis
                for s in range(len(coords)):
                    vT[:, s] = coords[s]
                #Compute distance matrix of the image
                dist = cdist(vT, vT)
                #Get the maximum distance from the matrix
                maxi = dist.max()
                #Find the corresponding coordinates
                coords_maxi = np.where(dist == maxi)
                if len(coords_maxi[0]) >= 2:
                    ipt1 = coords_maxi[0][0]
                    ipt2 = coords_maxi[0][1]
                    #Get the this long distance according to the factor of elongation
                    pt1 = np.array([coords[0][ipt1], coords[1][ipt1], coords[2][ipt1]])*factor
                    pt2 = np.array([coords[0][ipt2], coords[1][ipt2], coords[2][ipt2]])*factor
                    v = pt2 - pt1
                    #Compute seed along the axis , at 1/3 and 2/3 of the distance
                    seed1 = np.int32(pt1 + v * 1.0 / 3.0)
                    seed2 = np.int32(pt1 + v * 2.0 / 3.0)
                    #add the seeds to MorphoNet
                    for seed in [seed1,seed2]:
                        dataset.add_seed(seed)
                        nbc += 1

        printv(" --> Found " + str(nbc) + " new seeds",0)
        #Send the new data to MorphoNet
        self.restart()

