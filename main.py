from fastapi import FastAPI , Request
from slowapi import Limiter
from slowapi.util import get_remote_address
import uvicorn


app = FastAPI()
limiter = Limiter(key_func=get_remote_address)


@app.get("/welcome")
def welcome():
    return { "message" : "Good Morning Sir John !"  }

@app.get('/limited')
@limiter.limit("5/minute")
async def limited(request : Request):
    print (list(request))

    return { "message" : "Be careful few attempts remaining" 
            ,"details" : {
                "client_ip" : request.client,
                "request mthod" : request.method,
                "url" : request.url,
                "headers" : request.headers 
            }}




if __name__ == "__main__":
    uvicorn.run("main:app" , host="0.0.0.0" , port=8000 , reload=True)
