"""
Comments app models.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.datetime import get_datetime_tz


class Comment(models.Model):
    """
    Comment model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('created at'))
    work_stage = models.ForeignKey('works.FinalWorkStage', verbose_name=_('work stage'),
                                   on_delete=models.DO_NOTHING, related_name='stage_comment')
    author = models.ForeignKey('users.User', verbose_name=_('author'),
                               on_delete=models.DO_NOTHING, related_name='comment_author')

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def get_created_at(self):
        return get_datetime_tz(self.created_at).strftime("%d/%m/%Y %H:%M")
