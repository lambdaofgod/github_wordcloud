import matplotlib.pyplot as plt
import requests
import wordcloud
from gensim import summarization
from pandas.io.json import json_normalize


def make_repository_wordcloud(username, query, extracted_information, pages, filename=None):
    is_extracted_information_valid = extracted_information in ['topics', 'description', 'description_keywords']
    assert is_extracted_information_valid, 'We do not have data on ' + str(extracted_information)
    if username != '':
        title = str(username) + "'s starred repositories"
        repo_information_df = get_cleaned_repositories_df(get_starred_repos_for_user(username))
    else:
        title = 'Query: ' + query
        repo_information_df = get_cleaned_repositories_df(get_searched_repositories(query, pages=pages))

    texts = repo_information_df[extracted_information]
    wc = get_word_cloud(texts)
    if filename is None:
        show_word_cloud(wc, figure_kwargs={'figsize': (8, 5)}, title=title)
    else:
        wc.to_file(filename)


# github API
def get_response_from_url(url, pages=10):
    def get_items(tmp_response):
        tmp_response_json = tmp_response.json()
        if type(tmp_response_json) is dict:
            return tmp_response_json.get('items', [])
        else:
            return tmp_response_json
    responses = []
    url = url.replace('%F%', '{}')
    i = 1
    tmp_response = requests.get(url.format(i), headers={"Accept": "application/vnd.github.mercy-preview+json"})
    tmp_response_items = get_items(tmp_response)
    while tmp_response.ok and len(tmp_response_items) > 0 and i <= pages:
        responses = responses + tmp_response_items
        i += 1
        tmp_response = requests.get(url.format(i), headers={"Accept": "application/vnd.github.mercy-preview+json"})
        tmp_response_items = get_items(tmp_response)

    if len(responses) == 0:
        raise requests.HTTPError('Error occured while fetching, most likely you went over rate limit')
    else:
        return responses


def get_starred_repos_for_user(username):
    url = 'https://api.github.com/users/{}/starred?page=%F%&per_page=100'.format(username)
    return get_response_from_url(url)


def get_searched_repositories(query, pages=10, headers=dict()):
    url = 'https://api.github.com/search/repositories?q={}&page=%F%&per_page=100'.format(query)
    return get_response_from_url(url, pages=pages)


def get_cleaned_repositories_df(repo_information):
    repo_df = json_normalize(repo_information)
    repo_df.index = repo_df['name']
    repo_df.drop('name', axis=1, inplace=True)
    repo_df['topics'] = repo_df['topics'].apply(' '.join)
    repo_df['description'] = repo_df['description'].fillna('')
    repo_df['description_keywords'] = repo_df['description'].apply(summarization.keywords)
    return repo_df


# Wordclouds
def get_word_cloud(texts):
    text = ' '.join(texts)
    return wordcloud.WordCloud(max_font_size=40).generate(text)


def show_word_cloud(wc, figure_kwargs, title):
    plt.figure(**figure_kwargs)
    plt.title(title)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()

  
def show_word_cloud_from_texts(text_column):
    texts = text_column.fillna('').values
    cloud = get_word_cloud(texts)
    show_word_cloud(cloud, {}, '')
