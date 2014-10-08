#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#

import os
import sys
import tornado.ioloop
import tornado.web
from adminutils import inner_do_generate, do_check, do_complete

from tornado.util import bytes_type, unicode_type
from tornado import escape


LISTENER_PORT = 8888
CUSTOMFILES_DIR = 'structure'
files = [ 'description' , 'name', 'step1', 'step2', 'step3', 'link_url', 'link']

class AcceptSupporter(tornado.web.RequestHandler):

    PAGE = None

    @classmethod
    def compute_page(cls):
        # TODO grow-up and use JSON
        with file(os.path.join(CUSTOMFILES_DIR, 'skeleton.html'), 'r') as f:
            index = f.read()
            for f in files:
                fc = file(os.path.join(CUSTOMFILES_DIR, f), 'r').read()

                keyword = "%%%s%%" % f.upper()
                index = index.replace(keyword, fc)

        AcceptSupporter.PAGE = index


    def get(self, *ua, **kwa):

        self.write(AcceptSupporter.PAGE)
        self.finish()

class URLGen(tornado.web.RequestHandler):

    def get(self, *ua, **ka):

        url, random_name = inner_do_generate(sys.argv[1])
        self._headers['Content-type'] = 'application/json'
        self.write({
            'url' : url,
            'random_name' : random_name
        })
        self.finish()

class Complete(tornado.web.RequestHandler):

    def get(self, *ua, **ka):
        print ua
        print ka

        do_complete(sys.argv[1], 1234, "bbb")
        self.finish()

class CSSJS(tornado.web.RequestHandler):
    """
    beware: vulnerability ahead
    """

    def get(self, *a, **kw):

        fil = self.request.uri
        if fil.startswith('.') or fil.startswith('//'):
            self.set_status(500)
        else:
            x = os.path.join(CUSTOMFILES_DIR, fil[1:])
            if x.endswith('.js'):
                self._headers['Content-type'] = 'text/javascript'
            elif x.endswith('.css'):
                self._headers['Content-type'] = 'text/css'
            else:
                pass

            c = file(x, 'r').read()
            print x, len(c)
            self.write(c)

        self.finish()


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print "%s <INITIATIVE NAME>" % sys.argv[0]
        quit(-1)

    print "Checking initiative", sys.argv[1]
    do_check(sys.argv[1])

    apiMap = [
        (r"/", AcceptSupporter),
        (r"/gimmeuniqueurl", URLGen),
        (r"/complete", Complete),
        (r"/bower_components/bootstrap/dist/css/bootstrap.min.css", CSSJS),
        (r"/bower_components/bootstrap/dist/js/bootstrap.min.js", CSSJS),
        (r"/bower_components/jquery/dist/jquery.js", CSSJS),
    ]

    assert os.path.isdir(CUSTOMFILES_DIR), "Expected '%s' " % CUSTOMFILES_DIR
    print "Checking files inside directory %s" % CUSTOMFILES_DIR
    for f in files:
        assert os.path.isfile(os.path.join(CUSTOMFILES_DIR, f)), "missing '%s' " % f

    AcceptSupporter.compute_page()
    try:
        application = tornado.web.Application(apiMap, debug=True)
        application.listen(LISTENER_PORT)
    except Exception as xxx:
        print "Unable to bind port %d: %s" % \
              (LISTENER_PORT, xxx)
        quit(-1)

    tornado.ioloop.IOLoop.instance().start()



