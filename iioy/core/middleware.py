class ZumhMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Humans'] = 'Built by Elijah Wilson'
        response['X-ZUMH'] = 'https://github.com/tizz98'
        return response
