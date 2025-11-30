import json
from difflib import get_close_matches

def load_knowledgeBase(file_path: str) -> dict:
    """
    load data from the json file and return the data as a dictionary
    takes in file_path as a string for function arg
    """
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    
    return data

def save_knowledge(filePath:str, data:dict):
    """
    function to save new knowledge the bot gained to the json file
    filePath - path to the json file
    data - dictionary of old + new values
    """
    
    #open file path in write mode
    with open(filePath, 'w') as file:
        json.dump(data,file,indent=2)

def find_best_match(user_question:str, questions: list[str]) -> str | None:
    """
    function that tries to find existing answer from list of questions in json file
    user_question -> question from user
    questions -> converted list of questions from bot_knowledge.json
    returns None if answer is not found
    """
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer(question:str, knowledge: dict) -> str | None:
    """
    if best match to  the user's question is found, then this function is used to get the answer to that question
    question -> best match question
    knowledge -> loaded knowledge base
    """
    for q in knowledge['questions']:
        if q['question'] == question:
            return q['answer']

def chat_bot():
    """
    main application 
    """
    knowledge:dict = load_knowledgeBase('bot_knowledge.json')

    while True:
        user_input = input("You:")

        if user_input.lower() == "quit":
            exit
        else:
            best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge["questions"]])
            
            if best_match:
                answer = get_answer(best_match, knowledge)
                print(f'Bot:{answer}')
            else:
                print("Bot: I dont know the answer, can you teach me?")

                user_answer = input("Type the answer or 'skip' to skip:")

                if user_answer.lower() != "skip":
                    knowledge["questions"].append({"question": user_input, "answer":user_answer})
                    save_knowledge("bot_knowledge.json", knowledge)
                    print("Thank you! I learned a new response :D")

if __name__ == '__main__':
    chat_bot()

