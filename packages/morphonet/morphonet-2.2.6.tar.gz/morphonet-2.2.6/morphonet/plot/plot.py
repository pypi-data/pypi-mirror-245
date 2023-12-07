# -*- coding: latin-1 -*-
import os
import numpy as np

from morphonet import tools
from morphonet.plot.Dataset import Dataset
from morphonet.plot.Server import _MorphoServer
from morphonet.tools import isfile, rmrf, cp_dir, printv, convert_vtk_file_in_obj, RemoveLastTokensFromPath, \
    get_version, fast_convert_to_OBJ,_check_version,mkdir, convert, apply_mesh_offset
from os.path import isdir, join
from hashlib import sha256
from sys import platform
from math import floor
from scipy.ndimage import zoom




class Plot:  # Main function to initalize the plot mode
    """Plot data onto the 3D viewer of the MorphoNet Window.

    Parameters (mostly for debuging )
    ----------
    log : bool
        keep the log
    start_browser : bool
        automatically start the browser when plot initliaze
    port_send : int
        port number to communicate (send messages) with the MorphoNet Window.
    port_send : int
        port number to communicate (receive messages) with the MorphoNet Window.
    temp_folder: string
        Path where MoprphoNet store temporary data (annotation , meshes , etc ..)
    verbose : int
         verbose of the terminal (0 : nothing , 1 : normal user, 2 : develloper)

    Returns
    -------
    MorphoPlot
        return an object of morphonet which will allow you to send data to the MorphoNet Window.


    Examples
    --------
    >>> import morphonet
    >>> mn=morphonet.Plot()

    """

    def __init__(self, log=True, start_browser=False, port_send=9875, port_recieve=9876, memory=20,temp_folder=".TEMP",full_path=False,verbose=1,start_servers=True,check_version=True):
        #global verb
        self.full_path = full_path
        self.temp_folder = temp_folder
        self.memory=memory
        self.start_servers = start_servers
        if self.start_servers:
            self.setup_plot(port_send=port_send,port_recieve=port_recieve,start_browser=start_browser,check_version=check_version)
        self.start_plot(log)
        tools.verbose=verbose
        tools.plot_instance=self
        self.show_raw = True #Is user ask for showing raw
        self.show_raw_t=0
        self.set_mesh_parameters() #set default mesh parameters in base
        self.recompute = False
        self.uploading = False

    def set_current_time(self,time):
        self.current_time = time

    def setup_plot(self,port_send=9875,port_recieve=9876,start_browser=True,check_version=True):
        if check_version: _check_version()
        else : get_version()

        self.server_send = _MorphoServer(self, "send", port=port_send)  # Instantiate the local MorphoNet server
        self.server_send.daemon = True
        self.server_send.start()  #

        self.server_recieve = _MorphoServer(self, "recieve", port=port_recieve)  # Instantiate the local MorphoNet server
        self.server_recieve.daemon = True
        self.server_recieve.start()

        if start_browser:
            self.show_browser() #Open Firefox

    def wait_for_servers(self):
        if self.server_send is not None:
            self.server_send.join()
        if self.server_recieve is not None:
            self.server_recieve.join()

    def start_plot(self,log=True):
        '''
        Initialize MorphoPlot session
        '''
        self.plugins = []
        self.log = log

    def restart_plot(self):
        '''
        Restart MorphoPlot session
        '''
        if self.dataset is not None:
            printv("Restarting  morphoplot session",1)
            self.start_plot(self.log)
            begin = self.dataset.begin
            self.set_current_time(self.dataset.begin)
            end = self.dataset.end
            raw_path = self.dataset.raw_path
            segment = self.dataset.segment
            log = self.dataset.log
            background = self.dataset.background
            xml_file = self.dataset.xml_file
            del self.dataset
            self.set_dataset(begin=begin,end=end,raw=raw_path,segment=segment,background=background,xml_file=xml_file)
            self.curate()
    #########################################  SERVER COMMUNICATION

    def write_property(self, txt_filename, data):
        printv("save " + txt_filename,1)
        f = open(txt_filename, 'w')
        f.write(data)
        f.close()

    def connect(self, login, passwd):  # Need to be connected to be upload on MorphoNet
        """Connect to the MorphoNet server

        In order to directly upload data to the MorphoNet server, you have to enter your MorphoNet credentials

        Parameters
        ----------
        login : string
            your login in MorphoNet
        passwd : string
            your password in MorphoNet

        Examples
        --------
        >>> import morphonet
        >>> mc=morphonet.Plot()
        >>> mc.connect("mylogin","mypassword")
        """
        import morphonet
        self.mn = morphonet.Net(login, passwd)

    def send(self, cmd, obj=None):
        """ Send a command to the 3D viewer

        Examples
        --------
        >>> mc.send("hello")
        """
        self.server_send.wait()  # Wait the command available
        if type(obj) == list: obj = str(obj)
        if  type(obj) == str  and  not cmd.startswith("INFO")  and  not cmd.startswith("LOAD"): printv("SEND "+cmd + " -> "+str(obj),3)
        else:   printv("SEND "+cmd,3)


        if cmd is not None:
            cmd = cmd.replace(" ", "%20")
        if obj is not None:
            if type(obj) == str:
                obj = obj.replace(" ", "%20")
        self.server_send.post(cmd, obj)

    def quit(self):
        """ Stop communication between the browser 3D viewer and python

        Examples
        --------
        >>> mc.quit()
        """
        self.send("MSG","DONE")
        self.server_send.stop()  # Shut down the server
        self.server_recieve.stop()  # Shut down the server

    def quit_and_exit(self):
        """ Stop communication between the browser 3D viewer and python, than exit curation

        Examples
        --------
        >>> mc.quit_and_exit()
        """
        self.send("MSG","DONE_AND_EXIT")
        self.server_send.stop()  # Shut down the server
        self.server_recieve.stop()  # Shut down the server
        exit()

    def upload(self, dataname, net_instance=None, raw_factor=4,raw_z_factor=4):
        """Create the dataset on MorphoNet server and upload data

        Parameters
        ----------
        dataname : string
            Name of the new dataset on the server
        upload_factor : float
            the scaling attached to the dataset to match the raw data

        Examples
        --------
        >>> ...after starting MorphoPlot and curating the data
        >>> mc.upload("new dataset name",1)
        """
        self.uploading = True
        printv("Upload dataset " + dataname,1)
        net=None
        if net_instance is not None:
            net=net_instance
        else:
            net = self.mn
        net.create_dataset(dataname, minTime=self.dataset.begin, maxTime=self.dataset.end)

        for t in range(self.dataset.begin, self.dataset.end + 1):
            # compute voxel_size from seg
            seg = self.dataset.compute_voxel_size_from_seg(t)
            obj = self.compute_mesh(t)
            voxel_size = [self.dataset.get_voxel_size(t)[0], self.dataset.get_voxel_size(t)[1],
                          self.dataset.get_voxel_size(t)[2]]
            center = [self.dataset.center[0]*voxel_size[0], self.dataset.center[1]*voxel_size[1],
                      self.dataset.center[2]*voxel_size[2]]
            cobj = apply_mesh_offset(obj, center)
            net.upload_mesh_at(t,cobj)
            raw = self.dataset.get_raw(t)
            if raw is not None:
                data8 = convert(raw, 255, np.uint8)
                if raw_factor > 1 or raw_z_factor > 1:
                    data8 = data8[::raw_factor, ::raw_factor, ::raw_z_factor]

                if raw_factor != raw_z_factor:
                    voxel_size[2] = voxel_size[2]/(raw_factor/raw_z_factor)

                vs="{},{},{}".format(voxel_size[0],voxel_size[1],voxel_size[2])
                scale = raw_factor
                net.upload_image_at(t,data8,vs,scale=scale)

        printv("Uploading done",1)
        self.uploading = False

    def show_browser(self):
        """ Start Mozilla Firefox browser and open morphoplot page

        Examples
        --------
        >>> mc.show_browser()
        """
        import webbrowser
        from morphonet import url
        printv("Open " + url,1)
        try:
            webbrowser.get('firefox').open_new_tab("http://" + url + '/morphoplot')
        except Exception as e:
            printv("Firefox error: " % e,1)
            quit()

    def compute_meshes(self,times=None):
        """ Precompute meshes (without any windows visuaslaition)

        Parameters
        ----------
        times : list of int
            List of times steps to compute, None is equal to all

        Examples
        --------
        >>> mc=morphonet.Plot(start_browser=False)
        >>> mc.compute_meshes()
        """
        if times is None:
            times = range(self.dataset.begin, self.dataset.end + 1)
        for t in times:
            obj = self.compute_mesh(t)
            if obj is None:
                data = self.dataset.get_seg(t)
                if data is not None:
                    obj = self.compute_mesh(t, data)
                self.dataset.seg_datas.clear()

    def curate(self,load_default_plugins=True):  # START UPLOAD AND WAIT FOR ANNOTATION
        """ Start sending data to the browser 3D viewer, then wait for annotation from the browser

        Examples
        --------
        >>> mc=morphonet.Plot(start_browser=False)
        >>> mc.set_dataset(...)
        >>> mc.curate()
        """
        self.set_current_time(self.dataset.begin) #Initialise current time point at the first one
        printv("Wait for the MorphoNet Window",1)
        self.send("START_" + str(self.dataset.begin) + "_" + str(self.dataset.end))  # if curation on , restart_plot
        if load_default_plugins :self.set_default_plugins()  # Initialise Default set of plugins

        #PROPERTIES
        self.plot_properties()
        self.plot_annotations()
        self._reset_properties()
        self.send_properties_name()

        #INITALISE SCIKIT REGION PROPERTIES
        self.dataset.init_regionsprops()

        # MESHES
        self.plot_meshes()

        #RAW
        if self.dataset.raw:
            self.send("CONTAINSRAW_" + str(self.dataset.begin)) #Active Button Show Raw in Unity

        self.plot_raw(self.show_raw_t) #Activate the first time step only of no meshs

        # LAUNCH  SCIKIT PROPERTIES
        self.dataset.start_load_regionprops()  # Load all properties name

        #ACTIONS LIST
        self.send_actions()
        
        self.plot_stop_loading()

        self.wait_for_servers()

    def restart(self, times, label=None):
        if times is not None:  self.plot_meshes(times)  # PLOT MESHES

        self.plot_raw(self.current_time) # PLOT RAWDATAS

        self.plot_seeds(self.dataset.get_seeds())  # PLOT SEEDS

        self.delete_properties()  # REMOVE PROPERTIES WHICH HAVE BEEN DELETED

        self.plot_properties()  # PLOT ALL PROPERTIES

        self.plot_regionprops() #PLOT ALL LOADED REGION PROPERTIES

        self.plot_label(label)  # PLOT label

        self.send_actions()  # UPDATE ACTIONS LIST

        self._reset_properties()
        self.plot_stop_loading()

    def cancel(self):
        '''
        Cancel last action -> retrieve last backup
        '''
        self.dataset.cancel()

    def send_actions(self):
        '''
        Send To Unity the list of actions #TODO FUNCTION REICEVE IN UNITY
        '''
        actions = self.dataset.get_actions()
        self.send("ACTIONS",actions)

    #########################################  DATASET

    def set_dataset(self, begin=0, end=0, raw=None, segment=None, background=0, xml_file=None,import_temp=False,temp_archive_path=""):
        """ Define a dataset

        Parameters
        ----------
        begin : int
            minimal time point
        end : int
            maximal time point
        raw : string
            path to raw data file where time digits are in standard format (ex: {:03d} for 3 digits )(accept .gz)
        segment : string
            path to segmented data file  where time digits are in standard format (ex: {:03d} for 3 digits ) (accept .gz)
        background : int
            the pixel value of the background inside the segmented image
        xml_file : string
            path to the xml propertie files (.xml)
        factor : int
            reduction factor when meshes are calculated and send to the MorphoNet window
        raw_factor : int
            raw data reduction factor
        memory : int
            number of time step keep in memory durig curation (if you have memeory issue, decrease this number)

        Examples
        --------
        >>> ...after connection
        >>> mc.set_dataset(self,begin=0,end=10,raw="path/to/name_t{:03d}.inr.gz",segment="path/to/segmenteddata_t{:03d}.inr.gz",xml_file="path/to/properties_file.xml")
        """
        #default values for image scaling factors
        self.factor = 1  # Reduce factor to compute the obj
        self.z_factor = 1
        self.raw_factor = 1  # Reduction factor
        self.z_raw_factor = 1  # Reduction factor
        self.current_time = begin
        # Set Temporary folder
        if not self.full_path: #ONLY FOR DEV MODE
            self.temp_path =""
            temp_suffix = ""
            if segment is not None or raw is not None:
                if segment is not None and segment !="":
                    temp_suffix=segment
                elif raw is not None and raw !="":
                    temp_suffix=raw


                if platform == "win32" and ('{' in temp_suffix or '}' in temp_suffix or ':' in temp_suffix): #on windows, create a path without special characters
                    temp_suffix = temp_suffix.replace(":","")#.replace(os.sep,'_')

                self.temp_path = str(os.path.basename(temp_suffix))

            #add most params to path
            hcode = int(sha256(temp_suffix.encode('utf-8')).hexdigest(), 16) % 10**8
            self.temp_path += "_"+str(hcode)
            self.temp_path=join(self.temp_folder,self.temp_path)
        else:
            self.temp_path = self.temp_folder
            self.temp_folder = RemoveLastTokensFromPath(self.temp_folder,1)[:-1]

            if platform == "win32" and '{:' in self.temp_path: #on windows, create a path without special characters
                self.temp_path = self.temp_path.replace("{:","").replace("}","")

        mkdir(self.temp_folder)
        mkdir(self.temp_path)

        if import_temp:
            if os.path.isfile(temp_archive_path) and temp_archive_path.endswith("zip"):
                import shutil
                shutil.unpack_archive(temp_archive_path,self.temp_path,"zip")


        self.show_raw_t=begin#default: raw to show is the first one

        self.dataset = Dataset(self, begin, end, raw=raw, segment=segment, log=self.log, background=background,xml_file=xml_file, memory=self.memory,temp_path=self.temp_path)

    ######################################### PLUGINS

    def add_plugin(self, plug):
        """ Add a python plugin to be import in the MorphoNet Window

        Parameters
        ----------
        plugin : MorphoPlugin
            A plugin instance

        Examples
        --------
        from plugins.MARS import MARS
        mc.add_plugin(MARS())
        """
        if plug not in self.plugins:
            self.plugins.append(plug)
            self._create_plugin(plug)

    def _create_plugin(self, plug):
        """ Create the plugin in the MorphoNet Window

        Parameters
        ----------
        plug : MorphoPlugin
            A plugin instance

        """
        printv("Create Plugin " + plug.name,1)
        self.send("BTN", plug._get_btn())

        if plug.explanation is not None:
            bdata = plug.explanation_bytes #plug.explanation[:,:,0].tobytes(order="F")
            cmd = "EX_" +str(plug.explanation.shape[0])+"_"+str(plug.explanation.shape[1])+"_"+str(len(plug.explanation_bytes))+"_"+plug.name+"_"+plug.description
            self.send(cmd, bdata)
            
        if plug.icon is not None:
            bdata = plug.icon_bytes
            cmd = "IC_" +str(plug.icon.shape[0])+"_"+str(plug.icon.shape[1])+"_"+str(len(plug.icon_bytes))+"_"+plug.name
            self.send(cmd, bdata)

    def set_default_plugins(self):
        """ Load the default plugins to the 3D viewer

        Examples
        --------
        >>> mc.set_default_plugins()
        """
        printv("Load plugins...",1)
        from morphonet.plugins import defaultPlugins
        for plug in defaultPlugins:  self.add_plugin(plug)

    def clear_plugins(self):
        """ Clear all preloaded (default ) plugins

        Examples
        --------
        >>> mc.clear_plugins()
        """
        if self.plugins is None or len(self.plugins)==0: return True
        printv("Clear +" +str(len(self.plugins)))
        self.plugins.clear()


    ######################################### RAWIMAGES

    def hide_raw(self):
        """ Enable the possibility to plot raw images to the browser for a specified time point ?

        Parameters
        ----------
        t : int
            time point to display raw images from

        Examples
        --------
        >>> mc.hide_raw(1)
        """
        self.show_raw=False

    def plot_raw(self, t):
        """ Compute and send raw images to the browser for a specified time point

        Parameters
        ----------
        t : int
            time point to display raw images from

        Examples
        --------
        >>> mc.plot_raw(1)
        """
        if self.show_raw and self.dataset.raw and t is not None:
            #printv("Send rawdatas at " + str(t),1)
            rawdata = self.dataset.get_raw(t)
            if rawdata is not None:
                new_shape = np.uint16(np.floor(np.array(rawdata.shape) / self.raw_factor) * self.raw_factor)  # To avoid shifting issue
                new_shape_z = floor(rawdata.shape[2] / self.z_raw_factor) * self.z_raw_factor
                rawdata = rawdata[0:new_shape[0], 0:new_shape[1], 0:new_shape_z]
                factor_data = rawdata[::self.raw_factor, ::self.raw_factor, ::self.z_raw_factor]
                nbdata = np.uint8(np.float32(np.iinfo(np.uint8).max) * factor_data / factor_data.max())
                bdata = nbdata.tobytes(order="F")
                cmd = "RAW_" + str(t) + "_" + str(rawdata.shape[0]) + "_" + str(rawdata.shape[1]) + "_" + str(rawdata.shape[2]) + "_" + str(self.raw_factor) + "_"+ str(self.z_raw_factor) + "_" + self.dataset.get_center(txt=True) +"_"+self.dataset.get_voxel_size(t,txt=True)
                self.send(cmd, bdata)

    ######################################### ADDD SEEDS

    def plot_seeds(self, seeds):
        """ Plot seeds to the browser

        Parameters
        ----------
        seeds : string
            the centers of the seeds

        Examples
        --------
        >>> mc.plot_seeds(seeds)
        """
        if seeds is not None and seeds != "":
            self.send("SEEDS", seeds)

    ######################################### PRIMITIVES

    def add_primitive(self, name, obj):
        """ Add a primitive using specified content with the specified name to the browser

        Parameters
        ----------
        name : string
            the name of the primitive
        obj : bytes
            content of the primitive (3D data)

        Examples
        --------
        >>> #Specify a file on the hard drive by path, with rights
        >>> f = open(filepath,"r+")
        >>> #load content of file inside variable
        >>> content = f.read()
        >>> mc.add_primitive("primitive name",content)
        >>> f.close()
        """
        self.send("PRIM_" + str(name), obj)

    ######################################### PROPERTIES

    def _reset_properties(self):
        """
            Reset the updated of all properties
        """
        if self.dataset.properties is not None:
            for property_name in self.dataset.properties:
                pro = self.get_property(property_name)
                pro.updated = False

    def get_property_field(self, property_name):
        """ Called when Unity asked for the txt field of the propety name

        """
        prop = self.get_property(property_name)
        if prop is None:  #Not loaded yet loaded
            printv("not yet loaded: "+property_name,2)
            if property_name in self.dataset.xml_properties_type: #Confirm that it's in the avaiable xml file
                printv(" loading " + property_name+"...", 1)
                self.dataset.read_xml(self.dataset.xml_file, property=property_name, all=False,export=False)

        #self.plot_property(self.get_property(property_name))  #Now We plot the property
        self.restart(None)

    def send_properties_name(self):
        """
        Send only the name of the properties that are existing in the xml but not loaded
        """
        if self.dataset.properties is not None:
            for property_name in self.dataset.xml_properties_type:
                if self.get_property(property_name) is None: #only send property if it does not yet exist in text
                    if self.dataset.xml_properties_type[property_name] != "time":#do not send lineage in names, it should already be sent
                        self.send("INFONAME_" + property_name,self.dataset.xml_properties_type[property_name])

    def plot_properties(self):

        """ Plot all the Properties of the datasset
        """

        if self.dataset.properties is not None:
            for property_name in self.dataset.properties:
                self.plot_property(self.get_property(property_name))

    def plot_property(self, property):  # PLOT property
        """ Send the specified properties with the specified name to browser

        Parameters
        ----------
        property : Property Class
           the property to plot

        Examples
        --------
        >>> my_prop=mc.get_property("Cell Name")
        >>> mc.plot_property(my_prop)
        """

        if property is None: return None
        if property.updated:
            text = property.get_txt(time_begin=self.dataset.begin, time_end=self.dataset.end,empty=True)
            printv("plot " + property.name,1)
            self.send("INFO_" + property.name, text)

    def plot_stop_loading(self):
        printv("DONE", 0)  # To clear unity messages
        printv("Wait for a command", 1)
        self.send("STOPLOAD")

    def plot_annotations(self):

        """ Plot all the annotation for all the properties of the datasset
        """

        if self.dataset.properties is not None:
            for property_name in self.dataset.properties:
                self.plot_annotation(self.get_property(property_name))

    def plot_annotation(self,property):
        """ Send the specified annotation for the properties with the specified name to browser

        Parameters
        ----------
        property : Property Class
           the property to plot
        """

        if property is None:
            return
        if property.property_type!="time" and property.property_type!="label" and property.property_type!="selection":
            txt = property.get_txt(time_begin=self.dataset.begin, time_end=self.dataset.end, all_values=True)
            if txt is not None:
                printv("plot annotation for " + property.name,1)
                self.send("CUR_" + property.name, txt)
            else:
                printv("no annotation for " + property.name, 1)

    def get_properties(self):
        """ Return all the properties associated to the dataset
        """
        return self.dataset.properties

    def get_property(self, property_name):
        """ Return the property associated to the dataset

        Parameters
        ----------
        property_name : string
           the name of the property

        return property :  Property Class
            return an object of property


        Examples
        --------
        >>> my_prop=mc.get_property("Cell Name")
        """
        if property_name in self.dataset.properties:
            return self.dataset.properties[property_name]
        return None

    def create_property(self, property_name, property_type, data=None):
        """ Create an property associated to the dataset

        Parameters
        ----------
        property_name : string
           the name of the property
        property_type
            the type of the property (float,string, etc.. ) in string
        data (optional) : List<string> or property as in MorphoNet
            property content as a list of all lines

        Examples
        --------
        >>> prop=mc.create_property("Cell Name","string")
        >>> prop.set(el,"a7.8")
        """
        prop = self.dataset.get_property(property_name, property_type=property_type, reload=False)
        if data is not None:  prop.add_data(data)
        return prop

    def delete_property(self, property_name):
        """ delete an property associated to the dataset

        Parameters
        ----------
        property_name : string
           the name of the property

        Examples
        --------
        >>> prop=mc.delete_property("Cell Name")
        >>> prop.set(el,"a7.8")
        """
        if property_name in self.dataset.properties:
            self.dataset.properties.remove(property_name)

    def set_property_type(self, property_name, property_type):
        """ Change or specify the type of an property associated to the dataset
            The property can be created directly in python or load in the XML file

        Parameters
        ----------
        property_name : string
          the name of the property
        property_type
           the type of the property (float,string, etc.. )  in string

        Return True if the changement is affected

        Examples
        --------
        >>> mc.set_property_type("ThisField","label")
        """
        prop = self.get_property(property_name)
        if prop is None:
            return False
        prop.property_type = property_type
        return True

    def reload_properties(self):
        self.plot_properties()
        self.plot_annotations()

    def annotate(self, property_name, k, v, d):
        """ Apply the annotation value of a specific object for the property name

        Parameters
        ----------
        property_name : string
           the name of the property
        k : string
            object to annotate
        v : string
            value of annotate
        d : string
            date of annotate
        """
        printv("annotate property " + property_name,1)
        prop = self.get_property(property_name)
        o = self.dataset.get_object(k)
        prop.set(o, v, date=d)
        prop.export()
        prop.export_annotation()
        self.restart(None)

    def delete_annotation(self, property_name, k, v, date=None):
        """ Delete the annotation value of a specific object for the property name

        Parameters
        ----------
        property_name : string
           the name of the property
        k : string
            object to annotate
        v : string
            value of annotation
        d : string
            date of annotation
        """
        prop = self.get_property(property_name)
        o = self.dataset.get_object(k)
        if not prop.del_annotation(o, v, date=date):
            printv(" Error during the deletion of the annotatotion ",1)
        else:
            prop.export()
            prop.export_annotation()
        self.restart(None)

    def create_property_from_unity(self, property_name, property_type, data):
        """ Create or Update property when receiving data from unity

        Parameters
        ----------
        property_name : string
           the name of the property
        datatype : string
            property type
        data : string
            data to write in property file
        """
        pro=None
        if property_name in self.dataset.properties : #property already exist , it's an update
            if property_type == "label" or property_type == "selection" :
                pro=self.dataset.properties[property_name]
                pro.clear()
            else: printv("this name already exist ",0)# nothing to do, we cannot create two qualitative properties with the exact same name
        else:
            pro = self.dataset.get_property(property_name, property_type=property_type, reload=False)
        if pro is not None:
            if data is not None:  pro.add_data(data)
            pro.export()  # Save It
        self.restart(None)

    def delete_property_from_unity(self, property_name):
        """ Delete property asked from unity

        Parameters
        ----------
        property_name : string
           the name of the property
        """
        printv("delete property " + property_name,1)
        prop = self.get_property(property_name)
        if prop is not None:
            prop.delete()
            self.restart(None)

    def delete_label_from_unity(self, property_name, label_number):
        """ Delete property when receiving data from unity

        Parameters
        ----------
        property_name : string
           the name of the property
        datatype : string
            property type
        data : string
            data to write in property file
        """
        self.delete_property(property_name)
        self.restart(None)

    def delete_properties(self):
        '''
        Remove In unity the properties which have been deleted in python
        '''
        to_remove=[]
        if self.dataset.properties is not None:
            for property_name in self.dataset.properties:
                prop=self.get_property(property_name)
                if prop.todelete:
                    printv("delete "+property_name,1)
                    self.send("DELINFO_" + property_name) # TODO THE FUNCTION IS NOT EXISTING IN UNITY
                    to_remove.append(prop)
        for prop in to_remove:
            prop.delete() #Full Detion


    ######################################### SCIKIT PROPERTY
    def is_all_computed_regionprop(self,name):
        if name not in self.dataset.regionprops:
            return False
        if len(self.dataset.regionprops[name].data)==0:  #Raw only
            return False

        for t in range(self.dataset.begin, self.dataset.end + 1):
            if t in self.dataset.regionprops[name].computed_times:
                if not self.dataset.regionprops[name].computed_times[t]:
                    return False
            else:
                return False
        return True


    def get_regionprop(self, name):
        """ Called when Unity asked for the property  of the scikit regions property

        """
        printv(" get_property "+name,2)

        if self.dataset.regionprops is not None:
            if name in self.dataset.regionprops:
                printv("Set property "+name+ " loaded",1)
                self.dataset.regionprops[name].asked=True
        self.restart(None)

    def plot_regionprops(self):
        """
        Plot all the propeties required by the user
        And send the name that are existing in the xml but not yet asked by the user
        """
        if self.dataset.regionprops is not None:
            for name in self.dataset.regionprops:
                if self.is_all_computed_regionprop(name):  # All properties are calculated
                    if not self.dataset.regionprops[name].name_send : #Not the name already send ...
                        self.send("SKINFONAME_" + name, self.dataset.regionprops[name].type)
                        self.dataset.regionprops[name].name_send=True #Set that the name is already send

                    if self.dataset.regionprops[name].asked: #Update the values if asked
                        self.plot_regionprop(name)

    def plot_regionprop(self, name):  # PLOT Scikiimage property
        """ Send the specified property with the specified name to browser

        Parameters
        ----------
        name : property name
        """
        printv("Plot scikit property "+name,2)
        if self.dataset.regionprops is not None:
            if name in self.dataset.regionprops:
                self.dataset.wait_regionprops()
                prop=self.dataset.regionprops[name]
                prop_text = prop.get_txt()
                printv("plot " + name, 1)
                self.send("INFO_"+name, prop_text)

    #########################################  LABEL

    def plot_label(self, label):
        '''
        Plot label (list of objects separated by ;)
        '''
        if label is not None:
            printv("label " + label,1)
            self.send("SELECT", str(label))

    #########################################  MESH
    def set_mesh_parameters(self,voxel_override=False,voxel_size=(1.0,1.0,1.0),factor=1,z_factor=None,raw_factor=1,z_raw_factor=None,smoothing=True,smooth_passband=0.01,
                            smooth_iterations=25,quadric_clustering=True,qc_divisions=1,decimation=True,
                            decimate_reduction=0.8,auto_decimate_threshold=30):
        self.voxel_override = voxel_override
        self.voxel_size = voxel_size
        self.factor = factor
        self.raw_factor=raw_factor
        self.z_raw_factor=z_raw_factor if z_raw_factor is not None else raw_factor
        self.z_factor = z_factor if z_factor is not None else factor
        self.smoothing=smoothing
        self.smooth_passband = smooth_passband
        self.smooth_iterations = smooth_iterations
        self.quadric_clustering = quadric_clustering
        self.qc_divisions = qc_divisions
        self.decimation = decimation
        self.decimate_reduction = decimate_reduction
        self.auto_decimate_threshold = auto_decimate_threshold
    
    
    def compute_mesh(self, t, data=None):
        if t not in self.dataset.cells_updated: #The first start , we use the precomputed cell
            self.dataset.cells_updated[t] = []
            
        obj_step=self.dataset.get_last_version(str(t)+".obj",step_only=True)
        obj_path=join(self.temp_path,str(obj_step))
        if obj_step!=self.dataset.step: #The folder is different of the current one
            if self.dataset.cells_updated[t] is None or len(self.dataset.cells_updated[t]) > 0:
                if isdir(join(obj_path,str(t))):
                    cp_dir(join(obj_path,str(t)),join(self.dataset.step_folder,str(t))) #Copy Previous Cell
                obj_path=self.dataset.step_folder

        obj_filename = join(obj_path, str(t) + ".obj")
        if not isfile(obj_filename): #No need to try to compute if file is empty
            #printv("No mesh provided for time : "+str(t),2)
            if data is None:
                return None
        printv("Compute_mesh at " + str(t) + " from "+obj_path, 2)
        region=None
        if t not in self.dataset.regions_thread: self.dataset.compute_regionprops(t)
        if t in self.dataset.regions_thread:
            self.dataset.regions_thread[t].join() #Wait the region is initialized
            if t in self.dataset.regions: region=self.dataset.regions[t]
        obj = fast_convert_to_OBJ(data,regions=region, t=t, background=self.dataset.background,factor=self.factor, center=self.dataset.get_center(),VoxelSize=self.dataset.get_voxel_size(t),
                             cells_updated=self.dataset.cells_updated[t],path_write=obj_path,write_vtk=True,force_recompute=self.recompute,z_factor=self.z_factor,
                             Smooth=self.smoothing,smooth_passband=self.smooth_passband,
                             smooth_iterations=self.smooth_iterations,Decimate=self.quadric_clustering,QC_divisions=self.qc_divisions,
                             Reduction=self.decimation,TargetReduction=self.decimate_reduction,DecimationThreshold = self.auto_decimate_threshold)  # Create the OBJ
        if obj is None:
            printv("Unable to compute mesh at time : "+str(t)+" please verify your path to segmentation", 0)
        if data is not None:
            self.dataset.cells_updated[t] = [] #We don' want to reset if nothing was recalculated
        return obj

    def get_mesh_object(self,mo):
        """
        Return the mesh (in obj) for a given cell
        (Read the vtk temporart file and convert it to obj)
        """
        obj_step = self.dataset.get_last_version(str(mo.t) + ".obj", step_only=True) #Look for the location of th last time point
        obj_mesh_path = join(self.temp_path, str(obj_step),str(mo.t))
        if not isdir(obj_mesh_path):
            printv("error did not find the temporary mesh path "+obj_mesh_path, 1)
            return None
        cell_mesh_filename=join(obj_mesh_path,str(mo.t)+'-'+str(mo.id)+'.vtk')

        if not isfile(cell_mesh_filename):
            printv("error did not find the temporary cell mesh file " + cell_mesh_filename, 1)
            return None

        #Convert VTK in OBJ
        obj=convert_vtk_file_in_obj(cell_mesh_filename, mo, ch=0, factor=self.factor, center=self.dataset.get_center(), VoxelSize=self.dataset.get_voxel_size(mo.t))
        return obj

    def recompute_mesh_at_t(self,t):
        data = self.dataset.get_seg(t)
        if data is not None:
            self.dataset.cells_updated[t] = None
            obj = self.compute_mesh(t, data)

    def recompute_data(self):
        """ Force computation of meshes and properties for all time points

        """
        self.recompute=True
        printv("Recompute data ", 1)
        times = range(self.dataset.begin, self.dataset.end + 1)
        self.dataset.seg_datas.clear()
        for t in times:
            self.recompute_mesh_at_t(t) #Force computing mesh again , and send it to unity
            #self.dataset.load_regionprops_at(t,recompute=True,send_properties=False)
        self.recompute=False

    def plot_mesh(self, t):  # UPLOAD DIRECTLY THE OBJ TIME POINT IN UNITY
        """ Send the 3D files for the specified time point to browser and display the mesh

        Parameters
        ----------
        t : int
            the time point to display in browser

        Examples
        --------
        >>> mc.plot_mesh(1)
        """
        printv("Plot mesh " + str(t), 1)
        obj = self.compute_mesh(t) #We first look if a temporary file is available (ONLY WHEN NO cells_updated)
        if obj is None:
            data = self.dataset.get_seg(t)
            if data is not None:
                obj = self.compute_mesh(t, data)
        if obj is not None and obj!="":
            self.show_raw_t = t
            self.send("LOAD_" + str(t), obj)


    def plot_at(self, t, obj):  # PLOT DIRECTLY THE OBJ PASS IN ARGUMENT
        """ Plot the specified 3D data to the specified time point inside the browser

        Parameters
        ----------
        t : int
            the time point to display in browser
        obj : bytes
            the 3d data

        Examples
        --------
        >>> #Specify a file on the hard drive by path, with rights
        >>> f = open(filepath,"r+")
        >>> #load content of file inside variable
        >>> content = f.read()
        >>> mc.plot_at(1,content)
        >>> f.close()
        """
        self.send("LOAD_" + str(t), obj)

    def plot_meshes(self, times=None):  # PLOT ALL THE TIMES STEP EMBRYO IN MORPHONET
        """ Plot all data inside the browser

        Examples
        --------
        >>> mc.plot_meshes()
        """
        printv("Plot Meshes...",1)
        if times is None:
            times = range(self.dataset.begin, self.dataset.end + 1)
        for t in times:
            self.plot_mesh(t)

    def del_mesh(self, t):  # DELETE DITECLTY THE OBJ TIME POINT IN UNITY
        """ Delete the specified time point in the browser

        Parameters
        ----------
        t : int
            the time point to delete

        Examples
        --------
        >>> mc.del_mesh(1)
        """
        self.send("DEL_" + str(t))

    ################ TO QUIT PROPERLY
    def clear_backup(self):
        '''
        To Clear backup files
        '''
        rmrf(self.temp_path)

    def _receive_signal(self, signalNumber):
        if signalNumber == 2:
            self.quit_and_exit()
        return



