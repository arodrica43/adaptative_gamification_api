from django.db import models
from django.contrib.auth.models import User, Group
from enum import Enum
from enumfields import EnumField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
#from django.db.models.manager import EmptyManager
from jsonfield import JSONField
import json


def default_data_dict():
        return {"data": "This is the default data. Follow this example to fill gamer data."}

class EmotionProfile(models.Model):
    valence =  models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],default=0)
    arousal =  models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],default=0)

class GamerProfile(models.Model):
    #user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    disruptor = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],default=1)
    free_spirit = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],default=1)
    achiever = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],default=1)
    player = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],default=1)
    socializer = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],default=1)
    philantropist = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],default=1)
    no_player = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],default=0)
    data = JSONField(default = dict)

    
    associated_mechanic = {
        'disruptor':'Change',
        'free_spirit':'Autonomy',
        'achiever':'Mastery',
        'player':'Reward',
        'socializer':'Relatedness',
        'philantropist':'Purpose',
        'no_player':'',
        -1: 'Unknown',
        0:'Change',
        1:'Autonomy',
        2:'Mastery',
        3:'Reward',
        4:'Relatedness',
        5:'Purpose',
        6:''
    }

    def vectorize(self):
        return (self.disruptor,self.free_spirit,self.achiever,self.player,self.socializer,self.philantropist,self.no_player)

class SocialProfile(models.Model):

    class AvatarType(Enum):   # A subclass of Enum
        art = "art"
        diamond = "diamond"
        games = "games"
        money = "money"
        music = "music"
        photo = "photo"
        science = "science"
        tech = "tech" 
        user = "user"
    
    image = EnumField(AvatarType,max_length=11,default = AvatarType.diamond)
    description = models.TextField(default="")
    data = JSONField(default = list)       

# class GamificationProfile(models.Model):
#     #user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
#     disruptor = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],)
#     free_spirit = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],)
#     achiever = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],)
#     player = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],)
#     socializer = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],)
#     philantropist = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],)
#     no_player = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],)

def username_exists(value):
    qs = Gamer.objects.filter(user__username = value)
    if len(qs) == 0:
        raise ValidationError(
            _('%(value)s is not an existing username'),
            params={'value': value},
        )

def unique_individual_group(value):
    #print("Hey Hey")
    #print(value)
    #print(value['groups'])
    if 'groups' in value.keys():
        groups =  value['groups']
        #print("groups: ",groups)
        for g in groups:
            if len(g.name) >= 10:
                if g.name[:10] == 'individual' and g.name[10:] != '_' + value['username']:
                    raise ValidationError(
                        _('An user cannot be in an individual group other than its default'),
                        params={'value': value},
                    )
    else:
        raise ValidationError(
                        _('Every user should be in its own individual group. Automathically added.'),
                        params={'value': value},
                    )

class Gamer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    emotion_profile = models.OneToOneField(EmotionProfile, on_delete=models.CASCADE)
    gamer_profile =  models.OneToOneField(GamerProfile, on_delete=models.CASCADE)
    social_profile =  models.OneToOneField(SocialProfile, on_delete=models.CASCADE)

class GMechanic(models.Model):

    class MechanicType(Enum):   # A subclass of Enum
        Change = "Change"
        Autonomy = "Autonomy"
        Mastery = "Mastery"
        Reward = "Reward"
        Relatedness = "Relatedness"
        Purpose = "Purpose"
        Unknown = "Unknown"

    title = models.CharField(max_length=255)
    html = models.TextField(default="")
    mechanic_type = EnumField(MechanicType,max_length=11,default = MechanicType.Unknown)
    #owners = models.CharField(max_length=200,default = '', validators=[username_exists])
    #owners = models.ManyToManyField(Group)
    #statistics = models.ManyToManyField(InteractionStatistic) #JSONField(default = list)
    associated_profile = {
        'Change':0,
        'Autonomy':1,
        'Mastery':2,
        'Reward':3,
        'Relatedness':4,
        'Purpose':5,
        'Unknown':-1
    }


    def matrix(self):
        import numpy as np
        all_mechanics =  GMechanic.objects.all()
        M = np.zeros((len(all_mechanics),7))
        for i in range(len(all_mechanics)):
            idx = all_mechanics[i].associated_profile[all_mechanics[i].mechanic_type.value]
            if idx != -1:
                M[i,idx] = 1
        #print(M)
        return M

    def statistics_vector(self,user):
        all_mechanics = GMechanic.objects.all()
        v = []
        for gm in all_mechanics:
            stat_i = InteractionStatistic.objects.filter(user=user, mechanic = gm)
            if stat_i:
                stat_i = stat_i[0].interaction_index
                v += [stat_i] 
        #print(v, len(v))
        return v
        


# TO DO: Make class extensions to differentiate between GMechanics interaction statistics and GComponent statistics
#   For now, it's enough to add the field <mechanic> here.
class InteractionStatistic(models.Model):
    mechanic = models.ForeignKey(GMechanic, related_name='statistics',on_delete = models.CASCADE)
    #user = models.ForeignKey(Gamer,on_delete=models.CASCADE)
    # If we want to create statistics related to a user by the username, we should valdate that it exists
    # TO DO: Validate existence of gamer with username = <user>
    user = models.CharField(max_length=255, validators=[username_exists])
    log = JSONField(default = dict)
    # TO DO: add a logs JSON field containing <register> and <interaction index>
    interaction_index = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],)
    class Meta:
        unique_together = ("mechanic", "user")


