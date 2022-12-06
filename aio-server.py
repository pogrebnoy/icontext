from aiohttp import web
from django import setup
from django.conf import settings

from icontext import settings as my_settings  # not the same as django.conf.settings
from chat.routes import chat_app
from chat.ws import ws_chat


async def setup_django(app):
    settings.configure(
        INSTALLED_APPS=my_settings.INSTALLED_APPS,
        DATABASES=my_settings.DATABASES)
    setup()

app = web.Application()
app.on_startup.append(setup_django)
app.add_routes([web.get('/api/v1/ws', handler=ws_chat)])
app.add_subapp('/api/v1/', chat_app)


if __name__ == '__main__':
    web.run_app(app)
