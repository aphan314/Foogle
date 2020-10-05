#!/usr/bin/env python3
import create_tokens
import search_engine
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def query():
   return render_template('search_gui.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      query_list = create_tokens.tokenizer(result.values())
      main_urls = search_engine.main(query_list)
      if len(main_urls) > 0:
         return render_template("result.html", result = main_urls)
      else:
         return render_template("no_result.html")

if __name__ == '__main__':
   app.run(debug = True)