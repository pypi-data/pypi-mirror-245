from multiprocessing.pool import ThreadPool
from torpy.http.requests import tor_requests_session

def get_tor_multiprocessing(links, num_threads=3):
    """
    Perform HTTP GET requests using Tor for multiple links in parallel.

    Parameters:
    - links: A list of target URLs to perform GET requests.
    - num_threads: The number of threads to use in the ThreadPool (default is 3).

    Returns:
    - A list of responses received from the target URLs.
    """
    with tor_requests_session() as s:
        # Use ThreadPool for parallel GET requests
        with ThreadPool(num_threads) as pool:
            # Map the get method over the links
            responses = pool.map(s.get, links)

    return responses


# links_to_fetch = ['http://nzxj65x32vh2fkhk.onion', 'http://facebookcorewwwi.onion'] * 2
# responses = get_with_tor_multiprocessing(links_to_fetch)
# print(responses)
