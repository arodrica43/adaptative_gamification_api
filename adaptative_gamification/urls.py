"""adaptative_gamification URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from api import views
from django.conf.urls import url
from adaptative_gamification import settings


urlpatterns = [
    path('',  views.index),
    path('adaptative_statistics',views.adaptative_statistics),
    path('js_test/', views.js_test),
    #path('examples/adaptative-mechanic/random/',  views.adaptative_mechanic_example),
    #path('examples/adaptative-mechanic/matrix/',  views.adaptative_mechanic_example_matrix),
    path('admin/', admin.site.urls),
]


router = routers.DefaultRouter()
#Basic urls
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'gamers', views.GamerViewSet)
router.register(r'g_mechanics', views.GMechanicViewSet)
router.register(r'statistics', views.InteractionStatisticViewSet)
router.register(r'g_components', views.GComponentViewSet)
router.register(r'gamer_profiles', views.GamerProfileViewSet)
router.register(r'emotion_profiles', views.EmotionProfileViewSet)
router.register(r'social_profiles', views.SocialProfileViewSet)
# Gamification mechanics urls
router.register(r'development_tools', views.DevelopementToolViewSet)
router.register(r'challenges', views.ChallengeViewSet)
router.register(r'easter_eggs', views.EasterEggViewSet)
router.register(r'unlockables', views.UnlockableViewSet)
router.register(r'badges', views.BadgeViewSet)
router.register(r'levels', views.LevelViewSet)
router.register(r'points', views.PointViewSet)
router.register(r'leaderboards', views.LeaderboardViewSet)
router.register(r'lotteries', views.LotteryViewSet)
router.register(r'social_networks', views.SocialNetworkViewSet)
router.register(r'social_statuses', views.SocialStatusViewSet)
router.register(r'knowledge_shares', views.KnowledgeShareViewSet)
router.register(r'gifts', views.GiftViewSet)
router.register(r'gift_openers', views.GiftOpenerViewSet)
#Adaptative mechanics
router.register(r'adaptatives', views.AdaptativeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/gamers/<str:username>', views.GamerViewSet),
    path('api/gamers/<str:username>/add_gift', views.add_gift),
    path('api/gamers/<str:username>/open_gift', views.open_gift),
    path('api/gamers/<str:username>/add_friend/<str:friend_username>', views.add_friend),
    path('api/gamers/<str:username>/del_friend/<str:friend_username>', views.del_friend),
    path('api/gamers/<str:username>/retrieve_friends', views.retrieve_friends),
    path('api/gamers/<str:username>/edit_social_profile', views.edit_social_profile),
    path('api/retrieve_users_search', views.retrieve_users_search),
    path('api/g_mechanics/<int:gmechanic_id>/preview', views.preview_gmechanic),
    path('api/badges/retrieve_for_user/<str:username>', views.view_badge_set),
    path('api/unlockables/retrieve_for_user/<str:username>', views.view_unlockable_set),
    path('api/challenges/retrieve_for_user/<str:username>', views.view_challenge_set),
    path('api/g_mechancis/preview_game/<int:id>/<str:username>', views.preview_game),
   # path('api/badges/icons/<str:filename>', views.preview_badge_icon),
    #url(r'^tinymce/', include('tinymce.urls')),
    #path('gamers/(?P<username>.+)/', views.GamerViewSet),
    #path(r'^gamers/(?P<username>\w+)/$', views.index),
]

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 
 
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


