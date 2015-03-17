""" Video playlists
"""
from Products.Five import BrowserView
import urllib2
import json


class VideoPlaylist(BrowserView):
    """ BrowserView which returns youtube playlists
    """

    def playlist(self, *args):
        """ return video title, id and description as well
        as playlist title
        """
        # received the youtube playlist id's from portal_properties
        # which arrives as a tuple with one string item separated
        # by a comma
        if len(args) == 1:
            arg_list = args[0].split(',')
            arg_list = [i.strip() for i in arg_list]
            args = arg_list

        items = []

        for obj in args:
            if 'PL' in obj:
                obj = obj[2:]
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
