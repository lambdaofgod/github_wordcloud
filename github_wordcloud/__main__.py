import click
from .github_wordcloud import make_starred_repository_wordcloud


@click.command()
@click.option('--username', help='Whose starred repositories we will fetch')
@click.option(
    '--extracted_information', default='topics',
    help='What information to extract: topics, description or description_keywords')
@click.option(
    '--filename', default=None,
    help='Optional: filename for saving word cloud image')
def main(username, extracted_information, filename):
    make_starred_repository_wordcloud(username, extracted_information, filename)


if __name__ == '__main__':
    main()
