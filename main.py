from flask import Flask
from flask import render_template
from flask import request
import datos
from flask import Flask, redirect, url_for, request, session,  render_template_string

app = Flask(__name__)
datos.conn
datos.mydb
app.secret_key = datos.secret

@app.route('/home', methods=['GET', 'POST'])
def home():
   if 'username' in session:
      return render_template('loged.html')
   else:
      return render_template('home.html')

@app.route('/', methods=['GET', 'POST'])
def root():
   return redirect(url_for('home'))

@app.route('/loged/', methods=['GET', 'POST'])
def loged():
    if 'username' in session:
        return render_template('loged.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('root'))

@app.route('/home/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      mensaje = datos.login(username,password)
      print(mensaje)
      if mensaje.startswith("H"):
         session['username'] = username
         return redirect(url_for('loged'))
      else:
         return render_template('login.html', resultado_registro=True, mensaje=mensaje, resultado=mensaje)
      #return render_template('register.html',username = username, password = password, resultado = resultado)
   else:
      return render_template('login.html', resultado_registro= False)



@app.route('/home/register', methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']   
      datos.register(username,password)
      if username == "" or password == "":
         msg = "[!]Error, Rellena todo el formulario"
         resultado = False
         return render_template('register.html', resultado_registro=resultado, msg=msg, resultado=msg)
      else:
         resultado = True
         return redirect(url_for('login',resultado_registro = resultado))
      #return render_template('register.html',username = username, password = password, resultado = resultado)
   else:
      return render_template('register.html')


@app.route('/home/access', methods=['GET', 'POST'])
def access():
   return render_template('loged.html')


@app.route('/home/aboutme', methods=['GET', 'POST'])
def aboutme():
    if 'username' in session:
        return render_template('aboutme.html')
    else:
        return redirect(url_for('login'))


@app.route('/mail/<name>')
def mail(name):
   result = datos.get_data(name)
   resultado = True
   return render_template('getmailform.html', result = result, resultado = resultado)
    

@app.route('/home/about/getmail',methods = ['POST', 'GET'])
def getmail():
   if request.method == 'POST':  
      user = request.form['name']
      #logica buscar el mail y render result
      return redirect(url_for('mail',name = user))
   else:
      user = request.args.get('name')
      return render_template('getmailform.html')




@app.route('/home/about/addmail',methods = ['POST', 'GET'])
def addmail():
   if request.method == 'POST':
      user = request.form['name']
      mail = request.form['mail']
      datos.add_data(user,mail)
      resultado = True
      return render_template('addmailform.html',name = user, mail = mail, resultado = resultado) 
   else:
      return render_template('addmailform.html')      

if __name__ == '__main__':
   app.run(debug = True)