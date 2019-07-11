"""
This sample demonstrates a simple response based on a slot value
"""
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']
    
def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def answer(intent_request):
    """
    Performs response generation
    """

    tax_category = get_slots(intent_request)["TaxCategory"]

    if tax_category == 'personal':
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Please visit the following section to get more information: https://www.canada.ca/en/services/taxes/income-tax/personal-income-tax.html'})

    if tax_category == 'business':
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Please visit the following section for more information: https://www.canada.ca/en/services/taxes/income-tax/business-or-professional-income.html'})

    if tax_category == 'corporate':
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Please visit the following section for more information: https://www.canada.ca/en/services/taxes/income-tax/corporation-income-tax.html'})



def process_intent(intent_request):

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'CRAInquiryIntent':
        return answer(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """ 
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return answer(event)
