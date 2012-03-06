""" Video playlists
"""
from Products.Five import BrowserView
import urllib2
import json


class VideoPlaylist(BrowserView):
    """ BrowserView which returns youtube playlists
    """

    def playlist(self, playlist_id = None):
        """ return video title, id and description as well
        as playlist title
        """
        items = []

        if playlist_id and type(playlist_id) != list:
            url = 'http://gdata.youtube.com/feeds/api/playlists/' \
                    + playlist_id + '?v=2&alt=jsonc&orderby=position'
            link = urllib2.urlopen(url)
            playlist = json.load(link)
            playlist = playlist['data']
            playlist_title = playlist['title'] + ' (' \
                                + str(playlist['totalItems']) + ')'
            playlist_list = []
            playlist_list.append(playlist_title)
            vids = playlist['items']
            vid_id = []
            vid_title = []
            vid_desc = []
            for i in vids:
                vid = i['video']
                vid_id.append(vid['id'])
                vid_title.append(vid['title'])
                vid_desc.append(vid['description'])
            playlist_list.append(vid_id)
            playlist_list.append(vid_title)
            playlist_list.append(vid_desc)
            items.append(playlist_list)

        if playlist_id and type(playlist_id) == list:
            for obj in playlist_id:
                url = 'http://gdata.youtube.com/feeds/api/playlists/' \
                        + obj + '?v=2&alt=jsonc&orderby=position'
                link = urllib2.urlopen(url)
                playlist = json.load(link)
                playlist = playlist['data']
                playlist_title = playlist['title'] + ' (' \
                                    + str(playlist['totalItems']) + ')'
                playlist_list = []
                playlist_list.append(playlist_title)
                vids = playlist['items']
                vid_id = []
                vid_title = []
                vid_desc = []
                for i in vids:
                    vid = i['video']
                    vid_id.append(vid['id'])
                    vid_title.append(vid['title'])
                    vid_desc.append(vid['description'])
                playlist_list.append(vid_id)
                playlist_list.append(vid_title)
                playlist_list.append(vid_desc)
                items.append(playlist_list)

        return items
