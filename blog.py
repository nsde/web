import os
import flask
import markdown
import collections

from datetime import datetime

def get_posts():
    post_dates = {}

    for post in os.listdir('blog/'):
        post_dates[post] = os.path.getmtime(f'blog/{post}/page.md')

    posts = []
    for post in sorted(post_dates, key=post_dates.get, reverse=True):
        posts.append(get_info(post))
    
    return posts

def get_info(post: str):
    md_code = open(f'blog/{post}/page.md').read()

    author = md_code.split('\nauthor: ')[1].split('\n')[0]
    tags = md_code.split('\ntags: ')[1].split('\n')[0]

    title = md_code.split('\n# ')[1].split('\n')[0]
    description = md_code.split('\nsubtitle: ')[1].split('\n')[0]

    md_code = markdown.markdown(md_code.split('\n---\n')[1])
    last_update = datetime.fromtimestamp(os.path.getmtime(f'blog/{post}/page.md')).strftime('%a %d/%m/%Y')

    return {
        'path': f'blog/{post}',
        'title': title,
        'author': author,
        'tags': tags.split(', '),
        'md_code': md_code,
        'description': description,
        'last_update': last_update
    }

def register(app: flask.Flask):
    @app.route('/blog/<post>')
    def blog_post(post):
        if not os.path.isdir(f'blog/{post}'):
            return flask.render_template('error.html', title='Blog post not found!', description='Maybe the post got remove or renamed. In the last case, use the search box below.')

        info = get_info(post)

        return flask.render_template('blog.html', post=post, author=info['author'], tags=info['tags'], last_update=info['last_update'], content=info['md_code']) \
                                                            .replace(
            '$$ title $$',          info['title'])          .replace(
            '$$ description $$',    info['description'])    .replace(
            '$$ image $$',          f'/blog/{post}/image'
        )
    
    @app.route('/blog/<post>/image')
    def blog_post_image(post):
        return flask.send_file(f'blog/{post}/image.jpg', mimetype='image/jpg')

    @app.route('/blog/@<user>')
    def blog_user(user):
        posts = [post for post in get_posts() if post['author'] == user]
        
        tags = []
        for post in posts:
            for tag in post['tags']:
                tags.append(tag)

        tags = [tag[0] for tag in collections.Counter(tags).most_common()]
        
        return flask.render_template('posts.html', type='User', text=user, tags=tags, posts=posts)

    @app.route('/blog/+<tag>')
    def blog_tag(tag):
        return flask.render_template('posts.html', type='Tag', text=tag, posts=[post for post in get_posts() if tag in post['tags']])