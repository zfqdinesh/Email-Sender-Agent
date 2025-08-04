from flask import Flask, request, render_template, jsonify
import smtplib
import os
from twilio.rest import Client
from langchain.agents import tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI

app = Flask(__name__)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")









@tool
def send_email(input: str):
    """
    Send an email. Format:to: reciever eamil address; Subject: [Clear & Concise Subject Line]

Dear [Recipient’s Name],

I hope this email finds you well.

I am writing to [state the purpose of your email clearly and briefly — e.g., request information, follow up on a discussion, submit a document, ask for assistance, share an update, etc.].

[Add any necessary details or context in one or two short paragraphs. Keep it clear and to the point.]

Please let me know if you need any more information or if there’s anything else I should do on my end. I look forward to your response.

Thank you for your time and assistance.

Best regards,
[Dinesh Ajmera]
[at an healthy position]



    """
    parts = input.split(";")
    receiver_email = parts[0].split("to:")[1].strip()
    message = parts[1].split("Subject:")[1].strip()

    try:
        sender_email_id = os.getenv("EMAIL_ID")
        password = os.getenv("EMAIL_PASSWD")

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender_email_id, password)
        s.sendmail(sender_email_id, receiver_email, message)
        s.quit()

        return f"Email '{message}' sent successfully to {receiver_email}."
    except Exception as e:
        return f"Error: {str(e)}"



@app.route('/', methods=['GET', 'POST'])
def index():
    tools = [send_email , make_call ,send_sms]
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    result = None
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            try:
                result = agent.run(query)
            except Exception as e:
                result = f"Error: {str(e)}"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
