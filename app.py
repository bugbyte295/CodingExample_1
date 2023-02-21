from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired
import MERCAL
import rosters
import payroll
import requests
import datetime
app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'null'

# Flask-Bootstrap requires this line
Bootstrap(app)

positionIds = {"Sherlock Holmes and the Hound of the Baskervilles - St. George, Utah":4374064,
        "Nancy Drew and Hardy Boys \"Hidden Chamber\" - St. George Utah":5954498,
        "Escape From Jack the Ripper - St. George Utah": 6847181,
        "Nancy Drew: The Mystery of the Missing Jewelry - Salt Lake City, Utah":5990823,
	"The Secrets of Downton Abbey - Salt Lake City, Utah":5990824,
	"The Mirror Ghost\'s Haunted Basement - Salt Lake City, Utah":5990822,
	"The Sword of Zorro - Salt Lake City, Utah":5990827,
	"The Book of Houdini - Salt Lake City":6803090
        }

locationIds= {"Sherlock Holmes and the Hound of the Baskervilles - St. George, Utah":2160344,
        "Nancy Drew and Hardy Boys \"Hidden Chamber\" - St. George Utah":2160344,
	"Escape From Jack the Ripper - St. George Utah":2160344,
        "Nancy Drew: The Mystery of the Missing Jewelry - Salt Lake City, Utah":5571343,
	"The Secrets of Downton Abbey - Salt Lake City, Utah":5571343,
	"The Mirror Ghost's Haunted Basement - Salt Lake City, Utah":5571343,
	"The Sword of Zorro - Salt Lake City, Utah":5571343,
	"The Book of Houdini - Salt Lake City":5571343}

slingUrl = "https://api.getsling.com/shifts/bulk"

slingToken = "b4ccbc98e0fe4934acbf9f5d72c6071f"

stgRoomLst = ["Sherlock Holmes and the Hound of the Baskervilles - St. George, Utah",
        "Nancy Drew and Hardy Boys \"Hidden Chamber\" - St. George Utah",
        "Escape From Jack the Ripper - St. George Utah"]

slcRoomLst = ["Nancy Drew: The Mystery of the Missing Jewelry - Salt Lake City, Utah",
	"The Secrets of Downton Abbey - Salt Lake City, Utah",
	"The Mirror Ghost's Haunted Basement - Salt Lake City, Utah",
	"The Sword of Zorro - Salt Lake City, Utah",
	"The Book of Houdini - Salt Lake City"
        ]

roomLst = ["The Superhero Virtual Escape Room",
"Sherlock vs. Moriarty - Virtual Team Building - Learning Agility",
"The Superhero Virtual Team Building Escape Room - Collaboration",
"The Minutes to Midnight Virtual Team Building Escape Room",
"Moriarty\'s Parlor - Virtual Escape Room",
"Moriarty's Parlor - Virtual Escape Room",
"Return to Treasure Island Virtual Escape Room",
"Remember the Ghosts of Christmas - Virtual Escape Room",
"The Nancy Drew Virtual Escape Room",
"The Nancy Drew Virtual Team Building Escape Room - Coordination",
"The Enchanted Forest - Virtual Escape Room",
"Magicians Mansion Virtual Escape Room",
"El Escape Room Virtual de Supérheroes"]

