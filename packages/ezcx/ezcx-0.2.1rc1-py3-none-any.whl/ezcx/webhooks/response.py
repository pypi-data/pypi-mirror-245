
from google.cloud import dialogflowcx as cx

from google.protobuf.json_format import MessageToDict
from google.protobuf.struct_pb2 import Struct

class WebhookResponse:
    
    def __init__(self):
        self.__message: cx.WebhookResponse = cx.WebhookResponse(
            fulfillment_response=self.FulfillmentResponse(messages=[])
        )

    # gRPC Message attributes exposed as properties;
    # Easier on traditional linters and formatters. 

    @property
    def fulfillment_response(self) -> cx.WebhookResponse.FulfillmentResponse:
        return self.__message.fulfillment_response

    @property
    def page_info(self) -> cx.PageInfo:
        return self.__message.page_info

    @property
    def session_info(self) -> cx.SessionInfo:
        return self.__message.session_info

    @property
    def payload(self) -> Struct:
        return self.__message.payload

    @property
    def FulfillmentResponse(self) -> cx.WebhookResponse.FulfillmentResponse:
        return cx.WebhookResponse.FulfillmentResponse

    @property
    def ResponseMessage(self) -> cx.ResponseMessage:
        return cx.ResponseMessage

    @property
    def Text(self) -> cx.ResponseMessage.Text:
        return cx.ResponseMessage.Text

    @property
    def ConversationSuccess(self) -> cx.ResponseMessage.ConversationSuccess:
        return cx.ResponseMessage.ConversationSuccess

    @property
    def OutputAudioText(self) -> cx.ResponseMessage.OutputAudioText:
        return cx.ResponseMessage.OutputAudioText

    @property
    def LiveAgentHandoff(self) -> cx.ResponseMessage.LiveAgentHandoff:
        return cx.ResponseMessage.LiveAgentHandoff

    @property
    def PlayAudio(self) -> cx.ResponseMessage.PlayAudio:
        return cx.ResponseMessage.PlayAudio

    @property
    def TelephonyTransferCall(self) -> cx.ResponseMessage.TelephonyTransferCall:
        return cx.ResponseMessage.TelephonyTransferCall

    def add_response(self, response_message: cx.ResponseMessage):
        self.fulfillment_response.messages.append(response_message)
        return self

    def add_text_response(self, *texts, channel=""):
        text = self.Text(text=texts)
        response_message = self.ResponseMessage(text=text, channel=channel)
        self.add_response(response_message)
        return self
    
    def add_conversation_success(self, metadata: dict, channel=""):
        conversation_success = self.ConversationSuccess(metadata=metadata)
        response_message = self.ResponseMessage(conversation_success=conversation_success, channel=channel)
        self.add_response(response_message)
        return self        

    def add_payload_response(self, payload: dict, channel=""):
        # ResponseMessage instantiation with value of Payload handles this automatically
        # This is the "mapping" interface; no need for Struct and ParseDict
        response_message = self.ResponseMessage(payload=payload, channel=channel)
        self.add_response(response_message)
        return self

    def add_ssml_response(self, ssml: str, channel=""):
        output_audio_text = self.OutputAudioText(ssml=ssml)
        response_message = cx.ResponseMessage(output_audio_text=output_audio_text, channel=channel)
        self.add_response(response_message)
        return self

    def add_play_audio(self, audio_uri: str, channel=""):
        play_audio = self.PlayAudio(audio_uri=audio_uri)
        response_message = cx.ResponseMessage(play_audio=play_audio, channel=channel)
        self.add_response(response_message)
        return self

    
    def add_live_agent_handoff(self, metadata: dict, channel=""):
        live_agent_handoff = self.LiveAgentHandoff(metadata=metadata)
        response_message = cx.ResponseMessage(live_agent_handoff=live_agent_handoff, channel=channel)
        self.add_response(response_message)
        return self

    def add_telephony_transfer_call(self, phone_number: str, channel=""):
        telephony_transfer_call = self.TelephonyTransferCall(phone_number=phone_number)
        response_message = cx.ResponseMessage(telephony_transfer_call=telephony_transfer_call, channel=channel)
        self.add_response(response_message)
        return self

    def add_session_parameters(self, parameters: dict):
        session_info = cx.SessionInfo(parameters=parameters)
        self.__message.session_info = session_info
        return self

    def set_payload(self, payload: dict):
        self.__message.payload = payload
        return self

    def set_transition(self, target: str):
        target_length = len(target.split('/'))
        if target_length == 10:
            self.__message.target_page = target
        elif target_length == 8:
            self.__message.target_flow = target
        return self

    # JSON Encoding methods.  These are primarily for testing and logging.
    def to_dict(self) -> dict:
        return MessageToDict(self.__message._pb, including_default_value_fields=True)
    
    @property
    def as_dict(self) -> dict:
        return self.to_dict()

