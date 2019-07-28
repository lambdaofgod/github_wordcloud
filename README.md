# github_wordcloud

![](assets/wordcloud.png)

Generate wordclouds from Github repositories information

## Usage:

[Example notebook](https://colab.research.google.com/drive/1rO5nUX9VIKOrabL-_IAHwgeS37P2fbRe)

**Fetching user's starred repositories**

`python -m github_wordcloud --username {Github username} --extracted_information topics`

**Fetching github repository search results**

`python -m github_wordcloud --query 'topic:machine-learning'`


By default `--extracted_information` is set to `topics`, but you can also use `description` or `description_keywords` (keywords are extracted using gensim's TextRank)