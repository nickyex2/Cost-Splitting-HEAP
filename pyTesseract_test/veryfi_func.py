import veryfi as vf
import pprint

client_id = 'vrfuVyDcjJmYRAohzNAiydaUmjPBcsDEYhmeghV'
client_secret = 'I4autTxNZobvWkfxN70K41ch3GFrESltjaU6fxNxkbeOd3lbimbNk3pUzVyBOAgNTueczLoY680HPOLCwGLbiaoY1NApBeuEYe7orA1AbpIseXBUBmFfRly0rLoTx8O7'
username = 'nicholasgbr99'
api_key = 'ac3f7d62cb41b4666c763c856d3ac32e'

def read_img(receipt_file):
    client = vf.Client(client_id, client_secret, username, api_key)

    categories = ['Food and Beverages']

    json_result = client.process_document(receipt_file, categories) # change this to receipt file
    
    return json_result['total']

