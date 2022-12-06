import logging
from typing import Dict, List, Tuple, Union

from aiohttp import web

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def change_room(
    app: web.Application, new_room: str, old_room: str, nick: str
) -> Tuple[Dict[str, Union[str, bool]], bool]:
    """
    Получает пользователя и меняет его активный чат
    """
    # TODO переписать через БД или редис
    if not isinstance(new_room, str) or not 3 <= len(new_room) <= 20:
        return (
            {'action': 'join_room', 'success': False, 'message': 'Room name must be a string and between 3-20 chars.'},
            False,
        )
    if nick in app['websockets'][new_room].keys():
        return (
            {'action': 'join_room', 'success': False, 'message': 'Name already in use in this room.'},
            False,
        )
    app['websockets'][new_room][nick] = app['websockets'][old_room].pop(nick)
    return {'action': 'join_room', 'success': True, 'message': ''}, True


async def retrieve_messages(app: web.Application, room: str) -> Dict[str, Union[str, bool, List[str]]]:
    """
    Получает 30 последних соообщений
    """
    # TODO получить 30 последних сообщений

    return {'action': 'messages_list', 'success': True, 'room': room, 'users': list(app['websockets'][room].keys())}


async def broadcast(app: web.Application, room: str, message: dict, ignore_user: str = None) -> None:
    """
    Отправляет сообшение каждому пользователю в чате
    """
    # TODO переписать через редис
    # TODO сделать загрузку в БД отправленных любых сообщений
    for user, ws in app['websockets'][room].items():
            logger.info('> Sending message %s to %s', message, user)
            await ws.send_json(message)