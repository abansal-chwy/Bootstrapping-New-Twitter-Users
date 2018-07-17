from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import json
import numpy as np
from scipy import spatial
from scipy.spatial.distance import cdist
import operator
import matplotlib.pyplot as plt
# array1=np.array([0.0, 0.0, 0.0, 0.0]).reshape(-1,1)
# array2=np.array([1.5886342393349817, 1.6787580506949253, 1.0116403767747946, 0.0]).reshape(-1,1)


print(cosine_similarity([[0.0, 0.0, 0.0, 0.0]],
                       [[1.5886342393349817, 1.6787580506949253, 1.0116403767747946, 0.0]]))
data_path = 'Data/'
profiles_path = data_path + 'Profiles/'
output_path = data_path + 'Output/'


def loadTestingProfileIDs(filename):
    ids = set()
    with open(filename, 'r') as file:
        ids.update([int(token.strip()) for token in file])

    return ids


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
            user_data['hashtag_tfidf'] = dictdump['hashtag_tfidf']
            user_data['external_tfidf'] = dictdump['external_tfidf']
            user_data['tweet_tfidf'] = dictdump['tweet_tfidf']

            profiles.append(user_data)

    return profiles


def seperateTesting(profiles,testingID):

        print("Seperating Training and Testing Profiles")

        # seperate training and testing
        training=[]
        testing=[]

        id=testingID
        for profile in profiles:

            if profile['id'] in id:
                testing.append(profile)
            else:
                training.append(profile)



        return training,testing




def Findsimilarity(training,testing):

    print("Finding Similarity..")
    results_external=pd.DataFrame([])
    results_hash = pd.DataFrame([])
    results_tweet = pd.DataFrame([])
    testingProfiles=testing

    for i in testing:
        trainingProfiles = (training+testing)
        del[trainingProfiles["id"==i]]

        similaity_hash = []
        similaity_tweet = []
        similaity_external = []

        sim_hash=dict()
        sim_tweet=dict()
        sim_ext=dict()

        for j in trainingProfiles:



            hash_sim=cosine_similarity([i['hashtag_tfidf']], [j['tweet_tfidf']])
            hash_sim=str(hash_sim).replace("[","")
            hash_sim=str(hash_sim).replace("]","")

            extern_sim = cosine_similarity([i['external_tfidf']], [j['tweet_tfidf']])
            extern_sim = str(extern_sim).replace("[", "")
            extern_sim = str(extern_sim).replace("]", "")

            tweet_sim = cosine_similarity([i['tweet_tfidf']], [j['tweet_tfidf']])
            tweet_sim = str(tweet_sim).replace("[", "")
            tweet_sim = str(tweet_sim).replace("]", "")

            #results = results.append(pd.DataFrame({'TestID': i, 'NieghborID': j,'hashTFIDF':hash_sim},index=[0]), ignore_index=True)

            sim_hash[j['id']]=hash_sim
            sim_ext[j['id']]=extern_sim
            sim_tweet[j['id']]=tweet_sim
        #
        # sorted_hash=(sorted(sim_hash.items(), key=operator.itemgetter(1), reverse=True)[:20])
        # sorted_external = (sorted(sim_ext.items(), key=operator.itemgetter(1), reverse=True)[:20])
        # sorted_tweet = (sorted(sim_tweet.items(),key=operator.itemgetter(1), reverse=True)[:20])

        for k, v in (sorted(sim_ext.items(), key=operator.itemgetter(1), reverse=True)[:20]):

            results_external = results_external.append(pd.DataFrame({'TestID': i['id'], 'NieghborID': k, 'ExternalTFIDF': v,
                                                  },index=[0]),ignore_index=True)
            results_external.to_csv("FinalOutput.csv")

        for k, v in (sorted(sim_hash.items(), key=operator.itemgetter(1), reverse=True)[:20]):
            results_hash = results_hash.append(
                pd.DataFrame({'TestID': i['id'], 'NieghborID': k, 'ExternalTFIDF': v,
                              }, index=[0]), ignore_index=True)
            results_hash.to_csv("FinalOutput_hash.csv")

        for k, v in (sorted(sim_tweet.items(), key=operator.itemgetter(1), reverse=True)[:20]):

            results_tweet = results_tweet.append(pd.DataFrame({'TestID': i['id'], 'NieghborID': k, 'ExternalTFIDF': v,
                                                  },index=[0]),ignore_index=True)
            results_tweet.to_csv("FinalOutput_tweet.csv")





if __name__ == '__main__':
    testing = loadTestingProfileIDs(profiles_path + 'testing_profile_ids.txt')
    profiles = parseProfiles(data_path + 'vectorized_profiles.json')
    training,testing=seperateTesting(profiles,testing)
    similaity=Findsimilarity(training,testing)
