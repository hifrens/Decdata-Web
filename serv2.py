from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve

from program import *

import json

f = open('./liveServer/config.json')
config = json.load(f)

ip = config['ip']
port = config['port']

print(f'[Debug]: Server hosted on {ip}:{port}')

app = Flask(__name__)
cors = CORS(app)

@app.route("/receiver", methods=["POST"])
def postME():
   b64request = False
   data = request.get_json()

   # print(str(data)) (for debugging)
   # str(data) is the full command

   output = ""

   if data.get('Search'):
      print('Search: [{search}]'.format(search=data.get('Search')))
      isotopes = getContains(data.get('Search'))
      temp = isotopes.split()
      methods = ""
      halflife = ""
      unit = ""
      for i in range(len(temp)):
         index = searchFor(str(temp[i]).replace(",",""))
         methods = methods   + objs[index].get_decaymethod() + ","
         halflife = halflife + objs[index].get_halflife() + ","
         unit = unit         + objs[index].get_unit() + ","
         
      #Remove final commas.
      methods = methods[:-1]
      halflife = halflife[:-1]
      unit = unit[:-1]
      
      output = "{ \"isotopes\":\"" + isotopes + "\", \"decaymethods\":\"" + methods + "\", \"halflife\":\"" + halflife + "\", \"unit\":\"" + unit + "\"}"

   elif data.get('Info'):
      print('Info: [{info}]'.format(info=data.get('Info')))
      output = "{ \"HalfLife\":\"" + objs[searchFor(str(data.get('Info')).replace(" ",""))].get_halflife() + "\"}"
   
   elif data.get('Chain'):   
      print('CSS Chain: [{chain}]'.format(chain=data.get('Chain')))
      chainStr = ""
      chain = objs[searchFor(str(data.get('Chain')).replace(" ",""))].get_decay_chain()
      for i in range(len(chain)):
         chainStr = chainStr + str(chain[i]) + ":::"

      output = "{ \"chain\":\"" + chainStr + "\"}"
   

   elif data.get('ChainV2'):
      b64request = True
      print('Image Chain: [{chainV2}]'.format(chainV2=data.get('ChainV2')))
      b64 = objs[searchFor(str(data.get('ChainV2')).replace(" ",""))].get_radioactivedecay_chain()
      output = "{ \"b64\":\"" + b64 + "\"}"

   if not b64request:
      print(f'Output: [{output}]\n')
   else:
      print(f'Output: [b64 image (if issues, change b64request to False)]\n')
      
   return(output)
   
if __name__ == "__main__":
   serve(app, host=ip, port=port, threads=1)
