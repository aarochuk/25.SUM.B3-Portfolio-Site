import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        
    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()
        
    def test_create_timeline_post(self):
        post = TimelinePost.create(name="John Doe", email="john@example.com", content="Hello, world!")
        assert post.id == 1
        second_post = TimelinePost.create(name="Jane Doe", email="jane@example.com", content="Hello, world!")
        assert second_post.id == 2
        
        # Get timeline posts and assert that the posts are correct
        posts = TimelinePost.select()
        assert len(posts) == 2
        assert posts[0].name == "John Doe"
        assert posts[0].email == "john@example.com"
        assert posts[0].content == "Hello, world!"
        assert posts[1].name == "Jane Doe"
        assert posts[1].email == "jane@example.com"
        assert posts[1].content == "Hello, world!"