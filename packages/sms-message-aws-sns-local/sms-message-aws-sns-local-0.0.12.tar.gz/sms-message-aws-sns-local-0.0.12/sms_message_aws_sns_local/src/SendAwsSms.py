import boto3
from dotenv import load_dotenv
import http
import json
import time
from botocore.exceptions import ClientError
import os
from logger_local.Logger import Logger

# from url_local.url_circlez import OurUrl
from api_management_local.api_management_local import APIManagementsLocal
# from api_management_local import indirect
from message_local.MessageLocal import MessageLocal
from message_local.MessageImportance import MessageImportance


load_dotenv()
BETWEEN_SOFT_AND_HARD = 0
MORE_THAN_HARD_LIMIT = 1
SMS_MESSAGE_AWS_SNS_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 208
SMS_MESSAGE_AWS_SNS_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = "sms_message_aws_sns_local_python_package"
DEVELOPER_EMAIL = "emad.a@circ.zone"
logger = Logger.create_logger(object={
    "component_id": SMS_MESSAGE_AWS_SNS_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    "component_name": SMS_MESSAGE_AWS_SNS_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    "component_category": "Code",
    "developer_email": DEVELOPER_EMAIL
})

SMS_MESSAGE_AWS_SNS_API_TYPE_ID = 6  # For API-Management


# TODO Please add SMSMessage Class (SmsMessage.py) in messag_local in message-local-python-package


class SmsMessageAwsSns(MessageLocal):
    def __init__(self, sns_resource=boto3.resource("sns")):
        self.sns_resource = sns_resource
        super().__init__(original_body="body", importance=MessageImportance.HIGH, original_subject="subject",
                         api_type_id=SMS_MESSAGE_AWS_SNS_API_TYPE_ID, is_http_api=True, endpoint="endpoint")

    def create_topic(self, name):
        """
        Creates a notification topic.

        :param name: The name of the topic to create.
        :return: The newly created topic.
        """
        try:
            topic = self.sns_resource.create_topic(Name=name)
            logger.info("Created topic %s with ARN %s. " % (name, topic.arn))
        except ClientError:
            logger.exception("Couldn't create topic %s." % name)
            raise
        else:
            return topic

    def publish_text_message(self, phone_number, message) -> int:
        try:
            response = self.sns_resource.meta.client.publish(
                PhoneNumber=phone_number, Message=message
            )
            message_id = response["MessageId"]
            logger.info("Published message to %s, message id: %s." % (phone_number, message_id))
        except ClientError:
            logger.exception("Couldn't publish message to %s. message: %s" % (phone_number, message))
            raise
        return message_id

    @staticmethod
    def publish_message(topic, message, attributes):
        """
        Publishes a message, with attributes, to a topic. Subscriptions can be filtered
        based on message attributes so that a subscription receives messages only
        when specified attributes are present.

        :param topic: The topic to publish to.
        :param message: The message to publish.
        :param attributes: The key-value attributes to attach to the message. Values
                           must be either `str` or `bytes`.
        :return: The ID of the message.
        """
        try:
            att_dict = {}
            for key, value in attributes.items():
                if isinstance(value, str):
                    att_dict[key] = {
                        "DataType": "String", "StringValue": value}
                elif isinstance(value, bytes):
                    att_dict[key] = {
                        "DataType": "Binary", "BinaryValue": value}
            response = topic.publish(
                Message=message, MessageAttributes=att_dict)
            message_id = response["MessageId"]
            logger.info("Published message with attributes %s to topic %s." % (attributes, topic.arn))
        except ClientError:
            logger.exception(
                "Couldn't publish message to topic %s." % topic.arn)
            raise
        else:
            return message_id

    def send(self, phone_number, message) -> int:
        if os.getenv("IS_REALLY_SEND_SMS"):
            return self.publish_text_message(phone_number, message)
        else:
            print(f"SmsMessageAwsSns.send IS_REALLY_SEND_SMS is off: suppose to send sms to {phone_number} with body {message}", flush=True)
            return 0

    def was_read(self):
        """read"""
        return True

    def display(self):
        """display"""
        return "Message displayed"

    def _can_send(self, sender_profile_id: int = None, api_data: dict = None, outgoing_body: dict = None) -> bool:
        """can send"""
        return True

    def _after_send_attempt(self) -> None:
        """after send"""
        pass

    def get_id(self):
        return 0


