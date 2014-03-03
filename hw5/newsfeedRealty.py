# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 22:36:36 2014

@author: cbeery
"""

from pattern.web import *


def addWeightToRelationship(person,dictionary):
    """ 
    adds a unit of "significance" to interaction of the active party; also
    creates new entry in dictionary if interaction from party does not yet
    exist
    
    INPUTS  person, normally in form of tuple: id#, name  
            dictionary, dict of raw interaction frequencies to this point for friend
    OUTPUT  dictionary, updated
    """ 
         
    if person == 'other':
        name = person
    else:
        name = person[1]
        name = name.encode('ascii','ignore') 
            
    
    if name in dictionary:
        dictionary[name] += 1
    else:
        dictionary[name] = 1
        
    return dictionary

def searchNews(news,me,my_friends,friend,name,oneDict):
    """ 
    finds the author of the current posting and adds one the tally of that author
    
    INPUTS  news, current post id
            me, user id and name
            my_friends, list of user friends (Pattern class, form: id#,name)
            friend, current friend being examined (.id gives id#)
            oneDict, dictionary to be updated with frrquency of postings per author
    OUTPUT  oneDict, updated
    """

        
    if news.author[0] == friend.id: #if self post
        oneDict = addWeightToRelationship(news.author, oneDict)
            
        # assign current friend a name
        if name == 0:
            name = news.author[1]
            name = name.encode('ascii','ignore') 
                
    elif news.author[0] == me[0]: #if user post
        oneDict = addWeightToRelationship(news.author, oneDict)
            
    else:  
            
        for otherFriend in my_friends:   #if friend group post
             if news.author[0] == otherFriend.id:                       
                 oneDict = addWeightToRelationship(news.author, oneDict)
                 break
                    
             else:   #if post not from friend group                         
                 oneDict = addWeightToRelationship('other', oneDict) 
                
    return oneDict, name
    

def freqToPercent(dictionary):
    """ 
    Turns a dictionary of tally frequency into a dictionary of percent of 
    total posts     
    """
    
    #find total posts
    total = 0   
    for key in dictionary:
        total += dictionary[key]
        
    for key in dictionary:
        x = dictionary[key]/float(total)
        dictionary[key] = int(x * 10000) / 10000.0
        
    return dictionary
    
    
def analyzeOneFriend(f,me,my_friends,friend,time):
    """ 
    finds the likelyhood a wall post is from any of the user's friends
    
    INPUT:  f, user's profile permission
            me, user id and name
            my_friends, list of user friends (Pattern class, form: id#,name)
            friend, current friend being examined (.id gives id#)
            time, posts to be looked at
    OUTPUTS: oneFriend, dictionary of source of wall posts
                form: {Meg:.1, user:.2, Chris:.55, others:.05,Justin:.1}
             name, name of friend
            
    """
    
    # store friend's newsfeed
    friend_news = f.search(friend.id, type=NEWS, count=time)
    
    #storage
    oneDict = {} #raw frequency of interactions
    name = 0
    
    # for each entry in newsfeed, check author
    for news in friend_news:
        oneDict, name = searchNews(news,me,my_friends,friend,name,oneDict)
   
    # turn frequencies into percents
    oneFriend = freqToPercent(oneDict)
    
    return name,oneFriend
                    
                
def analyzeAllFriends(f,me,my_friends,time):
    """ 
    for any of the user's friends, finds the percentage distribution of 
    post contributorsfor their wall
    
    INPUT:  f, user's profile permission
            me, user id and name
            my_friends, list of user friends (Pattern class, form: id#,name)
            time, posts to be looked at
    """
    
    allDict = {}
    
    for friend in my_friends:
        name, oneFriend = analyzeOneFriend(f,me,my_friends,friend,time)
        allDict[name] = oneFriend
        
    return allDict

def newsfeedRealty(api,time):
    """ 
    Creates a dictionary of dictionaries for each facebook friend of user;
    the inter-dictionary defines who is responsible for what percentage of  
    the newsfeed for each friend
    
    INPUTS: api, string defining whose account is being accessed as the user
            time, number of posts per friend being accounted for (max 10,000)
    OUTPUT: dictionary, form:   {friend1:{friend2:.5001, you:, .0009,friend1:.4000}, 
                                 friend2:{friend2:.0001, others:.9999}}
    
    """
    
    # create profile
    f = Facebook(license=api)
    user = f.profile()
   
    # create people
    my_friends = f.search(user[0], type=FRIENDS, count=10000)
    reformatted_user = user[0], user[1]
   
    # create interaction ratios for all friends
    dictionary = analyzeAllFriends(f,reformatted_user,my_friends,time)
    
    
    return dictionary


if __name__ == '__main__':
   api = '' #place facebook lincense code here
   numPostHistory = 10000
   dictionary = newsfeedRealty(api,numPostHistory)
   print str(dictionary)
