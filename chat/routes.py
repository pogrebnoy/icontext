from aiohttp import web

from . import views

chat_app = web.Application()
chat_app.router.add_routes(views.routes)
