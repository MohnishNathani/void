from flask import Flask , render_template,jsonify,request
from recognize import recognize
from add_user import add_user
from pydub import AudioSegment
import os

app=Flask(__name__)
user = ""
count = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mapbasic')
def index2():
    return render_template('mapbasic.html')

@app.route('/json')
def json():
    return render_template('index.html')

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    identity=recognize()
    print("Answer: ",identity)
    op=jsonify(identity)
    print(op," : ",type(op))
    return op

@app.route('/background_process_test2')
def background_process_test2():
    global user,count
    user=request.args.get('a',0)
    count=int(request.args.get('b',0))
    return "nothing"



@app.route('/messagesadd', methods = ['POST'])
def api_messagesadd():
    global count
    print(count)
    source = "./voice_database/" + user
    try:
        os.mkdir(source)
    except Exception as e:
        print(e)

    fi = open('./trial', 'wb')
    fi.write(request.data)
    fi.close()

    src = "./trial"
    dst = source + "/"+str(count)+".wav"
    sound = AudioSegment.from_file(src)
    sound.export(dst, format="wav")
    count = count + 1

    if count == 4:
        add_user(str(user))
        count=1
    return "Binary message written!"



@app.route('/messages', methods = ['POST'])
def api_message():
    f = open('./file', 'wb')
    f.write(request.data)
    f.close()

    src = "./file"
    dst = "./test.wav"
    sound = AudioSegment.from_file(src)
    sound.export(dst, format="wav")
    identity=recognize()
    return "Binary message written!"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
