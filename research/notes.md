# notes
- explain an attacker's perspective, seeing input being rendered with classic
    - {{7*7}}
    .. etc
- easy remediations?
- proper remediations
- XSS sometimes leads to template injections, often skimmed over

## explain the reason for template engines and templates
- ease for backend to frontend
- dynamic data entry

- example in Jekyll, you can create `layouts`
- design HTML page with certain variables from backend
- some language example

## flask example


## vue.js
- https://github.com/dotboris/vuejs-serverside-template-xss




## object chain traversal in different languages



## language builtins
```java
$class.inspect("java.lang.Runtime").type.getRuntime().exec("bad-stuff-here")
```
```python
''.__class__.__mro__[1].__subclasses__()[340]('whoami', shell=True, stdout=-1).communicate()[0].strip()
```

## template builtins
In Flask, `cycler`, `lipsum` etc