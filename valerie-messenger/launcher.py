import tornado
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from server import app

print "Running at 0.0.0.0:9999"

sockets = tornado.netutil.bind_sockets(port=9999, backlog=256)
tornado.process.fork_processes(0)
server = HTTPServer(WSGIContainer(app))
server.add_sockets(sockets)
IOLoop.instance().start()