import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

## Loading the environment variables
load_dotenv()


## Gemini API setup
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

class ChatBot:
    def __init__(self,system=""):
        self.system=system
        self.messages = []
        if self.system:
            self.messages.append({"role":"system","content":system})

    def __call__(self,message):
        self.messages.append({"role":"user","content":message})
        result = self.execute()
        self.messages.append({"role":"assistant","content":result})
        return result
    ## using llm to generate content
    def execute(self):
        prompt = "\n".join([f'{msg["role"]}:{msg['content']}' for msg in self.messages])
        model=genai.GenerativeModel("gemini-1.5-flash")
        raw_response = model.generate_content(prompt)
        return raw_response.text
    

# system prompt for fitness assistant
prompt = """
You are a highly knowledgeable and friendly fitness assistant. Your role is to help users achieve their fitness goals by providing personalized workout plans, dietary advice, and motivational quotes. You should be supportive, encouraging, and provide actionable advice that suits the user's fitness level, preferences, and dietary restrictions.

1. **Workout Plans**: Offer structured workout routines that cater to the user's fitness level (beginner, intermediate, or advanced). Include details such as exercise names, repetitions, sets, and rest periods. Tailor the workouts to various goals, such as weight loss, muscle gain, or overall fitness.

2. **Dietary Advice**: Suggest meal plans and nutritional advice that align with the user's dietary preferences (e.g., vegetarian, vegan, keto). Ensure the suggestions are balanced, realistic, and adaptable to the user's lifestyle.

3. **Motivational Quotes**: Provide motivational quotes to inspire and keep the user motivated in their fitness journey. Ensure the quotes are positive, empowering, and relevant to maintaining a healthy lifestyle.

4. **Tone and Style**: Communicate in a friendly, approachable, and clear manner. Be concise but informative, and avoid overwhelming the user with too much information at once. Always prioritize the user's safety and well-being in your recommendations.

Remember, your goal is to empower users with the knowledge and motivation they need to improve their fitness and well-being.
""".strip()


action_regex = re.compile('^Action: (\w): (.*)$')

## action functions using gemini api

def generate_workout(level):
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(f" Generate a workout plan for {level} fitness level")
    return response.text

def suggest_meal(preference):
    respose = genai.GenerativeModel("gemini-1.5-flash").generate_content(f"suggest a meal plan for ${preference} ")
    return respose.text
def motivational_quote(_):
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content("Give me a motivational quote !")
    return response.text


## Mapping actions to functions
known_actions ={
    "generate_workout":generate_workout,
    "suggest_meal":suggest_meal,
    "motivational_quote":motivational_quote
}


## Query function

def query(question,max_turns=5):
    i=0
    bot = ChatBot(prompt)
    next_prompt=question
    while i < max_turns:
        i+=1
        result = bot(next_prompt)
        print(result)
        actions = [action_regex(a) for a  in result.split('\n') if action_regex.match(a) ]
        if actions :
            action,action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception(f"Unknown action :{action} : {action_input} ")
            print(f"--running {action} {action_input}")
            observation = known_actions[action](action_input)
            print("Observation : ", observation )
            next_prompt = f"Observations : {observation}"
        else:
            return



query("Can you help me with a beginner workout plan")