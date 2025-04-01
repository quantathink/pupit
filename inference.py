from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

# Youtube
from yt_dlp import YoutubeDL
import os, sys, time, shutil, base64

# Open AI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = OPENAI_API_KEY)

class chatBot:
    def __init__(self,system_role = {"role": "system", 
    "content": "You are Jarvis, my personal assistant. please answer question in professional way"} , max_length=30, temprature = 0.7):
        self.history = [system_role]
        self.max_length = max_length  # Maximum allowed length of the history
        self.system_role = system_role  # Store system role separately
        self.temprature = temprature  # Store temperature for controlling randomness
    def inference(self, user_input):        
        # Add user input to history
        self.history.append({"role": "user", "content": user_input})
        # Generate completion
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=self.history
        )
        # Extract and save the assistant's response
        assistant_reply = completion.choices[0].message.content
        self.history.append({"role": "assistant", "content": assistant_reply})
        self.history = self.history[-self.max_length:]
        return assistant_reply
    def get_history(self):
        return self.history
    def clear_history(self):
        """Clear history while keeping the system role."""
        self.history = [self.system_role ]


Router_bot = chatBot(system_role = {
    "role": "system", 
    "content": '''Classify the request as ONE of the following classes based on the context. DO NOT say anthing else:
    - "JARVIS" : for normal chat request 
    - "OPERATOR" : for request relating to operations like open garage close garage
    - "YOUTUBER" : for requests relating to you tube
    - "ACCOUNTANT" : for requests relating to payments of bills and parkings
    - "SECRETARY" : for requests relating my personal documents like ID'''}, max_length=0, temprature=0)

JARVIS_bot = chatBot(system_role = {
    "role": "system", 
    "content": "Your name is JARVIS, act like you are my friend JARVIS from iron man movie so that we can have chat"}, max_length=30, temprature=1)

Youtuber_bot = chatBot(system_role = {
    "role": "system", 
    "content": "Extract the URL from the text, DO Not write anything, just the URL"}, max_length=1)

simple_anser_bot = chatBot(system_role = {
    "role": "system", 
    "content": '''You provide simple ONE word answers to what is needed to be done'''}, max_length=0)

accountant_mind_bot = chatBot(system_role = {
    "role": "system", 
    "content": '''You are an accountant who likes to do likes to deals with finantial stuff like paying parking tickets and paying bills. YOU ASK YOU SELF IF YOU HAVE THE RIGHT INFORMATION THEN PROCEED ACCORDINGLY'''}, max_length=10, temprature=1)

## Main Functions
def router_func(s):
    return Router_bot.inference(s)

def simple_answer(s):
    return simple_anser_bot.inference(s)

def chat_func(s):
    return JARVIS_bot.inference(s)

def rename_function():
    for filename in os.listdir('./vids'):
        if filename.endswith(".mp3"):
            old_path = os.path.join("./vids", filename)
            new_filename = filename.replace(" ", "_").lower()
            new_path = os.path.join("./vids", new_filename)
            os.rename(old_path, new_path)
            break

def secretary_mind(s, Document,routing_dict):
    print(s)
    message_body = s + ' what is needed to be done, Just say "save" or "load"'
    output_folder = "/home/ubuntu/pupit/docs"
    purpose = simple_answer(message_body).lower()
    filename = simple_answer(f'from the follwing sentince "{s}":  give me a proper descriptive file name title so that I can save it and find it later. And DONT give any extentions  just name')
    if purpose == 'save':
        print(Document.keys())
        print(Document['mimetype'])
        mimetype = {'image/jpeg':'.png','application/pdf':'.pdf'}
        filename = filename + mimetype[Document['mimetype']]
        file_path = os.path.join(output_folder, filename)
        file_data = base64.b64decode(Document['data'])
        with open(file_path, "wb") as file:
            file.write(file_data)
        return 'File is Saved' 
    else:
        files = [f for f in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, f))]
        filename = simple_answer(f'from the follwing LIST "{files}":  give me the file name with extension that is closest to {filename}')
        print (filename)
        return filename

