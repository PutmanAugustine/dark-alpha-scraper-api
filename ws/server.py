import asyncio
import json
import redis.asyncio as redis
import copy

from websockets.asyncio.server import serve

clients = {}

async def openConnection(websocket):
  async for message in websocket:
    try:
      print(message)
      msg = json.loads(message)
    except:
      return await websocket.send("Invalid JSON")
    if (msg.get("type") == "register" and isinstance(msg.get("userId"), int)):
      clients.update({msg.get("userId"): websocket})
      print(clients)
      await websocket.send(json.dumps({"type": "registered", "userId": msg.get("userId")}))

async def problemDone(channel: redis.client.PubSub):
  message = await channel.get_message(ignore_subscribe_messages=True, timeout=None)
  while True:
    message = await channel.get_message(ignore_subscribe_messages=True, timeout=None)
    if message is not None:
      print("Recieved message from pubsub: " + json.dumps(message))
      result = None

      try:
        result = json.loads(message["data"])
      except:
        print("Invalid JSON in pubsub payload: " + json.dumps(message))
        return

      if not result["userId"]:
        print("Missing userId in message: " + json.dumps(message))
        return

      ws = clients.get(result["userId"])
      print("sending message to client: " + json.dumps(message))
      ws.send(
        json.dumps({
          "type": "problem_done",
          "productId": result["productId"],
          "status": result["status"],
          "productName": result["productName"]
        })
      )

async def main():
  r = redis.Redis(host='localhost', port=6379, decode_responses=True)
  pubClient = r.pubsub()
  await pubClient.subscribe("problem_done")
  print("subscribed")

  async with serve(openConnection, "localhost", 8080) as server:
    serveRedis = asyncio.create_task(problemDone(pubClient))
    serveServer = asyncio.create_task(server.serve_forever())
    await asyncio.gather(serveServer, serveRedis)

if __name__ == "__main__":
  asyncio.run(main())
