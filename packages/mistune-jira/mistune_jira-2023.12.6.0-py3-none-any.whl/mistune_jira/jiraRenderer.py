#!/usr/bin/env python3

import re

from mistune import BaseRenderer, BlockState
from mistune.util import strip_end
from mistune.renderers._list import render_list


class JiraRenderer(BaseRenderer):

    '''
    MistuneJiraRenderer

    Based off the RSTRenderer and some earlier work from 2018 of mine
    '''

    NAME = "jira"

    HEADING_MARKERS = [
        "h1. ",
        "h2. ",
        "h3. ",
        "h4. ",
        "h5. ",
        "h6. "
    ]

    INLINE_IMAGE_PREFIX = "img-"

    def iter_tokens(self, tokens, state):
        prev = None
        for tok in tokens:
            # ignore blank line
            if tok['type'] == 'blank_line':
                continue
            tok['prev'] = prev
            prev = tok
            yield self.render_token(tok, state)

    def __call__(self, tokens, state: BlockState):
        state.env['inline_images'] = []
        out = self.render_tokens(tokens, state)
        return strip_end(out)

    def render_referrences(self, state: BlockState):
        images = state.env['inline_images']
        for index, token in enumerate(images):
            attrs = token['attrs']
            alt = self.render_children(token, state)
            ident = self.INLINE_IMAGE_PREFIX + str(index)
            yield '.. |' + ident + '| image:: ' + attrs['url'] + '\n   :alt: ' + alt

    def render_children(self, token, state: BlockState):
        children = token['children']
        return self.render_tokens(children, state)

    def text(self, token, state):

        text = token["raw"]

        return text

    def emphasis(self, token, state):

        return "_{}_".format(self.render_children(token, state))

    def strong(self, token, state):

        return "*{}*".format(self.render_children(token, state))
    
    def image(self, token, state):

        return "!{}!".format(self.render_children(token, state))

    def linebreak(self, token, state):

        return "\\"

    def softbreak(self, token, state):

        return " "

    def inline_html(self, token, BlockState):
        return token['raw']


    def link(self, token, state):
        # This might need more logic to handle different types of links

        attrs = token['attrs']
        text = self.render_children(token, state)

        return "[{}|{}]".format(text, attrs["url"])

    def codespan(self, token, state):

        return "{{{{{}}}}}".format(token["raw"])

    def paragraph(self, token, state):

        return "{} \n\n".format(self.render_children(token, state))

    def heading(self, token, state):

        level = token["attrs"]["level"]

        return "\nh{}. {}\n".format(level, self.render_children(token, state))

    def thematic_break(self, token, state):

        return "\n----\n"

    def block_text(self, token, state):

        return "{}\n".format(self.render_children(token, state))

    def block_code(self, token, state):
        attrs = token.get('attrs', {})
        info = attrs.get('info')
        try:
            lang = info.split()[0]
        except (IndexError, AttributeError):
            langstr = ""
        else:
            if lang not in ("actionscript", "ada", "applescript", "bash", "c", "c#", "c++", "css", "erlang", "go", "groovy",
                        "haskell", "html", "javascript", "json", "lua", "nyan", "objc", "perl", "php", "python", "r",
                           "ruby", "scala", "sql", "swift", "visualbasic", "xml", "yaml"):
                langstr = ""
            else:
                langstr = ":{}".format(lang)

        codestr = token['raw']

        return '''\n{{code{langstr}}}
{codestr}
{{code}}\n'''.format(langstr=langstr, codestr=codestr)

    def block_quote(self, token, state):

        return '''\n{{quote}}
{quote}
{{quote}}\n'''.format(quote=self.render_children(token, state))

    def block_html(self, token, state):

        return '''\n{{noformat}}
{html}
{{noformat}}'''.format(html=token["raw"])

    def block_error(self, token, state):
        return '''\n{{noformat}}
{error}
{{noformat}}'''.format(error=token["raw"])

    def list(self, token, state):
        return render_list(self, token, state)
