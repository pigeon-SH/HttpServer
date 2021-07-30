from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json
import time

DBNAME = "memo.db"
HOST = "localhost"
PORT = 9999

def DBMS_get():
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    data = []
    for i in cur.execute("select * from MEMO"):
        record = {}
        record["name"] = i[0]
        record["content"] = i[1]
        data.append(record)
    con.close()
    return data

def DBMS_post(newrecord):
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    ex = "insert into MEMO values ("
    ex += "'" + newrecord["name"] + "', '" + newrecord["content"] + "')"
    cur.execute(ex)
    con.commit()
    con.close()

def DBMS_delete(key, value):
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    ex = "delete from MEMO where "
    ex += "" + key + " = '" + value + "'"
    cur.execute(ex)
    con.commit()
    con.close()

class RequestHandler(BaseHTTPRequestHandler):
    #if this server received a request, BaseHTTPRequestHandler calls do_REQUEST-TYPE() method
    #responses of requests are sended after the request methods(do_*()) are all done
    def send_response_JSON(self, data):
        self.wfile.write(bytes(json.dumps(data), "utf8"))
    def load_request_JSON(self):
        datalen = int(self.headers["Content-Length"])
        return json.loads(self.rfile.read(datalen).decode())
        
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = DBMS_get()
        self.send_response_JSON(data)
        print("Complete GET Request")

    def do_POST(self):
        data = self.load_request_JSON()
        print("POST Request:", data)
        DBMS_post(data)
        
        self.send_response(200)
        self.end_headers()
        print("Complete POST Request")
        self.send_response_JSON({"status": "OK"})

    def do_DELETE(self):
        key, value = self.path.split('/')[1:]
        print("DELETE Request:", key, value)
        DBMS_delete(key, value)

        self.send_response(200)
        self.end_headers()
        print("Complete DELETE Request")
        self.send_response_JSON({"status": "OK"})

print("Starting Server")
httpd = HTTPServer((HOST, PORT), RequestHandler)
print("Hosting Server on port", PORT)
httpd.serve_forever()
