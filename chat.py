import asyncio

clients = set()

async def broadcast(author: tuple, m: str):
    for client_reader, client_writer in clients:
        if (client_reader, client_writer) != author:
            client_writer.write(m)
            await client_writer.drain()

async def handler(r, w):
    clients.add((r, w))
    try:
        while True:
            bytesdata = await r.read(1024)
            if not bytesdata:
                raise ConnectionResetError

            msg = bytesdata.decode().strip()
            print(msg)

            if msg == '-quit':
                raise ConnectionResetError
            elif msg:
                asyncio.create_task(broadcast((r, w), f'{msg}\n'.encode()))

    except ConnectionResetError as e:
        print('Client connection reset: ', e)
    except Exception as e:
        print('Error: ', e)

    finally:
        w.close()
        await w.wait_closed()
        clients.remove((r, w))
        print('Client disconnected')


async def main():
    server = await asyncio.start_server(handler, 'localhost', 2000)
    async with server:
        await server.serve_forever()

asyncio.run(main())
