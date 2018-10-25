#!/usr/bin/python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# create and bind engine
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# session instance var is connected and ready to use
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                # send OK
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # get list of restaurants
                restaurants = session.query(Restaurant).all()
                # add list of restaurants to html code
                output = "<html><body>"
                output += "<a href='/restaurants/new'>Add Restaurant</a><p>"
                for r in restaurants:
                    output += r.name + "<br/>"
                    output += '<a href="'
                    output += "/restaurants/" + str(r.id) + "/edit"
                    output += '">Edit</a>' + "<br/>"
                    output += '<a href="'
                    output += "restaurants/%s/delete" % r.id
                    output += '">Delete</a>' + "<br/>"
                    output += "<br/>"
                output += "</p></body></html>"
                # send output and print to terminal
                self.wfile.write(output)
                print output
                return
            elif self.path.endswith("/restaurants/new"):
                # send OK
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # make html header
                output = "<html><body><h1>Make a new Restaurant</h1>"
                output += "</br><form method='POST' enctype='multipart/"
                output += "form-data' action='/restaurants/new'>"
                output += "<input name='newRestaurantName' type='text'"
                output += "placeholder='New Restaurant Name'>"
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return
            elif self.path.endswith("/edit"):
                # send OK
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # get id of restaurant
                rID = self.path.split("/")[2]
                # create output
                output = "<html><body><h1>"
                output += session.query(Restaurant).get(rID).name + "</h1>"
                output += "<form method='POST' enctype='multipart/"
                output += "form-data' action='/restaurants/" 
                output += str(rID) + "/edit'>"
                output += "<input name='updatedRestaurantName' type='text' "
                output += "placeholder='Update Restaurant Name'>"
                output += "<input type='submit' value='Rename'>"
                output += "</form></body></html>"
                self.wfile.write(output)
            elif self.path.endswith("/delete"):
                # send OK
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # get id of restaurant
                rID = self.path.split("/")[2]
                # create output
                output = "<html><body><h1>"
                output += "Are you sure you want to delete "
                output += session.query(Restaurant).get(rID).name + "?</h1>"
                output += "<form method='POST' enctype='multipart/"
                output += "form-data' action='/restaurants/" 
                output += str(rID) + "/delete'>"
                output += "<input type='submit' value='Delete'></form>"
                output += "</body></html>"
                self.wfile.write(output)

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.
                                                getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')

                # create restaurant
                newR = Restaurant(name=messagecontent[0])
                session.add(newR)
                session.commit()
                # send response
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
            elif self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.
                                                getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('updatedRestaurantName')
                # get old restaurant
                rID = self.path.split("/")[2]
                restaurant = session.query(Restaurant).get(rID)
                restaurant.name = messagecontent[0]
                # sql commit
                session.add(restaurant)
                session.commit()
                # send response
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
            elif self.path.endswith("/delete"):
                # get restaurant ID
                rID = self.path.split("/")[2]
                # sql commit
                restaurant = session.query(Restaurant).get(rID)
                session.delete(restaurant)
                session.commit()
                # send response
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
                
        except:
            print("ERROR on posting!")


def main():
    try:
        # set up server on port 8080
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        
        # output message
        print "Web Server running on port %s" % port
        # keep server running until control+c
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        session.close()
        server.socket.close()

if __name__ == '__main__':
    main()
