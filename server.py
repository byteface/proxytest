import os
import sys
import re
import json

import requests
import html5lib

from sanic import Sanic, response
from sanic_cors import CORS, cross_origin

from domonic.html import *
from domonic.ext.html5lib_ import getTreeBuilder
from domonic.javascript import Global


app = Sanic(__name__)
CORS(app)

# import glob
# templates = glob.glob('templates/*.pyml') 

def create_homepage():
    page = html(
        head(
            script(_src='https://code.jquery.com/jquery-3.5.1.min.js'),
            script("""
               
            const get_content = () => {
                let url = $('#url').val();
                // encode for sending to server
                url = encodeURIComponent(url);
                // TODO - may need to encode the css query also. dont they have illegal transport characters?
                let query = $('#query').val();

                window.console.log(url);
                window.console.log(query);

                $.ajax({
                    url: 'http://localhost:8000/c?url=' + url + '&query=' + query + "",
                    success: function(data) {
                        window.console.log('HI THERE!')
                        window.console.log(data);
                        $('#response').html(data);
                        $('#response_raw').html(data);
                    }
                });
            }

            const get_bytes = () => {
                let url = $('#url').val();
                let query = $('#query').val();
                $.ajax({
                    url: 'http://localhost:8000/b?url=' + url + '&query=' + query + "",
                    success: function(data) {
                        $('#response').html(data);
                        $('#response_raw').html(data);
                    }
                });
            }

            // this would only work on servers that support CORS
            const use_bytes_to_get_content = () => {
                let url = $('#url').val();
                let bytes = $('#response_raw').html();

                //window.console.log(url, bytes);
                bytes = JSON.parse(bytes);
                //window.console.log(url, bytes);

                // get the value of the first object out of the bytes
                let value = bytes[Object.keys(bytes)[0]];

                window.console.log(value);
                
                // format bytes to look like 0-50 with / seperator
                bytestr = ""
                for(var i = 0; i < value.length; i++) {
                    bytestr += value[i][0] + "-" + value[i][1] + "/";
                }
                bytestr = bytestr.slice(0, -1)

                // bytes needs to be expressed as a range i.e. bytes 0-50/1270
                // so can this be an array of ranges?

                window.console.log(bytestr);

                //if 'https' not in url:
                //   url = 'https://' + url

                // as javascript
                if(url.slice(0, 5) != 'https') {
                    url = 'https://' + url
                }

                /*
                // make a range request to get a slice of the file
                $.ajax({
                    url: url,
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include',
                    cache: false,
                    async: true,
                    crossDomain:true,
                    //contentType: 'text/plain',
                    //contentType: 'text/plain; charset=utf-8',
                    //dataType: 'jsonp',
			        //dataType : 'json',
			        //contentType:"multipart/byteranges",
                    headers: {
                        //"Access-Control-Allow-Origin": "*",
                        //"accept": "application/json",
                        "Range": "bytes=" + bytestr
                    },
                    success: function(data) {
                        window.console.log(data);
                        $('#response').html(data);
                    },
                    error: function(data) {
                        window.console.log(data);
                        $('#response').html(data);
                    }
                });
                */
                
                
                fetch(url, {
                        method : "GET",
                        //headers: {
                        //    "Range": "bytes=0-119" //"bytes=" + bytestr
                        //},
                        "mode": "cors",
                        "credentials": "include",
                        "cache": "no-cache",
                        "dataType": "text",
                        //"mode": "no-cors", // corb gets dicked around with per tag when no-cors is used
                        "credentials": "omit",
                        "body": null,
                    })
                    .then((response) => {
                        if (!response.ok) {
                            throw new Error(response.error)
                        }
                        window.console.log("HI HIHIHI");
                        window.console.log(response);
                        //return response;//.json();
                        return response.text();
                    })
                    .then(data => {
                        window.console.log("does this fucking run or what?");
                        window.console.log(data);
                        $('#response').html(data);
                    })
                    .catch(function(error) {
                        //alert('fail')
                        window.console.log(error);
                    });
                    

            }

            """),
        ),
        body(
            article(
                h1('Test page for proxy scraping and range requests'),
                p('Test the api to see the responses.'),
                # p('This is an excercise in returning partial pieces data from files.'),
                p('Enter a url and a query to return the response.'),
                p('The query is a css query to run on that webpage. i.e. try using a or img'),
                input(_id="url", _type='text', _name='url', _placeholder='google.com'),
                input(_id="query", _type='text', _name='query', _placeholder='Enter css selector here'),
                hr(),
                p('This button hits the api and just returns the nodes specified by the css query.'),
                button('Get Content', _type='button', _onclick='get_content()'),
                hr(),
                p('This button hits the api and just returns the character byte positions for which you can then make a range request.'),
                p('This can be done with or w/o tags.'),
                button('Get Bytes', _type='button', _onclick='get_bytes()'),
                hr(),
                comment(div(
                    p('This button uses the byte positions from the get bytes call to retrieve content with range requests.'),
                    p('this would only work on servers that support CORS and range requests.'),
                    button('Use bytes to get content.', _type='button', _onclick='use_bytes_to_get_content()'),
                    br(),
                )),
                h2('Response'),
                div(_id='response'),
                h2('Response raw'),
                xmp(_id='response_raw'),
            )
        )
    )
    with open('index.html', 'w') as f:
        f.write(f"{page}")

