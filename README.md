# modern-ti-research
A modern look at template injections with modern frameworks

## structure
### introduction
- introduce template injections, small differences between server-side and client-side injections
- this paper will take a modern look since James Kettle's 2015 release of [Server-Side Template Injection:
RCE for the modern webapp](https://www.blackhat.com/docs/us-15/materials/us-15-Kettle-Server-Side-Template-Injection-RCE-For-The-Modern-Web-App-wp.pdf)

### summary
- common XSS vulnerabilities can easily lead to template injections/RCE
- trusting user input and serving that data back to the user
- sandboxing, helps prevent more damaging RCE

### popular frameworks
#### flask
- very popular, tons of exploits
- quick review on the exploit
- bypassing filters with fixes

#### Vue.js/Express
- JavaScript frameworks, less used but still vulnerable
- review on exploits? (still need to research)
- bypassing filters with fixes

#### Laravel
- PHP, somehow still used
- review on exploits (still need to research)
- bypassing filters with fixes




## frameworks
- Flask - Jinja
- Laravel - Blade
- Vue.js - home-built? unsure
- Express - customizable