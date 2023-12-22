from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Set your OpenAI API key
client = OpenAI()

def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

# Specify the path to your .txt file
txt_file_path = 'all_output.txt'

# Define the system message and user message
system_message = "You are an Alim. You specialize in accurately translating Islamic books to an english audience. You will be provided with raw Arabic. your task is to translate it into English."

# Read content from the .txt file
user_content = read_txt_file(txt_file_path)

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_content}
    ],
    temperature=1,
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

# print(response.choices[0].message.content)
