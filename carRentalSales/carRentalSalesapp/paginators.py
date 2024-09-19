from rest_framework.pagination import PageNumberPagination


class CarPaginator(PageNumberPagination):
    page_size = 15


class SearchCarPaginator(PageNumberPagination):
    page_size = 15


class FavouriteCarPaginator(PageNumberPagination):
    page_size = 15
