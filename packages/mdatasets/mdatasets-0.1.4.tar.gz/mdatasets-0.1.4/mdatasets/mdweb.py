import subprocess

def run_command(command):
    """
    Run a command in the system shell and print the result or error.

    Parameters:
    - command (list): The list containing the command and its arguments.

    Prints:
    - Result of the command if successful.
    - Error message if the command fails.

    Example:
    >>> run_command(['echo', 'Hello, World!'])
    Hello, World!
    """

    try:
        result = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output}")


def text_search(keyword, region='', proxy=''):
    """
    Search for text content using DuckDuckGo Search.

    Parameters:
    - keyword (str): The search keyword.
    - region (str): The region to filter the search results.
    - proxy (str): The proxy server to use for the search.

    Example:
    >>> text_search('AI research', region='US', proxy='http://proxy.example.com')
    """    
    command = ['ddgs', 'text', '-k', keyword]

    if region:
        command.extend(['-r', region])

    if proxy:
        command.extend(['-p', proxy])

    run_command(command)


def text_search_with_download(keyword, file_type='', max_results=50, region='', proxy=''):
    """
    Search for text content with download option using DuckDuckGo Search.

    Parameters:
    - keyword (str): The search keyword.
    - file_type (str): The type of files to search for.
    - max_results (int): The maximum number of results to retrieve.
    - region (str): The region to filter the search results.
    - proxy (str): The proxy server to use for the search.

    Example:
    >>> text_search_with_download('AI research papers', file_type='pdf', max_results=10, region='US')
    """

    command = ['ddgs', 'text', '-k', f'"{keyword} {file_type}"', '-m', str(max_results), '-d']

    if region:
        command.extend(['-r', region])

    if proxy:
        command.extend(['-p', proxy])

    run_command(command)


def image_search(keyword, region='', proxy='', max_results=500, download=False, threads=1):
    """
    Search for images using DuckDuckGo Search.

    Parameters:
    - keyword (str): The search keyword.
    - region (str): The region to filter the search results.
    - proxy (str): The proxy server to use for the search.
    - max_results (int): The maximum number of image results to retrieve.
    - download (bool): If True, download the images.
    - threads (int): Number of threads to use for image download.

    Example:
    >>> image_search('AI technology', region='US', proxy='http://proxy.example.com', download=True, threads=2)
    """

    command = ['ddgs', 'images', '-k', keyword]

    if region:
        command.extend(['-r', region])

    if proxy:
        command.extend(['-p', proxy])

    if download:
        command.extend(['-m', str(max_results), '-d'])

    if threads > 1:
        command.extend(['-th', str(threads)])

    run_command(command)


def news_search(keyword, safe_search=True, time_filter='d', max_results=10, output_format=''):
    """
    Search for news articles using DuckDuckGo Search.

    Parameters:
    - keyword (str): The search keyword.
    - safe_search (bool): If True, enable safe search.
    - time_filter (str): The time filter for news articles ('d' for last day, 'w' for last week, etc.).
    - max_results (int): The maximum number of news results to retrieve.
    - output_format (str): The output format for news results.

    Example:
    >>> news_search('AI advancements', safe_search=False, time_filter='w', max_results=5, output_format='json')
    """

    command = ['ddgs', 'news', '-k', keyword]

    if not safe_search:
        command.append('-s off')

    command.extend(['-t', time_filter, '-m', str(max_results)])

    if output_format:
        command.extend(['-o', output_format])

    run_command(command)


def save_news_tocsv(keyword, time_filter='d', max_results=50):
    """
    Save news articles to a CSV file using DuckDuckGo Search.

    Parameters:
    - keyword (str): The search keyword.
    - time_filter (str): The time filter for news articles ('d' for last day, 'w' for last week, etc.).
    - max_results (int): The maximum number of news results to retrieve and save to CSV.

    Example:
    >>> save_news_to_csv('AI research', time_filter='m', max_results=20)
    """

    command = ['ddgs', 'news', '-k', keyword, '-t', time_filter, '-m', str(max_results), '-o', 'csv']
    run_command(command)


def answers_search(keyword, output_format=''):
    """
    Search for answers using DuckDuckGo Search.

    Parameters:
    - keyword (str): The search keyword.
    - output_format (str): The output format for answer results.

    Example:
    >>> answers_search('Machine Learning', output_format='json')
    """

    command = ['ddgs', 'answers', '-k', keyword]

    if output_format:
        command.extend(['-o', output_format])

    run_command(command)
