import inspect
import sys
from fabric.tasks import WrappedCallableTask

# taken from http://www.saltycrane.com/blog/2010/09/class-based-fabric-scripts-metaprogramming-hack/
def is_method_or_task(member):
    ""
    return bool(inspect.ismethod(member) or isinstance(member,WrappedCallableTask))

def class_methods_to_functions(instance,module_name):
    '''
    Utility to take the methods of the instance of a class, instance,
    and add them as functions to a module, module_name, so that Fabric
    can find and call them. Call this at the bottom of a module after
    the class definition.
    '''
    # get the module as an object
    module_obj = sys.modules[module_name]

    # Iterate over the methods of the class and dynamically create a function
    # for each method that calls the method and add it to the current module
    for method in inspect.getmembers(instance, predicate=is_method_or_task):
        method_name, method_obj = method
        if not method_name.startswith('_'):
            # get the bound method
            func = getattr(instance, method_name)

            # add the function to the current module
            setattr(module_obj, method_name, func)

def copy_keys(dict1,dict2):
    """
    copy keys from one dictionary to another
    """
    for key in dict2.keys(): dict1[key] = dict2[key]
