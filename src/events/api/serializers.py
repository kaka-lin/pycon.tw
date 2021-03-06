from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from events.models import ProposedTutorialEvent, SponsoredEvent
from proposals.models import TalkProposal


class PrimarySpeakerSerializer(serializers.Serializer):
    thumbnail_url = serializers.CharField()
    name = serializers.CharField()
    github_profile_url = serializers.CharField()
    twitter_profile_url = serializers.CharField()
    facebook_profile_url = serializers.CharField()


class TalkDetailSerializer(serializers.ModelSerializer):
    speakers = serializers.SerializerMethodField()

    def get_speakers(self, obj):
        return [
            ReturnDict(PrimarySpeakerSerializer(
                data={'thumbnail_url': i.user.get_thumbnail_url(),
                      'name': i.user.speaker_name,
                      'github_profile_url': i.user.github_profile_url,
                      'twitter_profile_url': i.user.twitter_profile_url,
                      'facebook_profile_url': i.user.facebook_profile_url}).get_initial(),
                serializer=PrimarySpeakerSerializer) for i in obj.speakers]

    class Meta:
        model = TalkProposal
        fields = [
            "title",
            "category",
            "language",
            "python_level",
            "recording_policy",
            "abstract",
            "detailed_description",
            "slide_link",
            "slido_embed_link",
            # "sponsored"
            "speakers"

        ]


class TalkListSerializer(serializers.ModelSerializer):
    speakers = serializers.SerializerMethodField()

    def get_speakers(self, obj):
        return [
            ReturnDict(PrimarySpeakerSerializer(
                data={'thumbnail_url': i.user.get_thumbnail_url(),
                      'name': i.user.speaker_name,
                      'github_profile_url': i.user.github_profile_url,
                      'twitter_profile_url': i.user.twitter_profile_url,
                      'facebook_profile_url': i.user.facebook_profile_url}).get_initial(),
                serializer=PrimarySpeakerSerializer) for i in obj.speakers]

    class Meta:
        model = TalkProposal
        fields = [
            "id",
            "title",
            "category",
            "labels",
            "speakers",
        ]


class SponsoredEventSerializer(serializers.ModelSerializer):

    host_name = serializers.CharField(source="host.speaker_name", required=False)

    class Meta:
        model = SponsoredEvent
        fields = [
            "slug",
            "title",
            "host_name"
        ]


class TutorialDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='proposal.title')
    date = serializers.DateTimeField(format='%Y-%m-%d', source='begin_time.value')
    begin_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', source='begin_time.value')
    end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', source='end_time.value')
    category = serializers.CharField(source='proposal.category')
    language = serializers.CharField(source='proposal.language')
    python_level = serializers.CharField(source='proposal.python_level')
    abstract = serializers.CharField(source='proposal.abstract')
    detailed_description = serializers.CharField(source='proposal.detailed_description')
    slide_link = serializers.CharField(source='proposal.slide_link')
    slido_embed_link = serializers.CharField(source='proposal.slido_embed_link')
    speakers = serializers.SerializerMethodField()

    def get_speakers(self, obj):
        return [
            ReturnDict(PrimarySpeakerSerializer(
                data={'thumbnail_url': i.user.get_thumbnail_url(),
                      'name': i.user.speaker_name,
                      'github_profile_url': i.user.github_profile_url,
                      'twitter_profile_url': i.user.twitter_profile_url,
                      'facebook_profile_url': i.user.facebook_profile_url}).get_initial(),
                serializer=PrimarySpeakerSerializer) for i in obj.proposal.speakers]

    class Meta:
        model = ProposedTutorialEvent
        fields = [
            "title",
            "location",
            "date",
            "begin_time",
            "end_time",
            "category",
            "language",
            "python_level",
            "abstract",
            "detailed_description",
            "slide_link",
            "slido_embed_link",
            "speakers"
        ]
