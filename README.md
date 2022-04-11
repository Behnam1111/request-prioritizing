# Request-priority

This is documentation of how to use request-priority application.

This application has been developed with sanic framework.


## Install

    pip install -r requirements.txt
    set mysql database config in config/runtime_config.py
    

## Run the app

    sanic main.app


# REST API

The REST API to the example app is described below.

## submit a job for accessing the limited service

### Request

`POST /limited/`

    curl -i -H 'Accept: application/json' -d 'data=data' http://localhost:8000/limited/

### Response
    HTTP/1.1 200 OK
    content-length: 134
    connection: keep-alive
    content-type: text/plain; charset=utf-8

    your job is submitted,
    Your request id is 102
    you can check the result of your request by going to
    "/check_status/<request_id>"
    

## Check status of a request

### Request

`GET /check_status/<request_id>`

    curl -i -H 'Accept: application/json'  http://localhost:8000/check_status/1

### Response

    HTTP/1.1 200 OK
    content-length: 56
    connection: keep-alive
    content-type: text/plain; charset=utf-8
    your request status is Finished and the result is result.


## Documentation

### Why I have chosen sanic over flask?
    
    Because I want to use asyncio and sanic is compatible with it and it has been written for this purpose.
    
    
### What are the models of this application?
    There are models for request and user and a class for workitem which represent the objects that will be put into the queue.
    

### How does the queue work?
    There are two types of queue in this application. One is a PriorityQueue and another is a Queue.
    The PriorityQueue takes a tuple and prioritize the tasks by the first argument which is user_weight.
    The Queue is for executing tasks and the data of that will be passed to the limited function.


### How does the application handle requests of accessing to the limited function?
    When a request is submitted, a middleware will extract data and send it to queue handler. 
    after that the request will be put into pending_queue. 
    Monitor_queue function will get a task based on the priority of the request which is determined by user_weight parameter.
    and send the request to the limited function.
    when the result of the request is ready, it will be inserted into database and the user can check status and get the result.

