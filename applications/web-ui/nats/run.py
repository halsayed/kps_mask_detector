import asyncio
from nats.aio.client import Client as NATS
from config import Config, cache, log
import pickle


nats_host = Config.NATS_HOST
nats_port = Config.NATS_PORT
nats_subject = Config.NATS_SUBJECT


async def run(loop):
    nc = NATS()

    log.info(f'connecting to nats service: {nats_host:{nats_port}}')
    await nc.connect(f'{nats_host}:{nats_port}', loop=loop)

    async def message_handler(msg):
        subject = msg.subject
        log.info(f'Received a message on: {subject}, data length: {len(msg.data)} bytes')
        payload = pickle.loads(msg.data)
        print(payload)
        cache.set('values', payload.get('values'))
        if payload.get('image'):
            cache.set('image', payload.get('image'))

    log.info(f'subscribe to subject: {nats_subject}')
    sid = await nc.subscribe(nats_subject, cb=message_handler)

    # await nc.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()