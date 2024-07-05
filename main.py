import telebot
from telebot import types
from parsing import get_vacancies
import psycopg2 as psy
from telebot import types

db_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db',
    'port': '5432'
}

bot = telebot.TeleBot('7444577672:AAF1liBfmrkSuLZGnGkQcHkVmylomM3tfbs')
vac_array = []

@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, 'привет-привет! /request - формирование запроса, /search - поиск по параметрам в базе данных')
  conn = psy.connect(**db_config)
  cur = conn.cursor()
  create_table= """        
  CREATE TABLE IF NOT EXISTS vacancies (
              id SERIAL PRIMARY KEY,
              title VARCHAR(200),
              experience VARCHAR(50),
              salary VARCHAR(200),       
              city VARCHAR(50),            
              company VARCHAR(200),
              link VARCHAR(10000)
              );    
          """
  cur.execute(create_table)
  conn.commit()
  cur.close()
  conn.close()

@bot.message_handler(commands=['request'])
def requestf(message):
    bot.send_message(message.chat.id, 'Напишите запрос')
    bot.register_next_step_handler(message, request_input_step)


def request_input_step(message):
    global request  # объявляем глобальную переменную
    global vac_array
    request = message.text
    repl = bot.send_message(message.chat.id, f'Ваш текст: {request}, /parse чтобы загрузить вакансии в базу данных')
    vac_array = get_vacancies(request, 10)


@bot.message_handler(commands=['parse'])
def parse(message):
    global vac_array

    conn = psy.connect(**db_config)
    cur = conn.cursor()
    insert_query = """ 
                            INSERT INTO vacancies 
                            (title, experience, salary, city, company, link) 
                            VALUES (%s, %s, %s, %s, %s, %s) 
                            RETURNING id; 
                            """

    for vacancy in vac_array:
        vacancy_title = vacancy['title']
        vacancy_exp = vacancy['experience']
        vacancy_sal = vacancy['salary']
        vacancy_city = vacancy['city']
        vacancy_comp = vacancy['company']
        vacancy_link = vacancy['link']

        res = f"Title: {vacancy_title}\nExp: {vacancy_exp}\n"
        res += f"Company: {vacancy_comp}\nCity: {vacancy_city}\n"
        res += f"Salary: {vacancy_sal}\nURL: {vacancy_link}\n\n"
        #vacancies_list.append(res)
        bot.send_message(message.chat.id, res)
        cur.execute(insert_query, (vacancy_title, vacancy_exp, vacancy_sal, vacancy_city, vacancy_comp, vacancy_link))

    conn.commit()
    cur.close()
    conn.close()


@bot.message_handler(commands=['search'])



def city_choice1(message):

    bot.send_message(message.chat.id, 'Введите город')
    bot.register_next_step_handler(message, city_choice2)




def city_choice2(message):
    global city
    city = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Опыт не требуется')
    btn2 = types.KeyboardButton('Опыт 1-3 года')
    btn3 = types.KeyboardButton('Опыт 3-6 лет')
    btn4 = types.KeyboardButton('Опыт более 6 лет')
    btn5 = types.KeyboardButton('Не имеет значения')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, 'Выберите опыт работы', reply_markup=markup)
    bot.register_next_step_handler(message, company_choice1)


def company_choice1(message):
    global experience
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    experience = message.text
    btn5 = types.KeyboardButton('Не имеет значения')
    markup.add(btn5)
    bot.send_message(message.chat.id, 'Введите название компании', reply_markup=markup)
    bot.register_next_step_handler(message, company_choice2)


def company_choice2(message):
    bot.send_message(message.chat.id, 'Вакансии по запросу:', reply_markup=types.ReplyKeyboardRemove())
    company = message.text
    conn = psy.connect(**db_config)
    cur = conn.cursor()
    if city == "Не имеет значения":
        cit = "city"
    else:
        cit = f"'{city}'"
    if experience == "Не имеет значения":
        exp = "experience"
    else:
        exp = f"'{experience}'"
    if company == "Не имеет значения":
        comp = "company"
    else:
        comp = f"'{company}'"
    query = (
        f"""SELECT * FROM vacancies WHERE vacancies.city = {cit} AND vacancies.experience = {exp} AND  vacancies.company = {comp};""")
    print(query)
    cur.execute(query)
    results = cur.fetchall()
    conn.commit()
    print(results)
    cur.close()
    conn.close()
    data = []
    count = 10
    for res_list in results:
        vacancy_title = res_list[1]
        vacancy_exp = res_list[2]
        vacancy_sal = res_list[3]
        vacancy_city = res_list[4]
        vacancy_comp = res_list[5]
        vacancy_link = res_list[6]
        res = f"Title: {vacancy_title}\nExp: {vacancy_exp}\n"
        res += f"Company: {vacancy_comp}\nCity: {vacancy_city}\n"
        res += f"Salary: {vacancy_sal}\nURL: {vacancy_link}\n\n"
        bot.send_message(message.chat.id, res)


bot.polling(non_stop= True)