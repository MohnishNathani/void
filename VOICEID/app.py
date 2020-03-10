from flask import Flask, redirect, url_for, request ,render_template
from recognize import recognize
app = Flask(__name__) 
  
@app.route('/')

def index():
    return render_template('input.html',variable='12345')

@app.route('/success/<name>') 
def success(name): 
   return 'welcome %s' % name 
  
@app.route('/login',methods = ['POST', 'GET']) 
def login(): 
   if request.method == 'POST': 
      user = request.form['nm'] 
      identity=str(recognize())
      return redirect(url_for('success',name = user+identity)) 
   else: 
      user = request.args.get('nm') 
      identity=str(recognize())
      return redirect(url_for('success',name = user+identity)) 
  
if __name__ == '__main__': 
   app.run(debug=True,host='0.0.0.0')
