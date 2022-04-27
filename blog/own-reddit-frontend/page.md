---
tags: programming, tutorial, flask, social media, python
author: ONLIX
subtitle: Create your own Reddit frontend using Flask and the Reddit API!
---

[Cover image by Brett Jordan on Unsplash](https://unsplash.com/photos/0FytazjHhxs).


# Code your own Reddit Frontend
## Introduction

<p><strong>Simplicity:</strong> ⭐⭐⭐<span style="color: rgba(0, 0, 0, 0.2);">⭐⭐</p>

**194 lines** of code (76+21=97 Python + 97 HTML) 

**Too lazy to follow the entire tutorial or to copy everything one by one? [Here's the entire code!](https://github.com/nsdea/own-reddit-frontend)**

***

Maybe you've heard of alternative Reddit front-ends such as [Libreddit](https://libredd.it/). But why do they exist?

Privacy/Transparency (open source), customization (for example, you can edit the top of `style.css` file to customize themes or just simply choose one of the default ones) and simplicity (no ads, huge menus/toolbars,...).

The official Reddit frontend isn't (even though [it used to be](https://github.com/reddit-archive/reddit)) open source - with low hope of the *open-sourceness* of Reddit coming back. This is really sad news, but since we are programmers and the Reddit API is free to use, we can just code our own frontend!

![Libreddit](/$$ path $$/libreddit.png)
*A screenshot of Libreddit (we're going to build something similar-ish)*

The great thing about this project is that you can customize every aspect of it. Want to add support for a login box? Don't like the color scheme (which is actually extremely simple to do thanks to LilaCSS [[docs & repo]](https://github.com/nsde/lilacss) [[demo of themes]](https://lilacss.netlify.app/)? Want to list the comments of a post? Just take a look at the [Reddit API](https://praw.readthedocs.io/en/stable/) and have fun!

## Preparation

We especially need the libraries [*Flask*](https://pypi.org/project/Flask/) and [*PRAW*](https://pypi.org/project/mcstatus/) (Python Reddit API Wrapper) in our project.

This project isn't quite simple, so I suggest you take a look at my tutorial on [how to build a Minecraft Serverlist](https://onlix.me/blog/own-minecraft-server-list) before. Even if you're not interested in doing so - it could be useful to have it opened because it's quite similar to this project.

First, we need to install a few packages. You need to have [pip installed](https://www.liquidweb.com/kb/install-pip-windows) for the following commands to work. I'm going to assume that you already have a new *Python* version (I'd recommend at least 3.7 or 3.8+) and *pip* installed correctly.

So, open up your command line and enter the following commands to install the required packages:

    pip3 install praw flask Markdown python-dotenv


The command above is short for:

    pip3 install praw
    pip3 install flask
    pip3 install Markdown
    pip3 install python-dotenv

If the commands above fail, try `pip` instead of `pip3`.
The output looks like this for me:

<pre>(base) <font color="#26A269"><b>lix@on</b></font>:<font color="#12488B"><b>~</b></font>$ pip3 install praw flask Markdown python-dotenv
...
Successfully installed Markdown-3.3.6 flask-2.1.1 praw-7.5.0 python-dotenv-0.20.0
(base) <font color="#26A269"><b>lix@on</b></font>:<font color="#12488B"><b>~</b></font>$ 

</pre>

You can also 

Alright, before we can actually start, we need to organize our project. Set up the following folder/file structure to get started:

    📂 reddit

        📂 static
            📄 style.css
        
        📂 templates
            📄 index.html
        
        📄 .env
        📄 web.py
        📄 reddit.py


> **Tip ·** Do not name Python files by a module/library. For example, don't create a Python file called `flask.py` or `mcstatus.py`. This is because then, Python will try to import the wrong module.

> **Notice ·** You might need to enable "show hidden files" in your file explorer's settings. [Here's how! (Windows 10/11)](https://support.microsoft.com/en-us/windows/view-hidden-files-and-folders-in-windows-97fbc472-c603-9d90-91d0-1166d1d9f4b5#WindowsVersion=Windows_11)

Again, I won't go into detail about some parts of the code which I have already explained in <a href="https://onlix.me/blog/own-minecraft-server-list">how to create a Minecraft server list</a>.

### API credentials

> **Warning ·** Keep these credentials super secure and private! If you don't, the bot could get used by malicious people to spread malware or other illegal content!

- Create a Reddit bot app ([here's how to, you just to watch it until 4:57](https://youtu.be/3FpqXyJsd1s)) and store all needed credentials safely, for example using [Bitwarden](https://bitwarden.com/) (or just copy them).

- Rename `env_template.txt` to `.env` and change its content accordingly to the values you just saved or copied.

- Make sure you copied them correctly! Double-check or view another tutorial. These pages might help: [https://www.reddit.com/wiki/api](https://www.reddit.com/wiki/api) and [https://praw.readthedocs.io/en/stable/getting_started/authentication.html](https://praw.readthedocs.io/en/stable/getting_started/authentication.html)

## Python Backend (`web.py`)

    import reddit

    import flask

    app = flask.Flask(__name__, static_url_path='/')

Again (2.0), I won't go over some code here as I already explained most Flask features in my tutorial about <a href="https://onlix.me/blog/own-minecraft-server-list">how to create a Minecraft server list</a>.

    @app.route('/')
    def index():
        return flask.redirect('/r/tech') # don't use r/all, because it crashes... maybe you find a fix for that ;)
    
This is just the default home page which redirects the website viewer to `r/tech` by default. You can change this, of course!

    @app.route('/r/<name>')
    def r(name):
        sort = flask.request.args.get('sort') or 'hot'
        return flask.render_template('index.html', posts=reddit.posts(name, sort=sort), sub=reddit.sub(name), sort=sort)

A function for displaying a subreddit. By the way `flask.request.args` finds out what `?sort=hot` in the URL is (or for the example of YouTube: `?v=`): a [query string](https://en.wikipedia.org/wiki/Query_string). We need this for the buttons in the navbar for changing the mode of the sorting system (*hot*, *top* or *new*). 

    @app.route('/u/<name>')
    def u(name):
        sort = flask.request.args.get('sort') or 'hot'
        return flask.render_template('index.html', posts=reddit.posts(name, sort=sort, is_user=True), sub=reddit.user(name), sort=sort)

Same for here.

    app.run(port=1111, debug=True)

Let's move on with the module which makes it easier for use to use the Reddit API! 

## Backend helper for API (`reddit.py`)

    import os
    import praw
    import datetime
    import markdown

We'll need `os` for loading the environment variables, `PRAW` for the API wrapping, `datetime` for formatting time and `markdown` for converting markdown to HTML so we can display text correctly.

    from dotenv import load_dotenv

    load_dotenv()

The function above retrieves the data from the file `.env` and sets the environment variables accordingly.

    client = praw.Reddit(
        client_id=os.getenv('ID'),
        client_secret=os.getenv('SECRET'),
        user_agent='script',
        username=os.getenv('NAME'),
        password=os.getenv('PASS')
    )

    client.validate_on_submit = True

Initializes the API wrapper with our credentials which were set into the environment variables.

    def sub(name):
        data = client.subreddit(name)
        setattr(data, 'subscribers', f'{data.subscribers:,}') # convert to comma-separated number
        setattr(data, 'name', data.display_name)
        setattr(data, 'type_char', 'r') # r = subreddit, u = user
        setattr(data, 'description', markdown.markdown(data.description))
        
        return data

The function above is used for retrieving details about a subreddit. I set some attributes to make it easier to use within the actual API-frontend (the HTML file). Next, let's make a function for accessing information from a user on Reddit.

    def user(name):
        data = client.redditor(name)
        setattr(data, 'subscribers', f'{data.comment_karma + data.link_karma:,} Karma') # convert to comma-separated number
        setattr(data, 'type_char', 'u') # r = subreddit, u = user
        setattr(data, 'description', f'''
            {"🌟 Reddit Premium" if data.is_gold else ""}
            {"✅ Verified" if data.has_verified_email else ""}
            {"👮 Mod" if data.is_mod else ""}
            {"🔧 Reddit Employee" if data.is_employee else ""}
            {"🤝 Friends" if data.is_friend else ""}
        ''')

        return data

The goes for here, use for an user. I set "subscribers" to the user karma so we don't have to check if the frontend is displaying an user or subreddit. 

    def posts(name, sort='hot', is_user=False): # fetch posts from subreddit
        if is_user:
            sub = client.redditor(name)
        else:
            sub = client.subreddit(name)

We need to check if the post that should be displayed are from a subreddit or an user.

        posts = []

        fetch = sub.hot # default sort
        if sort == 'top': fetch = sub.top
        if sort == 'new': fetch = sub.new

This is for making the choice to switch between "hot", "top" or "new" sort available.

        for p in fetch(limit=10): # only first 10 posts, to improve speed. you can change this to a higher number if you want more posts
            setattr(p, 'time', datetime.datetime.fromtimestamp(p.created_utc).strftime('%b %d %Y %H:%M')) # when the post was created

We need to convert the time from unix to a formatted string humans can actually understand properly.

            if isinstance(p, praw.models.reddit.comment.Comment):
                setattr(p, 'text', p.body_html)
                setattr(p, 'url', p.permalink)
                setattr(p, 'subreddit', p.subreddit.display_name)

Some fixes for if the post is actually a comment.

            else:
                setattr(p, 'text', markdown.markdown(p.selftext)) # convert markdown to HTML

Some Reddit description texts are saved in markdown, but we need to convert it into HTML so we can display it correctly. 

            setattr(p, 'score', f'{p.score:,}')
            setattr(p, 'num_comments', f'{p.num_comments:,}')

Self-explanatory. By the way, the `:,` adds commas for large numbers: 123456 → 123,456

            posts.append(p)

        return posts

Alright. We're done with this file!

## HTML Frontend (`templates/index.html`)

Let's get started with our last file (we have to create for ourselves) for this project - the Jinja2 HTML template!  

    <!DOCTYPE html>
    <html lang="en">

    <head>
        <title>RedditFrontend</title>
        <link rel="stylesheet" href="/style.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
        <link rel="favicon" href="/logo.png">
        <link rel="icon" type="image/png" href="/logo.png"/>

        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="initial-scale=1.0">

    </head>
        
...Just standard HTML head stuff...

    <body class="midnight">

My CSS framework that we use (LilaCSS) has a few [pre-defined color schemes](https://lilacss.netlify.app). We just set it to "midnight". You can change it how you want to (just check out [the demo]((https://lilacss.netlify.app))), for example `"ocean night"`.

        <header class="transparent-2" style="--image: url('{{ sub.banner_img }}')">

`transparent-2` makes the subreddit banner darker so we can read the text in the foreground properly.    

            <nav>
                <a href="?sort=hot" class="{{ 'current' if sort == 'hot' else '' }}"><i class="bi bi-graph-up"></i> Hot</a>
                <a href="?sort=top" class="{{ 'current' if sort == 'top' else '' }}"><i class="bi bi-star"></i> Top</a>
                <a href="?sort=new" class="{{ 'current' if sort == 'new' else '' }}"><i class="bi bi-stars"></i> New</a>   
            </nav>
        
Adds the three buttons for choosing the sort order and redirecting the user accordingly.

            <h1>{{sub.type_char}}/{{ sub.name }}</h1>
            <details>
                <summary>Click here to show the community description.</summary>
                <p>{{ sub.description | safe }}</p>
            </details>
            <p><strong><i class="bi bi-people-fill"></i> {{ sub.subscribers }}</strong></p>
            <!-- <a href="https://reddit.com/r/{{ sub.display_name }}"><button><i class="bi bi-arrow-up-right-circle"></i> Open in normal Reddit</button></a> -->
        </header>
        
As explained in my tutorial on [how to build a Minecraft Serverlist](https://onlix.me/blog/own-minecraft-server-list), `| safe` allows [Jinja2](https://jinja.palletsprojects.com/en/) to use actual HTML code inside of the template.

        <main>
            <div class="posts">
                {% for post in posts %}
                <div class="post">
                    {% if post.url.startswith('https://i.') %}
                    <img src="{{ post.url }}" style="{{ 'filter: blur(20px);' if post.over_18 else '' }}">

Obviously blurs media marked as "NSFW".

                    {% else %}
                    <br>
                    {% endif %}

                    <div class="content">

Next, we need to show a <mark>tag</mark> in which subreddit the post was submitted if we're on an user page.

                        {% if post.subreddit %}
                        <a href="https://reddit.com{{ post.url }}" class="plain">
                            <mark><strong>{{ post.subreddit }}</strong></mark>
                        {% else %}
                        <a href="/u/{{ post.author.name }}" class="plain">
                        {% endif %}

The following code displays the profile picture of the user that submitted the post.

                            <img src="{{ post.author.icon_img }}" style="width: 20px; border: 100%; position: relative; top: 5px;">&nbsp;
                            
And the user name as well as the date when the post was submitted:

                            <h5 style="display: inline;"><strong>u/{{ post.author.name }} ·</strong> {{ post.time }}</h5>
                        </a>

These if-statements are there to display *flairs* on Reddit:

                        <h6 style="margin: 0; display: inline;">
                            {% if post.link_flair_text %}
                            <mark>{{ post.link_flair_text }}</mark>
                            {% endif %}
                            
                            {% if post.is_original_content %}
                            <mark>OC</mark>
                            {% endif %}
                            
                            {% if post.over_18 %}
                            <mark>NSFW</mark>
                            {% endif %}
                            
                            {% if post.locked %}
                            <mark>🔒</mark>
                            {% endif %}

                            {% if post.distinguished %}
                            <mark>🏅</mark>
                            {% endif %}
                        </h6>
                        
And the post title which redirects to the original Reddit post when clicked: 

                        <h4 onclick="window.location.href = '{{ post.url }}'">{{ post.title }}</h4>

As well as text content, converted from markdown into HTML:

                        <p>{{ post.text | safe }}</p>

Lastly, up- and downvote arrows.

                        <p style="font-size: 1.5rem;">
                            <i class="bi bi-arrow-up vote" style="color: rgb(219, 72, 72);" onclick=""></i>
                            {{ post.score}}
                            <i class="bi bi-arrow-down vote" style="color: rgb(20, 114, 207);" onclick=""></i>&nbsp;&nbsp;
                            <i class="bi bi-chat-left-text"></i>
                            {{ post.num_comments }}
                        </p>
                    </div>
                </div>   
                {% endfor %}
            </div>
        </main>
        <footer>

You can leave an informational message in here if you want to, or links to your social media or privacy policy:

            <p>by <a href="https://onlix.me">ONLIX</a></p>
        </footer>
    </body>
    </html>

## Last tweaks

You can add `logo.png` in the directory `reddit/static/` if you want the website to have a little icon next to the tab. [Here's the icon I designed.](https://raw.githubusercontent.com/nsdea/own-reddit-frontend/main/reddit/static/logo.png)

To style the website, just copy everything from [here](https://raw.githubusercontent.com/nsdea/own-reddit-frontend/main/reddit/static/style.css) to `reddit/static/style.css`. If everything worked correctly, the new style should be applied now and the website should look something like this (I changed a few lines, but not too much):

![Result](/$$ path $$/result.png)

## Exercises for you!

I'm done with this project, but I'd really recommend you to try master the following challenges:

- <mark>HTML</mark> <mark>CSS</mark> Use a grid layout for media.
- <mark>HTML</mark> <mark>Python</mark> Create a overview homepage with popular subreddits.
- <mark>HTML</mark> <mark>CSS</mark> <mark>Python</mark> Display a comment section upon click of the comment button. 
- <mark>HTML</mark> <mark>CSS</mark> <mark>Python</mark> <mark>JavaScript</mark> Add a login box so that the up -and downvote buttons actually work. Of course, you can also add much more, such as a feature for commenting and saving posts, posting of your own content and customizing a overview homepage with user-defined subreddits.  

You can even send me a pull request to [the GitHub repository](https://github.com/nsdea/own-reddit-frontend) so I can add sample solutions!

## Conclusion
You've now learned how to use *Flask*, *Jinja2*, the *mcstatus* library and *HTML*. Questions? Issues? Tips to improve this tutorial? [Open an issue](https://github.com/nsdea/own-reddit-frontend/issues/new/choose)! I hope you've learned something. See you next time!