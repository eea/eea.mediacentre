""" Plonevideo fileutils
"""
import os
from zope.publisher.http import HTTPRequest
import tempfile


def write_ofsfile_to_tempfile(obj, preferred_name=None):
    """Assumes the file obj is of type OFS.Image.File and will write
    it to a temporary file returning the filename of the temp file.  Uses
    the possibly acquired index_html method to fetch the file.  This
    is a little more compatible with objects that seem like OFS.Image.File
    instances.
    """

    filename = preferred_name
    if filename is None:
        filename = obj.id
        if callable(filename):
            filename = filename()
    fd, filename = tempfile.mkstemp('_'+filename)
    os.close(fd)
    fout = open(filename, 'wb')

    class TempResponse(object):
        """ TempResponse
        """
        def getHeader(self, n):
            """ getHeader
            """
            pass
        def setHeader(self, n, v):
            """ setHeader
            """
            pass
        def setBase(self, v):
            """ setBase
            """
            pass
        def write(self, d):
            """ write
            """
            fout.write(d)

    class TempRequest(HTTPRequest):
        """ TempRequest
        """
        def get_header(self, n, default=None):
            """ get_header
            """
            if default is not None:
                return default
            return ''

    temp_res = TempResponse()
    req = TempRequest(obj, {}, temp_res)
    res = obj.index_html(req, temp_res)
    if res:
        if isinstance(res, str):
            fout.write(res)
        else:
            # assumes some sort of iterator
            for x in res:
                fout.write(x)

    fout.close()

    return filename
