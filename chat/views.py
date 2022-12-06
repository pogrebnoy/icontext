import json

from aiohttp import web
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import sync_to_async

from icontext import views

routes = web.RouteTableDef()


class ChatsAbstractView(views.ModelMixin):
    model = 'chat.Chat'


@routes.view('/chats')
class ChatsListView(ChatsAbstractView, web.View):

    async def get(self):
        queryset = await self.get_queryset()
        text = await sync_to_async(serialize, thread_sensitive=True)('json', queryset)
        return web.json_response(text=text)


@routes.view('/chats/{pk}')
class ChatsDetailView(ChatsAbstractView, web.View):

    async def get(self):
        try:
            pk = int(self.request.match_info['pk'])
        except ValueError:
            pk = None

        queryset = await self.get_queryset(pk=pk)
        chat = await sync_to_async(queryset.values().first)()

        if not chat:
            return web.json_response(data={'message': 'Not found'}, status=404)

        text = json.dumps(chat, cls=DjangoJSONEncoder)
        return web.json_response(text=text)
