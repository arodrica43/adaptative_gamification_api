from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import lock, AdaptativeSerializer, InteractionStatisticSerializer, BadgeSerializer, ChallengeSerializer, DevelopmentToolSerializer, EasterEggSerializer, GiftSerializer, GiftOpenerSerializer, KnowledgeShareSerializer, LevelSerializer, LotterySerializer, PointSerializer, SocialNetworkSerializer, SocialStatusSerializer, UnlockableSerializer, LeaderboardSerializer, UserSerializer, GroupSerializer, GamerSerializer, GMechanicSerializer, GComponentSerializer , GamerProfileSerializer, EmotionProfileSerializer, SocialProfileSerializer
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, Http404
from api.models import mechanics_list, mechanics_list_names,mechanic_list_total_interactions, InteractionStatistic, Adaptative, Badge, Challenge, DevelopmentTool, EasterEgg, Gift, GiftOpener, KnowledgeShare, Level, Lottery, Point, SocialNetwork, SocialStatus, Unlockable, Leaderboard, Gamer, GMechanic, GComponent, GamerProfile, EmotionProfile, SocialProfile
from django.template.response import TemplateResponse
from rest_framework.response import Response
import numpy as np
import random as rdm
import os
from django.conf import settings

import threading
lock2 = threading.Lock()
lock3 = threading.Lock()
lock4 = threading.Lock()
lock5 = threading.Lock()
lock6 = threading.Lock()
lock7 = threading.Lock()
lock8 = threading.Lock()

interaction_files = [("include-onclick-tracking","onclick.js"), 
                     ("include-base-tracking","default.js"), 
                     ("include_interaction_testing_tools","interaction_testing.js")
                    ]

def js_test(request):
    return TemplateResponse(request, 'test/js_test.html',{})


def open_gift(request,username):

    lock5.acquire()
    message = ""
    text = "false" 
    user = Gamer.objects.filter(user__username = username)[0]
    if 'index' in request.GET.keys():
        if user.gamer_profile.data['gifts'][int(request.GET['index'])][1] == 'text':
            text = "true"
            message = "The user " + user.gamer_profile.data['gifts'][int(request.GET['index'])][0] + " send you the following message: " +  user.gamer_profile.data['gifts'][int(request.GET['index'])][2]
        else:
            user.gamer_profile.data[user.gamer_profile.data['gifts'][int(request.GET['index'])][1]] += int(user.gamer_profile.data['gifts'][int(request.GET['index'])][2])
            what = "$"
            if(user.gamer_profile.data['gifts'][int(request.GET['index'])][1] == 'score'):
                what = "points"    
            message = "You have recieved " + user.gamer_profile.data['gifts'][int(request.GET['index'])][2] + " " + what + " from " + user.gamer_profile.data['gifts'][int(request.GET['index'])][0] + "!"
        del user.gamer_profile.data['gifts'][int(request.GET['index'])] 
        user.gamer_profile.save()
    lock5.release()
    return JsonResponse({'results': 'OK', 'message':message})

def add_gift(request,username):

    lock4.acquire()
    print("Adding gift to",username)
    user = Gamer.objects.filter(user__username = username)[0]
    if 'from' in request.GET.keys():
        if 'type' in request.GET.keys():
            if "content" in request.GET.keys():
                user.gamer_profile.data['gifts'] += [[request.GET['from'],request.GET['type'], request.GET['content']]]
                user.gamer_profile.save()
    lock4.release()
    #print(len(user.gamer_profile.data['gifts']))
    return JsonResponse({'results': 'OK'})

def add_friend(request,username,friend_username):

    lock2.acquire()
    user = Gamer.objects.filter(user__username = username)[0]
    if friend_username not in user.social_profile.data['friends']:
        
        user.social_profile.data['friends'] += [friend_username]
        user.social_profile.save()
    lock2.release()
    return HttpResponse('OK')

def del_friend(request,username,friend_username):
    
    lock3.acquire()
    user = Gamer.objects.filter(user__username = username)[0]
    if friend_username in user.social_profile.data['friends']:
        user.social_profile.data['friends'].remove(friend_username)
        user.social_profile.save()
    lock3.release()
    return HttpResponse('OK')

