from fastapi import FastAPI,File,UploadFile,HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

#Custom functions import
from functions.openai_requests import convert_audio_to_text,get_chat_response
from functions.database import store_messages,reset_messages
from functions.text_to_speech import convert_text_to_speech

#Initializing App
app = FastAPI()


#CORS origin
origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
    "http://localhost:8000",
    
]

#CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthy")
async def check_healthy():
    print("Bilal")
    return {"message": "Healthy"}

@app.get("/reset")
async def reset_msg():
    reset_messages()
    return {"message": "Reset"}


@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    # #Open Saved Audio
    # audio_input=open("voice.mpeg","rb")

    # Save the file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    #Decoding Audio to Text
    message_decoded=convert_audio_to_text(audio_input)

    #Guard:Ensure message is decode
    if not message_decoded:
        return HTTPException(status_code=400,detail="Failed to get decode audio")
    
    #Get Chat gpt response
    chat_response=get_chat_response(message_decoded)
    print(chat_response)

    #Guard:Ensure response
    if not chat_response:
        return HTTPException(status_code=400,detail="Failed to get chat response")
    
    #Store messages
    store_messages(message_decoded,chat_response)


    #Convert chat response to audio
    audio_output=convert_text_to_speech(chat_response)
    
    # Guard:Ensure response
    if not chat_response:
        return HTTPException(status_code=400,detail="Failed to get Elevent labs audio response")

    # # Create a generator that yields chunks of data
    def iterfile(audio_output):
      if audio_output is not None:
        yield audio_output

    # Use for Post: Return output audio
    # return StreamingResponse(audio_output, media_type="audio/mpeg")
    return StreamingResponse(iterfile(audio_output), media_type="application/octet-stream")






  












