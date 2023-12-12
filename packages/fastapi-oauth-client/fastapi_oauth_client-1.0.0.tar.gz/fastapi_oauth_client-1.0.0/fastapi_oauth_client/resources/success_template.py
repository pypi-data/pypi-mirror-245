template = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
</head>
<body>
    <div class="top-bar" style="background-color:#DCDCDC; height: 50px; width: 100%; position: fixed"></div>
    <div style="margin-top: 0px; padding: 50px;">
        <h2 style="color:#32CD32; text-align: center;">Success!</h2>
        <div class="container">
            <div class="input-group">
                <span id="copyButton" onclick="copyText()" class="input-group-addon btn" title="Click to copy">Copy
                    <i class="fa fa-clipboard" aria-hidden="true"></i>
                    <script>
                    function copyText() {
                        var copyText = document.getElementById("copyTarget");
                        
                        // Select the text field
                        copyText.select();
                        copyText.setSelectionRange(0,99999);
                        
                        // Copy the text inside the text field
                        navigator.clipboard.writeText(copyText.value);
                        
                        alert("Token has been copied!");
                    }
                    </script>
                </span>"""

token_template= """
                <input type="text" id="copyTarget" class="form-control" value="{token}">
            </div>
        </div>
        <p style="text-align: center;">It expires at {expires}</p>
        <h1 id="bearer-token-usage">Bearer Token Usage</h1>"""
explanation = """
<p>This page provides you with a Bearer token that is essential for authenticating your requests against our API.</p>
<h2 id="what-is-a-bearer-token-">What is a Bearer Token?</h2>
<p>A Bearer token is a type of access token used to verify the identity of the user and ensure that the requester is authorized to access the requested resource. It is essentially a string that signifies a granted permission and is passed along with the request.</p>
<h2 id="how-to-use-the-bearer-token-">How to use the Bearer Token?</h2>
<p>When making requests to the API, include the Bearer token in the header of the HTTP request. The token should be prefixed with the word <code>Bearer</code> followed by a space.</p>
<h3 id="example-">Example:</h3>
<p>Suppose you are given the token:</p>
<pre><code>YOUR_TOKEN_VALUE
</code></pre><p>Your HTTP request should have a header like this:</p>
<pre><code><span class="hljs-symbol">Authorization</span>: <span class="hljs-keyword">Bearer </span>YOUR_TOKEN_VALUE
</code></pre><p>Replace <code>YOUR_TOKEN_VALUE</code> with the actual token provided by this page.</p>
<h2 id="python-requests-example-">Python <code>requests</code> Example:</h2>
<p>If you&#39;re using the <code>requests</code> library in Python, here&#39;s how you can make an authenticated API call with the Bearer token:</p>
<pre><code class="lang-python"><span class="hljs-keyword">import</span> requests

url = <span class="hljs-string">'https://api.example.com/data'</span>  <span class="hljs-comment"># Replace with your API endpoint</span>
headers = {
    <span class="hljs-string">'Authorization'</span>: <span class="hljs-string">'Bearer YOUR_TOKEN_VALUE'</span>
}

response = requests.get(url, headers=headers)

<span class="hljs-comment"># Handle the response as needed</span>
<span class="hljs-built_in">print</span>(response.json())
</code></pre>
<p>Again, ensure you replace <code>YOUR_TOKEN_VALUE</code> with your actual token.</p>
<h2 id="important-notes-">Important Notes:</h2>
<ul>
<li>Ensure that you keep your Bearer token secure and do not share it publicly.</li>
<li>Bearer tokens have an expiration time, so you might need to refresh or request a new token after a certain period. (This token expires at {{ expires }})</li>
<li>Always use HTTPS when making requests to the API to ensure the security of your token during transit.</li>
</ul>

    </div>
</body>
    <style>
        .input-group {
            margin-top: 30px;
            position: relative;
        }
        
        #copyButton {
            cursor: pointer;
            background: #f1bb3a;
        }
    </style>
</html>
"""