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

    @classmethod
    def fetch(cls, aurl, some_params=None):
        return cls.client.get(aurl, params=some_params).json()

    def __init__(self, vimeoInfo):
        self.vimeoInfo = vimeoInfo
        VimeoObject.cache[self.vim_id] = self

    @property
    def vim_id(self):
        return self.url.rpartition('/')[2]

    @property
    def name(self):
        return self.vimeoInfo['name']

    @property
    def url(self):
        return '/vimeo' + self.vimeoInfo['uri']

    @property
    def embed_html(self):
        ehtml = self.vimeoInfo['embed']['html']
        lvh = BeautifulSoup(ehtml, "lxml")
        del lvh.iframe['style']
        lvh.iframe['width']="100%"
        lvh.iframe['height']="500px"
        return str(lvh.iframe)


class Audio(VimeoObject):

    @property
    def vim_id(self):
        return super(Audio, self).vim_id + "_audio"

    @property
    def url(self):
        return '/vimeo' + self.vimeoInfo['uri'].replace('videos','audio')

    @property
    def vimeo_url(self):
        return 'https://vimeo.com/' + super(Audio, self).vim_id

    def serve(self):
        ydl_opts = { 'format': 'bestaudio/best',
                     'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192', }],
                     'progress_hooks': [lambda : print("done")], }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            x = ydl.download([self.vimeo_url])
        # TODO: save the converted file on s3?

class Video(VimeoObject):

    def __init__(self, vimeoInfo, album=None):
        super(Video, self).__init__(vimeoInfo)
        self.album = album

    @property
    def album_name(self):
        try:
            return self.album.name
        except:
            return None

        
    @property
    def audio(self):
        return Audio(self.vimeoInfo)

    @staticmethod
    def latest(count=10):
        lvs = []
        try:
            for alb in Album.albums():
                for vid in alb.videos:
                    lvs.append(vid)
                    if len(lvs) == count:
                        return lvs
        except: 
            # Need to think about this...
            # What to do when Vimeo is down...
            # don't want it to take our site down with it...
            pass

        return lvs


class Album(VimeoObject):
        
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
            albs.extend([Album(x) for x in valbs['data']])
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


class VideoView(View):

    def get(self, request, video_id):
        vid = VimeoObject.cache[video_id]
        return render(request, "pleromanna/vimeo_vid.html", {'vid': vid})


class AudioView(View):

    def get(self, request, video_id):
        vid = VimeoObject.cache[video_id]
        return vid.audio.serve()

urlpatterns = [url(r'^videos/(\d+)/$', VideoView.as_view(), name="vimeo"),
               url(r'^audio/(\d+)/$', AudioView.as_view(), name="audio")]
