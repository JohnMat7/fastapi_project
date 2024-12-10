from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
import uvicorn
import time
import asyncio

# Create FastAPI app instance
app = FastAPI()

# Initialize rate limiter, limiting requests based on client IP address
limiter = Limiter(key_func=get_remote_address)

# Simple synchronous endpoint that responds with a welcome message
@app.get("/welcome")
def welcome():
    return {"message": "Good Morning Sir John !"}

# Rate-limited endpoint (allows only 5 requests per minute from a single IP)
@app.get('/limited')
@limiter.limit("5/minute")
async def limited(request: Request):
    print(list(request))  # Just for debugging, printing out request details
    return {
        "message": "Be careful, few attempts remaining",
        "details": {
            "client_ip": request.client,  # Client's IP address
            "request_method": request.method,  # HTTP method (GET, POST, etc.)
            "url": request.url,  # Requested URL
            "headers": request.headers  # Request headers
        }
    }

# Synchronous endpoint (takes 5 seconds to complete)
@app.get("/sync")
def sleep_1():
    time.sleep(5)  # This blocks the program for 5 seconds
    return {"message": "This is a synchronous endpoint"}

# Another synchronous endpoint (another 5 seconds sleep)
@app.get("/sync_2")
def sleep_2():
    time.sleep(5)  # This also blocks the program for 5 seconds
    return {"message": "Another synchronous endpoint"}

# Asynchronous endpoint (but using time.sleep, which is blocking)
@app.get("/async")
async def sleep_3():
    time.sleep(5)  # This is a blocking sleep, so it negates async advantages
    return {"message": "This is async without await, but still blocks"}

# Asynchronous endpoint (using asyncio.sleep, which is non-blocking)
@app.get("/async_await")
async def sleep_4():
    await asyncio.sleep(5)  # This non-blocking sleep allows other tasks to run
    return {"message": "This is async with await, non-blocking"}




@app.get("/blog/{id}")
def show(id:int) :
    return {"data id" : id}

@app.get("/blog")
def published_blog(limit , published):
    if published:
        return {'data' : f'{limit} published blogs from db'}


@app.get('/blog/{id}/comments')
def comments(id : int) :
    return {"data" : {'1' , '2'}}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
