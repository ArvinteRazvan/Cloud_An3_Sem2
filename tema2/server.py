import json
import os
import shutil
import time
from ast import literal_eval
from http.server import BaseHTTPRequestHandler, HTTPServer
import re

HOST_NAME = 'localhost'
PORT_NUMBER = 9000


class MyHandler(BaseHTTPRequestHandler):
    routes = {}

    def __init__(self, request, client_address, server, *args, **kwargs):
        super().__init__(request, client_address, server)
        self.routes = {
            r'^/movies/': {'GET': self.get_movie, 'POST': self.post_movie, 'PUT': self.put_movie,
                           'DELETE': self.delete_movie,
                           'movies': 'application/json'},
            r'^/movies$': {'GET': self.get_movies, 'POST': self.post_movies, 'PUT': self.put_movies,
                           'DELETE': self.delete_movies,
                           'movies': 'application/json'},
            r'^/$': {'file': 'index.html', 'movies': 'text/html'}}

    def get_movie(self):
        print(self.path)
        movie_name = self.path.split("/")[-1]
        my_json = json.load(open('movies.json'))
        if movie_name is not None:
            for data in my_json['movies']:
                if data['name'] == movie_name:
                    self.send_response(200)
                    self.end_headers()
                    return data
            self.send_response(404)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
        return {}

    def put_movie(self):
        movie_name = self.path.split("/")[-1]
        print("put movie")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        python_dict = literal_eval(post_data.decode('utf-8'))
        file = open('movies.json')
        my_json = json.load(file)
        file.close()
        new_name = python_dict['name']
        ok = False
        index = 0
        # print(python_dict)
        # print(movie_name)
        for data in my_json['movies']:
            # print(data)
            if data['name'] == movie_name:
                ok = True
                my_json['movies'][index] = {}
                for key, value in python_dict.items():
                    if key != "_id":
                        my_json["movies"][index][key] = value
                break
            index += 1
        if not ok:  # new entry
            my_json["movies"].append({})
            for key, value in python_dict.items():
                if key != "_id":
                    my_json["movies"][-1][key] = value

        with open('movies.json', 'w') as file:
            json.dump(my_json, file)
        self.send_response(200)
        self.end_headers()
        return my_json

    def post_movie(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        python_dict = literal_eval(post_data.decode('utf-8'))

        movie_name = self.path.split("/")[-1]
        my_json = json.load(open('movies.json'))
        if movie_name is not None:
            index = 0
            for data in my_json['movies']:
                if data['name'] == movie_name:
                    for key, value in python_dict.items():
                        if key != "_id":
                            my_json['movies'][index][key] = value
                    self.send_response(200)
                    self.end_headers()
                    with open('movies.json', 'w') as file:
                        json.dump(my_json, file)
                    return my_json
                index += 1
            self.send_response(404)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
        return {}

    def delete_movie(self):

        print(self.path)
        movie_name = self.path.split("/")[-1]
        my_json = json.load(open('movies.json'))
        print(movie_name)
        if movie_name is not None:
            index = 0
            for data in my_json['movies']:
                print(data)
                if data['name'] == movie_name:
                    self.send_response(200)
                    self.end_headers()
                    del my_json['movies'][index]
                    with open('movies.json', 'w') as file:
                        json.dump(my_json, file)
                    return {}
                index += 1
            self.send_response(404)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
        return {}

    def get_movies(self):
        return json.load(open('movies.json'))

    def put_movies(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        python_dict = literal_eval(post_data.decode('utf-8'))
        my_json = {}
        print(python_dict)
        for key, value in python_dict.items():
            my_json[key] = value

        with open('movies.json', 'w') as file:
            json.dump(my_json, file)
        self.send_response(200)
        self.end_headers()
        return my_json

    def post_movies(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        python_dict = literal_eval(post_data.decode('utf-8'))
        file = open('movies.json')
        my_json = json.load(file)
        file.close()
        movie_name = python_dict['name']
        index = 0
        ok = False
        for data in my_json['movies']:
            if data['name'] == movie_name:
                ok = True
                for key, value in python_dict.items():
                    if key != "_id":
                        my_json['movies'][index][key] = value
            index += 1
        if not ok:
            my_json['movies'].append({})
            for key, value in python_dict.items():
                if key != "_id":
                    my_json['movies'][-1][key] = value
        with open('movies.json', 'w') as file:
            json.dump(my_json, file)
        self.send_response(200)
        self.end_headers()
        return my_json

    def delete_movies(self):
        my_json = {}
        with open('movies.json', 'w') as file:
            json.dump(my_json, file)
        self.send_response(200)
        self.end_headers()
        return {}

    def handle_method(self, method):
        self.routes = {
            r'^/movies/': {'GET': self.get_movie, 'POST': self.post_movie, 'PUT': self.put_movie,
                           'DELETE': self.delete_movie,
                           'movies': 'application/json'},
            r'^/movies(($)|(\?.*))': {'GET': self.get_movies, 'POST': self.post_movies, 'PUT': self.put_movies,
                                      'DELETE': self.delete_movies,
                                      'movies': 'application/json'},
            r'^/$': {'file': 'index.html', 'movies': 'text/html'}}
        route = self.get_route()
        print(route)
        if route is None:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes('Route not found\n', 'utf-8'))
        else:
            print(method)
            if method == 'HEAD':
                self.send_response(200)
                route = self.get_route()
                if 'movies' in route:
                    self.send_header('Content-type', route['movies'])
                self.end_headers()
            else:
                if 'file' in route:
                    if method == 'GET':
                        try:
                            f = open(os.path.join(os.getcwd(), route['file']))
                            try:
                                self.send_response(200)
                                if 'movies' in route:
                                    self.send_header('Content-type', route['movies'])
                                self.end_headers()
                                # print(f.read())
                                # print(f)
                                # shutil.copyfileobj(f, self.wfile)
                                # my_movies = json.load(open('movies.json'))
                                # print(my_movies)
                                self.wfile.write(bytes("home", 'utf-8'))
                            finally:
                                f.close()
                        except Exception as e:
                            print(e)
                            self.send_response(404)
                            self.end_headers()
                            self.wfile.write(bytes('File not found\n', 'utf-8'))
                    else:
                        self.send_response(405)
                        self.end_headers()
                        self.wfile.write(bytes('Only GET is supported\n', 'utf-8'))
                else:
                    if method in route:
                        content = route[method]
                        if content is not None:
                            self.send_response(200)
                            self.end_headers()
                            # here we print the modifications
                            self.wfile.write(bytes(str(content()), 'utf-8'))
                        else:
                            self.send_response(404)
                            self.end_headers()
                            self.wfile.write(bytes('Not found   \n', 'utf-8'))
                    else:
                        self.send_response(405)
                        self.end_headers()
                        self.wfile.write(bytes(method + ' is not supported\n', 'utf-8'))

    def get_route(self):
        for path, route in self.routes.items():
            if re.match(path, self.path):
                # print(self.path)
                # print("route_selected=" + str(route))
                return route

        return None

    def do_HEAD(self):
        print("exec head")
        self.handle_method('HEAD')

    def do_GET(self):
        print("exec get")
        self.handle_method('GET')

    def do_POST(self):
        print("exec post")
        self.handle_method('POST')

    def do_PUT(self):
        print("exec put")
        self.handle_method('PUT')

    def do_DELETE(self):
        print("exec delete")
        self.handle_method('DELETE')


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
