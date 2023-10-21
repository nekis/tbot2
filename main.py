from PIL import Image, ImageFont, ImageDraw
import random
import sqlite3
import telebot
from io import BytesIO

# Создайте или подключитесь к базе данных SQLite
conn = sqlite3.connect('drivers.db')
cursor = conn.cursor()
cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            Id INTEGER PRIMARY KEY,
            name varchar(20)  CHECK (name GLOB '[a-zA-Z]*' AND name NOT NULL),
            surname varchar(20)  CHECK (name GLOB '[a-zA-Z]*' AND name NOT NULL),
            date_of_birth date CHECK (date_of_birth GLOB '??/??/??' AND date_of_birth NOT NULL),
            city varchar(20) CHECK (name GLOB '[a-zA-Z]*' AND name NOT NULL),
            country varchar(20) CHECK (name GLOB '[a-zA-Z]*' AND name NOT NULL),
            gender varchar(20),
            eye_color varchar(20),
            photo_binary BLOB
        )
    ''')
conn.commit()
conn.close()


# Функция для добавления текста на изображение
def add_text_to_image(image, text, position, font, fill):
    draw = ImageDraw.Draw(image)
    draw.text(position, text, font=font, fill=fill)


# Функция для обработки и сохранения итогового изображения
def process_and_save_image():
    image = Image.open('Front_DL.jpg')
    draw = ImageDraw.Draw(image)

    # Определите настройки шрифта
    font_size = 36
    color = (0, 0, 0)
    font_type = "/Library/Fonts/Arial Bold.ttf"
    font = ImageFont.truetype(font_type, size=font_size)

    # Open a file dialog for the user to select a photo

    # Получите данные из формы
    name = name_entry.get()
    surname = surname_entry.get()
    date_of_birth = date_of_birth_entry.get()
    city = city_entry.get()
    country = country_entry.get()
    eye_color = eye_color_var.get()
    gender = gender_var.get()

    # Сохраните данные в базе данных SQLite
    conn = sqlite3.connect('drivers.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO drivers (name, surname, date_of_birth, city, country, eye_color, gender, photo_binary) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (name, surname, date_of_birth, city, country, eye_color, gender, photo_binary)
    )
    conn.commit()
    conn.close()

    # Обновите список data с новыми данными, включая дату рождения

    data = [
        {"text": name, "position": (538, 260)},
        {"text": surname, "position": (532, 293)},
        {"text": date_of_birth, "position": (479, 326)},
        {"text": city, "position": (586, 357)},
        {"text": country, "position": (700, 392)},
        {"text": gender, "position": (477, 496)},
        {"text": eye_color, "position": (666, 496)},
    ]

    # Добавьте текст "ITU" с случайным числом на изображение
    itu_number = str(random.randrange(23452, 89674))
    itu_text = "ITU " + itu_number
    add_text_to_image(image, itu_text, (420, 210), font, (255, 0, 0))


                      # Draw the data on the image
    font_size = 18
    text_color = (0, 0, 0)
    font = ImageFont.truetype(font_type, size=font_size)
    for item in data:
        draw.text(item["position"], item["text"], font=font, fill=text_color)



    # Paste the photo on the image
    img1 = image.copy()
    img1.paste(photo_binary, (50, 240))

    # Save the final image
    img1.save('output_image.jpg', quality=95)

    # FREE SAMPLE WATERMARK



