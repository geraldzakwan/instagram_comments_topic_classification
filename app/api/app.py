import os
import json

from sanic import Sanic
from sanic import response

from dotenv import load_dotenv
load_dotenv()

from classifier import Classifier

app = Sanic(__name__, log_config={'version': 1, 'disable_existing_loggers': True})

@app.listener('before_server_start')
async def load_model(app, loop):
    app.cls = Classifier()

@app.route('/healthz', methods=['GET'])
async def healthz(_):
    return response.json({
        'status': 200,
        'data' : {
            'msg': 'OK'
        }
    })

@app.route('/get_info', methods=['GET'])
async def healthz(_):
    info = app.cls.get_info()

    return response.json({
        'status': 200,
        'data' : {
            'labels': info['labels']
        }
    })

@app.route('/get_class', methods=['POST'])
async def get_class(request):
    data = request.json
    if 'text' not in data:
        return response.json({
            'status': 400,
            'data' : {
                'err' : 'Missing "text" parameter'
            }
        })

    return response.json({
        'status': 200,
        'data' : {
            'text': data['text'],
            'label': app.cls.get_class(data['text'])
        }
    })

@app.route('/get_classes', methods=['POST'])
async def get_class(request):
    data = request.json
    if 'texts' not in data:
        return response.json({
            'status': 400,
            'data' : {
                'err' : 'Missing "texts" parameter'
            }
        })
    return response.json({
        'status': 200,
        'data' : {
            'texts': data['texts'],
            'labels': app.cls.get_classes(data['texts'])
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT')))
