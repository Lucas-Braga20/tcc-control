"""
Default values to Tcc Control Project.
"""

from django.utils.translation import gettext_lazy as _


WORK_STEP_ASSIGNED = 0
WORK_STEP_PENDING = 1
WORK_STEP_WAITING_CORRECTION = 2
WORK_STEP_ADJUSTED = 3
WORK_STEP_COMPLETED_LATE = 4
WORK_STEP_COMPLETED = 5
WORK_STEP_PRESENTED = 6

WORK_STEP_STATUS = (
    (WORK_STEP_ASSIGNED, _('assigned')),
    (WORK_STEP_PENDING, _('pending')),
    (WORK_STEP_WAITING_CORRECTION, _('correction')),
    (WORK_STEP_ADJUSTED, _('adjusted')),
    (WORK_STEP_COMPLETED_LATE, _('completed late')),
    (WORK_STEP_COMPLETED, _('completed')),
    (WORK_STEP_PRESENTED, _('presented')),
)

ACTIVITY_TYPE_TEXT = 'text'
ACTIVITY_TYPE_NUMBER = 'number'
ACTIVITY_TYPE_RICH = 'rich'

ACTIVITY_TYPES = [ACTIVITY_TYPE_TEXT, ACTIVITY_TYPE_NUMBER, ACTIVITY_TYPE_RICH]
