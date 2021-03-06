import os, subprocess
import vimeo
import urllib
import pleromanna.settings.dev as settings
from bs4 import BeautifulSoup
from django.conf.urls import url
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.utils.encoding import smart_str
from django.core.files.storage import default_storage
from ffmpy import FFmpeg
from concurrent.futures import ThreadPoolExecutor
from . import secrets

class VimeoClientClient(vimeo.VimeoClient):
    _albums = []
    _videos = {}
    _audios = {}

    def fetch(self, aurl, fparams=None):
        return self.get(aurl, params=fparams).json()

    @property
    def albums(self):
        if len(self._albums) == 0:
            albinfo = self.fetch('/me/albums',
                                 fparams={'fields': "uri,name,embed",
                                          'sort': "date",
                                          'direction': "desc"})
            while ('data' in albinfo):
                for album_data in albinfo['data']:
                    self._albums.append(Album(album_data))
                    nextpage = albinfo.get('paging', {}).get('next', False)
                if nextpage:
                    albinfo = self.fetch(nextpage)
                else:
                    albinfo = {}

        return self._albums

    def latest_videos(self, count=10):
        lvs = []
        try:
            for alb in self.albums:
                for vid in alb.videos:
                    lvs.append(vid)
                    self._videos[vid.id] = vid
                    if len(lvs) == count:
                        return lvs
        except Exception as e: 
            # Need to think about this...
            # What to do when Vimeo is down...
            # don't want it to take our site down with it...
            self._albums=[] #Trigger future reload of albums from vimeo.com
            print("Trouble loading ablums... {}".format(e))

        return lvs

    def albumFor(self, album_id):
        albumsById = { a.id:a for a in self._albums }
        if album_id in albumsById:
            alb = albumsById[album_id]
        else:
            alb_data = self.fetch("/me/albums/{}".format(album_id))
            alb = Album(alb_data)
            self._albums.append(alb)
        return alb

    def videoFor(self, video_id):
        if video_id not in self._videos:
            vid_data = self.fetch("/me/videos/{}".format(video_id))
            vid = self.cacheVideo(vid_data)
        return self._videos[video_id]

    def audioFor(self, audio_id):
        if audio_id not in self._audios:
            vid = self.videoFor(audio_id)
            self._audios[audio_id] = Audio(vid.info, album=vid.album)
        return self._audios[audio_id]


    def cacheVideo(self, vid_data, album=None, **kwargs):
        if album is None:
            vidid = client.parse_id(vid_data)
            alb_info = self.fetch("/videos/{}/albums".format(vidid))
            album = self.albumFor(client.parse_id(alb_info['data'][0]))
        vid = Video(vid_data, album=album, **kwargs)
        self._videos[vid.id] = vid
        return vid

    def parse_id(self, info):
        return int(info['uri'].rpartition('/')[2])


client = VimeoClientClient(token=secrets.VIMEO_TOKEN,
                           key=secrets.VIMEO_CLIENT_ID,
                           secret=secrets.VIMEO_SECRET)


class VimeoObject(object):
    def __init__(self, vim_info, **kwargs):
        self.info = vim_info
        self.extra = kwargs

    @property
    def name(self):
        return self.info['name']

    @property
    def url(self):
        return self.info['uri']

    @property
    def file_url(self):
        return self.info['files'][0]['link']

    @property
    def id(self):
        return client.parse_id(self.info)
    
    @property
    def embed_html(self):
        ehtml = self.info['embed']['html']
        lvh = BeautifulSoup(ehtml, "lxml")
        del lvh.iframe['style']
        lvh.iframe['width']="100%"
        lvh.iframe['height']="500px"
        return str(lvh.iframe)

    def __getattr__(self, key):
        return self.extra[key]


class Album(VimeoObject):
        
    @property
    def videos(self):
        lv = client.fetch('/me/albums/{}/videos'.format(self.id),
                          fparams={'fields': "uri,name,embed,files",
                                   'sort': "date",
                                   'direction': "desc"})
        vids = []
        for videoInfo in lv['data']:
            vids.append(client.cacheVideo(videoInfo, album=self))

        return vids


class Video(VimeoObject):

    @property
    def audio(self):
        return client.audioFor(self.id)

def human_size(bytes, units=[' bytes','KB','MB','GB','TB', 'PB', 'EB']):
    """ Returns a human readable string representation of bytes"""
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes>>10, units[1:])

class Audio(VimeoObject):
    audio_gen_threads = {}

    @property
    def gen_status(self):
        try:
            if self.is_generating:
                X, fsize = self.audio_gen_threads[self.id]
            else:
                return HttpResponse(self.url)
        except Exception as e: 
            fsize = 0;
        return HttpResponse("{}".format(human_size(fsize)))

    @property
    def url(self):
        if self.exists:
            return default_storage.url(self.audio_path)
        else:
            curl = super().url.replace('videos','genaudio') 
            return urllib.parse.quote(curl)

    @property
    def size(self):
        try:
            return human_size(default_storage.size(self.audio_path))
        except Exception:
            return 0

    @property
    def is_generating(self):
        return self.id in self.audio_gen_threads

    @property
    def exists(self):
        return not self.is_generating and default_storage.exists(self.audio_path)

    @property
    def audio_path(self):
        return "{}/{}/{}.mp3".format('audio', self.album.name, self.name)

    def generate(self):
        if self.id not in self.audio_gen_threads:
            X = ThreadPoolExecutor()
            X = X.submit(self._writeAudioToS3)
            self.audio_gen_threads[self.id] = (X, 0)
            def gen_audio_complete(x):
                del self.audio_gen_threads[self.id]
            X.add_done_callback(gen_audio_complete)
        else:
            pass #Audio generation for this file is already processing

    def _writeAudioToS3(self):
        ff = FFmpeg(inputs={"'{}'".format(self.file_url): None},
                    outputs={'pipe:1': '-f mp3 -ab 128000 -vn'})
        ffmpg = subprocess.Popen(ff.cmd, shell=True, stdout=subprocess.PIPE) 
        with default_storage.open(self.audio_path, 'wb') as out:
            bnew = out.write(ffmpg.stdout.read(5000))
            while (bnew):
                X, bold = self.audio_gen_threads[self.id]
                self.audio_gen_threads[self.id] = (X, bold + bnew)
                bnew = out.write(ffmpg.stdout.read(15000))

class VimeoView(View):

    def get(self, request, *args, **kwargs):
        self.vid = client.videoFor(kwargs['vimeo_id'])
        audio = self.vid.audio

        if "genaudio" in request.path: 
            audio.generate()

        if "audio_gen_status" in request.path:
            return audio.gen_status

        return render(request, 
                      "pleromanna/vimeo_vid.html", 
                      {'video':self.vid, 'audio': audio})

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['video'] = self.vid
        context['audio'] = self.vid.audio
        return context
