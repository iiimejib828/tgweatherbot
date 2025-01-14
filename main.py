import requests
import json
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

latitude = 61.7849
longitude = 34.3469
base_url = "https://api.open-meteo.com/v1/forecast"
bot = Bot(token='PLACE TOKEN HERE')
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, я могу тебе рассказать о погоде в Петрозаводске!")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/now\n/tendays")

@dp.message(Command('now'))
async def now(message: Message):
    # Параметры для API
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",  # Получить почасовую температуру на высоте 2 м
        "daily": "temperature_2m_max,temperature_2m_min",  # Максимальная и минимальная температура
        "current_weather": True,  # Текущая погода
        "timezone": "Europe/Moscow"  # Определение часового пояса автоматически
    }

    try:
        response = requests.get(base_url, params=params)
        weather_data = response.json()  # Преобразуем ответ в JSON
        await message.answer(f"Сейчас в Петрозаводске: {weather_data['current_weather']['temperature']}°C")
    except requests.RequestException as e:
        await message.answer(f"Ошибка при запросе: {e}")

@dp.message(Command('tendays'))
async def tendays(message: Message):
    # Параметры для API
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min",  # Максимальная и минимальная температура
        "forecast_days": "10",  # На 10 дней
        "timezone": "Europe/Moscow"  # Определение часового пояса автоматически
    }

    try:
        response = requests.get(base_url, params=params)
        weather_data = response.json()  # Преобразуем ответ в JSON
        data = weather_data['daily']

        await message.answer(
            "```\n" # Начало блока кода в Markdown
            "Прогноз на 10 дней в Петрозаводске:\n"  
            f"{'Дата':<12}{'Max Темп (°C)':<15}{'Min Темп (°C)':<15}\n"
            + "-" * 42 + "\n"  # Разделитель
            + "\n".join(
                f"{date:<12}{t_max:<15}{t_min:<15}"
                for date, t_max, t_min in zip(
                    data['time'],
                    data['temperature_2m_max'],
                    data['temperature_2m_min']
                )
            )
            + "\n```",  # Конец блока кода в Markdown
            parse_mode="Markdown"
        )
    except requests.RequestException as e:
        await message.answer(f"Ошибка при запросе: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())