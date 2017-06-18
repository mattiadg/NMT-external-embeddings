#! /usr/bin/python

from wsgiref.simple_server import make_server
import time
import os
import subprocess
import json
import datetime
import sys
import urllib

HOST = ''
PORT = 9080


command = ["python", "translate.py", "-m", "/home/farajian/NLP/tools/NMT/nematus-master.translation-server/nematus/TranServerModels/en-it/model.en-it.npz", "-s", "-k", "12", "-n", "-p", "1"]
process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(os.devnull, "w"), shell=False)
print >>sys.stderr, "Loading NMT server: ",
#while True:
#    if process.stderr.readline().strip() == "Server is up":
#        print>>sys.stderr, "Done."
#        break
#pid = process.pid
#print "pid %s" % pid


def requestHandler(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ['CONTENT_LENGTH'])
            request_body = urllib.unquote_plus(environ['wsgi.input'].read(request_body_size))
        except (TypeError, ValueError):
            request_body = "#WRAPPER POST error 1"
        print "  received POST with data |%s|" % request_body
        try:
            ## request_body = request_body.rstrip();
            request_body = request_body.translate(None, '\r\n');
            process.stdin.write(request_body+"\n")
            process.stdin.flush()
            print "sent |%s|" % request_body
            answer = process.stdout.readline().rstrip()
            print "received |%s|" % answer
            response_body = answer
        except:
            response_body = "#WRAPPER POST error 2"

        response_dict = { "src" : request_body,
                          "translation" : response_body }
        response_jstring = json.dumps(response_dict)
        status = '200 OK'
        headers = [('Content-type', 'application/json')]
        start_response(status, headers)
        return [response_jstring]

    elif environ['REQUEST_METHOD'] == 'GET':
        try:
            request_query = urllib.unquote_plus(environ['QUERY_STRING'])
            request_script = urllib.unquote_plus(environ['SCRIPT_NAME'])
            request_path = urllib.unquote_plus(environ['PATH_INFO'])
        except (TypeError, ValueError):
            request_body = "#WRAPPER GET error 1"
        print "  received GET with |SCRIPT %s|PATH %s|QUERY %s|" % (request_script, request_path, request_query)
        try:
            request_body = request_query.rstrip();
            process.stdin.write(request_body+"\n")
            process.stdin.flush()
            print "sent |%s|" % request_body
            answer = process.stdout.readline().rstrip()
            #answer, answer_err =process.communicate(input=request_body)
            print "received |%s|" % answer
            #print "error: |%s|" %answer_err
            response_body = answer
        except:
            response_body = "#WRAPPER GET error 2"

        response_dict = { "src" : request_body,
                          "translation" : response_body }
        response_jstring = json.dumps(response_dict)
        status = '200 OK'
        headers = [('Content-type', 'application/json')]
        start_response(status, headers)
        return [response_jstring]

    else:
        print "  received %s" % environ['REQUEST_METHOD']
        
        response_body = "unknown REQUEST_METHOD |%s|" % environ['REQUEST_METHOD']
        response_dict = { "error" : response_body }
        response_jstring = json.dumps(response_dict)
        status = '400 Bad Request'
        headers = [('Content-type', 'application/json')]
        start_response(status, headers)
        return [response_jstring]

def start_server():
    """Start the server."""
    httpd = make_server(HOST, PORT, requestHandler)
    print "server ready on |%s:%s| ... " % (HOST, PORT)
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
