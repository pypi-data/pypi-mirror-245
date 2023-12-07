# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv


class Delete(MorphoPlugin):
    """ This plugin removes any selected objects from the segmented images.
    Users can select objects at the current time point, or label any objects to delete at several time points.
    The background value (usually 0) will replace the object voxels inside the segmented image.


    Parameters
    ----------
    Objects:
        The selected objects to apply deformation on MorphoNet
    """

    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Delete.png")
        self.set_image_name("Delete.png")
        self.set_parent("Edit Objects")
        self.set_name("Delete : Delete the selected objects ")
        self.set_description("This plugin removes any selected objects from the segmented images. \n "
                             "Users can select objects at the current time point, or label any objects to delete at "
                             "several time points.  The background value (usually 0) will replace the object voxels "
                             "inside the segmented image.")


    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None
        #Get all of the times in the labeled objects list
        for t in dataset.get_times(objects):
            #For each time, load the segmentation data
            data = dataset.get_seg(t)
            cells_updated =[]
            #For each object at this time point
            for o in dataset.get_objects_at(objects, t):
                printv("delete object "+str(o.id)+" at "+str(o.t),0)
                #Delete objects lineage informations
                for m in o.mothers:
                    printv("delete link to mother " + str(m.id) + " at " + str(m.t), 1)
                    dataset.del_mother(o,m)
                for d in o.daughters:
                    printv("delete link to daughter " + str(d.id) + " at " + str(d.t), 1)
                    dataset.del_daughter(o,d)
                #Delete object in the image by applying background value
                dataset.set_cell_value(o, dataset.background)
                dataset.del_cell_from_properties(o)
                #Add to list of object to update
                cells_updated.append(o.id)
            if len(cells_updated)>0:
                #If we updated at least one object, save segmentation and recompute mesh
                dataset.set_seg(t,data,cells_updated=[dataset.background])
        #Resend data to MorphoNet viewer
        self.restart()
