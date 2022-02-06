from domonic.html import *
from domonic.CDN import CDN_CSS

questions_page = html(
    head(
        title("Questions"),
        link(_rel="stylesheet", _href=CDN_CSS.MARX),
        script(_src='https://code.jquery.com/jquery-3.5.1.min.js'),
        script("""

        const get_content = (url, query) => {
            let u = encodeURIComponent(url);
            let q = encodeURIComponent(query);
            window.console.log(url, q);
            $.ajax({
                url: 'http://localhost:8000/c?url=' + u + '&query=' + q + "",
                success: function(data) {
                    $('#response').html(data);
                }
            });
        }

        // on hash change, get the a tag with the matching hash
        $(window).on('hashchange', function() {
            let hash = window.location.hash;
            let $a = $('a[href="' + hash + '"]');
            let url = $a.data('url');
            let query = $a.data('selector');
            get_content(url, query);
        });

        """)
    ),
    body(
        h1("Questions answered by css"),
        ul(
            li(
                a(
                    "What's the headline on the bbc news website?",
                    _href="#q1",
                    **{"_data-url": "bbc.co.uk/news"},
                    **{"_data-selector": "h3"}
                )
            ),
            li(
                a(
                    "Show me googles logo?",
                    _href="#q2",
                    **{"_data-url": "google.com"},
                    **{"_data-selector": "img[alt='Google']"} # bug?. required quotes to work
                )
            ),
            li(
                a(
                    "What's the cheapest wine at Sainsburys? (wait for it)",
                    _href="#q3",
                    **{"_data-url": "tinyurl.com/uut2jdey"},
                    **{"_data-selector": "h3"}
                )
            ),
            li(
                a(
                    "Show me a random picture",
                    _href="#q4",
                    **{"_data-url": "https://en.wikipedia.org/wiki/Special:Random"},
                    **{"_data-selector": "img"}
                )
            ),
        )
    ),
    h4("Response"),
    div(
        _id="response",
        _style="border: 1px solid black; padding: 10px; margin: 10px;"
    )
)