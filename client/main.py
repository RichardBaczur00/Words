import requests
import json


game_id = None
game_token = None


def request_id() -> str:
    res = requests.get('http://127.0.0.1:8000/id')
    data = json.loads(res.content.decode('utf-8'))
    return data['user_id']


def create_game(player_id: str) -> str:
    global game_id

    content = {
        'user_id': player_id
    }

    res = requests.post('http://127.0.0.1:8000/game/create', json=content)
    
    if res.status_code != 200:
        return None
    
    data = json.loads(res.content.decode('utf-8'))
    print(data['game'])
    return (data['game_token']['access_token'], data['game_id'])


def join_game(player_id: str, game_id: str):
    content = {
        'user_id': player_id,
        'game_id': game_id
    }

    res = requests.post('http://127.0.0.1:8000/game/join', json=content)

    if res.status_code != 200:
        return None

    data = json.loads(res.content.decode('utf-8'))
    print(data['game'])
    return data['game_token']['access_token']


def print_menu() -> None:
    print('=================================================')
    print('Welcome to Words!')
    print('Blah Blah Rules, follow the rules, Tom Brady! :)')
    print('1. Create Game')
    print('2. Join Game')
    print('3. Exit')
    print('=================================================')


def start_game_menu(game_token, game_id, player_id):
    while True:
        word = input("Enter a 5 letter word: ")
        content = {
            'game_id': game_id,
            'user_id': player_id,
            'player_word': word
        }
        head = {
            'Authorization': 'Bearer ' + game_token
        }
        res = requests.post('http://127.0.0.1:8000/move', json=content, headers=head)

        if res.status_code != 200:
            print('Server responded with error. Status code:', res.status_code)
            continue
        
        data = json.loads(res.content.decode('utf-8'))

        status = data['status_code']
        
        if status == 0x01:
            print('Move was invalid!')
        elif status == 0x02:
            print('Not your move')
        else:
            print(data['game']['guesses'][word])



def main():
    global game_token
    global game_id

    player_id = request_id()
    
    while True:
        print_menu()
        choice = int(input('Enter choice: '))

        if choice == 3:
            break

        if choice == 1:
            game_token, game_id = create_game(player_id)
            if game_token is None:
                print("Couldn't create game!")
                continue
            head = {
                'Authorization': 'Bearer ' + game_token 
            }
            res = requests.post('http://127.0.0.1:8000/game/start', json={'game_id': game_id}, headers=head)

            print(game_token)
            if res.status_code != 200:
                print('Failed to start game!')
                continue
            start_game_menu(game_token, game_id, player_id)

        if choice == 2:
            game_id = input("Please provide the game id: ")
            game_token = join_game(player_id, game_id)
            if game_token is None:
                print("Couldn't join game")
                continue
            print(game_token)
            head = {
                'Authorization': 'Bearer ' + game_token 
            }
            res = requests.post('http://127.0.0.1:8000/game/start', json={'game_id': game_id}, headers=head)

            if res.status_code != 200:
                print('Failed to start game!')
                continue

            start_game_menu(game_token, game_id, player_id)




if __name__ == '__main__':
    main()