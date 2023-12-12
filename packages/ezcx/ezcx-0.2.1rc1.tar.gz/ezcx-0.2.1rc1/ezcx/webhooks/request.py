from google.cloud import dialogflowcx as cx
from google.protobuf.json_format import ParseDict
from google.protobuf.json_format import MessageToDict
from google.protobuf.struct_pb2 import Struct

# 2023-12-01
# - Dialogflow CX WebhookRequest object has changed with breaking changes
# - addition of "query" helper method to work through incoming payloads created.

# 2023-10-28
# - Replacement of self.request with self.__message to represent the proto message
# - Addition of __getattr__ which fetches from the self.__message now

class WebhookRequest:
    
    def __init__(self, body: dict = {}):
        self.__message = cx.WebhookRequest()
        # When a webhook comes in as JSON, we use ParseDict to convert JSON to Protobuf
        ParseDict(body, self.__message._pb, ignore_unknown_fields=True)
        self.__query = None
        self.__origin = None

    # gRPC Message attributes exposed as properties;
    # Easier on traditional linters and formatters. 

    @property
    def detect_intent_response_id(self) -> str:
        return self.__message.detect_intent_response_id

    @property
    def language_code(self) -> str:
        return self.__message.language_code

    @property
    def fulfillment_info(self) -> cx.WebhookRequest.FulfillmentInfo:
        return self.__message.fulfillment_info

    @property
    def intent_info(self) -> cx.WebhookRequest.IntentInfo:
        return self.__message.intent_info

    @property
    def session_info(self) -> cx.SessionInfo:
        return self.__message.session_info

    @property
    def messages(self) -> list:
        return self.__message.messages

    @property
    def payload(self) -> Struct:
        return self.__message.payload

    @property
    def sentiment_analysis_result(self) -> cx.SentimentAnalysisResult:
        return self.__message.sentiment_analysis_result

    # Helper properties.  These class properties make basic access easier
    @property
    def tag(self) -> str:
        return self.__message.fulfillment_info.tag

    @property
    def session(self) -> str:
        return self.__message.session_info.session

    @property
    def session_id(self) -> str:
        return self.session.split('/')[-1]

    @property
    def session_parameters(self):
        return MessageToDict(
            self.__message.session_info._pb, 
            including_default_value_fields=True
        ).get('parameters')
        
    @property
    def query(self):
        if self.__query and self.__origin:
            return self.__query, self.__origin

        r = self.__message
        
        # q is for query, o is for origin
        q, o = '', ''
        if r.text:
            q = r.text
            o = 'text'
        elif r.trigger_event:
            q = r.trigger_intent
            o = 'trigger_intent'
        elif r.transcript:
            q = r.transcript
            o = 'transcript'
        elif r.trigger_event:
            q = r.trigger_event
            o = 'trigger_event'
        elif r.dtmf_digits:
            q = r.dtmf_digits
            o = 'dtmf_digits'
        else:
            ...
        
        self.__query = q
        self.__origin = o
        return self.__query, self.__origin
    
    
    @property
    def origin(self) -> str:
        if not self.__origin:
            self.query
        return self.__origin

    # JSON Encoding methods.  These are primarily for testing and logging.
    def to_dict(self) -> dict:
        return MessageToDict(self.__message._pb, including_default_value_fields=True)

    @property
    def as_dict(self) -> dict:
        return self.to_dict()
