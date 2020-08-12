import requests
import json
import os


def getAuthToken(header: dict) -> dict:
    '''
    Return a dictonary containing a authorization token
    '''
    token = {}
    url = 'https://www.opensubtitles.com/api/v1/login'
    data = requests.post(url=url, data=header)
    token['Authorization'] = json.loads(data.text)['token']
    return token


def findMovieSubIdByName(movie: dict, token: dict) -> dict:
    '''
    Return a dictonary containing subtitle file_id
    '''
    file_id = {}
    sub_id_list = []
    count = 1

    url = 'https://www.opensubtitles.com/api/v1/find'
    data = requests.get(url=url, params=movie, headers=token)
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
    file_id = {'file_id': sub_id_list[usr_option-1]
               [0], 'file_name': sub_id_list[usr_option-1][1], 'sub_format': 'str'}
    return file_id


def getSubLink(sub_file_id: dict, token: dict) -> dict:
    '''
    Return a dict object contains subtitle download link
    '''
    url = 'https://www.opensubtitles.com/api/v1/download'
    data = requests.post(url=url, data=sub_file_id, headers=token)
    sub_link = json.loads(data.text)
    return sub_link


def getUserData(token: dict) -> dict:
    '''
    Return a dict object contains user data
    '''
    url = 'https://www.opensubtitles.com/api/v1/infos/user'
    data = requests.get(url=url, headers=token)
    return json.loads(data.text)


def main():
    token = {}

    while True:
        message = (
        '''
        *********************************
        *         OpenSubtitles         *
        *        Choose an Option       *
        *********************************
        
        1) Login OpenSubtitles
        2) Movie Subtitle
        3) Tv Series Subtitle
        4) Exit
        '''
        )
        print(message)
        option = int(input('=> '))
        
        if option == 1 and len(token) == 0:
            username = str(input('Username: '))
            passowrd = str(input('Password: '))
            header_ = {'username': username, 'password': passowrd}
            token = getAuthToken(header=header_)

        elif option == 2:
            query = str(input('\nEnter a movie title: '))
            movie_title = {'languages': 'en', 'query': query, 'type': 'movie'}
            file_id = findMovieSubIdByName(movie_title, token)
            link = getSubLink(file_id, token)
            sub = requests.get(url=link['link'])
            save_path = 'C:\\Users\\' + \
                str(os.getlogin()) + '\\Downloads\\' + link['fname']
            with open(save_path, 'w') as file:
                file.write(str(sub.text))
            print(f'\nFile saved. Location: {save_path}\n')

        elif option == 1 and len(token) > 0:
            print('\nYou have already loged in.')

        elif option == 4:
            print('Exit Successfully...')
            break

        else:
            print('Invalid option!')


if __name__ == '__main__':
    main()
