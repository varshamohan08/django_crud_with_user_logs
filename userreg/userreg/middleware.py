
from django.shortcuts import redirect
from django.contrib.auth import logout
from useractions.models import user_data

class userLogMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 'Email': 'varsha@g.com', 'Password': 'varsha'
        path = request.path_info.lstrip('/')
        if path in ['login','adminurls']:
            return self.get_response(request)
        else:
            if request.user and request.user.id:
                user_instance = user_data.objects.get(Email = request.user.email)
                shortened_urls = user_instance.shortened_urls
                if shortened_urls and path in shortened_urls.keys():
                    shortened_urls[path] = shortened_urls[path] + 1
                elif shortened_urls:
                    shortened_urls[path] = 1
                else:
                    shortened_urls = { path : 1 }
                user_instance.shortened_urls = shortened_urls
                user_instance.save()
                return self.get_response(request)
            else:
                return redirect('http://127.0.0.1:8000/login')
    # def __init__(self, request) -> None:
    #     self.request = request

    # def get(self, request):
    #     path = self.request.path_info.lstrip('/')
    #     if self.request.user.isauthenticated:
    #         user_instance = user_data.objects.get(email = self.request.user.email)
    #         shortened_urls = user_instance.shortened_urls
    #         shortened_urls[path] = shortened_urls[path] + 1 if path in shortened_urls.keys() else 1
    #         user_instance.shortened_urls = shortened_urls
    #         user_instance.save()
    #         return redirect(self.request.path_info)
    #     else:
    #         return redirect('http://127.0.0.1:8000/login')