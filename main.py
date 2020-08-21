import requests
import getpass
import json
import os


def getAuthToken(header: dict) -> dict:
    '''
    Return a dictonary containing a authorization token
    '''
    token = {}
    try:
        url = 'https://www.opensubtitles.com/api/v1/login'
        data = requests.post(url=url, data=header)
        token['Authorization'] = json.loads(data.text)['token']
    except ConnectionError:
        print('No internet connection!\nTry again.')
    return token


def findSubByName(query: dict, token: dict) -> dict:
    '''
    Return a dictonary containing subtitle file_id
    '''
    file_id = {}
    sub_id_list = []
    count = 1

    try:
        url = 'https://www.opensubtitles.com/api/v1/find'
        data = requests.get(url=url, params=query, headers=token)
        json_data = json.loads(data.text)
        consol_message = (
            '''\n--- Choose your subtitle file from the search result ---'''
        )
        print(consol_message)

        for movie_res in json_data['data']:
            if count == 6:
                break
            movie_title = movie_res['attributes']['release']
            sub_id = movie_res['attributes']['files'][0]['id']
            print(f'\n{count}. Movie title: {movie_title}')
            sub_id_list.append([sub_id, movie_title])
            count += 1
        if sub_id_list.__len__() == 0:
            return {}
        usr_option = int(input('\n=> '))
        file_id = {'file_id': sub_id_list[usr_option-1][0],
                   'file_name': sub_id_list[usr_option-1][1], 'sub_format': 'str'}
    except ConnectionError:
        print('No internet connection!')
    except IndexError:
        print('Invalid input.')
        findSubByName(query, token)
    except ValueError:
        return {}
    return file_id


def getSubLink(sub_file_id: dict, token: dict) -> dict:
    '''
    Return a dict object contains subtitle download link
    '''
    url = 'https://www.opensubtitles.com/api/v1/download'
    data = requests.post(url=url, data=sub_file_id, headers=token)
    sub_link = json.loads(data.text)
    return sub_link


def main():
    token = {}

    while True:
        message = (
            '''
        *********************************
        *         OpenSubtitles         *
        *        Choose an Option       *
        *********************************
        
        1) Search Subtitle
        2) Exit
        '''
        )
        print(message)
        try:
            option = int(input('=> '))

            if option == 1:
                header_ = {'username': 'rakibulraki10',
                           'password': 'D76GmNygKMbD8h.'}
                token = getAuthToken(header=header_)

                query = str(input('\nMovie/TV series title: '))
                movie_title = {'languages': 'en',
                               'query': query, 'type': 'all'}
                file_id = findSubByName(movie_title, token)

                if len(file_id) == 0:
                    continue

                link = getSubLink(file_id, token)
                sub = requests.get(url=link['link'])
                save_path = 'C:\\Users\\' + \
                    str(os.getlogin()) + '\\Downloads\\' + link['fname']
                with open(save_path, 'w', encoding="utf-8") as file:
                    file.write(str(sub.text))
                print(f'\nFile saved. Location: {save_path}\n')

            elif option == 2:
                print('Exit Successfully...')
                break
            else:
                print('Invalid option!')
        except ValueError:
            print('Invalid input.')
        except Exception as ex:
            print('Please try again.')


if __name__ == '__main__':
    main()
