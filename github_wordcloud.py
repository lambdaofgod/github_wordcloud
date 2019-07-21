import matplotlib.pyplot as plt
import requests
import wordcloud
from pandas.io.json import json_normalize
from gensim import summarization
import click


def make_starred_repository_wordcloud(username, extracted_information, filename=None):
    is_extracted_information_valid = extracted_information in ['topics', 'description', 'description_keywords']
    assert is_extracted_information_valid, 'We do not have data on ' + str(extracted_information)
    repo_information_df = get_cleaned_starred_repositories_df(get_starred_repos_for_user(username))
    texts = repo_information_df[extracted_information]
    wc = get_word_cloud(texts)
    if filename is None:
        show_word_cloud(wc, figure_kwargs={'figsize': (8, 5)}, title=str(username) + "'s starred repositories")
    else:
        wc.to_file(filename)


# github API
def get_starred_repos_for_user(username):
    i = 1
    query = 'https://api.github.com/users/{}/starred?page={}&per_page=100'
    starred_response = []
    tmp_response = requests.get(query.format(username, i), headers={"Accept": "application/vnd.github.mercy-preview+json"})
    while tmp_response.ok and len(tmp_response.json()):
        starred_response = starred_response + tmp_response.json()
        i += 1
        tmp_response = requests.get(query.format(username, i), headers={"Accept": "application/vnd.github.mercy-preview+json"})

    if len(starred_response) == 0:
        raise requests.HTTPError('Error occured while fetching, most likely you went over rate limit')
    else:
        return starred_response


def get_cleaned_starred_repositories_df(repo_information):
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


@click.command()
@click.option('--username')
@click.option('--extracted_information', default='topics')
@click.option('--filename', default=None)
def main(username, extracted_information, filename):
    make_starred_repository_wordcloud(username, extracted_information, filename)


if __name__ == '__main__':
    main()