from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dbProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Forum
    url(r'^db/api/forum/create/$', 'api.forum.views.create', name='forum_create'),
    url(r'^db/api/forum/details/$', 'api.forum.views.details', name='forum_details'),
    url(r'^db/api/forum/listThreads/$', 'api.forum.views.list_threads', name='forum_listThreads'),
    url(r'^db/api/forum/listPosts/$', 'api.forum.views.list_posts', name='forum_listPosts'),
    url(r'^db/api/forum/listUsers/$', 'api.forum.views.list_users', name='forum_listUsers'),

    # Post
    url(r'^db/api/post/create/$', 'api.post.views.create', name='post_create'),
    url(r'^db/api/post/details/$', 'api.post.views.details', name='post_details'),
    url(r'^db/api/post/list/$', 'api.post.views.post_list', name='post_list'),
    url(r'^db/api/post/remove/$', 'api.post.views.remove', name='post_remove'),
    url(r'^db/api/post/restore/$', 'api.post.views.restore', name='post_restore'),
    url(r'^db/api/post/update/$', 'api.post.views.update', name='post_update'),
    url(r'^db/api/post/vote/$', 'api.post.views.vote', name='post_vote'),

    # User
    url(r'^db/api/user/create/$', 'api.user.views.create', name='user_create'),
    url(r'^db/api/user/details/$', 'api.user.views.details', name='user_details'),
    url(r'^db/api/user/follow/$', 'api.user.views.follow', name='user_follow'),
    url(r'^db/api/user/unfollow/$', 'api.user.views.unfollow', name='user_unfollow'),
    url(r'^db/api/user/listFollowers/$', 'api.user.views.list_followers', name='user_listFollowers'),
    url(r'^db/api/user/listFollowing/$', 'api.user.views.list_following', name='user_listFollowing'),
    url(r'^db/api/user/updateProfile/$', 'api.user.views.update', name='user_updateProfile'),
    url(r'^db/api/user/listPosts/$', 'api.user.views.list_posts', name='user_listPosts'),

    # Thread
    url(r'^db/api/thread/create/$', 'api.thread.views.create', name='thread_create'),
    url(r'^db/api/thread/details/$', 'api.thread.views.details', name='thread_details'),
    url(r'^db/api/thread/subscribe/$', 'api.thread.views.subscribe', name='thread_subscribe'),
    url(r'^db/api/thread/unsubscribe/$', 'api.thread.views.unsubscribe', name='thread_unsubscribe'),
    url(r'^db/api/thread/open/$', 'api.thread.views.open', name='thread_open'),
    url(r'^db/api/thread/close/$', 'api.thread.views.close', name='thread_close'),
    url(r'^db/api/thread/vote/$', 'api.thread.views.vote', name='thread_vote'),
    url(r'^db/api/thread/list/$', 'api.thread.views.thread_list', name='thread_list'),
    url(r'^db/api/thread/update/$', 'api.thread.views.update', name='thread_update'),
    url(r'^db/api/thread/remove/$', 'api.thread.views.remove', name='thread_remove'),
    url(r'^db/api/thread/restore/$', 'api.thread.views.restore', name='thread_restore'),
    url(r'^db/api/thread/listPosts/$', 'api.thread.views.list_posts', name='thread_listPosts'),

    # Db
    url(r'^db/api/clear/$', 'api.db.views.clear', name='clear'),
)
