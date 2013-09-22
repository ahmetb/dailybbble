from dailybbble import app
import os

if __name__ == '__main__':
    port = int(os.environ['PORT']) if 'PORT' in os.environ else None
    debug = True if not port else False
    app.run(host='0.0.0.0', port=port, debug=debug)
