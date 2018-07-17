#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 10:03:03 2018

@author: alan
"""

import json
import math

# paths for data
data_path = '../Data/'
resources_path = data_path + 'Resources/'
profiles_path = data_path + 'Profiles/'
output_path = data_path + 'Output/'

# In[6]: to load the IDs of selected profiles
def loadTestingProfileIDs(filename):        
    ids = set()    
    with open(filename, 'r') as file:
        ids.update([int(token.strip()) for token in file])
            
    return ids 

# In[5]: write updated profiles in file
def saveProfiles(profiles, outfile):    
    with open(outfile, 'w') as file:
        for profile in profiles:
            file.write(json.dumps(profile) + '\n')

# In[4.5]: tfidf given lemmas features and idfs       
def getTFIDF(lemmas, features, idf):
    tfidf = []
    
    for i in range(len(features)):
        tf = math.log(1 + lemmas.count(features[i]))
        tfidf.append(tf * idf[i])
        
    # return tdidf
    return tfidf
    
# In[4]: compute tdidf for testing profile
def calculateOtherTFIDF(profiles, testing, features):
    # first find the static idfs
    idf = calculateIDF(profiles, features)
    
    print("Calculating TF-IDF for testing profiles...")
    
    for profile in profiles:     
        
        if profile['id'] not in testing:
            profile['external_tfidf'] = []
            profile['hashtag_tfidf'] = []
            continue
        
        # tfidf for hashtags
        lemmas = profile['hashtag_lemmas']           
        profile['hashtag_tfidf'] = getTFIDF(lemmas, features, idf)
        
        # tfidf for external text
        lemmas = profile['external_lemmas']           
        profile['external_tfidf'] = getTFIDF(lemmas, features, idf)
                                                
    return profiles    

# In[4]: compute tdidf for each profile
def calculateTFIDF(profiles, features):    
    
    # first find the static idfs
    idf = calculateIDF(profiles, features)
    
    print("Calculating TF-IDF...")
    
    for profile in profiles:        
                        
        # tfidf for tweet text for all profiles    
        lemmas = profile['tweet_lemmas']
        profile['tweet_tfidf'] = getTFIDF(lemmas, features, idf)
                                
    return profiles    

# In[3]: compute term idf
def calculateIDF(profiles, features): 
    
    print("Calculating IDF...")
    
    # num of docs
    doc_num = len(profiles)
    idf = []
    
    # find idf for all terms
    for feature in features:
        
        # doc freq
        doc_count = 0;                
        for profile in profiles:            
            if feature in profile['tweet_lemmas']:
                doc_count = doc_count + 1
            else:
                continue
        
        # calculate idf for current term
        idf.append(math.log(doc_num) - math.log(doc_count))
        
    # idfs is parallel with features
    return idf

# In[2]: load features
def loadFeatures(file):  
    features = []
    
    # open features file: feature, count\n
    with open(file, 'r') as features_file:
        lines = features_file.read().splitlines() 
        
        for line in lines:
            feature = line.split(",")[0]
            features.append(feature)
            
            # get top 100 lemmas
            if len(features) >= 100:
                break
        
    return features        

# In[1]: parse user profiles
def parseProfiles(file):     
    profiles = []
    
    print("Parsing profiles...")
        
    # each file has many profiles
    with open(file, 'r') as user_profiles:  
        user_profiles = user_profiles.readlines()
        
        # load each profile
        for profile in user_profiles: 
            dictdump = json.loads(profile)
            
            user_data = dict()
            user_data['external_lemmas'] = dictdump['external_lemmas']
            user_data['hashtag_lemmas'] = dictdump['hashtag_lemmas']            
            user_data['tweet_lemmas'] = dictdump['tweet_lemmas']
            user_data['followers'] = dictdump['followers']
            user_data['hashtags'] = dictdump['hashtags']
            user_data['external'] = dictdump['external']  
            user_data['friends'] = dictdump['friends']               
            user_data['tweets'] = dictdump['tweets']
            user_data['urls'] = dictdump['urls']        
            user_data['name'] = dictdump['name']
            user_data['id'] = dictdump['id']           
                                            
            profiles.append(user_data)
                
    return profiles

# In[0]: Main
if __name__ == '__main__':    
    testing = loadTestingProfileIDs(output_path + 'testing_profile_ids.txt')
    profiles = parseProfiles(output_path + 'processed_profiles.json')    
    features = loadFeatures(output_path + 'features.csv')
    
    profiles = calculateTFIDF(profiles, features)
    profiles = calculateOtherTFIDF(profiles, testing, features)
    
    saveProfiles(profiles, output_path + 'vectorized_profiles.json')
    
    
    