def usage_demo():
    print("-" * 88)
    print("Welcome to the Amazon Simple Notification Service (Amazon SNS) demo!")
    print("-" * 88)

    sns_client = boto3.client("sns")
    sns_resource = boto3.resource("sns")

    topic_name = os.getenv("AWS_SNS_TOPIC_NAME")
    print(f"Creating topic {topic_name}.")

    phone_number = input(
        "Enter a phone number (in E.164 format) that can receive SMS messages: "
    )
    if phone_number != "":
        print(f"Sending an SMS message directly from SNS to {phone_number}.")
        sns_client.publish(PhoneNumber=phone_number,
                           Message="Hello from the SNS demo!")

    if phone_number != "":
        print(
            f"Subscribing {phone_number} to {topic_name}. Phone numbers do not "
            f"require confirmation."
        )
        topic = sns_resource.Topic(topic_name)
        phone_sub = topic.subscribe(Protocol="sms", Endpoint=phone_number)
        print(f"Subscription ARN: {phone_sub.arn}")

    if phone_number != "":
        mobile_key = "mobile"
        friendly = "friendly"
        print(
            f"Adding a filter policy to the {phone_number} subscription to send "
            f"only messages with a '{mobile_key}' attribute of '{friendly}'."
        )

        print(
            f"Publishing a message with a {mobile_key}: {friendly} attribute.")
        sns_client.publish(
            PhoneNumber=phone_number,
            Message="Hello! This message is mobile-friendly.",
            MessageAttributes={mobile_key: {
                "DataType": "String", "StringValue": friendly}},
        )
        not_friendly = "not-friendly"
        print(
            f"Publishing a message with a {mobile_key}: {not_friendly} attribute.")
        sns_client.publish(
            PhoneNumber=phone_number,
            Message="Hey. This message is not mobile-friendly, so you shouldn't get "
                    "it on your phone.",
            MessageAttributes={mobile_key: {
                "DataType": "String", "StringValue": not_friendly}},
        )

    print(f"Getting subscriptions to {topic_name}.")
    topic_subs = sns_resource.Topic(topic_name).subscriptions.all()
    for sub in topic_subs:
        print(f"{sub.arn}")

    # print(f"Deleting subscriptions and {topic_name}.")
    # for sub in topic_subs:
    #     sub.delete()
    # sns_resource.Topic(topic_name).delete()

    print("Thanks for watching!")
    print("-" * 88)


# if __name__ == "__main__":
#     #usage_demo()
#     sms = SnsWrapper(boto3.resource('sns'))
#     sms.publish_text_message('+972545232179',"gfugcuf")
def send_sms_using_aws_sms_using_api_getaway(self, phone_number, message):
    example_instance = APIManagementsLocal.get_api
    external_user_id = None
    api_type_id = 4
    PRODUCT_USER_IDENTIFIER = os.getenv("PRODUCT_USER_IDENTIFIER")
    PRODUCT_PASSWORD = os.getenv("PRODUCT_PASSWORD")
    # user_context._instance = None
    # url_circlez = OurUrl()
    # authentication_auth_login_endpoint_url = url_circlez.endpoint_url(
    #         brand_name=BRAND_NAME,
    #         environment_name=os.getenv('ENVIRONMENT_NAME'),
    #         component_name=component_name_enum.ComponentName.AUTHENTICATION.value,
    #         entity_name=entity_name_enum.EntityName.AUTH_LOGIN.value,
    #         version=AUTHENTICATION_API_VERSION,
    #         action_name=action_name_enum.ActionName.LOGIN.value
    #         )
    authentication_auth_login_endpoint_url = "AWS SNS"

    data = {"user_identifier": PRODUCT_USER_IDENTIFIER, "password": PRODUCT_PASSWORD}
    headers = {"Content-Type": "application/json"}
    debug_data = {"url": authentication_auth_login_endpoint_url, "data": json.dumps(
        data, separators=(",", ":")), "headers": headers}
    logger.info(json.dumps(debug_data, separators=(",", ":"), indent=4))
    outgoing_body = (PRODUCT_USER_IDENTIFIER, PRODUCT_PASSWORD)
    incoming_message = ""
    response_body = ""
    while True:
        api_check, api_call_id, arr = example_instance.before_call_api(external_user_id=external_user_id,
                                                                       api_type_id=api_type_id,
                                                                       endpoint=authentication_auth_login_endpoint_url,
                                                                       outgoing_header=headers,
                                                                       outgoing_body=outgoing_body
                                                                       )
        if arr is None:
            used_cache = False
            if api_check == BETWEEN_SOFT_AND_HARD:
                logger.warn("You excced the soft limit")
            if api_check != MORE_THAN_HARD_LIMIT:
                try:

                    response = self.sns_resource.meta.client.publish(
                        PhoneNumber=phone_number, Message=message
                    )
                    message_id = response["MessageId"]
                    logger.info("Published message to %s, message id: %s." % (phone_number, message_id))
                except ClientError:
                    logger.exception("Couldn't publish message to %s." % phone_number)
                    raise
                else:
                    http_status_code = http.HTTPStatus.OK.value
            else:
                print(" You passed the hard limit")
                x = APIManagementsLocal.seconds_to_sleep_after_passing_the_hard_limit(api_type_id=api_type_id)
                if x > 0:
                    print("sleeping : " + str(x) + " seconds")
                    time.sleep(x)
                    # raise PassedTheHardLimitException

                else:
                    print("No sleeping needed : x= " + str(x) + " seconds")
        else:
            used_cache = True
            print("result from cache")
            print(arr)
            http_status_code = http.HTTPStatus.OK.value
        example_instance.after_call_api(external_user_id=external_user_id,
                                        api_type_id=api_type_id,
                                        endpoint=authentication_auth_login_endpoint_url, outgoing_header=headers,
                                        outgoing_body=outgoing_body,
                                        incoming_message=incoming_message,
                                        http_status_code=http_status_code,
                                        response_body=response_body, api_call_id=api_call_id, used_cache=used_cache)
