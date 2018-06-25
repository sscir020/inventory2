from . import ctr

@ctr.app_errorhandler(404)
def page_not_found(e):
    return "not found 404"

@ctr.app_errorhandler(500)
def internal_error(e):
    return "internal 500"
