"""
Web Routes - Define application routes with security middleware
"""

def register_routes(router, app):
    """Register all web routes with security features"""
    
    from app.Http.Controllers.HomeController import HomeController
    
    # Simple routes without middleware complexity for now
    controller = HomeController()
    router.get('/', controller.index)
    router.get('/contact', controller.contact)
    router.get('/api/data', controller.api_data)
    
    # Example of a simple secured route using decorator
    @app.flask_app.route('/dashboard')
    def dashboard():
        # This would normally check authentication
        return {"message": "Welcome to your dashboard!", "status": "success"}
    
    # Test route to verify CSRF tokens work
    @app.flask_app.route('/test-csrf', methods=['GET', 'POST'])
    def test_csrf():
        from flask import request, render_template_string
        
        if request.method == 'GET':
            form_html = '''
            <form method="POST">
                {{ csrf() }}
                <input type="text" name="test_input" placeholder="Test input">
                <button type="submit">Submit</button>
            </form>
            '''
            return render_template_string(form_html)
        else:
            return {"message": "Form submitted successfully", "data": dict(request.form)}
