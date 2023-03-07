import asyncio
import json
import logging

logging.basicConfig(filename='server.log', level=logging.INFO)

async def handle_client(reader, writer):
    # Получаем данные от клиента
    data = await reader.read(1024)
    message = data.decode()

    # Обрабатываем запрос клиента
    result = eval(message)

    # Отправляем ответ клиенту
    response = {"result": result}
    writer.write(json.dumps(response).encode())
    await writer.drain()

    # Закрываем соединение
    writer.close()

async def main():
    # Создаем сервер
    server = await asyncio.start_server(handle_client, 'localhost', 8888)

    # Запускаем сервер
    async with server:
        logging.info('Server started on localhost:8888')
        await server.serve_forever()

asyncio.run(main())