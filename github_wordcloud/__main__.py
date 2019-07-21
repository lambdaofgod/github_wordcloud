import click
from .github_wordcloud import make_starred_repository_wordcloud


@click.command()
@click.option('--username')
@click.option('--extracted_information', default='topics')
@click.option('--filename', default=None)
def main(username, extracted_information, filename):
    make_starred_repository_wordcloud(username, extracted_information, filename)


if __name__ == '__main__':
    main()
