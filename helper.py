# from urlextract import URLExtract
#
#
# def helper(selected_user , df):
#     if selected_user=='Overall Analysis':
#         number_messages=df.shape[0]
#         words = []
#         for i in df['message']:
#             words.extend(i.split())
#         media_files= len(df[df['message']=='<Media omitted>'])
#         links = []
#         extractor = URLExtract()
#         for i in df['message']:
#             links.extend(extractor.find_urls(i))
#         return number_messages , len(words) , media_files , len(links)
#     else:
#         new_df=(df[df['user']==selected_user])
#         number_messages = new_df.shape[0]
#         words = []
#         for i in new_df['message']:
#             words.extend(i.split())
#         media_files = len(new_df[new_df['message'] == '<Media omitted>'])
#         links = []
#         extractor = URLExtract()
#         for i in new_df['message']:
#             links.extend(extractor.find_urls(i))


#         return number_messages, len(words), media_files, len(links)

from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import seaborn as sns

import matplotlib.pyplot as plt
def fetch_stats(selected_user, df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]
    number_messages = df.shape[0]
    words = sum(df['message'].str.split().tolist(), [])
    media_files = (df['message'] == '<Media omitted>').sum()
    extractor = URLExtract()
    links = sum(df['message'].apply(extractor.find_urls).tolist(), [])
    return number_messages, len(words), media_files, len(links)

def overall_analysis(df):
    x = df['user'].value_counts().head()
    new_df=round((df['user'].value_counts() / len(df)) * 100, 2).reset_index().rename(
        columns={'user': 'Users', 'count': 'Total Contribution'})
    return x , new_df

def word_cloud(selected_user , df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']
    temp = temp[temp['message'] != 'You deleted this message']
    temp = temp[temp['message'] != 'null']
    temp = temp[temp['message'] != 'This message was deleted']
    with open('stop_hinglish.txt', 'r') as file:
        lines = file.readlines()
    stopwords = [line.rstrip('\n') for line in lines]
    corpus = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                corpus.append(word)
    text = " ".join(corpus)
    wc= WordCloud(width=800, height=400, background_color='white').generate(text)
    return wc

def most_common(selected_user , df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']
    temp = temp[temp['message'] != 'You deleted this message']
    temp = temp[temp['message'] != 'null']
    temp = temp[temp['message'] != 'This message was deleted']
    with open('stop_hinglish.txt', 'r') as file:
        lines = file.readlines()
    stopwords = [line.rstrip('\n') for line in lines]
    corpus = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                corpus.append(word)
    frequency_counter = Counter(corpus)

    top_25 = frequency_counter.most_common(25)
    final_df = pd.DataFrame(top_25).rename(columns={0: 'Word', 1: 'Frequency'})
    return final_df

def emoji_fetch(selected_user , df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_counts = Counter(emojis).most_common()
    df_emojis = pd.DataFrame(emoji_counts, columns=['Emoji', 'Count'])
    return df_emojis

def timeline(selected_user , df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    df['year_month'] = df['date'].dt.to_period('M')

    monthly_counts = df['year_month'].value_counts().sort_index()
    return monthly_counts

def monthly(selected_user , df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    months=df['month'].value_counts()
    return months

def daily(selected_user , df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    df['day_of_week'] = df['date'].dt.day_name()
    days=df['day_of_week'].value_counts()
    return days
