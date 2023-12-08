import subprocess

def run_command(command):
    try:
        result = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output}")

def text_search(keyword, region='', proxy=''):
    command = ['ddgs', 'text', '-k', keyword]

    if region:
        command.extend(['-r', region])

    if proxy:
        command.extend(['-p', proxy])

    run_command(command)

def text_search_with_download(keyword, file_type='', max_results=50, region='', proxy=''):
    command = ['ddgs', 'text', '-k', f'"{keyword} {file_type}"', '-m', str(max_results), '-d']

    if region:
        command.extend(['-r', region])

    if proxy:
        command.extend(['-p', proxy])

    run_command(command)

def image_search(keyword, region='', proxy='', max_results=500, download=False, threads=1):
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
    command = ['ddgs', 'news', '-k', keyword]

    if not safe_search:
        command.append('-s off')

    command.extend(['-t', time_filter, '-m', str(max_results)])

    if output_format:
        command.extend(['-o', output_format])

    run_command(command)

def save_news_to_csv(keyword, time_filter='d', max_results=50):
    command = ['ddgs', 'news', '-k', keyword, '-t', time_filter, '-m', str(max_results), '-o', 'csv']
    run_command(command)

def answers_search(keyword, output_format=''):
    command = ['ddgs', 'answers', '-k', keyword]

    if output_format:
        command.extend(['-o', output_format])

    run_command(command)