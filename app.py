from flask import Flask,request,jsonify
from dotenv import load_dotenv
import os
from main import ChatBot
from flask_cors import CORS

load_dotenv()
 
app = Flask(__name__)
CORS(app)
system_prompt = """
You are a highly knowledgeable and friendly fitness assistant. Your role is to help users achieve their fitness goals by providing personalized workout plans, dietary advice, and motivational quotes. Your responses should be concise, actionable, and encouraging.
""".strip()

chatbot = ChatBot(system=system_prompt)
@app.route('/chat',methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error":"No message provided"}),400
    response = chatbot(user_message)
    return jsonify({"response":response})

if __name__ ==  "__main__":
    app.run(debug= True )