import unittest
import os

os.environ["TESTING"] = "true"

from app import app

class AppTestCase(unittest.TestCase):
   def setUp(self):
       self.client = app.test_client()
       
   def test_home_page(self):
       response = self.client.get("/")
       assert response.status_code == 200
       html = response.get_data(as_text=True)
       assert "<title>Portfolio Home</title>" in html
       
       # Map of locations for each fellow
       fellows_locations = {
           'ryan': [
               {'name': 'Cusco, Peru', 'coordinates': [-71.984978, -13.529427]},
               {'name': 'Yosemite National Park, California USA', 'coordinates': [-119.538330, 37.865101]},
               {'name': 'NYC, New York USA', 'coordinates': [-73.935242, 40.730610]},
               {'name': 'Banff National Park, Alberta Canada', 'coordinates': [-115.928055, 51.496845]}
           ],
           'azam': [
               {'name': 'Barcelona, Spain', 'coordinates': [2.1734, 41.3851]},
               {'name': 'Rome, Italy', 'coordinates': [12.4964, 41.9028]},
               {'name': 'Cairo, Egypt', 'coordinates': [31.2357, 30.0444]},
               {'name': 'Mumbai, India', 'coordinates': [72.8777, 19.0760]}
           ],
           'andrew': [
               {'name': 'Bangkok, Thailand', 'coordinates': [100.5018, 13.7563]},
               {'name': 'Seoul, South Korea', 'coordinates': [126.9780, 37.5665]},
               {'name': 'Vancouver, Canada', 'coordinates': [-123.1207, 49.2827]}
           ]
       }
       #Check if all of the Fellow's locations are in the html
       for fellow in fellows_locations.keys():
           for location in fellows_locations[fellow]:
               assert location['name'] in html
               for coor in location['coordinates']:
                   assert str(coor) in html
       
       def test_timeline(self):
           response = self.client.get('/api/timeline_post')
           assert response.status_code == 200
           assert response.is_json
           json = response.get_json()
           
           assert "timeline_posts" in json
           assert len(json['timeline_posts']) == 0
           
           #Add timeline post and check if it is on the html
           response = self.client.post('/api/timeline_post', data={'name': 'John Doe', 'email': 'john@example.com', 'content': 'Hello, world!'})
           assert response.status_code == 200
           assert response.is_json
           json = response.get_json()
           assert json['name'] == 'John Doe'
           assert json['email'] == 'john@example.com'
           assert json['content'] == 'Hello, world!'
           
           response = self.client.get('/timeline')
           assert response.status_code == 200
           html = response.get_data(as_text=True)
           assert "<p>John Doe</p>" in html
           assert "<p>john@example.com</p>" in html
           assert "<p>Hello, world!</p>" in html
           
           
           
               
        
       
        