def retrieve_friends(request,username):

    user = Gamer.objects.filter(user__username = username)[0]
    friends = [[SocialProfileSerializer(x.social_profile,context={'request': request}).data, UserSerializer(x.user,context={'request': request}).data ] for x in Gamer.objects.all() if x.user.username in user.social_profile.data['friends']]
    
    return JsonResponse({'friends': friends})

def retrieve_users_search(request):
    if('uname_contains' in request.GET.keys()):
        queryset = [GamerSerializer(x,context={'request': request}).data for x in Gamer.objects.all() if  request.GET['uname_contains'] in x.user.username]
    else:
        queryset = [GamerSerializer(x,context={'request': request}).data for x in Gamer.objects.all()]

    return JsonResponse({'results':queryset})


def edit_social_profile(request,username):

    print("Uploading new social profile...")
    user = Gamer.objects.filter(user__username = username)[0]
    user.social_profile.image = request.GET['new_image']
    user.social_profile.description = request.GET['new_description']
    user.social_profile.save()
    return JsonResponse({'results':'OK'})
                  

def g_mechanic_cast(gmechanic_id):

    for mech_id in range(len(mechanics_list)):
        queryset = mechanics_list[mech_id].objects.filter(id = gmechanic_id)
        if queryset: 
            return queryset, mechanics_list_names[mech_id]
    
    return queryset, 'g_mechanics'

def index(request):
    """
    Landingpage
    TO DO: Migrate to the main webapp
    """
    users = Gamer.objects.all()
    #request.GET.get('id', '')
    return TemplateResponse(request, 'index.html', {'users': users})
    


def adaptative_statistics(request):
    """
    Landingpage
    TO DO: Migrate to the main webapp
    """
    users = Gamer.objects.all()
    #request.GET.get('id', '')
    user = ""
    existing_user = False
    if "user" in request.GET.keys():
        user = Gamer.objects.filter(user__username = request.GET['user'])
        if user:
            user = user[0].user.username
            existing_user = True
    return TemplateResponse(request, 'adaptative_statistics.html', {'users': users,'user':user, 'existing_user': existing_user})
    

def preview_gmechanic(request, gmechanic_id):
    """
    Page for rendering the html of a GComponent
    TO DO: Migrate to the main webapp
    """
    #print("hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    queryset, name = g_mechanic_cast(gmechanic_id)
    import os
    from django.conf import settings
    
    file = open(os.path.join(settings.TEMPLATES[0]['DIRS'][0], "mechanics/" + name + '.html'))
    queryset.update(html = file.read().replace("called_mechanic_url","http://127.0.0.1:8080/api/" + name + "/" + str(gmechanic_id) + "/?" + request.GET.urlencode()))
    #print(queryset[0].html)
    #print(file.read())
    serializer = GMechanicSerializer(queryset[0], context={'request': request}) 
    #print(serializer.data)
    return TemplateResponse(request, 'preview_mechanic.html', {"data":serializer.data, "url_query": request.GET.urlencode()})


# def preview_badge_icon(request, filename):

#     return TemplateResponse(request, 'badge_icon_preview.html', {"filename":filename})

def view_badge_set(request, username):
  
    try:
        user = Gamer.objects.filter(user__username = username)[0]
    except:
        print("User found")
        raise Http404

    badge_ids = []
    if 'badges' in user.gamer_profile.data.keys():
        badge_ids = user.gamer_profile.data['badges']
  
    all_badges = Badge.objects.all()

    badge_set = []
    for badge in all_badges:
         badge_set += [[BadgeSerializer(badge, context={'request': request}).data, badge.id in badge_ids]]
    
    return JsonResponse({'results':badge_set})


def view_unlockable_set(request, username):
   
    try:
        user = Gamer.objects.filter(user__username = username)[0]
    except:
        print("User found")
        raise Http404

    unlock_ids = []
    if 'unlockables' in user.gamer_profile.data.keys():
        unlock_ids = user.gamer_profile.data['unlockables']
  
    all_unlocks = Unlockable.objects.all()

    unlocks_set = []
    for unlk in all_unlocks:
         unlocks_set += [[UnlockableSerializer(unlk, context={'request': request}).data, unlk.id in unlock_ids]]
    
    return JsonResponse({'results':unlocks_set})

