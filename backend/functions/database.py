import json
import random

# Get Recent Messages


def get_recent_messages():

    # Define Filename and learn instructiond
    file_name = "stored_data.json"
    learned_instruction = {
        "role": "system",
        "content": "You are interviewing a user for a job as a retail assistant.Ask short question that are relevant to the junior position.Your name is Rachel.The user is called Arfa.Keep your answers to under 30 words"
    }

    # initialize messages
    messages = []

    # Add a random element
    x = random.uniform(0, 1)
    if x < 0.5:
        learned_instruction["content"] = learned_instruction["content"] + \
            " Your response will include some dry humour"
    else:
        learned_instruction["content"] = learned_instruction["content"] + \
            " Your response will include rather a challenging questions"

    # Append instruction to messages
    messages.append(learned_instruction)

    # Get Last messages
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

        # Append last 5 rows of items
        if data:
            if len(data) < 5:
                for item in data:
                    messages.append(item)
            else:
                for item in data[-5:]:
                    messages.append(item)

    except Exception as e:
        print(e)
    pass


    return messages  


#Store messages
def store_messages(request_message,response_message):


    #Define the file name
    file_name="stored_data.json"

    #Get recent messages
    messages=get_recent_messages()[1:]

    #Add messages to data
    user_message={"role":"user","content":request_message}
    assistant_message={"role":"assistant","content":response_message}
    messages.append(user_message)
    messages.append(assistant_message)


    #save the updated file
    with open(file_name,"w") as f:
        json.dump(messages,f)

#Reset messages
def reset_messages():

    #Overrite the current file with nothing
    open("stored_data.json","w")


    