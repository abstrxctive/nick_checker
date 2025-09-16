import requests
from urls import urls
from tqdm import tqdm

def check_user_exists(username):
    exists = [
        f"Список социальных сетей {username}",
        "-" * 60,
    ]
    
    print()
    for url in tqdm(urls):
        user_url = url + username

        try:
            response = requests.get(user_url, allow_redirects=True)
            
            if response.status_code == 200:
                exists.append(user_url)
        except Exception as e:
            print(e)
    
    with open(f"{username}.txt", 'w') as f:
        f.write(chr(10).join(exists))
    
    print()
    return chr(10).join(exists)

input_username = input("Введите имя пользователя: ")
exist_info = check_user_exists(input_username)
print(exist_info)
