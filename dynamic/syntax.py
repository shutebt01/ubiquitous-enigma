"""
Standard dynamic code spec:

args passed in kwargs from json

return: (datatype {mime}, data {which will be jsonified to be returned}, [code {if not present: 200}])
"""

def highlight(*args, **kwargs):
    language = kwargs["lang"]
    data = kwargs["data"]
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    lexer = get_lexer_by_name(language, stripall=True)
    formatter = HtmlFormatter(linenos=True, noclasses=True)
    result = highlight(data, lexer, formatter)
    return "text/html", result