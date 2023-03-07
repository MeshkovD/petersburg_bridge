import asyncio
import json
import logging
import sys

logging.basicConfig(filename='client.log', level=logging.INFO)

async def send_request(host, port, message):
    # Создаем соединение с сервером
    reader, writer = await asyncio.open_connection(host, port)

    # Отправляем запрос серверу
    writer.write(message.encode())
    await writer.drain()

    # Получаем ответ от сервера
    data = await reader.read(1024)
    response = json.loads(data.decode())

    # Закрываем соединение
    writer.close()
    await writer.wait_closed()

    return response['result']

async def main():
    # Читаем выражение из файла или с консоли
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            message = file.read()
    else:
        message = input('Enter expression: ')

    # Отправляем запрос серверу и получаем ответ
    result = await send_request('localhost', 8888, message)

    # Выводим результат
    print(result)

asyncio.run(main())