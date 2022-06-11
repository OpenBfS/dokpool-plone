APP_REGISTRY = {}
BEHAVIOR_REGISTRY = {}


def registerApp(
    name,
    title,
    typeBehavior,
    documentBehavior,
    dpAddedMethod,
    dpRemovedMethod,
    icon=None,
    logo=None,
    implicit=False,
):
    """
    @param name:
    @param factoryMethod:
    @return:
    """
    APP_REGISTRY[name] = {
        'title': title,
        'implicit': implicit,
        'icon': icon,
        'logo': logo,
        'typeBehavior': typeBehavior,
        'documentBehavior': documentBehavior,
        'dpAddedMethod': dpAddedMethod,
        'dpRemovedMethod': dpRemovedMethod,
    }
    if typeBehavior:
        BEHAVIOR_REGISTRY[typeBehavior.__identifier__] = (
            BEHAVIOR_REGISTRY.get(typeBehavior.__identifier__, None)
            and BEHAVIOR_REGISTRY[typeBehavior.__identifier__].append(name)
            or [name]
        )

    if documentBehavior:
        BEHAVIOR_REGISTRY[documentBehavior.__identifier__] = (
            BEHAVIOR_REGISTRY.get(documentBehavior.__identifier__, None)
            and BEHAVIOR_REGISTRY[documentBehavior.__identifier__].append(name)
            or [name]
        )


def appName(name):
    return APP_REGISTRY[name]['title']


def appIcon(name):
    return APP_REGISTRY[name]['icon']


def extensionFor(obj, name):
    """

    @param obj:
    @param name:
    @return:
    """
    from docpool.base.interfaces import IDPDocument

    if IDPDocument.providedBy(obj):
        return APP_REGISTRY[name]['documentBehavior']
    else:
        return APP_REGISTRY[name]['typeBehavior']


def extensionNameFor(obj, name):
    from docpool.base.interfaces import IDPDocument

    if IDPDocument.providedBy(obj):
        return APP_REGISTRY[name]['documentBehavior'].__identifier__
    else:
        return APP_REGISTRY[name]['typeBehavior'].__identifier__


def activeApps():
    """
    Return all active applications.
    @return:
    """
    apps = sorted(APP_REGISTRY.keys())
    return [
        (appname, APP_REGISTRY[appname]['title'], APP_REGISTRY[appname])
        for appname in apps
    ]


def extendingApps():
    """
    Just those apps, that actually provide dynamic extensions to documents.
    @return:
    """
    apps = sorted(APP_REGISTRY.keys())
    return [
        (appname, APP_REGISTRY[appname]['title'], APP_REGISTRY[appname])
        for appname in apps
        if APP_REGISTRY[appname].get('documentBehavior', None)
    ]


def implicitApps():
    """
    Return all implicit applications which do not require special activation per object.
    @return:
    """
    apps = sorted(APP_REGISTRY.keys())
    return [
        (appname, APP_REGISTRY[appname]['title'], APP_REGISTRY[appname])
        for appname in apps
        if APP_REGISTRY[appname]['implicit']
    ]


def selectableApps():
    """
    Just those apps, that correspond to a main application, i.e. they provide behavior and they are not implicit.
    @return:
    """
    apps = sorted(APP_REGISTRY.keys())
    return [
        (appname, APP_REGISTRY[appname]['title'], APP_REGISTRY[appname])
        for appname in apps
        if APP_REGISTRY[appname].get('documentBehavior', None)
        and not APP_REGISTRY[appname]['implicit']
    ]
