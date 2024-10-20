

def register_addon():

    # Operators
    from ..property import register_addon_properties
    register_addon_properties()

    from ..operator import register_operators
    register_operators()

    from ..menu import register_menus
    register_menus()


def unregister_addon():

    from ..property import unregister_addon_properties
    unregister_addon_properties()

    # Operators
    from ..operator import unregister_operators
    unregister_operators()

    from ..menu import unregister_menus
    unregister_menus()

