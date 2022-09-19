- https://portswigger.net/web-security/server-side-template-injection/exploiting
- https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/template-engines-special-vars.txt
- https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection
- https://www.cobalt.io/blog/a-pentesters-guide-to-server-side-template-injection-ssti
- https://www.invicti.com/blog/web-security/exploiting-ssti-and-xss-in-cms-made-simple/
- https://podalirius.net/en/publications/grehack-2021-optimizing-ssti-payloads-for-jinja2/GreHack_2021_-_Optimizing_Server_Side_Template_Injections_payloads_for_jinja2_paper.pdf
- https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection
- https://jinja.palletsprojects.com/en/3.1.x/templates/?highlight=lipsum#jinja-globals.lipsum
- https://github.com/dotboris/vuejs-serverside-template-xss
- https://owasp.org/www-pdf-archive/Owasp_SSTI_final.pdf

- https://github.com/twigphp/Twig
- https://shopify.github.io/liquid/
- Jinja2


- https://www.synacktiv.com/ressources/modern_php_security_sec4dev.pdf


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