import vimeo
import local


class VimeoCollection(object):

    def __init__(self):
        self.client = vimeo.VimeoClient(
                        token=local.VIMEO_TOKEN,
                        key=local.VIMEO_CLIENT_ID,
                        secret=local.VIMEO_SECRET)

    def listAlbumChoices(self):
        albums = self.client.get('/me/albums', params={'fields': "uri,name,"})
        alb_json = albums.json()
        alb_paging = alb_json['paging']
        alb_info = alb_json['data']
        while(alb_paging['next']):
            albums = self.client.get(alb_paging['next'])
            alb_paging = alb_json['paging']
            alb_info.append(alb_json['data'])
        return [(x.values()) for x in alb_info]

    def album_embed_html_for(self, album_uri):
        alb_info = self.client.get(album_uri, params={'fields': 'embed.html'})
        alb_info = alb_info.json()
        return alb_info['embed']['html']

    def album_name_for(self, album_uri):
        alb_info = self.client.get(album_uri, params={'fields': 'name'})
        alb_info = alb_info.json()
        return alb_info['name']

    @property
    def latestVideos(self):
        lv = self.client.get('/me/videos', params={'sort':"date",
                                                   'direction':"desc",
                                                   'sizes':"100x75",
                                                   'page':"1",
                                                   'per_page':"10"})
        lv = lv.json()
        lve = [x['embed']['html'] for x in lv['data']]
        return lve


vc = VimeoCollection()
