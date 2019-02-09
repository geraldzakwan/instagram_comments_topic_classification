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

@app.route('/get_class', methods=['POST'])
async def get_class(request):
    data = request.json
    if 'id' not in data:
        return response.json({
            'status': 400,
            'data' : {
                'err' : 'Missing "id" parameter'
            }
        })
    if 'text' not in data:
        return response.json({
            'status': 400,
            'data' : {
                'err' : 'Missing "text" parameter'
            }
        })
    label = app.cls.get_class(data['text'])
    return response.json({
        'status': 200,
        'data' : {
            'id' : data['id'],
            'text': data['text'],
            'label': label
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT')))
