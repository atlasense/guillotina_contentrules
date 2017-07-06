from guillotina import configure


app_settings = {
    "contentrules_executor": "guillotina_contentrules.executor.Executor"
}


def includeme(root):
    """
    custom application initialization here
    """
    configure.scan('guillotina_contentrules.api')
    configure.scan('guillotina_contentrules.install')
    configure.scan('guillotina_contentrules.utility')
    configure.scan('guillotina_contentrules.subscribers')
    configure.scan('guillotina_contentrules.conditions')
    configure.scan('guillotina_contentrules.actions')
