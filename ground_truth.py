# Run a server.
from app import app
if __name__ == '__main__':
    
    app.run(host=config.IP_ADDRESS,port=config.PORT, debug=config.DEBUG)
