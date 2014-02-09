from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root' : settings.MEDIA_ROOT }),
	(r'^topic$'      , 'newscredpython.views.topic'),
	(r'^article$'    , 'newscredpython.views.article'),
	(r'^articlepage$', 'newscredpython.views.articlepage'),
	(r'^topicpage$'  , 'newscredpython.views.topicpage'),
	(r'^source$'     , 'newscredpython.views.source'),
	(r'^author$'     , 'newscredpython.views.author'),
	(r'^category$'   , 'newscredpython.views.category'),
    (r'^extract$'    , 'newscredpython.views.extract'),
    (r'^stories$'    , 'newscredpython.views.stories'),
    (r'^'            , 'newscredpython.views.index'),	

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
