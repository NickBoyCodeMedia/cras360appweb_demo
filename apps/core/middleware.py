class XFrameOptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        
        # Verificar se a URL é de um padrão que queremos permitir em iframes
        if '/paif/' in request.path:
            response['X-Frame-Options'] = 'SAMEORIGIN'
            
        return response
