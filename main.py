from flask import Flask, render_template, request, jsonify,redirect,url_for
import random
import psycopg2


conn = psycopg2.connect(database="emlvwsts",
                        host="mahmud.db.elephantsql.com",
                        user="emlvwsts",
                        password="QZplqRjrPc5y3n2cf6VwgdvhcUZJ1hXV",
                        port="5432")

cursor = conn.cursor()

def create_table():
  cursor.execute("DROP TABLE IF EXISTS Chats")
  sql ='''CREATE TABLE Chats(
   USERNAME VARCHAR(255) NOT NULL,
   MESSAGE VARCHAR(255) NOT NULL,
   MODE VARCHAR(255) NOT NULL
)'''

  cursor.execute(sql)
  print("Table created successfully........")
  conn.commit()


def insert_messages(username,message,mode):
    query = "INSERT INTO chats (USERNAME,MESSAGE,MODE) VALUES('{}','{}','{}')".format(username,message,mode)
    cursor.execute(query)
    conn.commit()

def read_messages():
   cursor.execute("SELECT * FROM chats")     
   data = cursor.fetchall()
   return data

def delall_messages():
    cursor.execute("DELETE FROM chats")
    conn.commit()




#create_table()

openai.api_key = "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"

app = Flask(__name__)





def bot(user_input):
    messages = [{"role": "system", "content": "You Are a Genius Chatbot"}]
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    result = user_input + "\n\n"+ChatGPT_reply
    #messages.append({"role": "assistant", "content": ChatGPT_reply})
    return result




@app.route('/<username>')
def index(username):
    if username == None:
        username = "Unknown"
    return render_template('index.html',username=username)


@app.route('/add', methods=['POST'])
def message():
    user = request.form["username"]
    user_message = request.form["message"]
    if "/search" in user_message:
        query = user_message.replace("/search ","")
        insert_messages(user,query,"prompt")
        return jsonify({'user_message': user_message, 'bot_response':bot(query)})
    elif "/del" in user_message:
        delall_messages()
        return redirect(request.url)

    else:
         insert_messages(user,user_message,"chat")
         return jsonify({'user_message': user_message, 'bot_response': random.randrange(1,1000)})



@app.route("/get_messages",methods=['GET'])
def get_messages():
    messages = []
    for message in read_messages():
        messages.append({"sender":message[0],"message":message[1]})

    
    return jsonify({"messages":messages})





if __name__ == '__main__':
    app.run(debug=True)
