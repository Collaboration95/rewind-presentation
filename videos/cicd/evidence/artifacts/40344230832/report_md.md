# ZAP Scanning Report

ZAP by [Checkmarx](https://checkmarx.com/).


## Summary of Alerts

| Risk Level | Number of Alerts |
| --- | --- |
| High | 0 |
| Medium | 4 |
| Low | 7 |
| Informational | 6 |




## Insights

| Level | Reason | Site | Description | Statistic |
| --- | --- | --- | --- | --- |
| Low | Warning |  | ZAP warnings logged - see the zap.log file for details | 7    |
| Info | Informational | https://d2jelzl0fbj693.cloudfront.net | Percentage of endpoints with content type image/svg+xml | 100 % |
| Info | Informational | https://d2jelzl0fbj693.cloudfront.net | Percentage of endpoints with method GET | 100 % |
| Info | Informational | https://d2jelzl0fbj693.cloudfront.net | Count of total endpoints | 2    |
| Info | Informational | https://d2m6kz76y4kuvm.cloudfront.net | Percentage of responses with status code 2xx | 91 % |
| Info | Informational | https://d2m6kz76y4kuvm.cloudfront.net | Percentage of responses with status code 3xx | 3 % |
| Info | Informational | https://d2m6kz76y4kuvm.cloudfront.net | Percentage of responses with status code 4xx | 4 % |
| Info | Informational | https://d2m6kz76y4kuvm.cloudfront.net | Percentage of endpoints with content type application/javascript | 6 % |
| Info | Informational | https://d2m6kz76y4kuvm.cloudfront.net | Percentage of endpoints with content type application/json | 10 % |
| Info | Informational | https://d2m6kz76y4kuvm.cloudfront.net | Percentage of endpoints with content type application/octet-stream | 13 % |
| Info | Informational | https://d2m6kz76y4kuvm.cloudfront.net | Percentage of endpoints with content type image/png | 36 % |
| Info | Informational | https://d2m6kz76y4kuvm.cloudfront.net | Percentage of endpoints with content type image/x-icon | 3 % |
| Info | Informational | https://d2m6kz76y4kuvm.cloudfront.net | Percentage of endpoints with content type text/html | 26 % |
| Info | Informational | https://d2m6kz76y4kuvm.cloudfront.net | Percentage of endpoints with method GET | 100 % |
| Info | Informational | https://d2m6kz76y4kuvm.cloudfront.net | Count of total endpoints | 30    |
| Info | Informational | https://d2m6kz76y4kuvm.cloudfront.net | Percentage of slow responses | 100 % |
| Info | Informational | https://d33gr5sjna5oyg.cloudfront.net | Percentage of endpoints with content type text/css | 20 % |
| Info | Informational | https://d33gr5sjna5oyg.cloudfront.net | Percentage of endpoints with content type text/javascript | 79 % |
| Info | Informational | https://d33gr5sjna5oyg.cloudfront.net | Percentage of endpoints with method GET | 100 % |
| Info | Informational | https://d33gr5sjna5oyg.cloudfront.net | Count of total endpoints | 44    |
| Info | Informational | https://dag2zz4hdxr0w.cloudfront.net | Percentage of endpoints with content type text/css | 100 % |
| Info | Informational | https://dag2zz4hdxr0w.cloudfront.net | Percentage of endpoints with method GET | 100 % |
| Info | Informational | https://dag2zz4hdxr0w.cloudfront.net | Count of total endpoints | 1    |
| Info | Informational | https://rewind-dev-330599756236.auth.ap-southeast-1.amazoncognito.com | Percentage of endpoints with content type application/json | 50 % |
| Info | Informational | https://rewind-dev-330599756236.auth.ap-southeast-1.amazoncognito.com | Percentage of endpoints with content type text/html | 50 % |
| Info | Informational | https://rewind-dev-330599756236.auth.ap-southeast-1.amazoncognito.com | Percentage of endpoints with method GET | 100 % |
| Info | Informational | https://rewind-dev-330599756236.auth.ap-southeast-1.amazoncognito.com | Count of total endpoints | 2    |







## Alerts

| Name | Risk Level | Number of Instances |
| --- | --- | --- |
| CSP: Failure to Define Directive with No Fallback | Medium | 3 |
| CSP: Wildcard Directive | Medium | 3 |
| CSP: script-src unsafe-inline | Medium | 3 |
| CSP: style-src unsafe-inline | Medium | 3 |
| Cross-Origin-Embedder-Policy Header Missing or Invalid | Low | 3 |
| Cross-Origin-Opener-Policy Header Missing or Invalid | Low | 3 |
| Cross-Origin-Resource-Policy Header Missing or Invalid | Low | 3 |
| Dangerous JS Functions | Low | 1 |
| Permissions Policy Header Not Set | Low | Systemic |
| Server Leaks Version Information via "Server" HTTP Response Header Field | Low | Systemic |
| Timestamp Disclosure - Unix | Low | Systemic |
| Content Security Policy (CSP) Report-Only Header Found | Informational | Systemic |
| Information Disclosure - Suspicious Comments | Informational | 3 |
| Modern Web Application | Informational | 5 |
| Non-Storable Content | Informational | 4 |
| Re-examine Cache-control Directives | Informational | Systemic |
| Storable and Cacheable Content | Informational | Systemic |




## Alert Detail



### [ CSP: Failure to Define Directive with No Fallback ](https://www.zaproxy.org/docs/alerts/10055/)



##### Medium (High)

### Description

The Content Security Policy fails to define one of the directives that has no fallback. Missing/excluding them is the same as allowing anything.

* URL: https://d2m6kz76y4kuvm.cloudfront.net
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `frame-ancestors 'none'`
  * Other Info: `The directive(s): form-action is/are among the directives that do not fallback to default-src.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/robots.txt
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/robots.txt`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `frame-ancestors 'none'`
  * Other Info: `The directive(s): form-action is/are among the directives that do not fallback to default-src.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `frame-ancestors 'none'`
  * Other Info: `The directive(s): form-action is/are among the directives that do not fallback to default-src.`


Instances: 3

### Solution

Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.

### Reference


* [ https://www.w3.org/TR/CSP/ ](https://www.w3.org/TR/CSP/)
* [ https://caniuse.com/#search=content+security+policy ](https://caniuse.com/#search=content+security+policy)
* [ https://content-security-policy.com/ ](https://content-security-policy.com/)
* [ https://github.com/HtmlUnit/htmlunit-csp ](https://github.com/HtmlUnit/htmlunit-csp)
* [ https://web.dev/articles/csp#resource-options ](https://web.dev/articles/csp#resource-options)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

#### Source ID: 3

### [ CSP: Wildcard Directive ](https://www.zaproxy.org/docs/alerts/10055/)



##### Medium (High)

### Description

Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks. Including (but not limited to) Cross Site Scripting (XSS), and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.

* URL: https://d2m6kz76y4kuvm.cloudfront.net
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `frame-ancestors 'none'`
  * Other Info: `The following directives either allow wildcard sources (or ancestors), are not defined, or are overly broadly defined:
script-src, style-src, img-src, connect-src, frame-src, font-src, media-src, object-src, manifest-src, worker-src`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/robots.txt
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/robots.txt`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `frame-ancestors 'none'`
  * Other Info: `The following directives either allow wildcard sources (or ancestors), are not defined, or are overly broadly defined:
script-src, style-src, img-src, connect-src, frame-src, font-src, media-src, object-src, manifest-src, worker-src`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `frame-ancestors 'none'`
  * Other Info: `The following directives either allow wildcard sources (or ancestors), are not defined, or are overly broadly defined:
script-src, style-src, img-src, connect-src, frame-src, font-src, media-src, object-src, manifest-src, worker-src`


Instances: 3

### Solution

Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.

### Reference


* [ https://www.w3.org/TR/CSP/ ](https://www.w3.org/TR/CSP/)
* [ https://caniuse.com/#search=content+security+policy ](https://caniuse.com/#search=content+security+policy)
* [ https://content-security-policy.com/ ](https://content-security-policy.com/)
* [ https://github.com/HtmlUnit/htmlunit-csp ](https://github.com/HtmlUnit/htmlunit-csp)
* [ https://web.dev/articles/csp#resource-options ](https://web.dev/articles/csp#resource-options)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

#### Source ID: 3

### [ CSP: script-src unsafe-inline ](https://www.zaproxy.org/docs/alerts/10055/)



##### Medium (High)

### Description

Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks. Including (but not limited to) Cross Site Scripting (XSS), and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.

* URL: https://d2m6kz76y4kuvm.cloudfront.net
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `frame-ancestors 'none'`
  * Other Info: `script-src includes unsafe-inline.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/robots.txt
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/robots.txt`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `frame-ancestors 'none'`
  * Other Info: `script-src includes unsafe-inline.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `frame-ancestors 'none'`
  * Other Info: `script-src includes unsafe-inline.`


Instances: 3

### Solution

Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.

### Reference


* [ https://www.w3.org/TR/CSP/ ](https://www.w3.org/TR/CSP/)
* [ https://caniuse.com/#search=content+security+policy ](https://caniuse.com/#search=content+security+policy)
* [ https://content-security-policy.com/ ](https://content-security-policy.com/)
* [ https://github.com/HtmlUnit/htmlunit-csp ](https://github.com/HtmlUnit/htmlunit-csp)
* [ https://web.dev/articles/csp#resource-options ](https://web.dev/articles/csp#resource-options)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

#### Source ID: 3

### [ CSP: style-src unsafe-inline ](https://www.zaproxy.org/docs/alerts/10055/)



##### Medium (High)

### Description

Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks. Including (but not limited to) Cross Site Scripting (XSS), and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.

* URL: https://d2m6kz76y4kuvm.cloudfront.net
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `frame-ancestors 'none'`
  * Other Info: `style-src includes unsafe-inline.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/robots.txt
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/robots.txt`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `frame-ancestors 'none'`
  * Other Info: `style-src includes unsafe-inline.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `frame-ancestors 'none'`
  * Other Info: `style-src includes unsafe-inline.`


Instances: 3

### Solution

Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.

### Reference


* [ https://www.w3.org/TR/CSP/ ](https://www.w3.org/TR/CSP/)
* [ https://caniuse.com/#search=content+security+policy ](https://caniuse.com/#search=content+security+policy)
* [ https://content-security-policy.com/ ](https://content-security-policy.com/)
* [ https://github.com/HtmlUnit/htmlunit-csp ](https://github.com/HtmlUnit/htmlunit-csp)
* [ https://web.dev/articles/csp#resource-options ](https://web.dev/articles/csp#resource-options)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

#### Source ID: 3

### [ Cross-Origin-Embedder-Policy Header Missing or Invalid ](https://www.zaproxy.org/docs/alerts/90004/)



##### Low (Medium)

### Description

Cross-Origin-Embedder-Policy header is a response header that prevents a document from loading any cross-origin resources that don't explicitly grant the document permission (using CORP or CORS).

* URL: https://d2m6kz76y4kuvm.cloudfront.net
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net`
  * Method: `GET`
  * Parameter: `Cross-Origin-Embedder-Policy`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/robots.txt
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/robots.txt`
  * Method: `GET`
  * Parameter: `Cross-Origin-Embedder-Policy`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml`
  * Method: `GET`
  * Parameter: `Cross-Origin-Embedder-Policy`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``


Instances: 3

### Solution

Ensure that the application/web server sets the Cross-Origin-Embedder-Policy header appropriately, and that it sets the Cross-Origin-Embedder-Policy header to 'require-corp' for documents.
If possible, ensure that the end user uses a standards-compliant and modern web browser that supports the Cross-Origin-Embedder-Policy header (https://caniuse.com/mdn-http_headers_cross-origin-embedder-policy).

### Reference


* [ https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy ](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 14

#### Source ID: 3

### [ Cross-Origin-Opener-Policy Header Missing or Invalid ](https://www.zaproxy.org/docs/alerts/90004/)



##### Low (Medium)

### Description

Cross-Origin-Opener-Policy header is a response header that allows a site to control if others included documents share the same browsing context. Sharing the same browsing context with untrusted documents might lead to data leak.

* URL: https://d2m6kz76y4kuvm.cloudfront.net
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net`
  * Method: `GET`
  * Parameter: `Cross-Origin-Opener-Policy`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/robots.txt
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/robots.txt`
  * Method: `GET`
  * Parameter: `Cross-Origin-Opener-Policy`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml`
  * Method: `GET`
  * Parameter: `Cross-Origin-Opener-Policy`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``


Instances: 3

### Solution

Ensure that the application/web server sets the Cross-Origin-Opener-Policy header appropriately, and that it sets the Cross-Origin-Opener-Policy header to 'same-origin' for documents.
'same-origin-allow-popups' is considered as less secured and should be avoided.
If possible, ensure that the end user uses a standards-compliant and modern web browser that supports the Cross-Origin-Opener-Policy header (https://caniuse.com/mdn-http_headers_cross-origin-opener-policy).

### Reference


* [ https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy ](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 14

#### Source ID: 3

### [ Cross-Origin-Resource-Policy Header Missing or Invalid ](https://www.zaproxy.org/docs/alerts/90004/)



##### Low (Medium)

### Description

Cross-Origin-Resource-Policy header is an opt-in header designed to counter side-channels attacks like Spectre. Resource should be specifically set as shareable amongst different origins.

* URL: https://d2m6kz76y4kuvm.cloudfront.net
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net`
  * Method: `GET`
  * Parameter: `Cross-Origin-Resource-Policy`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/robots.txt
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/robots.txt`
  * Method: `GET`
  * Parameter: `Cross-Origin-Resource-Policy`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml`
  * Method: `GET`
  * Parameter: `Cross-Origin-Resource-Policy`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``


Instances: 3

### Solution

Ensure that the application/web server sets the Cross-Origin-Resource-Policy header appropriately, and that it sets the Cross-Origin-Resource-Policy header to 'same-origin' for all web pages.
'same-site' is considered as less secured and should be avoided.
If resources must be shared, set the header to 'cross-origin'.
If possible, ensure that the end user uses a standards-compliant and modern web browser that supports the Cross-Origin-Resource-Policy header (https://caniuse.com/mdn-http_headers_cross-origin-resource-policy).

### Reference


* [ https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy ](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 14

#### Source ID: 3

### [ Dangerous JS Functions ](https://www.zaproxy.org/docs/alerts/10110/)



##### Low (Low)

### Description

A dangerous JS function seems to be in use that would leave the site vulnerable.

* URL: https://d2m6kz76y4kuvm.cloudfront.net/_expo/static/js/web/AppEntry-206ca015a5a22034bd01e234b53e154e.js
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/_expo/static/js/web/AppEntry-206ca015a5a22034bd01e234b53e154e.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `eval(`
  * Other Info: ``


Instances: 1

### Solution

See the references for security advice on the use of these functions.

### Reference


* [ https://v17.angular.io/guide/security ](https://v17.angular.io/guide/security)


#### CWE Id: [ 749 ](https://cwe.mitre.org/data/definitions/749.html)


#### Source ID: 3

### [ Permissions Policy Header Not Set ](https://www.zaproxy.org/docs/alerts/10063/)



##### Low (Medium)

### Description

Permissions Policy Header is an added layer of security that helps to restrict from unauthorized access or usage of browser/client features by web resources. This policy ensures the user privacy by limiting or specifying the features of the browsers can be used by the web resources. Permissions Policy provides a set of standard HTTP headers that allow website owners to limit which features of browsers can be used by the page such as camera, microphone, location, full screen etc.

* URL: https://d2m6kz76y4kuvm.cloudfront.net
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/index.html
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/index.html`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/robots.txt
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/robots.txt`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``

Instances: Systemic


### Solution

Ensure that your web server, application server, load balancer, etc. is configured to set the Permissions-Policy header.

### Reference


* [ https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy ](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy)
* [ https://developer.chrome.com/blog/feature-policy/ ](https://developer.chrome.com/blog/feature-policy/)
* [ https://scotthelme.co.uk/a-new-security-header-feature-policy/ ](https://scotthelme.co.uk/a-new-security-header-feature-policy/)
* [ https://w3c.github.io/webappsec-feature-policy/ ](https://w3c.github.io/webappsec-feature-policy/)
* [ https://www.smashingmagazine.com/2018/12/feature-policy/ ](https://www.smashingmagazine.com/2018/12/feature-policy/)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

#### Source ID: 3

### [ Server Leaks Version Information via "Server" HTTP Response Header Field ](https://www.zaproxy.org/docs/alerts/10036/)



##### Low (High)

### Description

The web/application server is leaking version information via the "Server" HTTP response header. Access to such information may facilitate attackers identifying other vulnerabilities your web/application server is subject to.

* URL: https://d2m6kz76y4kuvm.cloudfront.net
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `nginx/1.31.6`
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/icons/apple-touch-icon.png
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/icons/apple-touch-icon.png`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `nginx/1.31.6`
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/icons/launch-1284x2778.png
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/icons/launch-1284x2778.png`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `nginx/1.31.6`
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/robots.txt
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/robots.txt`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `nginx/1.31.6`
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `nginx/1.31.6`
  * Other Info: ``

Instances: Systemic


### Solution

Ensure that your web server, application server, load balancer, etc. is configured to suppress the "Server" header or provide generic details.

### Reference


* [ https://httpd.apache.org/docs/current/mod/core.html#servertokens ](https://httpd.apache.org/docs/current/mod/core.html#servertokens)
* [ https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff648552(v=pandp.10) ](https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff648552(v=pandp.10))
* [ https://www.troyhunt.com/shhh-dont-let-your-response-headers/ ](https://www.troyhunt.com/shhh-dont-let-your-response-headers/)


#### CWE Id: [ 497 ](https://cwe.mitre.org/data/definitions/497.html)


#### WASC Id: 13

#### Source ID: 3

### [ Timestamp Disclosure - Unix ](https://www.zaproxy.org/docs/alerts/10096/)



##### Low (Low)

### Description

A timestamp was disclosed by the application/web server. - Unix

* URL: https://d2m6kz76y4kuvm.cloudfront.net/_expo/static/js/web/AppEntry-206ca015a5a22034bd01e234b53e154e.js
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/_expo/static/js/web/AppEntry-206ca015a5a22034bd01e234b53e154e.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `1604231423`
  * Other Info: `1604231423, which evaluates to: 2020-11-01 11:50:23.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/_expo/static/js/web/AppEntry-206ca015a5a22034bd01e234b53e154e.js
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/_expo/static/js/web/AppEntry-206ca015a5a22034bd01e234b53e154e.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `1687547391`
  * Other Info: `1687547391, which evaluates to: 2023-06-23 19:09:51.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/_expo/static/js/web/AppEntry-206ca015a5a22034bd01e234b53e154e.js
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/_expo/static/js/web/AppEntry-206ca015a5a22034bd01e234b53e154e.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `1768516095`
  * Other Info: `1768516095, which evaluates to: 2026-01-15 22:28:15.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/_expo/static/js/web/AppEntry-206ca015a5a22034bd01e234b53e154e.js
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/_expo/static/js/web/AppEntry-206ca015a5a22034bd01e234b53e154e.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `2005441023`
  * Other Info: `2005441023, which evaluates to: 2033-07-20 02:57:03.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/_expo/static/js/web/AppEntry-206ca015a5a22034bd01e234b53e154e.js
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/_expo/static/js/web/AppEntry-206ca015a5a22034bd01e234b53e154e.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `2096890111`
  * Other Info: `2096890111, which evaluates to: 2036-06-12 13:28:31.`

Instances: Systemic


### Solution

Manually confirm that the timestamp data is not sensitive, and that the data cannot be aggregated to disclose exploitable patterns.

### Reference


* [ https://cwe.mitre.org/data/definitions/200.html ](https://cwe.mitre.org/data/definitions/200.html)


#### CWE Id: [ 497 ](https://cwe.mitre.org/data/definitions/497.html)


#### WASC Id: 13

#### Source ID: 3

### [ Content Security Policy (CSP) Report-Only Header Found ](https://www.zaproxy.org/docs/alerts/10038/)



##### Informational (High)

### Description

The response contained a Content-Security-Policy-Report-Only header, this may indicate a work-in-progress implementation, or an oversight in promoting pre-Prod to Prod, etc.

Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.

* URL: https://d2m6kz76y4kuvm.cloudfront.net
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/index.html
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/index.html`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/robots.txt
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/robots.txt`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``

Instances: Systemic


### Solution

Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.

### Reference


* [ https://www.w3.org/TR/CSP2/ ](https://www.w3.org/TR/CSP2/)
* [ https://w3c.github.io/webappsec-csp/ ](https://w3c.github.io/webappsec-csp/)
* [ https://caniuse.com/#feat=contentsecuritypolicy ](https://caniuse.com/#feat=contentsecuritypolicy)
* [ https://content-security-policy.com/ ](https://content-security-policy.com/)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

#### Source ID: 3

### [ Information Disclosure - Suspicious Comments ](https://www.zaproxy.org/docs/alerts/10027/)



##### Informational (Medium)

### Description

The response appears to contain suspicious comments which may help an attacker.

* URL: https://d2m6kz76y4kuvm.cloudfront.net/sw.js
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sw.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `// bug 1394102). Direct ne`
  * Other Info: `The following pattern was used: \bBUG\b and was detected in likely comment: "// bug 1394102). Direct network requests retain server auth and no-store.", see evidence field for the suspicious comment/snippet.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/sw.js
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sw.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `or queue writes for later sync.`
  * Other Info: `The following pattern was used: \bLATER\b and was detected in likely comment: "// Never cache server-backed responses or queue writes for later sync.", see evidence field for the suspicious comment/snippet.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/sw.js
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sw.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `y invite/capability query strings or return J`
  * Other Info: `The following pattern was used: \bQUERY\b and was detected in likely comment: "// Navigation may carry invite/capability query strings or return JSON/media.", see evidence field for the suspicious comment/snippet.`


Instances: 3

### Solution

Remove all comments that return information that may help an attacker and fix any underlying problems they refer to.

### Reference



#### CWE Id: [ 615 ](https://cwe.mitre.org/data/definitions/615.html)


#### WASC Id: 13

#### Source ID: 3

### [ Modern Web Application ](https://www.zaproxy.org/docs/alerts/10109/)



##### Informational (Medium)

### Description

The application appears to be a modern web application. If you need to explore it automatically then the Client Spider may well be more effective than the standard one.

* URL: https://d2m6kz76y4kuvm.cloudfront.net
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<script>
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', function () {
          navigator.serviceWorker.register('/sw.js', { scope: '/' }).catch(function () {
            // The app remains usable online when service workers are unavailable.
          });
        });
      }
    </script>`
  * Other Info: `No links have been found while there are scripts, which is an indication that this is a modern web application.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<script>
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', function () {
          navigator.serviceWorker.register('/sw.js', { scope: '/' }).catch(function () {
            // The app remains usable online when service workers are unavailable.
          });
        });
      }
    </script>`
  * Other Info: `No links have been found while there are scripts, which is an indication that this is a modern web application.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/index.html
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/index.html`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<script>
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', function () {
          navigator.serviceWorker.register('/sw.js', { scope: '/' }).catch(function () {
            // The app remains usable online when service workers are unavailable.
          });
        });
      }
    </script>`
  * Other Info: `No links have been found while there are scripts, which is an indication that this is a modern web application.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/robots.txt
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/robots.txt`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<script>
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', function () {
          navigator.serviceWorker.register('/sw.js', { scope: '/' }).catch(function () {
            // The app remains usable online when service workers are unavailable.
          });
        });
      }
    </script>`
  * Other Info: `No links have been found while there are scripts, which is an indication that this is a modern web application.`
* URL: https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<script>
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', function () {
          navigator.serviceWorker.register('/sw.js', { scope: '/' }).catch(function () {
            // The app remains usable online when service workers are unavailable.
          });
        });
      }
    </script>`
  * Other Info: `No links have been found while there are scripts, which is an indication that this is a modern web application.`


Instances: 5

### Solution

This is an informational alert and so no changes are required.

### Reference




#### Source ID: 3

### [ Non-Storable Content ](https://www.zaproxy.org/docs/alerts/10049/)



##### Informational (Medium)

### Description

The response contents are not storable by caching components such as proxy servers. If the response does not contain sensitive, personal or user-specific information, it may benefit from being stored and cached, to improve performance.

* URL: https://d2m6kz76y4kuvm.cloudfront.net
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `no-store`
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/manifest.json
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/manifest.json`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `no-store`
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/robots.txt
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/robots.txt`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `no-store`
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/sitemap.xml`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `no-store`
  * Other Info: ``


Instances: 4

### Solution

The content may be marked as storable by ensuring that the following conditions are satisfied:
The request method must be understood by the cache and defined as being cacheable ("GET", "HEAD", and "POST" are currently defined as cacheable)
The response status code must be understood by the cache (one of the 1XX, 2XX, 3XX, 4XX, or 5XX response classes are generally understood)
The "no-store" cache directive must not appear in the request or response header fields
For caching by "shared" caches such as "proxy" caches, the "private" response directive must not appear in the response
For caching by "shared" caches such as "proxy" caches, the "Authorization" header field must not appear in the request, unless the response explicitly allows it (using one of the "must-revalidate", "public", or "s-maxage" Cache-Control response directives)
In addition to the conditions above, at least one of the following conditions must also be satisfied by the response:
It must contain an "Expires" header field
It must contain a "max-age" response directive
For "shared" caches such as "proxy" caches, it must contain a "s-maxage" response directive
It must contain a "Cache Control Extension" that allows it to be cached
It must have a status code that is defined as cacheable by default (200, 203, 204, 206, 300, 301, 404, 405, 410, 414, 501).

### Reference


* [ https://datatracker.ietf.org/doc/html/rfc7234 ](https://datatracker.ietf.org/doc/html/rfc7234)
* [ https://datatracker.ietf.org/doc/html/rfc7231 ](https://datatracker.ietf.org/doc/html/rfc7231)
* [ https://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html ](https://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html)


#### CWE Id: [ 524 ](https://cwe.mitre.org/data/definitions/524.html)


#### WASC Id: 13

#### Source ID: 3

### [ Re-examine Cache-control Directives ](https://www.zaproxy.org/docs/alerts/10015/)



##### Informational (Low)

### Description

The cache-control header has not been set properly or is missing, allowing the browser and proxies to cache content. For static assets like css, js, or image files this might be intended, however, the resources should be reviewed to ensure that no sensitive content will be cached.

* URL: https://d2m6kz76y4kuvm.cloudfront.net
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net`
  * Method: `GET`
  * Parameter: `cache-control`
  * Attack: ``
  * Evidence: `no-store`
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/manifest.json
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/manifest.json`
  * Method: `GET`
  * Parameter: `cache-control`
  * Attack: ``
  * Evidence: `no-store`
  * Other Info: ``

Instances: Systemic


### Solution

For secure content, ensure the cache-control HTTP header is set with "no-cache, no-store, must-revalidate". If an asset should be cached consider setting the directives "public, max-age, immutable".

### Reference


* [ https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#web-content-caching ](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#web-content-caching)
* [ https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control ](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)
* [ https://grayduck.mn/2021/09/13/cache-control-recommendations/ ](https://grayduck.mn/2021/09/13/cache-control-recommendations/)


#### CWE Id: [ 525 ](https://cwe.mitre.org/data/definitions/525.html)


#### WASC Id: 13

#### Source ID: 3

### [ Storable and Cacheable Content ](https://www.zaproxy.org/docs/alerts/10049/)



##### Informational (Medium)

### Description

The response contents are storable by caching components such as proxy servers, and may be retrieved directly from the cache, rather than from the origin server by the caching servers, in response to similar requests from other users. If the response data is sensitive, personal or user-specific, this may result in sensitive information being leaked. In some cases, this may even result in a user gaining complete control of the session of another user, depending on the configuration of the caching components in use in their environment. This is primarily an issue where "shared" caching servers such as "proxy" caches are configured on the local network. This configuration is typically found in corporate or educational environments, for instance.

* URL: https://d2m6kz76y4kuvm.cloudfront.net/favicon.ico
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/favicon.ico`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `max-age=31536000`
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/icons/apple-touch-icon.png
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/icons/apple-touch-icon.png`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `max-age=31536000`
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/icons/launch-1179x2556.png
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/icons/launch-1179x2556.png`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `max-age=31536000`
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/icons/launch-1284x2778.png
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/icons/launch-1284x2778.png`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `max-age=31536000`
  * Other Info: ``
* URL: https://d2m6kz76y4kuvm.cloudfront.net/icons/launch-828x1792.png
  * Node Name: `https://d2m6kz76y4kuvm.cloudfront.net/icons/launch-828x1792.png`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `max-age=31536000`
  * Other Info: ``

Instances: Systemic


### Solution

Validate that the response does not contain sensitive, personal or user-specific information. If it does, consider the use of the following HTTP response headers, to limit, or prevent the content being stored and retrieved from the cache by another user:
Cache-Control: no-cache, no-store, must-revalidate, private
Pragma: no-cache
Expires: 0
This configuration directs both HTTP 1.0 and HTTP 1.1 compliant caching servers to not store the response, and to not retrieve the response (without validation) from the cache, in response to a similar request.

### Reference


* [ https://datatracker.ietf.org/doc/html/rfc7234 ](https://datatracker.ietf.org/doc/html/rfc7234)
* [ https://datatracker.ietf.org/doc/html/rfc7231 ](https://datatracker.ietf.org/doc/html/rfc7231)
* [ https://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html ](https://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html)


#### CWE Id: [ 524 ](https://cwe.mitre.org/data/definitions/524.html)


#### WASC Id: 13

#### Source ID: 3


