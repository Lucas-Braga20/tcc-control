"""
Comments app models.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    """
    Comment model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(verbose_name=_('description'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('created at'))
    work_step = models.ForeignKey('works.WorkStep', verbose_name=_('work step'),
                                  on_delete=models.DO_NOTHING, related_name='step_comment')
    author = models.ForeignKey('users.User', verbose_name=_('author'),
                               on_delete=models.DO_NOTHING, related_name='step_author')

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
