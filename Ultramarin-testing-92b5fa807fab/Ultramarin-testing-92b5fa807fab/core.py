import requests
import os
import bs4
import re
import json

BASE_URL = "https://github.com/" #базовий url
BASE_PATH = "ansver"#шлях збереження

USER = "Raggamasta"# login github
PASS = "changer15011996"# pasword github

token = "9e51a2917dabf65e5111fabacd2e8b4f8187e7d6"# token add rep

def new_file_name(path: "папка", name:"імя файлу", _format="html"):
    """
    Генеруює нове імя файлу якщо в системі вже є цей файл  
    :param path: папка шлях
    :param name: имя файлу
    :param format: формат файла
    :return: нове імя файлу шалях
    """
    counter = 0
    while True:
        new_patch = "{}//{}{}.{}".format(path, name,  counter, _format)
        if not os.path.exists(new_patch):
            break
        counter += 1
    return new_patch


def save(path, name, content, _format="html"):
    """
    Зберігає файл 
    :param path: шлях директорія
    :param name: імя
    :param content: контент
    :param _format: формат файлу
    :return: шлях імя файлу за яким збережено файл
    """
    if os.path.exists("{}//{}.{}".format(path, name, _format)):
        print("Такий файл вже існує")
        path = new_file_name(BASE_PATH, name, _format)
        print("Нова назва файлу : {}".format(path))
    else:
        path = "{}//{}.{}".format(path, name, _format)
    file = open(path, 'wb')
    try:
        file.write(content)
        print("файл записано")
    except:
        print("Помилка запису фаллу")
        file.close()
    file.close()
    return path

text = lambda x: x.rstrip().lstrip()

def assignments_1():
    """
    1 завдання 
    
    :return: 
    """
    #1  Можна зробити так

    #param_1 = {"o": "desk", "q": "Selenide", "s": "stars", "type": "Repositories"}
    #respons = requests.get(BASE_URL, params=param_1)
    #if respons.ok:
    #    print("Запит відправлений успішно")
    #else:
    #    print("Помилка код помилки^ {}".format(respons.status_code))

    #1 завдання  або можна так



    respons = requests.get("https://github.com/search?o=desc&q=Selenide&s=stars&type=Repositories")# get запит
    if respons.ok:
        print("Запит відправлений успішно")
        name_file = save(BASE_PATH, "assignments_1", respons.content)# збереження у файл
    else:
        print("Помилка код помилки: {}".format(respons.status_code))#запит не пройшов повернення коду помилки
        return 0

    # 3Парсинг
    with open(name_file) as ansver:
        soup = bs4.BeautifulSoup(ansver.read())
    list_repo = soup.find("ul", class_="repo-list")# знаходимо список репозиторіїв
    div_repo = list_repo.find("div")#1 репозиторії

    #параметри тесту  отримані з git
    param_dict_git = {
        "name": div_repo.find("a", class_="v-align-middle").get("href")[1::],
                      "description": text(div_repo.find("p", class_="col-9 d-inline-block text-gray mb-2 pr-4").string),
                      "license": text(div_repo.find("p", class_="f6 text-gray mr-3 mb-0 mt-2").string),
                      "language":  text(div_repo.find("div", class_="d-table-cell col-2 text-gray pt-2").text),
                      "stars":  text(div_repo.find_all("a", class_="muted-link")[-1].text),
                      }
    # параметри тесту користувача
    dict_param_assignments = {
        "name": "codeborne/selenide",
        "description": "Concise UI Tests with Java!",
        "license": "MIT license",
        "language": "Java",
        "stars": "740",
    }
    # проведення тесту якщо не збігаєтсья тоді перериває тест
    for key in param_dict_git:
        if param_dict_git[key] != dict_param_assignments[key]:
            print("{} : Наявний {} != Користувача {}".format(key, param_dict_git[key], dict_param_assignments[key]))
            return 0

    #4 Превірка на кількість репозиторіїв
    repositories_git = int(re.findall(r'\d+',soup.find("a", class_="menu-item selected").text)[0])
    repositories_assignments = 526
    if repositories_git != repositories_assignments:
        print("Кількість репозиторіїв не рівні github {} user {}".format(repositories_git, repositories_assignments))
        return 0

    print("---------------\n\tstatus ok")

#
def assignments_2():
    """
    2 завдання 
    :return: 
    """
    respons = requests.get("https://github.com/search?o=desc&q=Selenide&s=stars&type=Repositories")
    if respons.ok:
        print("Запит відправлений успішно")
    else:
        print("Помилка код помилки: {}".format(respons.status_code))
        return 0
    soup = bs4.BeautifulSoup(respons.text)
    list_repo = soup.find("ul", class_="repo-list")
    div_repo = list_repo.find("div")  # 1
    param_dict_git = {
        "name": div_repo.find("a", class_="v-align-middle").get("href")[1::],
        "description": text(div_repo.find("p", class_="col-9 d-inline-block text-gray mb-2 pr-4").string),
        "license": text(div_repo.find("p", class_="f6 text-gray mr-3 mb-0 mt-2").string),
        "language": text(div_repo.find("div", class_="d-table-cell col-2 text-gray pt-2").text),
        "stars": text(div_repo.find_all("a", class_="muted-link")[-1].text),
    }#
    dict_param_assignments = {
        "name": "codeborne/selenide",
        "description": "Concise UI Tests with Java!",
        "license": "MIT license",
        "language": "Java",
        "stars": "740",
    }#
    for key in param_dict_git:#
        if param_dict_git[key] != dict_param_assignments[key]:
            print("{} : Git key{} != user key {}".format(key, param_dict_git[key], dict_param_assignments[key]))
            return 0
    print("---------------\n\tstatus ok")

def assignments_3_1():
    """
    Створення репозиторія
    :return: 
    """
    response = requests.get('https://api.github.com', auth=('USER', 'PASS'))#спроба аунт за користувачем паролем
    if response.ok != True:
        response = requests.get("https://api.github.com/?access_token={}".format(token))# якщо не вдало то за токеном
    headers = {"Authorization": "token %s" % token}
    repos_url = 'https://api.github.com/user/repos'# адреса додання
    data = {
        "name": "temp",
        "description": "This is your first repository",
        "homepage": "https://github.com",
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }# json запит
    data = json.dumps(data)# кодування у джисон
    response = requests.post(repos_url, data=data, headers=headers)# відправлення запиту
    print(response.json())

def assignments_3_2():
    """
    видалення репозиторію
    :return: 
    """
    response = requests.get('https://api.github.com', auth=('USER', 'PASS'))
    if response.ok != True:
        response = requests.get("https://api.github.com/?access_token={}".format(token))

    token_delete = "17dabf659483k28398hg6h54299sd2c31dadf7as"# токен видалення
    headers = {"Authorization": "token %s" % token_delete}# заголовок
    repos_url = 'https://api.github.com/repos/temppd32/temp'
    response = requests.delete(repos_url, headers=headers)# запит видалення
    if response.status_code != 204:# перевірка по статусу видалення
        print("Репа не видалена код помилки:{}".format(response.status_code))
        return 0
    print("---------------\n\ttest ok")
#
if __name__ == '__main__':
    print("1 Тест")
    assignments_1()
    print("2 тест")
    assignments_2()
    print("3 тест створення репозиторію")
    assignments_3_1()
    l = input("Далі пуде видалено репозиторій натисніть будь-яку клавішу")
    print("3 тест видалення репозиторію")
    assignments_3_2()