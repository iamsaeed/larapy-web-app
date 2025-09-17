"""
Web Routes - Define application routes
"""

def register_routes(router, app):
    """Register all web routes"""
    
    from app.Http.Controllers.HomeController import HomeController
    
    # Initialize controller
    controller = HomeController()
    
    # Web routes (return HTML views)
    router.get('/', controller.index)
    router.get('/contact', controller.contact)
