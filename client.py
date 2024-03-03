import asyncio

async def receive_messages(reader):
    while True:
        data = await reader.readline()
        if not data:
            break
        print(f'{data.decode().strip()}\n')

async def send_messages(writer):
    while True:
        message = await asyncio.to_thread(input)
        if message.strip():
            writer.write(message.encode() + b'\n')
            await writer.drain()

async def main():
    try:
        reader, writer = await asyncio.open_connection('localhost', 2000)
        await asyncio.gather(receive_messages(reader), send_messages(writer))
    except KeyboardInterrupt:
        print("Connection closed.")
    finally:
        writer.close()
        await writer.wait_closed()

asyncio.run(main())
