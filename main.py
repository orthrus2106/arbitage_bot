import requests
import json
import pandas as pd
import time
import numpy as np
import streamlit as st
import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging
import asyncio
import os

# API ключи

binance_api_key = "6OgEbdHsah6R9qGEPbH85DiEACLeSmmF5XzBWQHjKw6y5qQKgeHG5DrVOuVDS1BJ"
binance_secret_key = "1ysoI2Eb79eIr78mDSNU9YpBh0kW5L7tjFBHVOVbHz8BGc0Xwqn9jURPTPrxN6o0"

bybit_api_key = "7tRmF4PFE787bSYLDi"
bybit_secret_key = "8hHjb3pEVVUpeMFEY01Bfp3owrY9EVrlSTix"

API_TOKEN = '5834409537:AAFqk08poSl-iwHRgywoS-HkktFHIzvDtxE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def get_binance_prices():
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url)
    prices = json.loads(response.text)
    return prices


def get_bybit_prices():                                     # Получаем текущие курсы Bybit
    url = "https://api.bybit.com/v2/public/tickers"
    response = requests.get(url)
    prices = json.loads(response.text)
    return prices


def compare_prices(binance_prices, bybit_prices):
    result = {}
    for pair in binance_prices:
        symbol = pair["symbol"]
        if symbol.endswith("USDT"):
            binance_price = float(pair["price"])
            bybit_price = None
            for ticker in bybit_prices["result"]:
                ticker_symbol = ticker["symbol"].replace("/", "")
                if symbol == ticker_symbol:
                    bybit_price = float(ticker["last_price"])
                    break
            if bybit_price is not None:
                diff = float(abs(binance_price - bybit_price))
                percent_diff = diff / binance_price
                result[symbol] = {
                    "binance_price": binance_price,
                    "bybit_price": bybit_price,
                    "percent_diff": percent_diff
                }
    result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1]["percent_diff"], reverse=True)}
    return result


def get_price_diff():
    binance_prices = get_binance_prices()
    bybit_prices = get_bybit_prices()
    price_diff = compare_prices(binance_prices, bybit_prices)
    message = "Разница в курсах:\n"
    for symbol, data in price_diff.items():
        message += f"{symbol}: Binance - {data['binance_price']:.2f}, Bybit - {data['bybit_price']:.2f}\n"
    return message


@dp.message_handler(commands=['/price'])
async def send_price_diff(message: types.Message):
    await message.answer("Hi")
    await message.answer(get_price_diff())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
"""""
print("Курсы валют:")
if len(price_diff) == 0:  # Проверяем, есть ли результаты
    print("Результаты не найдены.")
else:
    for symbol, data in price_diff.items():
        print(f"{symbol}: Binance - {data['binance_price']:.2f}, Bybit - {data['bybit_price']:.2f}")
"""""



