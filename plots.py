import matplotlib.pyplot as plt
import pandas as pd
import json

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


def plot_20_ext(testing,external_profiles,k):

    precision = []
    recall=[]
    for i in testing:
        followers = []


        followers.extend(i['followers'])
        count=0
        external_followers=[]
        for j in range(len(external_profiles)):


                if (external_profiles.iloc[j, 3] == i['id']):


                      external_followers.append(external_profiles.iloc[j, 2])

        external_followers = sorted(external_followers, reverse=True)
        for m in range(k):
            if(external_followers[m] in followers ):
                count+=1
        TP=count
        FP=k-count
        FN=len(followers)-count

        precision.append(TP/(TP+FP))
        if((TP+FN)!=0):
            recall.append(TP/(TP+FN))
        else:
            recall.append(0)
    # print(recall)
    # print(precision)
    return float(sum(recall)/len(recall)),float(sum(precision)/len(precision))



if __name__ == '__main__':
    results = pd.DataFrame([]);
    results_prec=pd.DataFrame([]);

    hash_profiles = pd.read_csv("FinalOutput_hash.csv")
    tweet_profiles = pd.read_csv("FinalOutput_tweet.csv")
    external_profiles = pd.read_csv("FinalOutput.csv")

    testing = loadTestingProfileIDs(profiles_path + 'testing_profile_ids.txt')
    profiles = parseProfiles(data_path + 'vectorized_profiles.json')
    training, testing = seperateTesting(profiles, testing)


    recall_ext_20, precision_ext_20 = plot_20_ext(testing,external_profiles,20)
    recall_tweet_20, precision_tweet_20 = plot_20_ext(testing,tweet_profiles,20)
    recall_hash_20, precision_hash_20 = plot_20_ext(testing,hash_profiles,20)

    recall_ext_10, precision_ext_10 = plot_20_ext(testing,external_profiles,10)
    recall_tweet_10, precision_tweet_10 =plot_20_ext(testing,tweet_profiles,10)
    recall_hash_10, precision_hash_10 = plot_20_ext(testing,hash_profiles,10)


    recall_ext_15, precision_ext_15 = plot_20_ext(testing,external_profiles,15)
    recall_tweet_15, precision_tweet_15 = plot_20_ext(testing,tweet_profiles,15)
    recall_hash_15, precision_hash_15 = plot_20_ext(testing,hash_profiles,15)

    recall_ext_5, precision_ext_5 = plot_20_ext(testing,external_profiles,5)
    recall_tweet_5, precision_tweet_5 = plot_20_ext(testing,tweet_profiles,5)
    recall_hash_5, precision_hash_5 = plot_20_ext(testing,hash_profiles,5)

    results = results.append(
        pd.DataFrame({'recall_ext20':recall_ext_20,'recall_tweet20':recall_tweet_20,'recall_hash20':recall_hash_20,'recall_ext10':recall_ext_10,'recall_tweet10':recall_tweet_10,
                      'recall_hash10':recall_hash_10,'recall_ext15':recall_ext_15,'recall_tweet15':recall_tweet_15
                      ,'recall_hash15':recall_hash_15,'recall_ext5':recall_ext_5,'recall_tweet5':recall_tweet_5,'recall_hash5':recall_hash_5},index=[0]), ignore_index=True)
    results.to_csv("plot.csv")

    results_prec = results_prec.append(
        pd.DataFrame({'precision_ext20': precision_ext_20, 'precision_tweet20': precision_tweet_20,
                      'precision_hash20': precision_hash_20,
                      'precision_ext10': precision_ext_10, 'precision_tweet10': precision_tweet_10,
                      'precision_hash10': precision_hash_10, 'precision_ext15': precision_ext_15,
                      'precision_tweet15': precision_tweet_15
                         , 'precision_hash15': precision_hash_15, 'precision_ext5': precision_ext_5,
                      'precision_tweet5': precision_tweet_5, 'precision_hash5': precision_hash_5}, index=[0]),
        ignore_index=True)
    results_prec.to_csv("plot_Prec.csv")


    # y = [[recall_ext_20, recall_ext_15, recall_ext_10, recall_ext_5],
    #      [recall_hash_20, recall_hash_15, recall_hash_15, recall_hash_5],
    #      [recall_tweet_20, recall_tweet_15, recall_tweet_10, recall_tweet_5]]
    # x = [20, 15, 10, 5]
    # plt.plot(x, y)
    # plt.show()