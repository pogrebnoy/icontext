import logging
import random

from aiohttp import web
from aiohttp.http_websocket import WSCloseCode, WSMessage
from aiohttp.web_request import Request

from .utils import broadcast, change_room, retrieve_messages

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_USER_ACTIONS = ['join_room', 'send_message', 'messages_list']


async def ws_chat(request: Request) -> web.WebSocketResponse:
    current_websocket = web.WebSocketResponse(autoping=True, heartbeat=60)
    ready = current_websocket.can_prepare(request=request)
    if not ready:
        await current_websocket.close(code=WSCloseCode.PROTOCOL_ERROR)
    await current_websocket.prepare(request)

    room = 'Default'
    # TODO переписать участок на взаимодействие через БД или редис
    user = f'User{random.randint(0, 999999)}'
    logger.info('%s connected to room %s', user, room)
    await current_websocket.send_json({'action': 'connecting', 'room': room, 'user': user})

    for ws in request.app['websockets'][room].values():
        await ws.send_json({'action': 'join', 'user': user, 'room': room})

    try:
        async for message in current_websocket:  # for each message in the websocket connection
            if isinstance(message, WSMessage):
                if message.type == web.WSMsgType.text:  # If it's a text, process it as a message

                    message_json = message.json()
                    action = message_json.get('action')

                    if action not in ALLOWED_USER_ACTIONS:
                        await current_websocket.send_json(
                            {'action': action, 'success': False, 'message': 'Not allowed.'}
                        )

                    elif action == 'join_room':
                        return_body, success = await change_room(
                            app=request.app, new_room=message_json.get('room'), old_room=room, nick=user
                        )
                        if not success:
                            logger.info(
                                '%s: Unable to change room for %s to %s, reason: %s',
                                room,
                                user,
                                message_json.get('room'),
                                return_body['message'],
                            )
                            await current_websocket.send_json(return_body)
                        else:
                            logger.info('%s: User %s joined the room', user, message_json.get('room'))
                            await broadcast(
                                app=request.app,
                                room=room,
                                message={'action': 'left', 'room': room, 'user': user, 'shame': False},
                            )
                            await broadcast(
                                app=request.app,
                                room=message_json.get('room'),
                                message={'action': 'joined', 'room': room, 'user': user},
                                ignore_user=user,
                            )
                            room = message_json.get('room')

                    elif action == 'messages_list':
                        logger.info('%s: %s requested user list', room, user)
                        user_list = await retrieve_messages(app=request.app, room=message_json['room'])
                        await current_websocket.send_json(user_list)

                    elif action == 'chat_message':
                        logger.info('%s: Message: %s', room, message_json.get('message'))
                        await current_websocket.send_json(
                            {'action': 'chat_message', 'success': True, 'message': message_json.get('message')}
                        )
                        await broadcast(
                            app=request.app,
                            room=room,
                            message={'action': 'chat_message', 'message': message_json.get('message'), 'user': user},
                            ignore_user=user,
                        )
    finally:
        request.app['websockets'][room].pop(user)
    if current_websocket.closed:
        await broadcast(
            app=request.app, room=room, message={'action': 'left', 'room': room, 'user': user, 'shame': False}
        )
    else:
        await broadcast(
            app=request.app, room=room, message={'action': 'left', 'room': room, 'user': user, 'shame': True}
        )
    return current_websocket
