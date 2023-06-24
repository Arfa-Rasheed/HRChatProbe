import { useState } from "react";
import Title from "./Title";
import RecordMessage from "./RecordMessage";
import axios from 'axios'

function Controller() {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);
  const [blob,setBlob]=useState('')


  const createBlobURL = (data: any) => {
    const blob=new Blob([data],{type:"audio/mpeg"});         
    const url=window.URL.createObjectURL(blob);            
    return url;
  };

  const handleStop = async (blobURL:string) => {
   const myMessage={sender:"me",blobURL}
   const messageArr=[...messages,myMessage]

   //Convert bloburl to blob object
   fetch(blobURL)
    .then((res)=>res.blob())
    .then(async (blob)=>{
        const formData=new FormData();
        formData.append("file",blob,'myfile.wav');

        //Send form data to API endpoint 
        await axios
         .post("http://localhost:8000/post-audio",formData,
          {
            headers:{"Content-Type":"audio/mpeg"},
            responseType:"arraybuffer",
          })
          .then((res:any)=>{
            const blob =res.data;
            const audio=new Audio();
            audio.src=createBlobURL(blob);


            //Append rachel response to messageArr
            const rachelMessage={sender:'rachel',blobURL:audio.src};
            messageArr.push(rachelMessage);
            setMessages(messageArr)

            //Play Audio
            setIsLoading(false);
            audio.play();
          })
          .catch((err)=>{
             console.error(err.message);
          }) 
    })


  };

  return (
    <div className="h-screen overflow-y-hidden">
      <Title setMessages={setMessages} />
      <div className="flex flex-col justify-between h-full overflow-y-scroll pb-96">
       {/* Conversations */}
       <div className="mt-5 px-5">
        {
            messages.map((audio,index)=>(
                <div key={index + audio.sender} className={"flex flex-col " + (audio.sender === 'rachel' && "flex items-end")}>
                    <div className="mt-4">
                        <p className= {audio.sender == 'rachel'? "text-right mr-2 italic text-green": 'ml-2 italic text-blue'}>
                            {audio.sender}
                        </p>
                        {/* Audio Message */}
                        <audio 
                        src={audio.blobURL}
                        className='appearance-none'
                        controls
                        />    
                    </div>
                </div>
            ))
        }
           
       </div> 


       {/* Recorder */}
        <div className="fixed bottom-0 w-full py-7 border-t text-center bg-gradient-to-r from-sky-500 to-green-500">
          <div className="flex justify-center items-center w-full">
            <RecordMessage  handleStop ={handleStop}/>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Controller;