def accountant_mind(s,routing_dict):
    print(f'The request: {s}')

    # first thought: purpose
    thought = s + ' what do you need to do?'
    print('THOUGHT....: ',accountant_mind_bot.inference(thought).lower())
    print('********************************************************')
    car_plate_dict = {'edge':'G93724','ecosport':'C22409','lexus':'P873300'}
    car_list = ['ecosport','lexus','edge']

    thought = s + f' from the list "{car_list}". do you have the car name? , if you do what you the car number plate from {car_plate_dict}, if car is not mentioned then you should keep in mind to ask for the car name'
    print('THOUGHT....: ',accountant_mind_bot.inference(thought).lower())
    print('********************************************************')

    thought = s + f' for how many hours. if not mensioned just say "1"'
    print('THOUGHT....: ',accountant_mind_bot.inference(thought).lower())
    print('********************************************************')

    thought = s + f' what is the parking code. Extract only the parking code, the parking code should be alpha numercial i.e. three numbers and one letter. if nothing is mentioned then you should keep in mind to ask for the code'
    print('THOUGHT....: ',accountant_mind_bot.inference(thought).lower())
    print('********************************************************')

    thought = s + '''if you have all the feilds give me the message in this format "CAR_PLATE_NUMBER CODE HOUR" like for example "G93724 343c 1" JUST the message
    Otherwise ask me for the missing feilds politely'''
    routing_dict['answer'] = accountant_mind_bot.inference(thought).lower()
    print('THOUGHT....: ',routing_dict['answer'])
    print('********************************************************')

    thought = s + 'was the task sucessfuly completed, if "yes" then just say "complete" if you still require more info say "not complete"'
    routing_dict['status'] = accountant_mind_bot.inference(thought).lower()
    print('THOUGHT....: ',routing_dict['status'])
    print('********************************************************')

    if routing_dict['status'] == 'complete':
        routing_dict['route'] == 'jarvis'
        accountant_mind_bot.clear_history()


    return routing_dict
'''
def accountant_mind(s,routing_dict):
    print(f'The request: {s}')
    thought_chain = {}

    
    # first thought: purpose
    thought = s + ' what is needed to be done, If somthing about paying parking ticket, then say "parking" otherwise say "somthing else"'
    thought_chain['purpose'] = simple_answer(thought).lower()
    car_plate_dict = {'edge':'G93724','ecosport':'C22409','lexus':'P873300'}

    print(thought_chain)

    if thought_chain['purpose'] == 'parking':
        routing_dict['status'] = 'not complete'
        car_list = ['ecosport','lexus','edge']
        thought = s + f' for which car from list "{car_list}". Just say the car name. if core is not name is not mentioned return ""'
        thought_chain['car'] = simple_answer(thought).lower()

        thought = s + f' for how many hours. if not mensioned just say "1"'
        thought_chain['hour'] = simple_answer(thought).lower()


        thought = s + f' what is the parking code. Extract only the parking code, the parking code should be alpha numercial three numbers and one letter. if nothing is mentioned return ""'
        thought_chain['code'] = simple_answer(thought).lower()

        thought = s + f' from the dictionary {thought_chain}, do I have all the required feilds, answer "yes" or "no"'
        thought_chain['asking'] = simple_answer(thought).lower()
        print(thought_chain)
        if thought_chain['asking'] == 'no':
            thought = s + f' from the dictionary {thought_chain},what is missing?, please ask me to be provided of the missing information in polite way'
            routing_dict['answer'] = simple_answer(thought).lower()
        elif thought_chain['asking'] == 'yes':
            routing_dict['answer'] = f'{car_plate_dict[thought_chain['car']]} {thought_chain['code']} {thought_chain['hour']}'
            routing_dict['route'] = 'jarvis'
    return routing_dict
'''

def jarvis_mind(s):
    chat = chat_func(s)
    return chat

def clear_folder(folder_path = './vids'):
    shutil.rmtree(folder_path)  # Delete everything in the folder
    os.makedirs(folder_path) 

def convert_text_to_url(s):
    return [Youtuber_bot.inference(s),'audio']


def download_audio_as_mp3(url,TypeOfFile = 'audio'):
    # Directory to save the downloaded file
    save_path = './vids'
    
    # Define download options
    options = {
        'audio':{
            'format':'bestaudio/best',
            'outtmpl':os.path.join(save_path, '%(title)s.%(ext)s'),
            'TypeOfFile':'.mp3',
            'postprocessors':[{
                'key':'FFmpegExtractAudio',
                'preferredcodec':'mp3',
                'preferredquality':'192'}]
        },
        'video':{
            'TypeOfFile':'.mp4',
            'format':'bestvideo+bestaudio/best',
            'outtmpl':os.path.join(save_path, '%(title)s.%(ext)s'),
            'merge_output_format':'mp4'
        }
    }

    try:
        with YoutubeDL(options[TypeOfFile]) as ydl:
            print("YOUTUBEDL :---->", url)
            info_dict = ydl.extract_info(url, download=True)
            #rename_function()
            #file_path = os.path.join(save_path, f"{info_dict['title']}.mp3".replace(" ","_"))
            #file_path = file_path.replace(" ", "_").lower()
            while not os.path.exists('./vids'):
                time.sleep(1)
        type_of_media = options[TypeOfFile]['TypeOfFile']
        return type_of_media
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'Some error occured while downloading'


