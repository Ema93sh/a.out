


from django import template
register = template.Library()
from pygments.lexers import guess_lexer, get_lexer_by_name
import pygments
from pygments.formatters import HtmlFormatter
from django.utils.safestring import mark_safe
from pygments.styles import get_style_by_name

def is_qouted(text):
    return (text[0] in ["'",'"']) and (text[-1] in ["'",'"'])

class Highlight(template.Node):
    def __init__(self, code, syntax, linenos = None):
        self.code = code
        self.syntax = syntax
        self.linenos = linenos
    
    def _get_lexer(self):
        if self.syntax:
            return get_lexer_by_name(self.syntax)
        else:
            return guess_lexer(self.code)  
    
    def render(self, context):
        if not is_qouted(self.code):
            self.code = template.Variable(self.code).resolve(context)
        else: self.code = self.code[1:-1]
        if self.syntax:
            if not is_qouted(self.syntax):
                self.syntax = template.Variable(self.syntax).resolve(context)
            else:
                self.syntax = self.syntax[1:-1]
        
        lexer = self._get_lexer()
        if self.linenos:
            formatter = HtmlFormatter(linenos = self.linenos)
        else: formatter = HtmlFormatter()
        return  mark_safe(pygments.highlight(self.code, lexer, formatter))

def do_highlight(parser, token, linenos = None):
    try: tag_name, code, syntax = token.split_contents()
    except ValueError: 
        tag_name, code = token.split_contents()
        syntax = None
    return Highlight(code, syntax, linenos)

def do_highlight_table(parser, token):
    return do_highlight(parser, token, 'table')

def do_highlight_inline(parser, token):
    return do_highlight(parser, token, 'inline')


class HighlightCss(template.Node):
    def __init__(self, style, linenos = None):
        self.style = style
        self.linenos = linenos
        
    def render(self, context):
        if not is_qouted(self.style):
            self.style = template.Variable(self.style).resolve(context)
        else: self.style = self.style[1:-1]
        if self.linenos:
            formatter = HtmlFormatter(style = get_style_by_name(self.style), linenos = self.linenos)
        else: formatter = HtmlFormatter(style = get_style_by_name(self.style))
        return mark_safe(formatter.get_style_defs('.highlight'))

def do_highlight_css(parser, token, linenos = None):
    try: tag_name, style = token.split_contents()
    except ValueError: 
        style = default
    return HighlightCss(style, linenos)

def do_highlight_css_table(parser, token):
    return do_highlight_css(parser, token, 'table')

def do_highlight_css_inline(parser, token):
    return do_highlight_css(parser, token, 'inline')

        
register.tag('highlight', do_highlight)
register.tag('highlight_table', do_highlight_table)
register.tag('highlight_inline', do_highlight_inline)
register.tag('highlight_css', do_highlight_css)
