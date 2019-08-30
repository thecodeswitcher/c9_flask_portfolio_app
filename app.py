from flask import Flask, render_template, request, redirect
import datetime
import pytz # timezone 
import requests
import os

"""
For Unmarried Individuals
For Married Individuals Filing Joint Returns
For Heads of Households
"""

filing_single = {
             0.10: {'lower':0, 'upper':9700}
            ,0.12: {'lower': 9701, 'upper': 39475}
            ,0.22: {'lower': 39476, 'upper': 84200}
            ,0.24: {'lower': 84201, 'upper': 160725}
            ,0.32: {'lower': 160726, 'upper': 204100}
            ,0.35: {'lower': 204101, 'upper': 510300}
            ,0.37: {'lower': 510301, 'upper':None}
              }

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_page():
	return render_template('index.html')

@app.route('/<name>')
def profile(name):
	return render_template('index.html', name=name)

@app.route('/tax_calc', methods=['GET','POST'])
def tax_bracket_calc():
    tax_dict = filing_single
    deduction = 12200

    # elif request.method == 'POST':
    #     print(request.form['text'].split())
    #     total = 0
    #     try:
    #         for str_num in request.form['text'].split():
    #             total += int(str_num)
    #         return render_template('add_numbers.html', result=str(total))

    if request.method == 'GET':

        return render_template('tax_calc.html')

    elif request.method == 'POST':

        try:

            income = float(request.form['text'])

        except:

            return "Please make sure you enter a number with no commas!"

        taxable_income = income - deduction

        print("Taxable income {}".format(taxable_income))

        tax_owed = 0

        tax_owed_dict = tax_dict

        for bracket in tax_dict:

            bracket_lower = tax_dict[bracket]['lower']
            bracket_upper = tax_dict[bracket]['upper']

            if bracket_upper == None:

                bracket_upper = taxable_income

            if taxable_income < bracket_lower:

                break

            taxable_income_in_range = min(taxable_income, bracket_upper)-bracket_lower

            tax_owed += bracket* taxable_income_in_range

            tax_owed_dict[bracket]['tax_owed'] = bracket* taxable_income_in_range
            tax_owed_dict[bracket]['portion_income_taxed'] = taxable_income_in_range

        print("Total tax_owed: {}".format(tax_owed))

        print("Effective Tax Rate: {0:3.2f}%".format((tax_owed/income)*100))

        return render_template('tax_calc.html', result='${:,.2f}'.format(tax_owed))



@app.route('/add_numbers', methods=['GET','POST'])
def add_numbers_post():
	  # --> ['5', '6', '8']
	  # print(type(request.form['text']))
	  if request.method == 'GET':
	  	return render_template('add_numbers.html')
	  elif request.method == 'POST':
  	      print(request.form['text'].split())
  	      total = 0
  	      try:
  	      	for str_num in request.form['text'].split():
  	      		total += int(str_num)
  	      	return render_template('add_numbers.html', result=str(total))
  	      except ValueError:
  	      	return "Easy now! Let's keep it simple! 2 numbers with a space between them please"


@app.route('/shopping_list', methods=['GET','POST'])
def shopping_list_post():
	  # --> ['5', '6', '8']
	  # print(type(request.form['text']))

    if request.method == 'GET':
      return render_template('shopping_list.html')
    elif request.method == 'POST':
          print(request.form['text'].split())
          
          shop_list = []
          try:
            for item in request.form['text'].split():
              
              shop_list.append(item)

              
              
            return render_template('shopping_list.html', result="\n".join([str(item) for item in shop_list]))
          except ValueError:
            return "Easy now! Let's keep it simple! Just words with a space between them"
          
  	      
@app.route('/time', methods=['GET','POST'])
def time_post():
    # --> ['5', '6', '8']
    # print(type(request.form['text']))

    if request.method == 'GET':
      return render_template('time.html')
    elif request.method == 'POST':
          print(request.form['text'].split())
          
          for item in request.form['text'].split():
            answer = (datetime.datetime.now(pytz.timezone("Europe/Dublin")).strftime('Time = ' + '%H:%M:%S' + ' GMT ' + ' Year = ' + '%d-%m-%Y'))
            #answer = datetime.datetime.now().strftime('Time == ' + '%H:%M:%S' + ' Year == ' + '%d-%m-%Y')
            #answer = datetime.datetime.now().strftime('%Y-%m-%d \n %H:%M:%S')

              
              
            return render_template('time.html', result=answer)

         

@app.route('/python_apps')
def python_apps_page():
	# testing stuff
	return render_template('python_apps.html')


@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/blog', methods=['GET'])
def blog_page():
  return render_template('blog.html')

app.run(host=os.getenv('IP', '0.0.0.0'), port = int(os.getenv('PORT', 8080)))

if __name__ == '__main__':
	app.run(debug=False)
