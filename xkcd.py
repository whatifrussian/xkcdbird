# *- coding: utf-8 *-

import json
import os
import urllib2, urllib
import requests
fp = open("backup.json", "r")
backup = json.load(fp)
fp.close()

TEMPLATE = u"Title: {title} \n\
Slug: {num} \n\
Category: xkcd \n\
Date: {date} \n\
SourceNum: {num} \n\
SourceTitle: {sourcetitle} \n\
Image: /comics/{num:0>4}{ext} \n\
MicroImage: /comics/{num:0>4}_micro{uext} \n\
MiniImage: /comics/{num:0>4}_mini{mext} \n\
Description: {description} \n\
\n\
{transcription}\
"

try:    
    from cStringIO import StringIO
except ImportError, msg: 
    from StringIO import StringIO

class RangeError(IOError):
    """Error raised when an unsatisfiable range is requested."""
    pass
    

class HTTPRangeHandler(urllib2.BaseHandler):
    """Handler that enables HTTP Range headers.

    This was extremely simple. The Range header is a HTTP feature to
    begin with so all this class does is tell urllib2 that the 
    "206 Partial Content" reponse from the HTTP server is what we 
    expected.

    Example:
        import urllib2
        import byterange

        range_handler = range.HTTPRangeHandler()
        opener = urllib2.build_opener(range_handler)

        # install it
        urllib2.install_opener(opener)

        # create Request and set Range header
        req = urllib2.Request('http://www.python.org/')
        req.header['Range'] = 'bytes=30-50'
        f = urllib2.urlopen(req)
    """

    def http_error_206(self, req, fp, code, msg, hdrs):
        # 206 Partial Content Response
        r = urllib.addinfourl(fp, hdrs, req.get_full_url())
        r.code = code
        r.msg = msg
        return r

    def http_error_416(self, req, fp, code, msg, hdrs):
        # HTTP's Range Not Satisfiable error
        r = urllib.addinfourl(fp, hdrs, req.get_full_url())
        r.code = code
        r.msg = msg
        return r

def download_partial(url, target):
    range_handler = HTTPRangeHandler()
    opener = urllib2.build_opener(range_handler)
    urllib2.install_opener(opener)
    url_handle = urllib2.Request(url)

    if os.path.exists(target):
        file_handler = open(target, 'a', buffering=-1)
        size = os.path.getsize(target)
        url_handle.add_header("Range", "bytes={}-".format(size))
    else:
        file_handler = open(target, 'w', buffering=-1)
        size = 0

    target_url = urllib2.urlopen(url_handle)

    if int(target_url.headers['Content-Length']) == size:
        file_handler.writelines(target_url)
    
    file_handler.close()

    

if __name__ == "__main__":
    for comic in backup:
        c = comic["fields"]
        cid = c["cid"]
        published = c["published"]
        title = c["title"]
        text = c["text"]
        image = c["image"]
        thumb = c["thumbnail"]
        transcription = c["transcription"]
        if c["published"] != None:
            ext = str(os.path.splitext(image)[1])
            print u"wget -c http://xkcd.ru/{img} -O content/comics/{num:0>4}{ext}".format(img=image, num=cid, ext=ext)
            uext = str(os.path.splitext(thumb)[1])
            print u"wget -c  http://xkcd.ru/{img} -O content/comics/{num:0>4}_micro{ext}".format(img=thumb, num=cid, ext=uext)
            print u"Get xkcd.com/{}".format(cid)
            sourcetitle = requests.get("http://xkcd.com/{num}/info.0.json".format(num=cid)).json()["title"]
            print u"Written content/xkcd/{num:0>4}.md".format(num=cid)
            fp = open(u"content/xkcd/{num:0>4}.md".format(num=cid), "w")
            fp.write(TEMPLATE.format(title=title, num=cid, date=published, sourcetitle=sourcetitle, description=text, transcription=transcription, ext=ext, mext=ext, uext=uext).encode('utf-8'))
            fp.close()
