from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, SentimentResult, DASSResult
from . import db 
import json, subprocess, nltk, sys, sqlite3, os
from nltk.sentiment import SentimentIntensityAnalyzer
from rasa.core.agent import Agent
from rasa.core.utils import EndpointConfig
from requests.exceptions import ConnectionError
import asyncio
from datetime import datetime

views = Blueprint('views', __name__)

# Set up the action endpoint configuration
# Remember to run 'rasa run actions' in the directory that saved the rasa actions.py first to make it work
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")

# Load the Rasa agent
#agent = Agent.load(r'C:\Users\Hp\Documents\da-midst\current_directory\models\20230413-230954-dry-font.tar', action_endpoint=action_endpoint)
agent = Agent.load('./models/20230703-212816-concave-saddle.tar', action_endpoint=action_endpoint)

@views.route('/', methods=['GET', 'POST']) 
def welcome():
    
    return render_template("welcome.html", user=current_user) 

@views.route('/home', methods=['GET', 'POST'])   #放target URL在单引号里面
@login_required
def home():     #will run the home whenever we go / route
    
    return render_template("home.html", user=current_user)  #reference to current_user and check if is authenticated

@views.route('/all-journal', methods=['GET', 'POST']) 
@login_required
def all_journal(): 

    return render_template("journal-list.html", user=current_user) 

@views.route('/home/chat', methods=['GET', 'POST']) 
@login_required
def chat():
    #print('AAA')
    #print(request.__dict__)
    if request.method == 'POST':
        #print('Request method is POST')
        #print(request.form)
        try:
            # Get the user message from the form data
            # having error: ImmutableMultiDict([]) but currently not effecting the project run
            data = request.get_data().decode('utf-8')
            user_input = json.loads(data)['message']
            print('CHECKING USER INPUT HERE:')
            print(user_input)

            try:
                # Use the Rasa agent to handle the user message
                response = asyncio.run(agent.handle_text(user_input)) #this code is working, chatbot will reply to the text

                # Extract the first response message
                bot_message = response[0]['text']

                # Return the bot message as a JSON response
                return jsonify({'message': bot_message})
            
            except ConnectionError as e:
                print("Failed to connect to the action server:", e)

        except KeyError:
            print("Key not found in dictionary")
            return jsonify({'message': 'Error: Invalid request payload.'})
         
    return render_template("chat.html", user=current_user)

@views.route('/moodtrack', methods=['GET', 'POST'])
@login_required
def moodtrack():
    # Use the session to query the SentimentResult table for the current user
    # .all() to print all results
    # .first() to print first result only
    # if print only first result, delete the for loop in the template, and change rows to row
    row = SentimentResult.query.filter_by(user_id=current_user.id).order_by(SentimentResult.sentResult_id.desc()).first()

    # Pass the data to the template
    return render_template("moodtrack.html", user=current_user, row=row )

@views.route('/moodtrack/dass-21', methods=['GET', 'POST']) 
@login_required
def dass21():

    results = DASSResult.query.filter_by(user_id=current_user.id).order_by(DASSResult.dass_id.desc()).first()
    
    return render_template("dass21.html", user=current_user, results=results) 

@views.route('/moodtrack/dass-21/result', methods=['GET', 'POST']) 
@login_required
def dass21_result():
    
    # Display DASSResult 
    #results = db.session.query(DASSResult).all()
    results = DASSResult.query.filter_by(user_id=current_user.id).order_by(DASSResult.dass_id.desc()).all()

    return render_template("dass21-result.html", user=current_user, results=results) 

@views.route('/moodtrack/dass-21/submit', methods=['POST'])
def submit_dass():
    data = request.get_json()
    depressionScore = data['depressionScore']
    anxietyScore = data['anxietyScore']
    stressScore = data['stressScore']
    result = DASSResult(
        depression=depressionScore,
        anxiety=anxietyScore,
        stress=stressScore,
        user_id=current_user.id,
        submission_time=datetime.now()
    )
    db.session.add(result)
    db.session.commit()
    return jsonify(message='DASS result saved'), flash('DASS result saved!', category='success')

