"""
Metting serializers.
"""

from rest_framework import serializers

from meetings.models import Meeting, ApprovedMeeting

from users.serializers import UserSerializer
from users.models import User


class ApprovedMeetingSerializer(serializers.ModelSerializer):
    """
    Approved Meeting Serializer.
    """
    user_detail = UserSerializer(many=False, read_only=True, source='user')

    class Meta:
        model = ApprovedMeeting
        fields = ['id', 'approved', 'user', 'user_detail']


class MeetingSerializer(serializers.ModelSerializer):
    """
    Meeting Serializer.
    """
    created_at = serializers.SerializerMethodField(read_only=True)
    participants = ApprovedMeetingSerializer(many=True, read_only=True, source='meeting_approved')
    is_approved = serializers.SerializerMethodField(read_only=True)
    meeting_approved = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(), required=False, many=True)
    meeting_date = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = ['id', 'description', 'work_stage', 'meeting_approved', 'participants', 'created_at', 'meeting_date',
                  'is_approved']

    def get_created_at(self, obj):
        return obj.get_created_at()

    def get_is_approved(self, obj):
        return obj.get_is_approved()

    def get_meeting_date(self, obj):
        return obj.get_meeting_date()

    def create(self, validated_data):
        meeting = super().create(validated_data)

        mentees = meeting.work_stage.final_work.mentees.all()
        supervisor = meeting.work_stage.final_work.supervisor

        for mentee in mentees:
            ApprovedMeeting.objects.create(meeting=meeting, user=mentee, approved=None)

        ApprovedMeeting.objects.create(meeting=meeting, user=supervisor, approved=None)

        return meeting
