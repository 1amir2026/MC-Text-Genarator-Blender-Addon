from . import operators, panels, properties

MODULES = (properties, operators, panels)


def register():
    for module in MODULES:
        module.register()


def unregister():
    for module in reversed(MODULES):
        module.unregister()
