---
tags: programming, tutorial, flask, social media
author: ONLIX
subtitle: Create your own Reddit frontend using Flask and the Reddit API!
---

[Cover image by Brett Jordan on Unsplash](https://unsplash.com/photos/0FytazjHhxs).


# Code your own Reddit frontend!
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

***
## THIS BLOG POST IS UNDER CONSTRUCTION

> **Tip ·** Do not name Python files by a module/library. For example, don't create a Python file called `flask.py` or `mcstatus.py`. This is because then, Python will try to import the wrong module.

> **Notice ·** You might need to enable "show hidden files" in your file explorer's settings. [Here's how! (Windows 10/11)](https://support.microsoft.com/en-us/windows/view-hidden-files-and-folders-in-windows-97fbc472-c603-9d90-91d0-1166d1d9f4b5#WindowsVersion=Windows_11)


## Python Backend

Great! We're now ready to start coding.
First, let's talk about the first file. `web.py`. This file is used for managing the backend code. The server is being created using `flask` because of its simplicity. Also, `mcstatus` is needed for the Minecraft server API.

Let's start with importing the required libraries and setting up our backend.


    import flask
    import mcstatus

    app = flask.Flask(__name__, static_url_path='/')

`__name__` is just a needed argument for initializing the Flask server.

`static_url_path` makes it so that we can access the local folder `/serverlist/static/` online directly in the root (`localhost:1111/`). This makes the URLs a bit shorter: `/serverlist/static/style.css` will be accessible by viewing  `localhost:1111/style.css`.

### Functions

Uh, so the next function may look a bit weird, but trust me, I'll explain it later.

    def color_codes(text: str): # formatting
        text = text.strip(' <>') # some descriptions have a lot of spaces to center the text in-game but we don't want this here; the <> if for security purposes

        num = 0 # number of spans we used

        codes = {
            '0': 'color: #000000',
            '1': 'color: #0000AA',
            '2': 'color: #00AA00',
            '3': 'color: #00AAAA',
            '4': 'color: #AA0000',
            '5': 'color: #AA00AA',
            '6': 'color: #FFAA00',
            '7': 'color: #AAAAAA',
            '8': 'color: #555555',
            '9': 'color: #5555FF',

            'a': 'color: #55FF55',
            'b': 'color: #55FFFF',
            'c': 'color: #FF5555',
            'd': 'color: #FF55FF',
            'e': 'color: #FFFF55',
            'f': 'color: #FFFFFF',
            
            'l': 'font-weight: bold',
            'm': 'text-decoration:line-through',
            'n': 'text-decoration:underline',
            'o': 'font-style:italic'
        }

        for code in codes.keys():
            text = text.replace(f'§{code}', f'<span style="{codes[code]};">') # add all spans
            num += 1

        return text + num*'</span>' # close all spans

Looks confusing, right? Don't worry, it's simpler than you might think.

Minecraft gives servers the opportunity to customize their server description with colors and other formatting options such as **bold** oder ~~strike through~~ text. [Here's](https://minecraft.fandom.com/wiki/Formatting_codes) more info on how this works.

So, the server could set a description like this:

    §lOur Server! §oJoin now

Which will result in:
> **Our Server!** *Join now*

Alright. You probably can see where this is going. This function just converts the raw description to a readable `HTML` code using a `dict`ionary in Python (to replace the keys and values).


Another function is needed. Don't worry. This one is easier to understand.

    def get_infos(*ips):
        server_data = []

        for ip in ips:
            data = mcstatus.JavaServer.lookup(ip).status()
            text = color_codes(data.description)
            ping = data.latency

            if ping > 0:    color = 'cyan'
            if ping > 20:   color = 'lightgreen'
            if ping > 100:  color = 'yellow'
            if ping > 200:  color = 'orange'
            if ping > 500:  color = 'red'

            server_data.append({'ip': ip, 'data': data, 'text': text, 'color': color})
        
        return server_data

We're doing nothing more than just using the `mcstatus` library to retrieve the server data. The ping (also called *latency*) is the delay for the server to respond to a certain request measured in milliseconds. If the server's slow, the `color` is set to `red`. If the server is super fast it's `color` set to `lightgreen` or even `cyan`. Pretty easy, huh?


### Pages

Okay, let's move on. To host the pages, just a few lines are needed:

    # Shows stats of a few featured servers
    @app.route('/') # can be accessed via: "localhost:1111/"
    def index():
        return flask.render_template('index.html', servers=get_infos('hypixel.net', 'gommehd.net', '2b2t.org', 'neruxvace.net')) # render the homepage with all default/featured servers

    # Shows only stats of a specific server
    @app.route('/only/<ip>') # can be accessed via: "localhost:1111/only/hypixel.net" (for example)
    def server(ip): 
        return flask.render_template('index.html', servers=get_infos(ip)) # render the page with just the specified server

A Flask `@app.route` gives us a the opportunity of adding a new subpath. This means if we type have the route `/example/site`, we'd have to type `localhost:1111/example/site` (or `127.0.0.1:1111/example/site` of course) on our web browser to access the site. 

All standard web browser render `HTML` code to display a page to the visitor. This means, we need to pass such code. The problem is: we have dynamic content with variables (the `servers` parameter) to pass. Jinja2 is helping us with that by filling out the template we'll [soon](#html-frontend) create with these values.

In the second function, we also specify parameters for the URL which can be used: we can visit anything from `localhost:1111/only/hypixel.net` to `localhost:1111/only/gommehd.net` and the backend will process the data and render a new webpage.

Okay, we're almost done with the Python code! Just one more line to run the server:

    app.run(port=1111, debug=True)

`port=1111` hosts the server the specified port. Basically the number when typing `localhost:1111` or `127.0.0.1:1111`. If you get an `OSError` saying `OSError: [Errno 98] Address already in use`, just try to change the port. Obviously, this also means you have to change all other parts in the code where you mentioned port. In addition to that, a new URL is going to be needed for viewing the website.

Most of the time, Flask ports such as 3000 or 5000 are being used, but you can customize it to pretty much whatever you want to - under the assumption that the port isn't taken yet and the port is in the valid range.

> **Linux pro tip ·** If you want to expose your app to the local network you can try running `sudo ufw allow 1111/tcp` to open the port, this may not be necessary depending on your distribution or firewall-settings.

`debug=True` makes it so that every time one of the server's files (no matter if it's a Python or HTML file) are changed, the server restarts to apply the change. This is really useful when testing the server.

## HTML Frontend
To set up the frontend, we're going to need website structure. Thanks to Jinja2, we can use variables. We need to add the following to our `index.html`:

    <!DOCTYPE html>
    <html lang="en">

    <head>
        <title>Server List</title>
        <link rel="stylesheet" href="/style.css">

        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="initial-scale=1.0">
    </head>

This is just the basic start of the HTML document. The only important thing is `<link rel="stylesheet" href="/style.css">`, which sets the path to our CSS file. More on that later.

    <body>
        <header>
            <h1>Minecraft Server List</h1>
            <p>This app was created using <i>Flask</i> and <i>mcstatus</i></p>
        </header>

This is, as you can imagine, just the simple header of the website with a bit of info.

        <main>
            <div class="posts">
                {% for server in servers %}

Now it's starting to get a bit of complicated - we're looping through every single server in our list. The list is passed using Jinja2 with `render_template` at the end of every `@app.route` function.

The `div` is obviously there to make it look more organized when applying our CSS. Let's move on!

                <div class="post" onclick="navigator.clipboard.writeText('{{ server.ip }}'); alert('Copied IP {{ server.ip }}!');">

Right here, we're adding a `div` for the server in our loop for the info widgets. The `onclick` parameter defines a inline-JavaScript code which is being ran every time the user clicks on the `post`: the server address (IP) is copied to the clipboard. This is useful for when you want to join the Minecraft server.

                    <img src="{{ server.data.favicon }}">

Add the server logo.

                    <div class="content">

This is needed for the CSS to work properly - otherwise the box might look quite weird.

                        <h5>{{ server.data.version.name }}</h5>
                        <h4><code>{{ server.ip }}</code></h4>

A bit more information about the server.

                        <h4 style="color: {{ server.color }};">{{ server.data.latency | round }} ms</h4>

We're using **inline CSS** to quickly change the color of the ping text depending on its value, for slow connections, it will be red, and for fast ones obviously green. 

                        <h4>{{ server.data.players.online }}/{{ server.data.players.max }} online</h4>

How how many players are currently connected to the Minecraft server.

                        <p>{{ server.text | safe }}</p>

You might ask what the `| safe ` does. It simply allows Jinja2 to render HTML code. This is considered unsafe because malicious code could be inserted here, so Jinja2 requires us to use this tag. 

This paragraph shows the server description formatted using the function `color_codes()`. If we didn't have this function, the output would look quite weird because of all the formatting used in Minecraft server descriptions.

                    </div>
                </div>   
                {% endfor %}
            </div>
        </main>
    </body>
    </html>

There we go! In theory, we are already done and our website is working fine. But wait - it looks horrible! This is because it does not have a CSS file. The only fine left! But don't worry. You can just use my self made framework *LilaCSS*. 

Just copy everything from [here](https://raw.githubusercontent.com/nsdea/own-minecraft-server-list/main/serverlist/static/style.css) to `serverlist/static/style.css`. If everything worked correctly, the new style should be applied now and the website should look something like this (I changed a few lines for simplicity, but it should look almost the same):

![Result](/$$ path $$/result.png)

- <mark>HTML</mark> <mark>CSS</mark> Use a grid layout for media.
- <mark>HTML</mark> <mark>Python</mark> Create a overview homepage with popular subreddits.
- <mark>HTML</mark> <mark>CSS</mark> <mark>Python</mark> Display a comment section upon click of the comment button. 
- <mark>HTML</mark> <mark>CSS</mark> <mark>Python</mark> <mark>JavaScript</mark> Add a login box so that the up -and downvote buttons actually work. Of course, you can also add much more, such as a feature for commenting and saving posts, posting of your own content and customizing a overview homepage with user-defined subreddits.  

You can even send me a pull request to [the GitHub repository](https://github.com/nsdea/own-reddit-frontend) so I can add sample solutions.

## Conclusion
You've now learned how to use *Flask*, *Jinja2*, the *mcstatus* library and *HTML*. Questions? Issues? Tips to improve this tutorial? [Open an issue](https://github.com/nsdea/own-minecraft-server-list/issues/new/choose)! I hope you've learned something. See you next time!