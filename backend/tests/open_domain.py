from ScrapeThread import ScrapeThread


users_data = [
    {
        'email': 'test@mail.ru',
        'password': 'test'
    },
    {
        'email': 'test1@mail.ru',
        'password': 'test'
    },
    {
        'email': 'test2@mail.ru',
        'password': 'test'
    },
    {
        'email': 'test3@mail.ru',
        'password': 'test'
    },
    {
        'email': 'ishkining@mail.ru',
        'password': 'atuset'
    },
]



if __name__ == '__main__':
    threads = []
    for user in users_data:
        t = ScrapeThread(user['email'], user['password'])
        t.start()
        threads.append(t)

    for t in threads:
        t.join()