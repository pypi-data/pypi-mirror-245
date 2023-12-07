# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from ...tools import printv


class Stardist(MorphoPlugin):
    """ This plugin uses an intensity image of the nucleus from a local dataset at a specific time point, to compute a
    segmentation of the nucleus, using the 3D Stardist deep learning algorithm.

    Parameters
    ----------
    downsampling : int, default :2
        The resolution reduction applied to each axis of the input image before performing segmentation, 1 meaning that
        no reduction is applied. Increasing the reduction factor may reduce segmentation quality


    Reference : Uwe Schmidt, Martin Weigert, Coleman Broaddus, and Gene Myers. Cell Detection with Star-convex Polygons.
    International Conference on Medical Image Computing and Computer-Assisted Intervention (MICCAI), Granada, Spain,
    September 2018.

    https://github.com/stardist/stardist

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Stardist.png")
        self.set_image_name("Stardist.png")
        self.set_name("Startdist : Perform nuclei segmentation on intensity images ")
        self.add_inputfield("downsampling", default=2)
        self.add_inputfield("nms_thresh", default=0.3)
        self.add_inputfield("prob_thresh", default=0.707933)
        self.add_dropdown("time points", ["Current time", "All times"])
        self.add_dropdown("use tiles ?", ["No","Yes"])
        self.set_parent("Create Segmentation")
        self.set_description( "This plugin uses an intensity image of the nucleus from a local dataset at a specific time "
                              "point, to compute a segmentation of the nucleus, using the 3D Stardist deep learning algorithm.\n \n"
                             "Parameters : \n \n "
                             "- downsampling (numeric,default:2) : he resolution reduction applied to each axis of the "
                              "input image before performing segmentation, 1 meaning that no reduction is applied. "
                              "Increasing the reduction factor may reduce segmentation quality "
                             "- nms_thresh (float,default 0.3) : Non Max Suppression threshold in Stardist"
                             "- prob_thresh (float,default 0.707933) :  Mask probability threshold in Stardist"
                             "- time points : Launch Stardist at all times points or the current one"
                             "- use tiles : for big images, we recommend to use tiles\n")


    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None

        from csbdeep.utils import normalize
        from stardist.models import StarDist3D
        from skimage.transform import resize

        import tensorflow as tf
        which = "GPU" if len(tf.config.list_physical_devices('GPU')) >= 1 else "CPU"
        printv("Stardist  will run on " + which,1)

        Downsampled = int(self.get_inputfield("downsampling"))
        nms_thresh = float(self.get_inputfield("nms_thresh"))
        prob_thresh = float(self.get_inputfield("prob_thresh"))
        use_tiles=self.get_inputfield("prob_thresh")=="Yes"
        times = [t]
        if str(self.get_dropdown("time points")) == "All times":  # should we process at current time or all times
            times = range(self.dataset.begin, self.dataset.end + 1)

        cancel = True
        printv("load the stardist 3D model", 0)
        model = StarDist3D.from_pretrained('3D_demo')

        for t in times:
            rawdata = dataset.get_raw(t)
            if rawdata is None:
                printv("please specify the rawdata at "+str(t),0)
            else:
                init_shape = rawdata.shape
                if Downsampled>1:
                    rawdata=rawdata[::Downsampled,::Downsampled,::Downsampled]


                printv("normalize the rawdata at "+str(t),0)
                rawdata = normalize(rawdata)

                printv("predict at "+str(t)+" with nms_thresh="+str(nms_thresh)+' and prob_thresh='+str(prob_thresh),0)
                if use_tiles:
                    n_tiles = model._guess_n_tiles(rawdata)
                    printv("with tiles "+str(n_tiles),1)
                    data, _ = model.predict_instances(rawdata, nms_thresh=nms_thresh, prob_thresh=prob_thresh,n_tiles=n_tiles)
                else:
                    data, _ = model.predict_instances(rawdata,nms_thresh =nms_thresh,prob_thresh =prob_thresh)

                if Downsampled > 1:
                    data = resize(data,init_shape,preserve_range=True,order=0)

                dataset.set_seg(t, data)
                cancel = False
        self.restart(cancel=cancel)
