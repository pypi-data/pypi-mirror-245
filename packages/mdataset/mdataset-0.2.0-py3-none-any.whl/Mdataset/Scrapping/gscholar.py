from scholarly import scholarly

def search_author_and_print(author_name):
    search_query = scholarly.search_author(author_name)
    first_author_result = next(search_query)
    scholarly.pprint(first_author_result)

def retrieve_author_details_and_print(author_result):
    author = scholarly.fill(author_result)
    scholarly.pprint(author)

def retrieve_first_publication_and_print(author_result):
    first_publication = author_result['publications'][0]
    first_publication_filled = scholarly.fill(first_publication)
    scholarly.pprint(first_publication_filled)

def print_publication_titles(author_result):
    publication_titles = [pub['bib']['title'] for pub in author_result['publications']]
    print(publication_titles)

def print_citations_for_first_publication(author_result):
    first_publication = author_result['publications'][0]
    first_publication_filled = scholarly.fill(first_publication)
    citations = [citation['bib']['title'] for citation in scholarly.citedby(first_publication_filled)]
    print(citations)
