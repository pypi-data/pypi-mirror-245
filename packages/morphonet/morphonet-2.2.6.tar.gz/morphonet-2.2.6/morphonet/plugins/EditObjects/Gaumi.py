# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv


class Gaumi(MorphoPlugin):
    """ This plugin calculates the gaussian mixture model probability distribution on selected objects in order to split
     them into several objects which will replace the selected ones.

    Parameters
    ----------
    Objects:
        The selected or labeled objects on MorphoNet
    n_components : int , default 2
        The number of mixture components which correspond to the number of new objects to be created in each input
        object (>1)
    method : list of methods
        The method used to initialize the weights, the means and the precisions of the algorithms

    Reference : this plugin use the Gaussian Mixture function in scikit-learn : https://scikit-learn.org/stable/modules/
    generated/sklearn.mixture.GaussianMixture.html

    """
    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Gaumi.png")
        self.set_image_name("Gaumi.png")
        self.set_name("Gaumi : Split the selected objects using probability distribution")
        self.add_dropdown("method",["kmeans", "randomFromData", "k-means++", "random"])
        self.add_inputfield("n components", default=2)
        self.set_description("This plugin calculates the gaussian mixture model probability distribution on selected "
                             "objects in order to splitthem into several objects which will replace the selected ones\n \n"
                             "Parameters : \n \n"
                             "- nb components (numeric,default:2) : Number of object to be created \n"
                             "- method : method used to initialize the weights, the means and the precisions of the "
                             "algorithms")
        self.set_parent("Edit Objects")


    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None

        import numpy as np
        from sklearn.mixture import GaussianMixture

        method=self.get_dropdown("method")
        n_components= int(self.get_inputfield("n components"))
        for t in dataset.get_times(objects): #For each time point in objects to split

            data = dataset.get_seg(t)  #Load the segmentations
            cells_updated = []
            for o in dataset.get_objects_at(objects, t): #For each object at time point
                printv('Split Object '+str(o.get_name())+ " with  "+str(method),0)

                coords = dataset.np_where(o)
                X = np.array(coords).transpose()
                r = np.random.RandomState(seed=1234)
                gmm = GaussianMixture(n_components=n_components, init_params=method, tol=1e-9, max_iter=0,random_state=r).fit(X)

                cells_updated.append(o.id)
                lastID = int(data.max())+1
                for i in range(1,n_components):
                    w = gmm.predict(X) == i
                    data[coords[0][w], coords[1][w], coords[2][w]] = lastID
                    printv('Create a new ID ' + str(lastID) + " with " + str(len(coords[0][w])) + " pixels", 0)
                    cells_updated.append(lastID)
                    lastID += 1
                '''for o in cells_updated:
                    obj = dataset.get_object(str(t) + "," + str(o))
                    if obj is not None:
                        next_t = t+1
                        if dataset.begin <= next_t <= dataset.end:
                            data_next_t = dataset.get_seg(next_t)
                            # Future
                            bb = dataset.get_regionprop("bbox", obj)
                            labels, counts = np.unique(data_next_t[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5]], return_counts=True)
                            bigest_id = labels[counts == counts[1:].max()][0]
                            m = dataset.get_object(next_t, bigest_id)
                            dataset.add_link(obj, m)

                        previous_t = t-1
                        if dataset.begin <= previous_t <= dataset.end:
                            data_next_t = dataset.get_seg(previous_t)
                            # Future
                            bb = dataset.get_regionprop("bbox", obj)
                            labels, counts = np.unique(data_next_t[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5]], return_counts=True)
                            bigest_id = labels[counts == counts[1:].max()][0]
                            m = dataset.get_object(previous_t, bigest_id)
                            dataset.add_link(obj, m)
                '''
            if len(cells_updated)>0:  dataset.set_seg(t,data,cells_updated=cells_updated) #If we created a cell ,save it to seg

        self.restart()   #send data back to morphonet
