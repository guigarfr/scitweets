import os
import platform

computer = platform.node()

if 'finestral' in computer:
    print "** Loading local settings"
    try:
        from .local import *
    except ImportError:
        pass

else:


    # NOTA: heroku config:set ON_HEROKU=1 --app myapp

    if 'ON_HEROKU' in os.environ:
        print "** Loading HEROKU production settings"
        try:
            from .production_heroku import *
        except ImportError:
            pass


    # NOTA: rhc set-env ON_OPENSHIFT=1 -a myapp
    if 'ON_OPENSHIFT' in os.environ:
        print "** Loading OPENSHIFT production settings"
        try:
            from .production_openshift import *
        except ImportError:
            pass