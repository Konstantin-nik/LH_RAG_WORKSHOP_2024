# LH_RAG_WORKSHOP_2024

1. [Setup the project](#setup-the-project)
2. [Project stucture](#project-stucture)
3. [QR-code](#qr-code-to-this-repo)


## Setup the project 
 
### Short version

To initialize the project:

 1. Install python3.11 in you don't have python3+ intalled
 2. Run `git clone git@github.com:Konstantin-nik/LH_RAG_WORKSHOP_2024.git`
 3. Run `./setup.sh`
 4. Place the API key in the .env file
 5. Open the project in the course folder


 ### Detailed version

 **!!! IF YOU HAD ANY PROBLEMS BEFORE, please <u>delete</u> local version of this repo and follow this instruction.**

 1. Make sure you have python3+ installed. To check it run `python --version` in your console/terminal.
 If it's not installed download and install python3.11 from [here](https://www.python.org/downloads/).
 2. Clone this repo to your local directory `git clone git@github.com:Konstantin-nik/LH_RAG_WORKSHOP_2024.git`.
 3. Open this directory (you should be inside the folder 'LH_RAG_WORKSHOP_2024') in terminal/console.
 4. Run `python -m venv .venv` to create virtual enviroment.
 5. Activate virtual enviroment using one of the following commands (instead of '\<venv\>' put '.venv', for example: `. .venv/bin/activate` (mac command))
 ![alt text](img/image.png)
 6. Make sure it was activated. Your console/terminal should look like this: `(venv) C:\Users\acer\Desktop>`
 7. Now run `pip install -r requirements.txt` to install all needed requirements to this virtual enviroment.
 8. It's mostly done but there are two moments you'll need to check. 
 If you are using VSCode open any python file ('.py') and click in the bottom-right corner on the python version and then select your virtual enviroment (venv) ![alt text](img/telegram-cloud-photo-size-2-5465647820817163602-y.jpg)
 Then open any jupiter notebook ('.ipynb') and in the top-right corner select your virtual enviroment (venv) as a kernel ![alt text](img/telegram-cloud-photo-size-2-5465647820817163604-y.jpg)
 9. Create '.env' file and put there your API keys ('.env.example' is a dummy for your '.env' file)


## Project stucture

 - [main.ipynb](main.ipynb) - contains whole workshop material
 - [src/](src/) - contains folders with ready-to-use code of different rag solutions
    - [simple_chat/](src/0.%20simple_chat/) - implementation of simle chat with LLM, example of world restriction prompt
    - [simple_rag/](src/1.%20simple_rag/) - implementation of simle RAG using SQLite, chat with LLM memorizing everithing
    - [key_words/](src/2.%20key_words/) - RAG, chat with LLM memorizing only messages that contain key words
    - [llm_determinator/](src/3.%20llm_determinator/) - RAG, key_words-based memorization, LLM determines if retrieved content fits the query
    - [user_data_extractor/](src/4.%20user_data_extractor/) - RAG, LLM determination of usefull context, LLM-based extraction of user date from query to memorize  

## QR-code to this repo
![alt text](img/qrcodee.png)