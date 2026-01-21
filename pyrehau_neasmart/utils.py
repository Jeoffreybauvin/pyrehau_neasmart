def autoupdate_property(func):
    def update_and_get(*args):
        args[0]._update_if_needed()
        return func(*args)
    return property(update_and_get)
