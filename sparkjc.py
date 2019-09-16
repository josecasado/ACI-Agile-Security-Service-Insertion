from ciscosparkapi import CiscoSparkAPI

api = CiscoSparkAPI(access_token='your token room')


def writeMessage(text1):
    response = api.messages.create(roomId="Y2lzY29zcGFyazovL3VzL1JPT00vNzliODdiMTAtMDM1Yi0xMWU3LWIxNzctYzVlMGNmNTQ4YmNi", text=text1)
    # print response
