from __future__ import print_function
import random
import urllib.request
CardTitle= "News in slow French"
# --------------- Helpers that build all of the responses ----------------------
#def build_speechlet_response(title, output, reprompt_text, should_end_session):
def build_speechlet_response(output, reprompt_text, should_end_session,dir):
    """
    Build a speechlet JSON representation of the title, output text, 
    reprompt text & end of session
    """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': CardTitle,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
		"directives": 
		[
		{
			#"type": "AudioPlayer.Play",
			"type": dir,
			"playBehavior": "REPLACE_ALL",
			"audioItem":
			{
				"stream": 
				{
					"token": "This-is-the-audio-token",
					"url": "https://s3-us-west-2.amazonaws.com/news-in-french/newsfrench.mp3",
					"offsetInMilliseconds": 0
				}
			}
		}
		],
        'shouldEndSession': should_end_session
    }
def build_response(session_attributes, speechlet_response):
	"""
	Build the full response JSON from the speechlet response
	"""
	return {
		'version': '1.0',
		'sessionAttributes': session_attributes,
		'response': speechlet_response
	}
# --------------- Functions that control the skill's behavior ------------------
def on_launch_response():
	#resp=urllib.request.urlopen("https://news-in-french.herokuapp.com/")
	#resp_data = eval(resp.read().decode('utf-8'))
	#url = resp_data['url']
	speech_output=""
	should_end_session=True
	dir="AudioPlayer.Play"
	return build_response({}, build_speechlet_response(speech_output,None,should_end_session,dir))
	
def handle_session_end_request():
    speech_output = ""
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(speech_output, None, should_end_session,"AudioPlayer.Stop"))
 
def get_welcome_response():
    speech_output = "Hi!! you can say Alexa, launch the news in slow french for news and say Alexa, stop to stop audio at any given time "
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response({}, build_speechlet_response(speech_output, speech_output, should_end_session,"AudioPlayer.Stop"))
   
def handle_resume_request():
    speech_output = "I cannot resume or pause the news. "
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response({}, build_speechlet_response(speech_output, speech_output, should_end_session,"AudioPlayer.Play"))

# --------------- Events ------------------
def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])
def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return on_launch_response()
def on_intent(intent_request, session):
	""" Called when the user specifies an intent for this skill """
	print("on_intent requestId=" + intent_request['requestId'] +
			", sessionId=" + session['sessionId'])
	intent = intent_request['intent']
	intent_name = intent_request['intent']['name']
	print(intent_name)
    # Dispatch to your skill's intent handlers
	if intent_name == "AMAZON.HelpIntent":
		return get_welcome_response()
	elif intent_name == "AMAZON.CancelIntent" or intent_name== "StopNewsIntent" or intent_name == "AMAZON.StopIntent":
		return handle_session_end_request()
	elif intent_name == "AMAZON.PauseIntent" or intent_name == "AMAZON.ResumeIntent":
		return handle_session_end_request()
	else:
		raise ValueError("Invalid intent")
def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session. Is not called when the skill returns should_end_session=true """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
# --------------- Main handler ------------------
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    if 'session' in event:
        if event['session']['new']:
            on_session_started({'requestId': event['request']['requestId']},
                               event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])	