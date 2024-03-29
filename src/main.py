"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6
For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import urllib, json, re

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Amazon Alexa Content Search Skills Kit. " \
                    "You can search for content by saying, " \
                    "Tell me something about water."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "You can search for content by saying, " \
                    "Tell me something about water."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def getHelpContent():
    session_attributes = {}
    card_title = "Help Content"
    speech_output = "I am here to give you details about any topic " \
                    "You can search for content by saying, " \
                    "Tell me something about water."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "You can search for content by saying, " \
                    "Tell me something about water."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def getErrorMessage():
    session_attributes = {}
    card_title = "Help Content"
    speech_output = "If you just said something then I can't understand it. " \
                    "You can search for content by saying, " \
                    "Tell me something about water." \
        # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "You can search for content by saying, " \
                    "Tell me something about water."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Amazon Alexa Content Search Skills Kit. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def Search(intent, session):
    """ Get the content details and prepares the speech to reply to the user.
    """
    if 'Query' in intent['slots']:
        query = intent['slots']['Query']
        if 'value' in query:
            query = query['value']
            if query.lower() != "":
                return ContentSearch(intent, session, query)
            else:
                return getErrorMessage()
        else:
            return getErrorMessage()
    else:
        return getErrorMessage()

def ContentSearch(intent, session, query):
        """ Get the content details.
        """
        card_title = query
        query = query.replace(' ', '+')
        query = re.sub(r'[^\x00-\x7F]+',' ', query)
        session_attributes = {}
        should_end_session = True
        reprompt_text = ""
        speech_output = "No Content Found from your query."
        url = "https://en.wikipedia.org/w/api.php?action=query&origin=*&prop=extracts&converttitles=zh&format=json&exintro=&titles=" + query.title()
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        data = data['query']['pages']
        page = data.keys()[0]
        if page != '-1':
            speech_output = re.sub('<[^<]+?>', '', data[page]['extract'].split('\n')[0])
            speech_output = re.sub("[\(\[].*?[\)\]]", "", speech_output)
            speech_output = speech_output.replace('(', '').replace(') ', '')
            if speech_output == '':
                speech_output = "No Content Found from your query."
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "SearchIntent":
        return Search(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return getHelpContent()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
