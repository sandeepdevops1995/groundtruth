# Run a server.
from app import app
import config

if __name__ == '__main__':
    app.run(host=config.IP_ADDRESS,port=config.PORT, debug=config.DEBUG)
