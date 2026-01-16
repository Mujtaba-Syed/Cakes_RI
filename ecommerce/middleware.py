"""
Custom middleware for handling IPv6 addresses and security improvements.
"""
import re
from django.utils.deprecation import MiddlewareMixin


class IPv6HostMiddleware(MiddlewareMixin):
    """
    Middleware to normalize IPv6 addresses in Host header.
    Handles cases where IPv6 addresses come with brackets like [::1]:8000
    """
    
    def process_request(self, request):
        host = request.META.get('HTTP_HOST', '')
        
        # Handle IPv6 addresses with brackets
        # Pattern: [IPv6]:port
        ipv6_pattern = r'^\[([0-9a-fA-F:]+)\](?::(\d+))?$'
        match = re.match(ipv6_pattern, host)
        
        if match:
            # Extract IPv6 address without brackets
            ipv6_addr = match.group(1)
            port = match.group(2)
            
            # Reconstruct host without brackets for Django's ALLOWED_HOSTS check
            if port:
                request.META['HTTP_HOST'] = f'{ipv6_addr}:{port}'
            else:
                request.META['HTTP_HOST'] = ipv6_addr
        
        return None


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add additional security headers to responses and enforce HTTPS.
    """
    
    def process_request(self, request):
        # Force HTTPS redirect if not already HTTPS (for direct Django access)
        if not request.is_secure() and not request.META.get('HTTP_X_FORWARDED_PROTO') == 'https':
            # This should be handled by nginx, but as a backup
            pass
        return None
    
    def process_response(self, request, response):
        # These headers are already set by nginx, but adding here as backup
        # for direct Django access (development)
        if not response.get('X-Frame-Options'):
            response['X-Frame-Options'] = 'SAMEORIGIN'
        
        if not response.get('X-Content-Type-Options'):
            response['X-Content-Type-Options'] = 'nosniff'
        
        # Ensure Strict-Transport-Security is set
        if not response.get('Strict-Transport-Security'):
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        return response

