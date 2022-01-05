# encoding: utf-8
from app import app
from gevent import pywsgi

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 40000), app)
    server.serve_forever()
