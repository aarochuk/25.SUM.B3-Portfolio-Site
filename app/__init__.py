import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

mydb =  MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                       user=os.getenv("MYSQL_USER"),
                       password=os.getenv("MYSQL_PASSWORD"),
                       host=os.getenv("MYSQL_HOST"),
                       port=3306)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

# For whatever reason flask can't handle using 127.0.0.1 AND localhost at the same time smh
def get_base_url():
    """Get the base URL for the current request"""
    return request.host_url.rstrip('/')

@app.route('/')
def index():
    return render_template('index.html', title="Portfolio Home", url=get_base_url(), mapbox_token=os.getenv("MAPBOX_API_TOKEN"))


def handle_route(route_name, content_template, page_title):
    """Helper function to handle both AJAX and direct page requests"""
    content = render_template(content_template, mapbox_token=os.getenv("MAPBOX_API_TOKEN"))
    
    # Check if this is an AJAX request by looking for Accept header that indicates JSON response is expected
    accept_header = request.headers.get('Accept', '')
    is_ajax = (
        'application/json' in accept_header or
        request.headers.get('X-Requested-With') == 'XMLHttpRequest' or
        request.args.get('ajax') == 'true'
    )
    
    if is_ajax:
        # Return JSON for AJAX requests
        return jsonify({
            'title': page_title,
            'content': content
        })
    else:
        # Return full HTML page for direct visits/reloads
        return render_template('index.html', 
                             title=page_title, 
                             url=get_base_url(),
                             initial_content=content,
                             active_route=route_name)

@app.route('/about')
def about():
    return handle_route('about', 'content/about_content.html', 'About Page')

@app.route('/experience')
def experience():
    return handle_route('experience', 'content/experience_content.html', 'Experience')

@app.route('/education')
def education():
    return handle_route('education', 'content/education_content.html', 'Education')

@app.route('/hobbies')
def hobbies():
    return handle_route('hobbies', 'content/hobbies_content.html', 'Hobbies')

@app.route('/travel')
def travel():
    return handle_route('travel', 'content/travel_content.html', 'Travel')

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post', methods=['DELETE'])
@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_timeline_post(post_id=None):
    if post_id is not None:
        # If post_id provided delete that
        try:
            post = TimelinePost.get_by_id(post_id)
            post.delete_instance()
            return jsonify({'message': f'The timeline post with id {post_id} has been deleted successfully.'}), 200
        except TimelinePost.DoesNotExist:
            return jsonify({'message': f'There was no timeline post with id {post_id}.'}), 404
    else:
        # If no post_id deleted the most recently created entry
        post = TimelinePost.select().order_by(TimelinePost.created_at.desc()).first()
        if post:
            post_id = post.id
            post.delete_instance()
            return jsonify({'message': f'Latest timeline post with id {post_id} deleted successfully.'}), 200
        else:
            return jsonify({'message': 'There are no timeline posts to delete'}), 404

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")

if __name__ == '__main__':
    app.run(debug=True)