class DevelopmentTool(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Change
            # self.fields.pop('parent') # or remove the field

    class Mechanic(Enum):   # A subclass of Enum
        Badge = "Badge"
        Unlockable = "Unlockable"
        Challenge = "Challenge"

    mechanic_class = EnumField(Mechanic,max_length=10,default = Mechanic.Badge)
    attempts =  models.IntegerField(validators=[MinValueValidator(1)],default = 1)

class Challenge(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Change
            # self.fields.pop('parent') # or remove the field
    icon = models.ImageField(upload_to="challenge_icons", default='challenge_icons/challenge.png')
    name = models.CharField(max_length=100,default = 'Challenge')
    state = models.BooleanField(default = False)
    by = models.CharField(max_length=100,default = 'score')
    threshold = models.FloatField(default = 99999999)

    class Meta:
         unique_together = (('by', "threshold"))

class EasterEgg(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Autonomy
            # self.fields.pop('parent') # or remove the field
    feedback = models.ImageField(upload_to="easter_egg_icons", default='easter_egg_icons/well_done.jpg')
    egg_html = models.TextField(default="")


class Unlockable(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Autonomy
            # self.fields.pop('parent') # or remove the field
    icon = models.ImageField(upload_to="unlockable_icons", default='unlockable_icons/reward.png')
    name = models.CharField(max_length=100,default = 'Unlockable')
    state = models.BooleanField(default = False)
    by = models.CharField(max_length=100,default = 'score')
    threshold = models.FloatField(default = 99999999)

    locked_html = models.TextField(default="")

    class Meta:
         unique_together = (('by', "threshold"))

class Badge(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Mastery
            # self.fields.pop('parent') # or remove the field
    icon = models.ImageField(upload_to="badge_icons", default='badge_icons/reward.png')
    name = models.CharField(max_length=100,default = 'Badge')
    state = models.BooleanField(default = False)
    by = models.CharField(max_length=100,default = 'score')
    threshold = models.FloatField(default = 99999999)

    class Meta:
         unique_together = (('by', "threshold"))

class Level(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Mastery
            # self.fields.pop('parent') # or remove the field
    #user = models.CharField(max_length=200,default = '', validators=[username_exists])
    value = models.IntegerField(validators=[MinValueValidator(0)],default = 0)
    max_value = models.IntegerField(validators=[MinValueValidator(0)],default = 1)
    by = models.CharField(max_length=100,default = '')


class Point(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Reward
            # self.fields.pop('parent') # or remove the field
    user = models.CharField(max_length=200,default = '', validators=[username_exists])
    score = models.FloatField(validators=[MinValueValidator(0)],default = 0)
    given_by = models.CharField(max_length=100,default = '')

    class Meta:
         unique_together = (('user', "given_by"))

class Leaderboard(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Reward
            # self.fields.pop('parent') # or remove the field
    leadders = JSONField(default = dict) #models.ManyToManyField(Gamer)
    length = models.IntegerField(validators=[MinValueValidator(0)],default = 0)
    sort_by = models.CharField(max_length=100,default = '')

class Lottery(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Reward
            # self.fields.pop('parent') # or remove the field
    items = JSONField(default = list)
    by = models.CharField(max_length=100,default = '')

class SocialNetwork(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Relatedness
            # self.fields.pop('parent') # or remove the field
    messages = JSONField(default = dict)

class SocialStatus(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Relatedness
            # self.fields.pop('parent') # or remove the field

    class CompetitionLevel(Enum):   # A subclass of Enum
        Low = "Low"
        Medium = "Medium"
        High = "High"

    competitiveness = EnumField(CompetitionLevel,max_length=6,default = CompetitionLevel.High)

class KnowledgeShare(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Purpose
            # self.fields.pop('parent') # or remove the field
    messages = JSONField(default = dict)

class Gift(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Purpose
            # self.fields.pop('parent') # or remove the field
    

class GiftOpener(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Reward
            # self.fields.pop('parent') # or remove the field
 

class Adaptative(GMechanic):

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        self.mechanic_type = GMechanic.MechanicType.Unknown
            # self.fields.pop('parent') # or remove the field


class GComponent(models.Model):

    class ComponentType(Enum):   # A subclass of Enum
        Block = "Block"
        Section = "Section"
        Course = "Course"
        Page = "Page"


    link =  models.CharField(max_length=2000)
    mechanics =  models.ManyToManyField(GMechanic)
    interacting_users = models.ManyToManyField(Gamer)
    component_type = EnumField(ComponentType,max_length=7) 

    # def gamification_status(self):

    #     result = {}
    #     for gm in self.mechanics.all():
    #         if not result[gm.mechanic_type]:
    #             result[gm.mechanic_type] = 1
    #         else:
    #             result[gm.mechanic_type] += 1
    #     return result
            
mechanics_list = [Adaptative, Badge, Challenge, DevelopmentTool, EasterEgg, Gift, GiftOpener, KnowledgeShare, Level, Lottery, Point, SocialNetwork, SocialStatus, Unlockable, Leaderboard]
mechanics_list_names = ['adaptatives','badges', 'challenges', 'development_tools', 'easter_eggs', 'gifts', 'gift_openers', 'knowledge_shares', 'levels', 'lotteries', 'points', 'social_networks', 'social_statuses', 'unlockables', 'leaderboards']
mechanic_list_total_interactions = {
    'badges':9, 
    'challenges':9, 
    'development_tools':30, 
    'easter_eggs':2, 
    'gifts':30, 
    'gift_openers':10, 
    'knowledge_shares':6, 
    'levels':2, 
    'lotteries':2, 
    'points':1, 
    'social_networks':35, 
    'social_statuses':20, 
    'unlockables':10, 
    'leaderboards':5
}
