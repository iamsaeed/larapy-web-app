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
    router.get('/about', controller.about)
    router.get('/contact', controller.contact)
    
    # API routes (return JSON responses)
    router.get('/health', controller.health)
    router.get('/api/status', controller.api_status)
    router.get('/api/users', controller.api_users)
    router.post('/api/users', controller.api_user_store)
    router.get('/api/users/<int:user_id>', controller.api_user_show)
    
    # Demo routes (return JSON responses)
    router.get('/demo/container', controller.demo_container)
    router.get('/demo/orm', controller.demo_orm)
    router.get('/demo/middleware', controller.demo_middleware)