class NameForm(FlaskForm):
    name = StringField('Password', validators=[DataRequired()])
    start = DateField('Start', validators=[DataRequired()])
    end = DateField('End', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/kameronCurtis", methods=['POST'])
def main ():
	email = request.json['email']
	room = request.json['room']
	date = request.json['date']
	time = request.json['time']
	quantity = request.json['quantity']
	phoneNumber = request.json['phone']
	lastNames = request.json['lastname']
	firstNames = request.json['firstname']
	MERCAL.main(email, room, date, time, quantity, phoneNumber, lastNames, firstNames)
	return "Done!", 200

@app.route("/payroll", methods=['GET','POST'])
def payroll():
	form = NameForm()
	if form.validate_on_submit():
		passw = form.name.data
		start = form.start.form
		end = form.end.form
		payroll.main(start,end)
		#sdate = request.form['
		payroll.main(sdate,edate)
	return(render_template('output.html',form=form))

@app.route("/keaton", methods= ['GET','POST'])
def keaton():
        return(render_template('payrollForm.html'))

@app.route("/roster", methods=['GET','POST'])
def test():
	t = rosters.main()
	return render_template('test.html')

@app.route("/", methods=['GET','POST'])
def index ():
	return render_template('test.html', my_string="This is a test", my_list=[5,4,3,2,1])

@app.route("/resova", methods=['GET','POST'])
def resova():
	if request.method == 'POST':
		fin = open('data.txt','a')
		bookings = True
		counts = 0
		dict = request.form.to_dict(flat = True)
		if dict['type'] == 'transaction.created':
			email = dict['data[customer][email]']
			lastName = dict['data[customer][last_name]']
			firstName = dict['data[customer][first_name]']
			phoneNumber = dict['data[customer][mobile]']
			while bookings:
				try:
					room = dict['data[bookings]['+str(counts)+'][item][name]']
					date = dict['data[bookings]['+str(counts)+'][booking_date]']
					time = dict['data[bookings]['+str(counts)+'][booking_time]']
					time = time[:5]
					quantity = dict['data[bookings]['+str(counts)+'][quantities][0][quantity]']
					print(str(room))
				except KeyError:
					break
				if room in roomLst:
					try:
						MERCAL.main(email, room, date, time, quantity, phoneNumber, lastName, firstName)
					except:
						print("Error: Room wasnt able to be made when sent to MERCAL "+email)
				elif room in stgRoomLst:
					try:
						ti=date+'T'+time+":00"
						current_date_and_time = datetime.datetime.strptime(ti,'%Y-%m-%dT%H:%M:%S')
						min_added = datetime.timedelta(minutes = 90)
						min_subtracted = datetime.timedelta(minutes = 30)
						beginTime= current_date_and_time - min_subtracted
						eTime = current_date_and_time + min_added
						startTime = beginTime.isoformat()
						endTime = eTime.isoformat()
						#endTime=date+'T'+str(int(time[:2])+1)+str(time[2:])+":00"
						location = locationIds[room]
						position = positionIds[room]
						data = "[{\"available\":true,\"type\":\"shift\",\"status\":\"published\",\"slots\":1,\"dtstart\": \""+startTime+"\",\"dtend\": \""+endTime+"\",\"location\": { \"id\": "+str(location)+" },\"position\": { \"id\": "+str(position)+" },\"summary\":\""+email+"\"}]"
						headers = {
						'Content-Type': 'application/json',
						'Authorization':slingToken,
						'accept': '*/*',
						}
						if location == 2160344:
							response = requests.request("POST",slingUrl, headers=headers, data=data)
							print("sling:" + response)
					except:
						print("Error: Room wasn't added to Sling SLC"+ email)
				elif room in slcRoomLst:
					try:
						ti=date+'T'+time+":00"
						current_date_and_time = datetime.datetime.strptime(ti,'%Y-%m-%dT%H:%M:%S')
						min_added = datetime.timedelta(minutes = 120)
						beginTime= current_date_and_time
						eTime = current_date_and_time + min_added
						startTime = beginTime.isoformat()
						endTime = eTime.isoformat()
						#endTime=date+'T'+str(int(time[:2])+1)+str(time[2:])+":00"
						location = locationIds[room]
						position = positionIds[room]
						data ="[{\"available\":true,\"type\":\"shift\",\"status\":\"published\",\"slots\":1,\"dtstart\": \""+startTime+"\",\"dtend\": \""+endTime+"\",\"location\": { \"id\": "+str(location)+" },\"position\": { \"id\": "+str(position)+" },\"summary\":\""+email+"\"}]"
						headers = {
						'Content-Type': 'application/json',
						'Authorization':slingToken,
						'accept': '*/*',
						}
						if location == 5571343:
                        	response = requests.request("POST",slingUrl, headers=headers, data=data) 
							print("sling:" + str(response))

					
					except:
						print("Error: Room wasn't added to Sling STG"+ email)
				else:
					print("Error: Nothing Works")
				counts+=1
				
		fin.close()
	return render_template('test.html')

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=80)

