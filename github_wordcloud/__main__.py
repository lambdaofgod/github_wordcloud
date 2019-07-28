import click
from .github_wordcloud import make_repository_wordcloud


@click.command()
@click.option('--username', help='Whose starred repositories we will fetch', default='')
@click.option('--query', help='Query for github repository search', default='')
@click.option(
    '--extracted_information', default='topics',
    help='What information to extract: topics, description or description_keywords')
@click.option('--pages', help='Number of returned pages (we use page size of 100)', default=10)
@click.option(
    '--filename', default=None,
    help='Optional: filename for saving word cloud image')
def main(username, query, extracted_information, pages, filename):
    specify_condition = (query != '') != (username != '')
    assert specify_condition, 'You need to specify only username for starred repositories or query for searching'
    make_repository_wordcloud(username, query, extracted_information, pages, filename)


if __name__ == '__main__':
    main()
