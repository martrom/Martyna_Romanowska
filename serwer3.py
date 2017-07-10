from socket import *
import time
from flask import Flask,jsonify
from flask import request
from flask import abort
from sys import getsizeof
import json

app = Flask(__name__)

tasks =[
			{ 'id': 1,
			  'description': 'first',
			  'name':'Ala'
			},
			
			{ 'id': 2,
			  'description': 'second',
			  'name':'Filip'
			},
		
			{ 'id': 3,
			  'description': 'third',
			  'name':'Artur'
			},
			
			{ 'id': 4,
			  'description': 'fourth',
			  'name':'Kamila'
			}
		]


#write to file
def write_to_file():
	with open('data2.txt','w+') as out_file:
		json.dump(tasks,out_file)
	out_file.close()	
	


#read from file
def open_file():
	with open('data2.txt','r+') as new_file:
		lines=json.load(new_file)	
	return lines



#read all tasks
@app.route('/api/tasks',methods=['GET'])
def get_tasks():
	open_file()
	return jsonify({'tasks':open_file()})
	
	
	
	
#read from id  task
@app.route('/api/tasks/<int:task_id>',methods=['GET'])
def get_tasks_by_id(task_id):
	tasks=open_file()
	new_task=[new_task for new_task in tasks if(new_task['id']==task_id)]
	if(len(new_task)==0):
		abort(404)
	else:
		return jsonify({'tasks':tasks[task_id-1]})	


#add value
@app.route('/api/tasks/<int:task_id>',methods=['POST'])
def create_task(task_id):
	if not request.json:
		abort(400)
	open_file()
	if not 'description' in request.json or not 'name' in request.json:       
		abort(400)
	task={
	'id':task_id,
	'description':request.json['description'],
	'name':request.json['name']
	}
	task_size=getsizeof(task['description'])+getsizeof(task['name'])
	if(task_size>1024):
		abort(413)
	tasks.append(task)
	write_to_file()
	return jsonify({'Task':task_size}),201
	

@app.route('/api/tasks/<int:task_id>',methods=['DELETE'])
def method_delete(task_id):
	abort(404)


#delete task
@app.route('/api/tasks/<int:task_id>',methods=['PUT'])
def delete_task(task_id):
	open_file()
	new_task=[new_task for new_task in tasks if(new_task['id']==task_id)]
	if(len(new_task)==0):
		abort(404)
	tasks.remove(new_task[0])
	write_to_file()
	return jsonify({'results':True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
	
