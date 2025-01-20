# Insecure Social media web app

Base application, adapted for the purpose of training. Modified from the original at https://github.com/paramsgit/Socialbook
Check the source for proper documentation.

Credits to the original owner.

# Social book Web app

In this folder, it's possible to find a web application, that contains the following vulnerabilities:

1. Information Leakage
2. SQL Injection
3. Cryptographic Failure
4. Server Side Request Forgery
5. Cross-site Scripting (XSS)
6. Server Side Template Injection

To see how you can explore the above vulnerabilities and how to fix them, you can check the ```vuln``` folder.

To run this project:

```bash
docker compose up --build
```

There might be problems with SQLite3 Database setup.

If everything looks good, just open ```localhost:8080``` in your browser.