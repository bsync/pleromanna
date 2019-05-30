import os
import vimeo
import youtube_dl
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from django.views import View
from django.conf.urls import url
from django.shortcuts import render
from django.http import HttpResponse
from . import secrets

# Set the Referer in the header to allow download via youtube_dl
# This is necessary for mp4 audio only conversion of video files
youtube_dl.utils.std_headers['Referer'] = "https://dev.pleromabiblechurch.org"

class VimeoObject(object):
    cache = {}
    client = vimeo.VimeoClient(
                    token=secrets.VIMEO_TOKEN,
                    key=secrets.VIMEO_CLIENT_ID,
                    secret=secrets.VIMEO_SECRET)

    def __init__(self, vimeoInfo, **kwargs):
        self.title = vimeoInfo['name']
        self.url = vimeoInfo['uri']
        self.vim_id = self.url.rpartition('/')[2]
        self._parseInfo(vimeoInfo, **kwargs)
        VimeoObject.cache[self.vim_id] = self

    @classmethod
    def fetch(cls, aurl, some_params=None):
        return cls.client.get(aurl, params=some_params).json()


class Audio(VimeoObject):
    def _parseInfo(self, audioInfo, **kwargs):
        ydl_opts = { 'format': 'bestaudio/best',
                     'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192', }],
                     'progress_hooks': [lambda : print("done")], }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            x = ydl.download(['https://vimeo' + audioInfo['uri']])
            # TODO: save the converted file on s3?

class Video(VimeoObject):

    def _parseInfo(self, vidInfo, album=None, **kwargs):
        self.vidInfo = vidInfo
        self.album = album
        self.title = vidInfo['name']
        embedHtml = vidInfo['embed']['html']
        lvh = BeautifulSoup(embedHtml, "lxml")
        del lvh.iframe['width']
        del lvh.iframe['height']
        self.embedHtml = str(lvh.iframe)

    @property
    def album_name(self):
        if getattr(self, 'album', False):
            return self.album.name
        return None

    @staticmethod
    def latest(count=10):
        lvs = []
        for alb in Album.albums():
            for vid in alb.videos:
                lvs.append(vid)
                if len(lvs) == count:
                    return lvs
        return lvs


class Album(VimeoObject):
        
    def _parseInfo(self, albInfo, **kwargs):
        self.albInfo = albInfo
        self.embed_html = albInfo['embed']['html']

    @staticmethod
    def albums():
        valbs = Album.fetch('/me/albums',
                            some_params={'fields': "uri,name,embed",
                                         'sort': "date",
                                         'direction': "desc"})
        paging = valbs['paging']
        albs = [Album(x) for x in valbs['data']]
        while(paging['next']):
            valbs = Album.fetch(paging['next'])
            albs.append([Album(x) for x in valbs['data']])
            paging = valbs['paging']
        return albs

    @property
    def videos(self):
        lv = self.fetch('/me/albums/{}/videos'.format(self.vim_id),
                        some_params={'fields': "uri,name,embed",
                                     'sort': "date",
                                     'direction': "desc"})
        vids = []
        for x in lv['data']:
            vid = Video(x, album=self)
            vids.append(vid)

        return vids

    @property
    def name(self):
        return self.albInfo['name']


class VimeoView(View):

    def get(self, request, video_id):
        vid = VimeoObject.cache[video_id]
        return render(request, "pleromanna/vimeo_vid.html", {'vid': vid})

urlpatterns = [url(r'^(\d+)/$', VimeoView.as_view(), name="vimeo")]
