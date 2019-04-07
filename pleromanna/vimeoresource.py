import os
import vimeo
import youtube_dl
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from django.views import View
from django.conf.urls import url
from django.shortcuts import render
import secrets

# Set the Referer in the header to allow download via youtube_dl
# This is necessary for mp4 audio only conversion of video files
youtube_dl.utils.std_headers['Referer'] = "https://dev.pleromabiblechurch.org"


class Audio(View):
    def __init__(self, audioInfo):
        ydl_opts = {'format': 'bestaudio[ext=mp3]', }
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            x = ydl.download([audioInfo])
            # TODO: save the converted file on s3?


class Video(View):
    def __init__(self, vidInfo):
        self.vidInfo = vidInfo

    @property
    def url(self):
        src = urlsplit(self.vidInfo['src'])._replace(query=None).geturl()
        return src

    def embedHtml(self):
        return self.vidInfo


class Album(View):
    def __init__(self, albInfo):
        import pdb; pdb.set_trace()
        self.albInfo = albInfo


class Collection(View):
    client = vimeo.VimeoClient(
                    token=secrets.VIMEO_TOKEN,
                    key=secrets.VIMEO_CLIENT_ID,
                    secret=secrets.VIMEO_SECRET)

    def get(self, request, *args, **kwargs):
        return render(request,
                      'pleromanna/lessons_page.html',
                      {"latest": self.latestVideos,
                       "albums": self.albums})

    def fetch(self, aurl, some_params=None):
        return self.client.get(aurl, params=some_params).json()

    @property
    def latestVideos(self):
        lv = self.fetch('/me/videos', some_params={'sort': "date",
                                              'direction': "desc",
                                              'page': "1",
                                              'per_page': "10"})
        lve = [x['embed']['html'] for x in lv['data']]
        lvp = []
        for eachLv in lve:
            lvh = BeautifulSoup(eachLv, "lxml")
            lvh.iframe['width'] = '640'
            lvh.iframe['height'] = '360'
            lvp.append(Video(lvh.iframe))
        return lvp

    @property
    def albums(self):
        valbs = self.fetch('/me/albums', some_params={'fields': "uri,name,"})
        paging = valbs['paging']
        albs = [Album(valbs['data'])]
        while(paging['next']):
            valbs = self.fetch(paging['next'])
            paging = valbs['paging']
            albs.append(Album(valbs['data']))
        return albs

    def album_embed_html_for(self, album_uri):
        alb_info = self.client.get(album_uri, params={'fields': 'embed.html'})
        alb_info = alb_info.json()
        return alb_info['embed']['html']

    def album_name_for(self, album_uri):
        alb_info = self.client.get(album_uri, params={'fields': 'name'})
        alb_info = alb_info.json()
        return alb_info['name']

urlpatterns = [
    url(r'', Collection.as_view(), name="vimeo"),
    url(r'(?P<album>\w+)', Collection.as_view(), name="vimeo_album")]
