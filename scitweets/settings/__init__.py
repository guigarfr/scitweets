import platform

computer = platform.node()

if 'finestral' in computer:
    print "** Loading local settings"
    try:
        from .local import *
    except ImportError:
        pass

else:
    print "** Loading production settings"
    try:
        from .production import *
    except ImportError:
        pass

