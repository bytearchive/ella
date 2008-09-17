# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _


class Question(models.Model):
    text = models.CharField(_(u'Question'), max_length=100)
    specification = models.TextField(_(u'Specification'))
    nick = models.CharField(_('Nickname'), max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ('-created',)

class Answer(models.Model):
    text = models.TextField(_('Answer text'))
    nick = models.CharField(_('Nickname'), max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ('-created',)
