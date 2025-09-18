# Larapy Security Implementation

This document describes the Laravel-style security features implemented in Larapy and how to use them in your application.

## Overview

The security system provides Laravel-compatible protection against common web vulnerabilities:

- CSRF (Cross-Site Request Forgery) protection
- Cookie encryption
- Rate limiting/throttling  
- CORS (Cross-Origin Resource Sharing) handling
- Security headers (CSP, HSTS, X-Frame-Options, etc.)
- Password hashing with bcrypt/Argon2
- Authentication middleware
- Encryption services

## Quick Start

### 1. Environment Configuration

Copy `.env.example` to `.env` and configure your security settings:

```bash
cp .env.example .env
```

Generate a secure APP_KEY (32 characters):
```bash
python -c "import secrets; print('APP_KEY=' + secrets.token_urlsafe(32))"
```

### 2. Basic Usage

The security middleware is automatically applied when using the HTTP kernel:

```python
# In routes/web.py
def register_routes(router, app):
    kernel = app.resolve('kernel')
    
    # Apply security middleware groups
    protected_route = kernel.apply_middleware_to_route(
        your_controller_method,
        ['global', 'web']  # global + web middleware
    )
    router.post('/form', protected_route)
```

## CSRF Protection

### Templates

Add CSRF tokens to your forms:

```html
<!-- Method 1: Using csrf() helper -->
<form method="POST" action="/submit">
    {{ csrf() }}
    <!-- your form fields -->
</form>

<!-- Method 2: Using csrf_field() -->
<form method="POST" action="/submit">
    {{ csrf_field() }}
    <!-- your form fields -->
</form>

<!-- Method 3: Manual token -->
<form method="POST" action="/submit">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
    <!-- your form fields -->
</form>
```

For AJAX requests, add the meta tag and configure your HTTP client:

```html
<head>
    {{ csrf_meta() }}
</head>

<script>
// Configure axios
axios.defaults.headers.common['X-CSRF-TOKEN'] = 
    document.querySelector('meta[name="csrf-token"]').content;

// Or for fetch
const token = document.querySelector('meta[name="csrf-token"]').content;
fetch('/api/endpoint', {
    method: 'POST',
    headers: {
        'X-CSRF-TOKEN': token,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
});
</script>
```

### Excluding Routes

To exclude routes from CSRF protection:

```python
# In config/security.py
'csrf': {
    'exclude': [
        'api/*',
        'webhooks/*',
        'stripe/webhook',
    ]
}
```

## Rate Limiting

### Using Decorators

```python
from larapy.routing.middleware.throttle_requests import throttle

# Limit to 5 requests per minute
@throttle('login', 5, 1)
def login():
    return "Login endpoint"

# Use predefined rate limiters
@throttle('api')  # Uses API rate limit from config
def api_endpoint():
    return {"data": "API response"}
```

### Route Groups

```python
# Apply rate limiting via middleware groups
api_route = kernel.apply_middleware_to_route(
    api_controller_method,
    ['global', 'api']  # Includes API rate limiting
)
```

### Configuration

Set rate limits in environment or config:

```bash
# .env
RATE_LIMIT_DEFAULT=60,1    # 60 requests per minute
RATE_LIMIT_API=1000,60     # 1000 requests per hour  
RATE_LIMIT_LOGIN=5,1       # 5 attempts per minute
```

## Authentication

### Protecting Routes

```python
from larapy.auth.middleware.authenticate import auth_required

@auth_required(['web'])
def dashboard():
    return render_template('dashboard.html')

@auth_required(['api'])
def api_user_data():
    return {"user": "data"}
```

### Helper Functions

```python
from larapy.auth.middleware.authenticate import (
    auth_user, auth_check, auth_id, auth_login, auth_logout
)

# Check if authenticated
if auth_check():
    user = auth_user()
    user_id = auth_id()

# Login a user
auth_login(user, remember=True)

# Logout
auth_logout()
```

### Guest Routes

Redirect authenticated users away from guest-only pages:

```python
from larapy.auth.middleware.authenticate import guest_only

@guest_only(redirect_to='/dashboard')
def login_page():
    return render_template('auth/login.html')
```

## Password Hashing

### Basic Usage

```python
from larapy.support.facades.hash import Hash

# Hash a password
hashed = Hash.make('secret123')

# Verify a password
if Hash.check('secret123', hashed):
    print("Password matches!")

# Check if rehashing needed (after changing cost)
if Hash.needs_rehash(hashed):
    new_hash = Hash.make('secret123')
```

### Configuration

```bash
# .env
HASH_DRIVER=bcrypt
BCRYPT_ROUNDS=12

# Or use Argon2
HASH_DRIVER=argon2
ARGON2_MEMORY=65536
ARGON2_TIME=4
ARGON2_THREADS=3
```

## Encryption

### Encrypting Data

```python
from larapy.support.facades.crypt import Crypt

# Encrypt data (supports strings, dicts, lists)
encrypted = Crypt.encrypt({'user_id': 123, 'role': 'admin'})

# Decrypt data
decrypted = Crypt.decrypt(encrypted)

# String-only encryption
encrypted_string = Crypt.encrypt_string('sensitive data')
decrypted_string = Crypt.decrypt_string(encrypted_string)
```

