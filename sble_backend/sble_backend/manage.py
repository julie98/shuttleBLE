import os

from gevent import monkey
# monkey.patch_all()

from app import create_app
from gevent.pywsgi import WSGIServer

app = create_app("development")  # 'development' or 'production'

# method 1
print("Starting WSGIServer...")
port = os.getenv('PORT', '5000')
http_server = WSGIServer(("0.0.0.0", int(port)), app)
http_server.serve_forever()

# method 2
# port = os.getenv('PORT', '5000')
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=int(port), threaded=True)
