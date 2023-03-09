import requests
import concurrent.futures

def download_hash_file(id):
    url = f'https://virusshare.com/hashfiles/VirusShare_{str(id).zfill(5)}.md5'
    try:
        response = requests.get(url, stream=True)
        response.encoding = 'utf-8'
        return response.text
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 404:
            return None
        raise error

if __name__ == '__main__':
    print('Downloading...')
    with open('virushashes.txt', 'w') as virushashes_file:
        isFirstLine = True
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(download_hash_file, id) for id in range(99999)]
            for future in concurrent.futures.as_completed(futures):
                hash_file = future.result()
                if hash_file is not None:
                    for line in hash_file.splitlines():
                        if line.startswith('#'):
                            continue
                        if isFirstLine:
                            isFirstLine = False
                        else:
                            line = '\n' + line
                        virushashes_file.write(line)
                print(f'Downloaded hash file {id}.md5')

    print('Download complete')
