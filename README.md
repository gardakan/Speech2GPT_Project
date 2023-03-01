## Speech2GPT - a command line speech-to-text implementation of ChatGPT

Speech2GPT (working title) is a command line tool written in Python which gives voice access to <a href="https://openai.com/blog/chatgpt/">ChatGPT</a>.  This is intended as a personal productivity tool.  As an individual with ADHD and ASD symptoms, one of the most paralysing aspects of my professional life is <a href="https://en.wikipedia.org/wiki/HTTP_404">what happens to my mind</a> when I have to write an email or documentation.  So instead of spending hours trying to reel myself in to write a two sentence email response about some work thing, maybe it's better to dictate a rough prompt and have an AI do the heavy lifting?  Doing touch up editing is far more agreeable than second guessing my tone constantly.

## Version 0.1.0 features and todo:

<h3>Features:</h3>
- Core engine is working.  User can speak a prompt and review what Speech2GPT <em>thinks</em> you said, and prompts the user to verify.  ChatGPT is fed the approved prompt and generates a response.
- Help and version option flags implemented.

<h3>Todo:</h3>
- Proper multi-platform CLI configuration with man page and various optional arguments.
- ChatGPT session persistence.
- Save outputs in database
- Multiple export options (text file, pdf etc)
- Different reader voices

<h3>Known issues:</h3>
- Exits with error if the prompt is spoken less than ~.25 seconds after intro prompt finishes.
- You tell me!  Pretty basic so far

## Installation

Speech2GPT was written with Python 3.11.2, but appears to be working with 3.10 as well.  I haven't tested it on earlier versions yet.

Install required python dependencies:
'''
$ python -m pip install -r requirements.txt
'''

Add your ChatGPT API key to line 47 of Speech2GPT.py:
'''
...
44 def passToOpenAI(command):
45     maxT = 4097
46     print("Passing to OpenAI: "+command)
47     openai.api_key = ""
48     usrPrompt = command
...
'''

Navigate to top level folder (Speech2GPT_Project) and initialize and create database:
'''
$ python -m Speech2GPT init
'''

## Using Speech2GPT

'''
$ python -m Speech2GPT
'''