from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import cast,String

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Arko.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False    #perfomance boost
db = SQLAlchemy(app)

class Data(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    PhoneNumber = db.Column(db.Integer, nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return (f"Here are the following details of the requested person:\n"
                f" Name: {self.Name}\n"
                f" PhoneNumber: {self.PhoneNumber}\n"
                f" E-mail: {self.Email}\n"
                f" Age: {self.age}")

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
         Name=request.form['Name']
         PhoneNumber=request.form['Phone']
         Email=request.form['Email']
         age=request.form['Age']
         print("POST")
         data = Data(Name=Name, PhoneNumber=PhoneNumber, Email=Email, age=age)
         db.session.add(data)
         db.session.commit()
         print("Committed")
         

    return render_template("index.html")

@app.route("/search",methods=["GET","POST"])
def search():
    details=[]
    if request.method=="POST":
        search=request.form.get("q","").strip()
        if search:
            details=Data.query.filter(Data.Name.ilike(f"%{search}%") | Data.PhoneNumber.ilike(f"%{search}%") | Data.Email.ilike(f"%{search}%") | Data.age.ilike(f"%{search}%")).all()
            return render_template("Query.html",send=details)
    
    data=Data.query.all()
    return render_template("Query.html",tab=data)
            
            
    

if __name__ == "__main__":
    app.run(debug=True, port=8000)
