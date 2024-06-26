from os import environ
# import platform
# computer = platform.node()
#
# if 'finestral' in computer:
#     print "** Loading local settings"
#     try:
#         from .local import *
#     except ImportError:
#         pass

loaded_settings = False

# NOTA: heroku config:set ON_HEROKU=1 --app myapp
if 'ON_HEROKU' in environ:
    print "** Loading HEROKU production settings"
    try:
        from .production_heroku import *
        loaded_settings = True
    except ImportError:
        print "Error importing HEROKU settings!"
        pass


# NOTA: rhc set-env ON_OPENSHIFT=1 -a myapp
if 'ON_OPENSHIFT' in environ:
    print "** Loading OPENSHIFT production settings"
    try:
        from .production_openshift import *
        loaded_settings = True
    except ImportError:
        print "Error importing OPENSHIFT settings!"
        pass

if not loaded_settings:
    print "** Loading local settings"
    try:
        from .local import *
    except ImportError:
        pass
