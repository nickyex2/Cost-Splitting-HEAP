import veryfi as vf
import pprint

client_id = 'vrfuVyDcjJmYRAohzNAiydaUmjPBcsDEYhmeghV'
client_secret = 'I4autTxNZobvWkfxN70K41ch3GFrESltjaU6fxNxkbeOd3lbimbNk3pUzVyBOAgNTueczLoY680HPOLCwGLbiaoY1NApBeuEYe7orA1AbpIseXBUBmFfRly0rLoTx8O7'
username = 'nicholasgbr99'
api_key = 'ac3f7d62cb41b4666c763c856d3ac32e'

client = vf.Client(client_id, client_secret, username, api_key)

categories = ['Food and Beverages']

json_result = client.process_document('D:\\Github\\Cost-Splitting-HEAP\\pyTesseract_test\\receipt4.jpg', categories)

pprint.pprint(json_result)

print(json_result['total'])