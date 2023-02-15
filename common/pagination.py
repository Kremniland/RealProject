from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasePagination(PageNumberPagination):
    page_size_query_param = 'page_size' # по какому параметру будет запрос с фронта
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(), # ссылка на след стр
            'previous': self.get_previous_link(), # ссылка на предидущую страницу
            'count': self.page.paginator.count, # кол-во объектов на странице
            'pages': self.page.paginator.num_pages, # кол-во страниц
            'results': data, # данные которые у нас есть
        })