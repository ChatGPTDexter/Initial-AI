from openai import ChatCompletion

# Function to read the file and extract text
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# Function to create questions using OpenAI
def create_questions_with_openai(text, api_key):
    response = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Generate five multiple choice questions based on the following text: {text}"},
        ],
        n=1,
        stop=None,
        temperature=0.5,
        api_key=api_key
    )
    
    questions = response.choices[0].message.content.split("\n")
    return questions

# Main code
api_key = "API_KEY"
filename = 'algebra2.txt'
text = read_file(filename)
questions = create_questions_with_openai(text, api_key)

# Print the questions
for question in questions:
    print(question)
with open('updated_algebra2_questions.txt', 'w', encoding='utf-8') as output_file:
    for question in questions:
        output_file.write(question + "\n")
