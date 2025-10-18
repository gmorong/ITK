import json
import aiohttp
from urllib.parse import parse_qs


async def application(scope, receive, send):
    if scope['type'] != 'http':
        return
    
    path = scope['path'].strip('/')
    
    if not path:
        await send({
            'type': 'http.response.start',
            'status': 400,
            'headers': [[b'content-type', b'application/json']],
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps({'error': 'Currency code required'}).encode(),
        })
        return
    
    currency = path.upper()
    
    try:
        async with aiohttp.ClientSession() as session:
            url = f'https://api.exchangerate-api.com/v4/latest/{currency}'
            async with session.get(url) as response:
                if response.status != 200:
                    await send({
                        'type': 'http.response.start',
                        'status': response.status,
                        'headers': [[b'content-type', b'application/json']],
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': json.dumps({'error': 'Invalid currency code'}).encode(),
                    })
                    return
                
                data = await response.json()
                
                await send({
                    'type': 'http.response.start',
                    'status': 200,
                    'headers': [[b'content-type', b'application/json']],
                })
                await send({
                    'type': 'http.response.body',
                    'body': json.dumps(data).encode(),
                })
    
    except Exception as e:
        await send({
            'type': 'http.response.start',
            'status': 500,
            'headers': [[b'content-type', b'application/json']],
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps({'error': str(e)}).encode(),
        })
        
# Запуск: uv run uvicorn m_6.asgi:application --host 0.0.0.0 --port 8000 (или без "m_6", но нужно cd в папку)
# Проверка: curl http://localhost:8000/USD и т.д.
