import asyncio
import websockets
import random

RANDOM_SEED="TEST";
@asyncio.coroutine
def hello():
	websocket = yield from websockets.connect('ws://localhost:8789/')
	msg = yield from websocket.recv();
	print(msg);
	#print (Decrypt(msg));

def Decrypt(data):
        global RANDOM_SEED;
        random.seed(RANDOM_SEED);
        crypt = "";
        for x in range(0, len(data)):
                seed = random.randint(0,100);
                val = data[x]
                crypt += "" + chr(val- seed)
        return crypt;

asyncio.get_event_loop().run_until_complete(hello())
