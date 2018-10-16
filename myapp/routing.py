from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/autosave_editor/(?P<slug>[^/]+)/$', consumers.AutoSaveEditorConsumer),
]