# proxy scraping and range requests tests

A proxy that only returns the bits of content you want. (like YQL used to)

(And a service to tell you which bits they might be.)


## install

```
cd proxytest
python3 -m venv venv
. venv/bin/activate
python3 -m pip install -r requirements.txt
```

## run

```
. venv/bin/activate
python server.py
```

then just drag index.html into a browser.


## endpoints

### /c?url=xxx&query=xxx

Get content like a regular proxy but passing a css query to get just the content you want.

http://localhost:8000/c?url=google.com&query=a


### /b?url=xxx&query=xxx

passing a css query and webpage. Returns the byte positions of the data in the file.

might look something like...

```localhost:8000/b?site=somesite.com&query=a[href*='twitter']```

Would return...

```[ [startpos_in_bytes, endpos_in_bytes], ... ]```

Allowing you to then make follow up Ajax range request for the given data.

further goals:

- make a follow up range request for the given bytes.

Making Range Requests can get you parts of a file. See...

https://en.wikipedia.org/wiki/Byte_serving

https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests

github tests don't seem to work due to CORB or CORS issues (only happens when using a range header.)



## TODO

test loading in some content from range requests from a single huge file.

xpath as well as css queries. (old yahoo service that used to do that.) << domonic doesn't do xpath yet. (is it in std lib?)


## Notes

try a curl first to see if range requests work on a given site.

i.e github seems to work on resources when using curl...

curl -r 0-119 https://raw.githubusercontent.com/byteface/domonic/master/docs/_templates/sidebarintro.html

but I think they are missing all the necessary CORS headers for range requests in the browser. As only works for whole file not partials. trying jsonp causes issues with CORB due to mime type not matching.

