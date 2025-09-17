"""
Web Routes - Define application routes
"""

def register_routes(router, app):
    """Register all web routes"""
    
    from app.Http.Controllers.HomeController import HomeController
    
    # Web routes (return HTML views)
    router.get('/', HomeController().index)
    router.get('/contact', HomeController().contact)