@views.route('/activity', methods=['GET', 'POST'])   #放target URL在单引号里面
@login_required
def activity():
    
    return render_template("activity.html", user=current_user)  

@views.route('/space', methods=['GET', 'POST'])
@login_required
def space(): 
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Journal is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id, date=datetime.now(), updated_on=datetime.now())
            db.session.add(new_note)
            db.session.commit()
            flash('Journal added!', category='success')

            noteId = new_note.id
            # Pass the note to sent_analysis() for sentiment analysis
            sent_analysis(note, noteId)

    return render_template("space.html", user=current_user) 

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/space/edit-note/<noteId>', methods=['GET', 'POST'])
@login_required
def edit_note(noteId):
    # get the target noteId 
    note_toedit = Note.query.get(noteId)

    return render_template("editnote.html", user=current_user, note=note_toedit) 

@views.route('/update-note', methods=['POST'])
@login_required
def update_note():
    noteId = request.json.get('noteId')
    note = Note.query.get(noteId)
    note.data = request.json.get('note')
    #note.date = datetime.now() # update the date
    note.updated_on = datetime.now()
    db.session.commit()

    # Pass the note to sent_analysis() for sentiment analysis
    sent_analysis(note.data, noteId)    #different from 'Add Note' at /space because the initialization and declaration is different

    return jsonify(message='Journal Updated'), flash('Journal updated!', category='success')

def sent_analysis(note,noteId):
    # get the journal from views.py which saved by user
    journal = note
    
    # Instantiate the sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Analyze the sentiment of the text
    sentiment = analyzer.polarity_scores(journal)

    # Print the results
    print("Sentiment analysis results:")
    print("Negative: ", sentiment['neg'])
    print("Neutral: ", sentiment['neu'])
    print("Positive: ", sentiment['pos'])
    print("Compound: ", sentiment['compound'])
    # The compound score is a normalized value between -1 and 1,
    # where -1 is negative, 1 is positive, and 0 is neutral.

    sent_neg = sentiment['neg']
    sent_neu = sentiment['neu']
    sent_pos = sentiment['pos']
    sent_com = sentiment['compound']

    new_sentResult = SentimentResult(sent_neg=sent_neg, sent_neu=sent_neu, sent_pos=sent_pos, sent_com=sent_com, note_id=noteId, user_id=current_user.id)
    db.session.add(new_sentResult)
    db.session.commit()

    # Test if this file work
    print('sentiment.py: BELLO, I am sentiment analysis')
    print(journal)  

    return jsonify({})

@views.route('/about-us', methods=['GET', 'POST'])
def about_us():
    
    return render_template("about-us.html", user=current_user)  

@views.route('/activity/animal', methods=['GET', 'POST'])
@login_required
def activity_animal():
    
    return render_template("act-animal.html", user=current_user) 

@views.route('/activity/drawing', methods=['GET', 'POST'])
@login_required
def activity_drawing():
    
    return render_template("act-drawing.html", user=current_user) 

@views.route('/activity/eating', methods=['GET', 'POST'])
@login_required
def activity_eating():
    
    return render_template("act-eating.html", user=current_user) 

@views.route('/activity/exercise', methods=['GET', 'POST'])
@login_required
def activity_exercise():
    
    return render_template("act-exercise.html", user=current_user) 

@views.route('/activity/meditation', methods=['GET', 'POST'])
@login_required
def activity_meditation():
    
    return render_template("act-meditation.html", user=current_user) 

@views.route('/activity/music', methods=['GET', 'POST'])
@login_required
def activity_music():
    
    return render_template("act-music.html", user=current_user) 

@views.route('/activity/sing', methods=['GET', 'POST'])
@login_required
def activity_sing():
    
    return render_template("act-sing.html", user=current_user) 

@views.route('/activity/sleep', methods=['GET', 'POST'])
@login_required
def activity_sleep():
    
    return render_template("act-sleeping.html", user=current_user) 

@views.route('/activity/talk', methods=['GET', 'POST'])
@login_required
def activity_talk():
    
    return render_template("act-talk.html", user=current_user) 