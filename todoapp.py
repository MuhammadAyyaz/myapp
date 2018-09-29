from flask_wtf import FlaskForm
from flask import Flask,request,session, redirect, jsonify,render_template
from wtforms.validators import Required, Length
from wtforms import StringField, SubmitField,IntegerField,TextAreaField,PasswordField,DateField
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap


app=Flask(__name__)
app.config['MONGO_DBNAME'] = 'miti'
app.config['MONGO_URI'] = 'mongodb://mayaz:ayaz31@ds263571.mlab.com:63571/axiomdt'
mongo = PyMongo(app)
bootstrap=Bootstrap(app)
class User(FlaskForm):
    f_name=StringField("First Name", validators=[Required()])
    l_name=StringField("Lask Name", validators=[Required()])
    password=PasswordField("Enter Password",validators=[Required()])
    dob=DateField("DOB",validators=[Required()])
    sign_up=SubmitField("Sign Up")
    name=StringField("username",validators=[Required()])
    pas=PasswordField("pass",validators=[Required()])
    sign_in=SubmitField("Sign In")
    logout=SubmitField("Log out")


class InsertForm(FlaskForm):
    task = StringField("Task",validators=[Required()])
    description = TextAreaField("Description",validators=[Required()])
    submit = SubmitField("submit")
    task2=StringField('New Title',validators=[Required()])
    description2=TextAreaField('New Description',validators=[Required()])

class SearchForm(FlaskForm):
    task=StringField('Task',validators=[Required()])
    submit=SubmitField('Search Task')
    incomplete = SubmitField("Find incomplete")
    complete=SubmitField("Find completed")
    findall=SubmitField("Find All")
class DeleteForm(FlaskForm):
    task=StringField('Task',validators=[Required()])
    submit=SubmitField('delete')
@app.route('/')
def index():
    form=User(request.form)
    return render_template("index.html",form=form)
@app.route('/todo/v1_v01/user/register', methods=['GET','POST'])
def register():
    form=User(request.form)
    data=mongo.db.student

    if request.method=="POST":
        f_name = request.form["f_name"]
        l_name = request.form["l_name"]
        password = request.form["password"]
        dob = request.form["dob"]
        data.insert({"First_Name":f_name,"Last_Name":l_name,"Password":password,
                     "Date of Birth":dob})
        return 'Welcome to our application'
    return render_template('user.html',form=form)
@app.route('/todo/v1_v01/user/login', methods=['GET','POST'])
def login():
    form=User(request.form)
    if request.method=="POST":
        if mongo.db.student.find({"First_Name":request.form['name'],
                                "Password":request.form["pas"]}):
            session['First_Name'] = request.form['name']

    return render_template("user.html",form=form)
@app.route('/todo/v1_v01/user/logout', methods=['GET','POST'])
def logout():
    form=User(request.form)

    if request.method=="POST":
        if mongo.db.student:
            session.pop('First_Name',None)
    return render_template("user.html",form=form)

@app.route('/todo/v1_v01/tasks/api', methods=['GET','POST'])

def findone():
    form = SearchForm(request.form)
    out = []
    if request.method == "POST":

        if mongo.db.todo.find({"Task":request.form['task']}):
            records=mongo.db.todo.find({"Task":request.form['task']})

            for dt in records:
                out.append({'id':dt["id"],"Task":dt["Task"],
                            "description":dt["description"],'complete':dt['complete']})
            #return jsonify({'result':out})
        else:
            return 'no data found'
    return render_template('findone.html',form=form,out=out)

@app.route('/todo/v1_v01/tasks/incomplete', methods=['GET','POST'])
def findcompleted():
    form = SearchForm(request.form)
    out = []
    if request.method == "POST":

        if mongo.db.todo.find({"complete":False}):
            records=mongo.db.todo.find({"complete":False})

            for dt in records:
                out.append({'id':dt["id"],"Task":dt["Task"],
                            "description":dt["description"],'complete':dt['complete']})
        else:
            return 'no data found'
    return render_template('incomplete.html',form=form,out=out)

@app.route('/todo/v1_v01/tasks/complete', methods=['GET','POST'])
def completed():
    form = SearchForm(request.form)
    out = []
    if request.method == "POST":

        if mongo.db.todo.find({"complete":True}):
            records=mongo.db.todo.find({"complete":True})

            for dt in records:
                out.append({'id':dt["id"],"Task":dt["Task"],
                            "description":dt["description"],'complete':dt['complete']})
        else:
            return 'no data found'
    return render_template('complete.html',form=form,out=out)
@app.route('/todo/v1_v01/tasks', methods=['GET','POST'])
def findall():
    form=SearchForm(request.form)
    frame=mongo.db.todo
    out = []
    if request.method == 'GET':
        for dt in frame.find():
            out.append({"ID":dt["id"],"Task":dt["Task"],
                        "Description":dt["description"],'complete':dt['complete']})

    return render_template('Query all.html', form=form,out=out)
@app.route('/todo/v1_v01/tasks/add', methods=['GET','POST'])
def adding():
    frame=mongo.db.todo
    form=InsertForm(request.form)
    if request.method=='POST':
        task=request.form["task"]
        description=request.form["description"]
        count = mongo.db.todo.find({}).count()

        frame.insert({"id":count+1,"Task":task,"description":description,'complete':False})
        return 'Task successfully added'
    return render_template('addition.html',form=form,frame=frame)

@app.route('/todo/v1_v01/tasks/delete', methods=['GET','POST','DELETE'])
def deletion():
    form=DeleteForm(request.form)
    if request.method == 'POST':
        if mongo.db.todo.find():
            task = request.form['task']
            mongo.db.todo.delete_one({'Task': task})
            return "task deleted successfully"
        else:
            return 'no data found'
    return render_template('deletion.html',form=form)
@app.route('/todo/v1_v01/tasks/update',methods=['GET','POST','PUT'])
def updation():
    data=mongo.db.todo
    form=InsertForm(request.form)
    if request.method == 'POST':

        task1=request.form['task']
        task2=request.form['task2']
        description=request.form['description2']
        #complete=request.form['complete']
        if mongo.db.todo.find({'Task':task1}):
            record=mongo.db.todo.update_one({'Task':task1},
                                            {'$set':{'Task':task2,'description':description,
                                                     'complete':True}})
            return 'task updated successfully'
        else:
            return 'task not found'
    return render_template('updation.html',data=data,form=form)


if __name__ == '__main__':
    app.secret_key = 'this is my app'
    app.run(debug=True,port=8080)
