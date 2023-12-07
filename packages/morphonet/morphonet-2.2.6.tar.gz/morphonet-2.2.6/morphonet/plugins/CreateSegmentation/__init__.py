# -*- coding: latin-1 -*-
defaultPlugins=[]

from .Stardist import Stardist
defaultPlugins.append(Stardist())

from .Cellpose import Cellpose
defaultPlugins.append(Cellpose())

from .Mars import Mars
defaultPlugins.append(Mars())
