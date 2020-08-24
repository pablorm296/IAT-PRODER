import cherrypy

from .main import create_app

if __name__ == '__main__':
    # Create app
    app = create_app()

    # Mount application
    cherrypy.tree.graft(app, "/")

    #Unsubscribe the default server
    cherrypy.server.unsubscribe()

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    # Configure the server object
    server.socket_host = "0.0.0.0"
    server.socket_port = 5000
    server.thread_pool = 30

    # Subscribe this server
    server.subscribe()

    server2 = cherrypy._cpserver.Server()

    server2.socket_host = "0.0.0.0"
    server2.socket_port = 5001
    server2.thread_pool = 30
    server2.subscribe()

    # Start the server engine (Option 1 *and* 2)
    cherrypy.engine.start()
    cherrypy.engine.block()