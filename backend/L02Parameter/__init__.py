from L02Parameter.Enumeration.ParameterType import *
from L02Parameter.Supported import *

""" this models contains all the classes to represent the 
different parameters that might be used in the different
steps of the process discovery. They are intended to be used
in a very generic way and can of course be expanded upon. All 
parameter classes inherit their basic structure form the 
ParameterSuperClass that is also contained in this module and 
are represented by a corresponding entry in the ParameterType
enumeration. 

In case you want to add more parameter types, you have to 
consider a few things. First you should make sure to extend
the ParameterType enumeration with your new type and initiate
the super class correctly. Afterwards you should stay close to
the other implemented parameter types. The methods get_info_dict,
set_info_dict, set_current_value and the attribute current_value 
have to be included in every parameter class. You can enforce 
additional restrictions if you wish, take a look at the existing 
parameter classes to get an impression on how to do it. At this
point you should make sure that all your methods are working and
that an instance of your parameter class can be dumped by the 
python pickle module. If this is not the case, please overwrite 
the internal __getstate__ and __setstate__ methods!

After having a working parameter class you still need to make 
sure that the parameter type will be supported by the other
modules in this project as. The optimizer module is the first
one you should adapt, and includes it's own documentation on 
how to include a new parameter type. At this point the flask 
api should already be working, but the gui might still have 
problems with displaying your parameter type and editing it's 
value. This is normal and no cause for concern, since  it does 
not now what to dowith the info dict that your class provides.
Check out the documentation of the frontend module to deal with
this problem! """

