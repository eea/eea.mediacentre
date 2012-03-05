""" Video playlists
"""
from Products.Five import BrowserView
import urllib2
import json


class VideoPlaylist(BrowserView):
    """ Front page
    """
    #def __init__(self, context, request):
    #    BrowserView.__init__(self, context, request)

    def playlist(self, playlist_id = None):
        """ return video title id and description as well 
        as playlist title
        """
        #items = []
        if playlist_id:
        #for obj in playlist_id:
            url = 'http://gdata.youtube.com/feeds/api/playlists/' \
                    + playlist_id + '?v=2&alt=jsonc&orderby=position'
            link = urllib2.urlopen(url)
            playlist = json.load(link)
            playlist = playlist['data']
            #playlist_title = playlist['title']
            #playlist_list = []
            #playlist_list.append(playlist_title)
            #items.append(playlist_list)
            #items.append(playlist_title)
            vids = playlist['items']
            vid_id = []
            vid_title = []
            vid_desc = []
            for i in vids:
                vid = i['video']
                vid_id.append(vid['id'])
                vid_title.append(vid['title'])
                vid_desc.append(vid['description'])
            #items.append(vid_id)
            #items.append(vid_title)
            #items.append(vid_desc)
        return (vid_id, vid_title, vid_desc)
        #return items
