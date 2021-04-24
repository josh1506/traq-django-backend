import random
import string
from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Url, Viewer
from .serializer import UrlSerializer, ViewerSerializer


def handle_sort_viewer(viewer_list):
    viewer_list = [viewer for viewer in viewer_list]
    viewer_list.sort(reverse=True)
    new_viewer_list = [{
        'date_viewed': viewer_detail.date_viewed.strftime('%B %d,%Y - %I:%M:%S')
    } for viewer_detail in viewer_list]

    return new_viewer_list


def handle_viewer_chart(url_list):
    viewer_day_list = []
    viewer_month_list = []
    viewer_year_list = []

    view_all_list = [Viewer.objects.filter(url=url) for url in url_list]
    print(view_all_list)
    for viewer_list in view_all_list:
        for viewer in viewer_list:
            date = viewer.date_viewed.strftime('%B %d,%Y')

            if len(viewer_day_list) <= 0:
                viewer_day_list.append({'name': date})

            if not len(viewer_day_list) <= 0:
                index = next((index for index, data in enumerate(
                    viewer_day_list) if data['name'] == date), None)

                if index is not None:
                    if viewer.url.title in viewer_day_list[index]:
                        viewer_day_list[index][viewer.url.title] += 1

                    else:
                        viewer_day_list[index][viewer.url.title] = 1

                else:
                    viewer_day_list.append({'name': date})

        for viewer in viewer_list:
            date = viewer.date_viewed.strftime('%B %Y')

            if len(viewer_month_list) <= 0:
                viewer_month_list.append({'name': date})

            if not len(viewer_month_list) <= 0:
                index = next((index for index, data in enumerate(
                    viewer_month_list) if data['name'] == date), None)

                if index is not None:
                    if viewer.url.title in viewer_month_list[index]:
                        viewer_month_list[index][viewer.url.title] += 1

                    else:
                        viewer_month_list[index][viewer.url.title] = 1

                else:
                    viewer_month_list.append({'name': date})

        for viewer in viewer_list:
            date = viewer.date_viewed.strftime('%Y')

            if len(viewer_year_list) <= 0:
                viewer_year_list.append({'name': date})

            if not len(viewer_year_list) <= 0:
                index = next((index for index, data in enumerate(
                    viewer_year_list) if data['name'] == date), None)

                if index is not None:
                    if viewer.url.title in viewer_year_list[index]:
                        viewer_year_list[index][viewer.url.title] += 1

                    else:
                        viewer_year_list[index][viewer.url.title] = 1

                else:
                    viewer_year_list.append({'name': date})

    data = {
        'date': viewer_day_list,
        'month': viewer_month_list,
        'year': viewer_year_list
    }

    return data


# Create your views here.
class UrlView(generics.GenericAPIView):
    serializer_class = UrlSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        user = User.objects.get(username=request.user)
        url_list = user.url.all()

        data = [{
            'id': url.id,
            'title': url.title,
            'link': url.link,
            'short_url': url.short_url,
            'total_visitors': url.total_visitors(),
        } for url in url_list]

        graph_list = handle_viewer_chart(url_list)

        return Response({'data': data, 'graph_list': graph_list}, status=status.HTTP_200_OK)

    def post(self, request):
        def gen_unique_string(unique_string=''):
            user = Url.objects.filter(short_url=unique_string).exists()

            if not user and unique_string != '':
                return unique_string

            else:
                alphanumeric_list = string.ascii_letters + string.digits
                unique_string = ''.join(random.choice(alphanumeric_list)
                                        for num in range(5))
                return gen_unique_string(unique_string)

        short_url = gen_unique_string()
        request.data['user'] = request.user.pk
        request.data['short_url'] = short_url
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        link = Url.objects.filter(link=request.data['link'])

        if link.exists():
            data = {
                'title': link[0].title,
                'link': link[0].link,
                'short_url': link[0].short_url
            }

            return Response({'data': data, 'error': 'Link already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(username=request.user)

        if len(user.url.all()) >= 10:
            return Response({'error': 'Test user can only track 10 urls'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)


class UrlDetailView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request, pk):
        url_data = Url.objects.filter(id=pk, user=request.user)

        if not url_data.exists():
            return Response({'error': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'id': url_data[0].id,
            'title': url_data[0].title,
            'link': url_data[0].link,
            'short_url': url_data[0].short_url,
            'total_visitors': url_data[0].total_visitors(),
            'viewer_list': handle_sort_viewer(Viewer.objects.filter(url=url_data[0])),
            'graph_list': handle_viewer_chart(url_data)
        }

        return Response({'data': data}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        url_data = Url.objects.filter(id=pk, user=request.user)

        if not url_data.exists():
            return Response({'error': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)

        url_data[0].delete()

        return Response('Url deleted', status=status.HTTP_200_OK)


class ViewerView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, short_url):
        url = Url.objects.filter(short_url=short_url)

        if not url.exists():
            return Response({'error': 'URL does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        Viewer.objects.create(url=url[0])

        return Response({'data': url[0].link}, status=status.HTTP_200_OK)
