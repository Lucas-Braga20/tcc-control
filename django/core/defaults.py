"""
Default values to Tcc Control Project.
"""

from django.utils.translation import gettext_lazy as _


WORK_STAGE_ASSIGNED = 0
WORK_STAGE_PENDING = 1
WORK_STAGE_WAITING_CORRECTION = 2
WORK_STAGE_ADJUSTED = 3
WORK_STAGE_COMPLETED_LATE = 4
WORK_STAGE_COMPLETED = 5
WORK_STAGE_PRESENTED = 6
WORK_STAGE_UNDER_CHANGE = 7
WORK_STAGE_UPDATED = 8

WORK_STAGE_STATUS = (
    (WORK_STAGE_ASSIGNED, _('assigned')),
    (WORK_STAGE_PENDING, _('pending')),
    (WORK_STAGE_WAITING_CORRECTION, _('correction')),
    (WORK_STAGE_ADJUSTED, _('adjusted')),
    (WORK_STAGE_COMPLETED_LATE, _('completed late')),
    (WORK_STAGE_COMPLETED, _('completed')),
    (WORK_STAGE_PRESENTED, _('presented')),
    (WORK_STAGE_UNDER_CHANGE, _('under change')),
    (WORK_STAGE_UPDATED, _('updated')),
)

ACTIVITY_TYPE_TEXT = 'text'
ACTIVITY_TYPE_NUMBER = 'number'
ACTIVITY_TYPE_RICH = 'rich'

ACTIVITY_TYPES = [ACTIVITY_TYPE_TEXT, ACTIVITY_TYPE_NUMBER, ACTIVITY_TYPE_RICH]

completed_status = [
    WORK_STAGE_COMPLETED, WORK_STAGE_COMPLETED_LATE, WORK_STAGE_PRESENTED, WORK_STAGE_UPDATED
]

NOT_DELAYED_STATUS = [
    WORK_STAGE_COMPLETED, WORK_STAGE_PRESENTED, WORK_STAGE_UPDATED,
]

NOT_COMPLETED_STATUS = [
    WORK_STAGE_ASSIGNED, WORK_STAGE_WAITING_CORRECTION, WORK_STAGE_ADJUSTED
]
