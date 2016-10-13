from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from pygments.styles import get_all_styles

LEXER = [_ for _ in get_all_lexers() if _[1]]
LANGUAGE_CHOICES = sorted([(_[1][0], _[0]) for _ in LEXER])
STYLE_CHOICES = sorted((_, _) for _ in get_all_styles())


class Snippet(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets')
    highlighted = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code,lexer=lexer,formatter=formatter)
        super(Snippet,self).save(*args, **kwargs)