def view_challenge_set(request, username):
   
    try:
        user = Gamer.objects.filter(user__username = username)[0]
    except:
        print("User found")
        raise Http404

    unlock_ids = []
    if 'challenges' in user.gamer_profile.data.keys():
        unlock_ids = user.gamer_profile.data['challenges']
  
    all_unlocks = Challenge.objects.all()

    unlocks_set = []
    for unlk in all_unlocks:
         unlocks_set += [[UnlockableSerializer(unlk, context={'request': request}).data, unlk.id in unlock_ids]]
    
    return JsonResponse({'results':unlocks_set})


def preview_game(request, id,username):
    
    queryset = Unlockable.objects.filter(id = id)
    return TemplateResponse(request, 'preview_game.html', {"data":queryset[0], "uname": username})



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        queryset = User.objects.filter(username=pk)
        try:
            pk = int(pk)
            queryset = User.objects.filter(id=pk)
            if len(queryset) > 0:
                serializer = UserSerializer(queryset[0], context={'request': request})
                return Response(serializer.data)
            else:
                raise Http404       
        except ValueError as error:
            if len(queryset) > 0:
                serializer = UserSerializer(queryset[0], context={'request': request})
                return Response(serializer.data)
            else:
                raise Http404

    def update(self, request, *args, **kwargs):
        #lock8.acquire()
        try:
            instance = self.queryset.get(pk=kwargs.get('pk'))
        except ValueError:
            instance = self.queryset.get(username=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True,context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #lock8.release()
        return Response(serializer.data)

class GamerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Gamer.objects.all().order_by('-user_id')
    serializer_class = GamerSerializer
    filter_fields = ('user__username' )

    def retrieve(self, request, pk=None):

        queryset = Gamer.objects.filter(user__username=pk)
        try:     
            pk = int(pk)
            queryset = Gamer.objects.filter(user__id=pk)
            if len(queryset) > 0:
                sp_data = queryset[0].social_profile.data
                sp_data['followers'] = len([x for x in Gamer.objects.all() if queryset[0].user.username in x.social_profile.data['friends']])
                sp = SocialProfile.objects.filter(id = queryset[0].social_profile.id)
                sp.update(data = sp_data)
                serializer = GamerSerializer(queryset[0], context={'request': request})    
                return Response(serializer.data)
            else:
                raise Http404       
        except ValueError as error:
            if len(queryset) > 0:
                sp_data = queryset[0].social_profile.data
                sp_data['followers'] = len([x for x in Gamer.objects.all() if queryset[0].user.username in x.social_profile.data['friends']])
                sp = SocialProfile.objects.filter(id = queryset[0].social_profile.id)
                sp.update(data = sp_data)
                serializer = GamerSerializer(queryset[0], context={'request': request})
                return Response(serializer.data)
            else:
                raise Http404

    def update(self, request, *args, **kwargs):
        #lock7.acquire()
        try:
            instance = self.queryset.get(pk=kwargs.get('pk'))
           
        except ValueError:
            instance = self.queryset.get(user__username=kwargs.get('pk'))
        # print(type(instance.gamer_profile.data))
        # print(instance.gamer_profile.data)

        serializer = self.serializer_class(instance, data=request.data, partial=True,context={'request': request})
        
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        #lock7.release()
        return Response(serializer.data)

class GamerProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = GamerProfile.objects.all()
    serializer_class = GamerProfileSerializer

class EmotionProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = EmotionProfile.objects.all()
    serializer_class = EmotionProfileSerializer

class SocialProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SocialProfile.objects.all()
    serializer_class = SocialProfileSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

def ensamble_interaction_dynamic_properties(queryset, filenames = interaction_files):
    for i in range(len(filenames)):
        file = open(os.path.join(settings.TEMPLATES[0]['DIRS'][1],  "interactions/" + filenames[i][1]))
        queryset.update(html = queryset[0].html.replace(filenames[i][0],file.read())) 

class GMechanicViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = GMechanic.objects.all()
    serializer_class = GMechanicSerializer
    concrete_class = 'g_mechanics'
    concrete_model = GMechanic

    def logic(self,queryset,request):
        pass

    def abstract_retrieve(self, request, pk=None):
        #print("There?",request.GET.urlencode())
        if pk:
            lock.acquire()
            try:
                #print(self.concrete_model)
                #main_queryset = self.concrete_model.objects.filter(id=pk)
                queryset, name = g_mechanic_cast(pk)
                file = open(os.path.join(settings.TEMPLATES[0]['DIRS'][0],  "mechanics/" + name + '.html'))
                print("http://127.0.0.1:8080/api/" + name + "/" + pk + "/?" + request.GET.urlencode())
                queryset.update(html = file.read().replace("called_mechanic_url","http://127.0.0.1:8080/api/" + name + "/" + pk + "/?" + request.GET.urlencode()))
                queryset.update(html = queryset[0].html.replace("dynamic_mechanic_index", pk))
                queryset.update(html = queryset[0].html.replace("dynamic_mechanic_name", name))
                

                # Dynamic properties of a g_mechanic :: dynamic_user
                #                                       dynamic_index
                ensamble_interaction_dynamic_properties(queryset)
                #file = open(os.path.join(settings.TEMPLATES[0]['DIRS'][1],  "interactions/onclick.js"))
                #queryset.update(html = queryset[0].html.replace("include-onclick-tracking",file.read())) 
                try:             
                    queryset.update(html = queryset[0].html.replace("dynamic_user",request.GET['user']))
                except:
                    print("Query url doesn't contain username argument")
                try:             
                    queryset.update(html = queryset[0].html.replace("dynamic_index",request.GET['dynamic_index']))
                except:
                    print("Query url doesn't contain dynamic_index argument")
                    

                tmp_title = queryset[0].title
                if 'show_title' in request.GET.keys():
                    #print("Halooo", request.GET['show_title'])
                    st = request.GET['show_title']
                    if st == 'false':
                        queryset.update(title = "")
                    
                self.logic(queryset,request)
                #print(queryset[0].leadders['user1'])
                serializer = self.serializer_class(queryset[0], context={'request': request})
                queryset.update(title = tmp_title)
                lock.release()   
                return Response(serializer.data)
            except:
                lock.release() 
                ensamble_interaction_dynamic_properties(queryset)
                raise Http404
        else: 
            return Http404

    def retrieve(self, request, pk=None):
        return self.abstract_retrieve(request,pk)
   
    def update(self, request,pk):
        lock.acquire()
        try:
            instance = self.queryset.get(id=pk)
            data = request.data
            #print(data)
            if data['user'] != "dynamic_user":
                statistic = InteractionStatistic.objects.filter(mechanic = instance, user = data['user'])
                for arg in ['history', 'main_time', 'focus_time', 'interaction_time','hidden_content_time', 'shown_content_time']:
                    uplog = statistic[0].log
                    if arg in statistic[0].log.keys():
                        uplog[arg] += data['log'][arg]
                    else: 
                        uplog[arg] = data['log'][arg]
                    statistic.update(log = uplog)
                #Interaction index update ----------------------------------------------------------------------------------------------------
                # for s in InteractionStatistic.objects.all():
                #     s.log = {}
                #     s.interaction_index = 0
                #     s.save()
                # for u in Gamer.objects.all():
                #     u.gamer_profile.disruptor = 0
                #     u.gamer_profile.free_spirit = 0
                #     u.gamer_profile.achiever = 0
                #     u.gamer_profile.player = 0
                #     u.gamer_profile.socializer = 0
                #     u.gamer_profile.philantropist = 0
                #     u.gamer_profile.no_player = 0
                #     u.gamer_profile.save()   

                import math
                _, name = g_mechanic_cast(pk)
                n = sum([(0.2*x[0]["level"] + 0.8) for x in statistic[0].log["history"]])/mechanic_list_total_interactions[name]
                l = 4
                I = 0
                for t_label in ['main_time', 'focus_time', 'interaction_time']:
                    I += 1 - math.exp(-l*(n/(statistic[0].log[t_label] + 1e-100)))
                I = I/3
                statistic.update(interaction_index = I)
                #------------------------------------------------------------------------------------------------------------------------------
                # Gamer profile update --------------------------------------------------------------------------------------------------------
                current_user = Gamer.objects.filter(user__username = data['user'])
                if current_user:
                    current_gstate = np.array(current_user[0].gamer_profile.vectorize())
                    current_statistics = np.array(instance.statistics_vector(data['user']))
                    #print("Here",instance.matrix().T.dot(current_statistics))
                    print(instance.matrix()[:,:len(current_statistics)].shape,len(current_statistics))
                    new_gstate = 0.5*(current_gstate + np.linalg.pinv(instance.matrix()[:len(current_statistics),:]).dot(current_statistics))
                    print(new_gstate)
                    current_user[0].gamer_profile.disruptor = new_gstate[0]
                    current_user[0].gamer_profile.free_spirit = new_gstate[1]
                    current_user[0].gamer_profile.achiever = new_gstate[2]
                    current_user[0].gamer_profile.player = new_gstate[3]
                    current_user[0].gamer_profile.socializer = new_gstate[4]
                    current_user[0].gamer_profile.philantropist = new_gstate[5]
                    current_user[0].gamer_profile.no_player = new_gstate[6]
                    current_user[0].gamer_profile.save()                
                #------------------------------------------------------------------------------------------------------------------------------
                serializer = self.serializer_class(instance, data=data, partial=True,context={'request': request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                lock.release()
                return Response(serializer.data)
            else:
                lock.release()
                return HttpResponse('Invalid user!')  
        except:
            lock.release()
            raise Http404     
           

class InteractionStatisticViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = InteractionStatistic.objects.all()
    serializer_class = InteractionStatisticSerializer

class GComponentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = GComponent.objects.all()
    serializer_class = GComponentSerializer

class DevelopementToolViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = DevelopmentTool.objects.all()
    serializer_class = DevelopmentToolSerializer
    concrete_class = 'development_tools'
    concrete_model = DevelopmentTool

    def retrieve(self, request, pk=None):
        #print("WTFFFs")
        return super().abstract_retrieve(request,pk)

class ChallengeViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    concrete_class = 'challenges'
    concrete_model = Challenge

    def retrieve(self, request, pk=None):
        #print("WTFFFs")
        return super().abstract_retrieve(request,pk)

    def logic(self,queryset,request):
        #lock2.acquire() # I don't know if its necessary, sience we have lock in parent class
        #print("Im hereee")
        if 'user' in request.GET.keys():
            if request.GET['user']:
                user = Gamer.objects.filter(user__username = request.GET['user'])
                if user:
                    user = user[0]
                    by = queryset[0].by
                    th = queryset[0].threshold
                    u_keys = user.gamer_profile.data.keys()
                    if by in u_keys:
                        if user.gamer_profile.data[by] >= th:
                            if 'challenges' in u_keys:
                                if queryset[0].pk not in user.gamer_profile.data['challenges']:
                                    user.gamer_profile.data['challenges'] += [queryset[0].id]
                            else:
                                user.gamer_profile.data['challenges'] = [queryset[0].id]
                            user.gamer_profile.save()
                            queryset.update(state = True)
                            #print("Im entering hereee")
                            #print(queryset[0].state)
                        else:
                           queryset.update(state = False)
                    else:
                        queryset.update(state = False)
                else:
                    queryset.update(state = False)
            else:
                queryset.update(state = False)
        else:
            queryset.update(state = False)    

class EasterEggViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = EasterEgg.objects.all()
    serializer_class = EasterEggSerializer
    concrete_class = 'easter_eggs'
    concrete_model = EasterEgg

class UnlockableViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Unlockable.objects.all()
    serializer_class = UnlockableSerializer
    concrete_class = 'unlockables'
    concrete_model = Unlockable


    def retrieve(self, request, pk=None):
        #print("WTFFFs")
        return super().abstract_retrieve(request,pk)

    def logic(self,queryset,request):
        #lock2.acquire() # I don't know if its necessary, sience we have lock in parent class
        #print("Im hereee")
        if 'user' in request.GET.keys():
            if request.GET['user']:
                user = Gamer.objects.filter(user__username = request.GET['user'])
                if user:
                    user = user[0]
                    by = queryset[0].by
                    th = queryset[0].threshold
                    u_keys = user.gamer_profile.data.keys()
                    if by in u_keys:
                        if user.gamer_profile.data[by] >= th:
                            if 'unlockables' in u_keys:
                                if queryset[0].pk not in user.gamer_profile.data['unlockables']:
                                    user.gamer_profile.data['unlockables'] += [queryset[0].id]
                            else:
                                user.gamer_profile.data['unlockables'] = [queryset[0].id]
                            user.gamer_profile.save()
                            queryset.update(state = True)
                            #print("Im entering hereee")
                            #print(queryset[0].state)
                        else:
                           queryset.update(state = False)
                    else:
                        queryset.update(state = False)
                else:
                    queryset.update(state = False)
            else:
                queryset.update(state = False)
        else:
            queryset.update(state = False)        


class BadgeViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    concrete_class = 'badges'
    concrete_model = Badge

    def retrieve(self, request, pk=None):
        #print("WTFFFs")
        return super().abstract_retrieve(request,pk)

    def logic(self,queryset,request):
       # I don't know if its necessary, sience we have lock in parent class
        #print("Im hereee")
        if 'user' in request.GET.keys():
            if request.GET['user']:
                user = Gamer.objects.filter(user__username = request.GET['user'])
                if user:
                    user = user[0]
                    by = queryset[0].by
                    th = queryset[0].threshold
                    u_keys = user.gamer_profile.data.keys()
                    if by in u_keys:
                        if user.gamer_profile.data[by] >= th:
                            if 'badges' in u_keys:
                                if queryset[0].pk not in user.gamer_profile.data['badges']:
                                    user.gamer_profile.data['badges'] += [queryset[0].id]
                            else:
                                user.gamer_profile.data['badges'] = [queryset[0].id]
                            user.gamer_profile.save()
                            queryset.update(state = True)
                            #print("Im entering hereee")
                            #print(queryset[0].state)
                        else:
                           queryset.update(state = False)
                    else:
                        queryset.update(state = False)
                else:
                    queryset.update(state = False)
            else:
                queryset.update(state = False)
        else:
            queryset.update(state = False)        

class LevelViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    concrete_class = 'levels'
    concrete_model = Level

    def retrieve(self, request, pk=None):
        #print("WTFFFs")
        return super().abstract_retrieve(request,pk)

    def logic(self,queryset,request):
        # I don't know if its necessary, sience we have lock in parent class
        
        if 'user' in request.GET.keys():
            if request.GET['user']:
                user = Gamer.objects.filter(user__username = request.GET['user'])
                if user:
                    #queryset.update(user = user[0].user.username)
                    by = queryset[0].by
                    if by in user[0].gamer_profile.data.keys():
                        if 'increase' in request.GET.keys():
                            user[0].gamer_profile.data[by] = min(user[0].gamer_profile.data[by] + 1, queryset[0].max_value)
                            user[0].gamer_profile.save() 
                        queryset.update(value = user[0].gamer_profile.data[by])
                    else:
                        if 'increase' in request.GET.keys():
                            user[0].gamer_profile.data[by] = 1
                        else:
                            user[0].gamer_profile.data[by] = 0
                        user[0].gamer_profile.save() 
                        queryset.update(value = 1)
                else:
                    queryset.update(value = 0)
                    print("No such user")
            else:
                queryset.update(value = 0)
                print("No such user")
        else:
            queryset.update(value = 0)
            print("No such user")
        #lock2.release()

class PointViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    concrete_class = 'points'
    concrete_model = Point

    def retrieve(self, request, pk=None):
        #print("WTFFFs")
        return super().abstract_retrieve(request,pk)

    def logic(self,queryset,request):
         # I don't know if its necessary, sience we have lock in parent class
        
        if 'user' in request.GET.keys():
            if request.GET['user']:
                user = Gamer.objects.filter(user__username = request.GET['user'])
                if user:
                    queryset.update(user = user[0].user.username)
                    by = queryset[0].given_by
                    if by in user[0].gamer_profile.data.keys():
                        if 'increase' in request.GET.keys():
                            queryset.update(score = user[0].gamer_profile.data[by] + float(request.GET['increase']))
                            user[0].gamer_profile.data[by] +=  float(request.GET['increase'])
                            user[0].gamer_profile.save() 
                        else:  
                            queryset.update(score = user[0].gamer_profile.data[by])
                    else:
                        inc = 0
                        if 'increase' in request.GET.keys():
                            inc = float(request.GET['increase'])
                        user[0].gamer_profile.data[by] = inc
                        user[0].gamer_profile.save() 
                        queryset.update(score = inc)
                else:
                    queryset.update(user = '---')
                    queryset.update(score = 0)
                    print("No such user")
            else:
                queryset.update(user = '---')
                queryset.update(score = 0)
                print("No such user")
        else:
            queryset.update(user = '---')
            queryset.update(score = 0)
            print("No such user")
        #lock2.release()
      


class LeaderboardViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """        
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    concrete_class = 'leaderboards'
    concrete_model = Leaderboard

    def retrieve(self, request, pk=None):
        return super().abstract_retrieve(request,pk)

    # Concrete logic for leaderboards view
    def logic(self,queryset,request):
        users, json = Gamer.objects.all(), {}
        for user in users:
            if user.gamer_profile.data:
                if user.gamer_profile.data.keys():
                    if queryset[0].sort_by in user.gamer_profile.data.keys():
                        json[user.user.username] = user.gamer_profile.data[queryset[0].sort_by]   
                    elif queryset[0].sort_by == 'following':
                        json[user.user.username] = len(user.social_profile.data['friends'])   
                    elif queryset[0].sort_by == 'followers':
                        json[user.user.username] = len([x for x in Gamer.objects.all() if user.user.username in x.social_profile.data['friends']])
                    elif queryset[0].sort_by == 'views':
                         json[user.user.username] = user.social_profile.data['views'] # TO DO :: Add views count mechanism
        json = dict(sorted(json.items(), key=lambda x: x[1], reverse=True)[:queryset[0].length])
        queryset.update(leadders = json)

        
   
    
class LotteryViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Lottery.objects.all()
    serializer_class = LotterySerializer
    concrete_class = 'lotteries'
    concrete_model = Lottery

    def retrieve(self, request, pk=None):
        return super().abstract_retrieve(request,pk)

    # Concrete logic for leaderboards view
    def logic(self,queryset,request):

        if 'prize' in request.GET.keys():
            if 'user' in request.GET.keys():
                user = Gamer.objects.filter(user__username =  request.GET['user'])
                if user:
                    by = queryset[0].by
                    if user[0].gamer_profile.data:
                        if by in user[0].gamer_profile.data.keys():
                            prize = request.GET['prize']
                            try:
                                p = int(prize)
                                user[0].gamer_profile.data[by] += p
                                user[0].gamer_profile.save() 
                            except:
                                pass
                        else:
                            prize = request.GET['prize']
                            try:
                                p = int(prize)
                                user[0].gamer_profile[by] = p
                                user[0].gamer_profile.data.save()
                            except:
                                pass

    

class SocialNetworkViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SocialNetwork.objects.all()
    serializer_class = SocialNetworkSerializer
    concrete_class = 'social_networks'
    concrete_model = SocialNetwork
    

class SocialStatusViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SocialStatus.objects.all()
    serializer_class = SocialStatusSerializer
    concrete_class = 'social_statuses'
    concrete_model = SocialStatus

class KnowledgeShareViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = KnowledgeShare.objects.all()
    serializer_class = KnowledgeShareSerializer
    concrete_class = 'knowledge_shares'
    concrete_model = KnowledgeShare


    def retrieve(self, request, pk=None):
        return super().abstract_retrieve(request,pk)

    # Concrete logic for leaderboards view
    def logic(self,queryset,request):
        if not queryset[0].messages:
            queryset.update(messages = {})
        if 'from' in request.GET.keys():
            if request.GET['from'] != "dynamic_user":
                if 'message' in request.GET.keys():
                    old_messages = queryset[0].messages
                    if 'length' in old_messages.keys():
                        old_messages['content'] += [[request.GET['from'],request.GET['message']]]
                        old_messages['length'] += 1
                    else:
                        old_messages['length'] = 1
                        old_messages['content'] = [[request.GET['from'],request.GET['message']]]
                    queryset.update(messages = old_messages)
                



class GiftViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer
    concrete_class = 'gifts'
    concrete_model = Gift


class GiftOpenerViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = GiftOpener.objects.all()
    serializer_class = GiftOpenerSerializer
    concrete_class = 'gift_openers'
    concrete_model = GiftOpener

# Adaptative mechanics

class AdaptativeViewSet(GMechanicViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Adaptative.objects.all()
    serializer_class = AdaptativeSerializer

    def retrieve(self, request, pk=None):
        return super().abstract_retrieve(request,pk)

    def update_utilities(self,queryset,user): 
        # DEFAULT :: "UserType-Mechanics Matrix" update policy 
        # v = np.array(user.gamer_profile.vectorize()) 
        # M = queryset[0].matrix()
        # return Mv
        return  queryset[0].matrix().dot(np.array(user.gamer_profile.vectorize()))

    def select_mechanic(self,utilities):
        # DEFAULT :: "Choosing random index between argmax indexes" update policy
        #idx = rdm.choice(np.argwhere(utilities == np.amax(utilities)).flatten().tolist())
        #print(utilities)
        # PONDERATED PROBABILITY SELECTION
        prob = utilities/utilities.sum()
        r = rdm.random()
        acc, idx = 0, 0
        for i in range(len(prob)):
            pi = prob[i]
            if acc < r and r < acc + pi:
                idx = i
                break
            acc += pi
        return GMechanic.objects.all()[idx]

    # Concrete logic for leaderboards view
    def logic(self,queryset,request):
        print("DEFAULT :: Adaptative logic")
        args = request.GET
        if 'user' in args.keys():
            user = Gamer.objects.filter(user__username = args['user'])
            if user:
                user = user[0]
                gmechanic = self.select_mechanic(self.update_utilities(queryset,user))

                #g_mechanic serialization and html update
                serializer = GMechanicSerializer(gmechanic, context={'request': request}) 
                data = serializer.data      
                file = open(os.path.join(settings.TEMPLATES[0]['DIRS'][0], "mechanics/adaptatives.html"))
                new_html = file.read().replace('called_mechanic_url', "http://127.0.0.1:8080/api/g_mechanics/" + str(data['id']) + "/?" + args.urlencode())
                queryset.update(html = new_html)
        else:
            file = open(os.path.join(settings.TEMPLATES[0]['DIRS'][0], "mechanics/adaptatives.html"))
            new_html = file.read().replace('called_mechanic_url', "http://127.0.0.1:8080/api/g_mechanics/" + str(5) + "/?" + args.urlencode())
            queryset.update(html = new_html)
        ensamble_interaction_dynamic_properties(queryset)


class AdaptativeUtilitiesViewSet(AdaptativeViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    def update_utilities(self,queryset,user): 
        # TO DO :: Add variable mechanics interaction index
        # UTILITIES :: "UserType-Mechanics Matrix" update policy 
        # input  queryset : QuerySet
        #        user : Gamer
        # return Mv : List
        print("Concrete Implementation of the Utilities Update")
        stats = InteractionStatistic.objects.filter(user = user.user.username)
        u = queryset[0].matrix().dot(np.array(user.gamer_profile.vectorize()))
        all_mechanics = GMechanic.objects.all()
        v = np.ones(len(all_mechanics))
        for idx in range(len(all_mechanics)):
            for s in stats:
                if all_mechanics[idx].id == s.mechanic.id:
                    v[idx] = s.interaction_index
        print(np.matrix(u).T.dot(np.matrix(v)).diagonal())
        return np.array( np.matrix(u).T.dot(np.matrix(v)).diagonal())[0].tolist()

    def select_mechanic(self,utilities):
        # UTILITIES :: "UserType-Mechanics Matrix" update policy 
        # input  queryset : QuerySet
        #        user : Gamer
        # return Mv : List
        print("Concrete Implementation of the Mechanic Selection")
        # DEFAULT :: "Choosing random index between argmax indexes" update policy
        #print("Uts",utilities)
        idx = rdm.choice(np.argwhere(utilities == np.amax(utilities)).flatten().tolist())
        #print(np.argwhere(utilities == np.amax(utilities)).flatten().tolist())
        return GMechanic.objects.all()[idx]