# dont need to do this yet. for now parse a live site
# def create_datapage():
#     page = html(
#         head(

#         ),
#         body(

#             div(
#                 h1('Data Page'),
#                 p('This is the data page.'),
#             ),
#             div(_id='data').append(
#                 # atoms
#                 div(_id="hydrogen").append(
#                     h2('Hydrogen'),
#                     p('Hydrogen is a chemical element with symbol H and atomic number 1. With a standard atomic weight of 1.008, hydrogen is the lightest element on the periodic table. More than half of all the elements in the periodic table are made up of hydrogen, but the rest have a heavier atom weight.'),
#                     p('Hydrogen is a colorless, odorless, tasteless, non-toxic, inert, monatomic gas that heads the noble gas group on the periodic table.'),
#                     p('Hydrogen is the most abundant chemical substance in the Universe. Hydrogen is a colorless, odorless, tasteless, non
#                 ),
#                 div(_id="helium").append(
#                     h2('Helium'),
#                     p('Helium is a chemical element with symbol He and atomic number 2. It is a colorless, odorless, tasteless,')
#                 ),
#                 div(_id="lithium").append(
#                     h2('Lithium'),
#                     p('Lithium is a chemical element with symbol Li and atomic number 3. It is a soft, silvery-white alkali metal.')
#                 ),
#                 div(_id="beryllium").append(
#                     h2('Beryllium'),
#                     p('Beryllium is a chemical element with symbol Be and atomic number 4. It is a relatively rare element in the universe, usually occurring as a product of the spallation of larger atomic nuclei that have collided with cosmic rays.')
#                 ),
#             )

#         )
#     )
#     with open('db.html', 'w') as f:
#         f.write(f"{page}")

@app.route("/b")
async def get_bytes(request):
    url = request.args.get("url") # url = Global.decodeURIComponent(u)
    q = request.args.get("query")

    # q = request.args("query")
    # m = request.args("method")
    # p = request.args("params")
    # t = request.args("tags") # optional to have tags or not. this changes the byte position returned

    # print(url, q)
    # return 'hi'
    if 'https' not in url:
        url = 'https://' + url

    r = requests.get(url)
    parser = html5lib.HTMLParser(tree=getTreeBuilder())
    raw = parser.parse(r.content)
    src = parser.parse(r.content.decode("utf-8"))

    elements = src.querySelectorAll(q)

    # create a dict with the byte positions of the elements retrieved.
    # start_byte and end_byte are to be the byte positions of content within html tags

    # for start_byte, the first byte we want is the one after the '>' symbol of the opening tag. so the first byte of actual content.
    # for end_byte, the first byte we want is the one before the '<' symbol of the closing tag. so the last byte of actual content.
    
    # i.e {q:[[start_byte, end_byte],[start_byte, end_byte]]}
    
    # the byte positions should be relative to their positions in the source html.

    # use the elemets returned from the query to know what blobs of content we want to find byte positions for.

    results = {q:[]}
    for e in elements:
        # results[q].append([e.start_byte, e.end_byte])
        # TODO find the start bytes in the source html using regex
        # TODO find the end bytes in the source html using regex

        # this is the with tags version .#TODO - so are these byte positions or char positions?
        elstr = str(e)
        start_byte = str(raw).find(elstr)
        end_byte = str(raw).find(elstr) + len(elstr)
        results[q].append([start_byte, end_byte])

    return response.json(json.dumps(results))


@app.route("/c", methods=['GET', 'OPTIONS', 'POST'])
async def get_content(request):
    url = request.args.get("url")
    q = request.args.get("query")

    # print(url, q)
    # return 'hi'
    if 'https' not in url:
        url = 'https://' + url

    r = requests.get(url)

    parser = html5lib.HTMLParser(tree=getTreeBuilder())
    page = parser.parse(r.content.decode("utf-8"))

    result = page.querySelectorAll(q)
    
    print("result")
    print(result)

    return response.html(f"{''.join([str(r) for r in result])}")


# ideas...
# utilise tiny url?
# create byte maps. of meta data or tag nodes
# TODO - make an infinite scroller making range requests to one large file


if __name__ == '__main__':
    create_homepage()
    app.run(host='0.0.0.0', port=8000, debug=True)