### Cookie Encryption

Cookies are automatically encrypted/decrypted by the middleware:

```python
# Cookies are automatically encrypted
response.set_cookie('user_preference', 'dark_mode')

# And automatically decrypted when accessed
preference = request.cookies.get('user_preference')  # Returns 'dark_mode'
```

Exclude cookies from encryption:

```python
# In config/security.py  
'cookies': {
    'exclude': [
        'cookie_consent',
        'analytics_id',
    ]
}
```

## CORS

### Configuration

```python
# In config/security.py
'cors': {
    'paths': ['api/*', 'webhooks/*'],
    'allowed_origins': ['https://yourdomain.com', 'https://app.yourdomain.com'],
    'allowed_methods': ['GET', 'POST', 'PUT', 'DELETE'],
    'allowed_headers': ['Content-Type', 'Authorization'],
    'exposed_headers': ['X-Total-Count'],
    'max_age': 86400,  # 24 hours
    'supports_credentials': True,
}
```

### Environment Configuration

```bash
# .env
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
CORS_ALLOWED_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_SUPPORTS_CREDENTIALS=true
```

## Security Headers

### Content Security Policy

```bash
# .env - Strict CSP
CSP_HEADER=default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'

# Moderate CSP (allows HTTPS resources)
CSP_HEADER=default-src 'self' https:; script-src 'self' 'unsafe-inline' https:

# For development (more permissive)
CSP_HEADER=default-src 'self' 'unsafe-inline' 'unsafe-eval' data: https:
```

### Other Security Headers

```bash
# .env
X_FRAME_OPTIONS=SAMEORIGIN
X_CONTENT_TYPE_OPTIONS=nosniff
X_XSS_PROTECTION=1; mode=block
HSTS_HEADER=max-age=31536000; includeSubDomains; preload
REFERRER_POLICY=strict-origin-when-cross-origin
```

## Middleware Groups

The HTTP kernel defines these middleware groups:

### Global Middleware (all requests)
- Security headers
- Frame guard (clickjacking protection)  
- CORS handling
- Cookie encryption

### Web Middleware (form-based routes)
- CSRF protection

### API Middleware (API routes)
- Rate limiting

## Testing Security Features

### CSRF Testing

```python
def test_csrf_protection():
    # Without token - should fail
    response = client.post('/form', data={'name': 'test'})
    assert response.status_code == 419
    
    # With valid token - should succeed
    with client.session_transaction() as sess:
        token = generate_csrf_token()
        sess['_csrf_token'] = token
    
    response = client.post('/form', data={
        'name': 'test',
        '_token': token
    })
    assert response.status_code == 200
```

### Rate Limiting Testing

```python
def test_rate_limiting():
    # Make requests up to limit
    for i in range(60):
        response = client.get('/api/data')
        assert response.status_code == 200
    
    # Next request should be throttled
    response = client.get('/api/data')
    assert response.status_code == 429
    assert 'Retry-After' in response.headers
```

## Best Practices

### 1. Environment Security
- Never commit .env files to version control
- Use strong, unique APP_KEY values
- Rotate encryption keys periodically
- Use HTTPS in production

### 2. CSRF Protection
- Always include CSRF tokens in forms
- Use the meta tag for AJAX requests
- Be selective with excluded routes
- Validate origin for state-changing requests

### 3. Rate Limiting
- Different limits for different endpoints
- Stricter limits for authentication endpoints
- Monitor rate limit violations
- Consider user reputation

### 4. Authentication
- Hash passwords with strong algorithms
- Implement proper session management
- Use secure session cookies
- Implement account lockout policies

### 5. Headers and CORS
- Be specific with CORS origins in production
- Implement proper CSP policies
- Enable HSTS for HTTPS sites
- Regular security header audits

## Production Checklist

- [ ] Strong APP_KEY set in environment
- [ ] CSRF protection enabled for all forms
- [ ] Rate limiting configured appropriately
- [ ] CORS origins restricted to known domains  
- [ ] Security headers properly configured
- [ ] Cookies encrypted for sensitive data
- [ ] HTTPS enforced with HSTS
- [ ] Content Security Policy implemented
- [ ] Error pages don't leak sensitive information
- [ ] Security middleware applied to all routes

## Troubleshooting

### CSRF Token Mismatch
- Check that forms include `{{ csrf() }}`
- Verify AJAX requests send X-CSRF-TOKEN header
- Ensure session cookies are working
- Check if route is excluded from CSRF

### Rate Limiting Issues
- Check rate limit configuration
- Verify client IP detection is working
- Consider if behind a proxy/load balancer
- Review rate limit logs

### CORS Errors
- Verify origin is in allowed_origins
- Check preflight request handling
- Ensure headers/methods are allowed
- Validate credentials configuration

### Authentication Problems
- Check session configuration
- Verify user loading logic
- Test authentication guards
- Review password hashing

For more detailed information, see the Laravel documentation as the APIs are compatible.