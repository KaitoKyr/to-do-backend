from rest_framework import serializers
from .models import Tasks, Tags


"""
class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'



# serializers.py


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


"""



# Serializer für Tags (Labels wie "work", "personal")
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'name']

"""
# Serializer für Tasks
class TasksSerializer(serializers.ModelSerializer):
    # Damit du die Tags nicht nur als IDs siehst, sondern auch Namen
    tags = TagSerializer(many=True, read_only=True)

    # Damit du Tags per ID setzen kannst (POST/PATCH)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True,
        write_only=True,
        source='tags'
    )

    class Meta:
        model = Tasks
        fields = ['id', 'content', 'completed', 'tags', 'tag_ids']

"""


class TasksSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    class Meta:
        model = Tasks
        fields = ['id', 'content', 'completed', 'tags']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'content': instance.content,
            'completed': instance.completed,
            'tags': [tag.name for tag in instance.tags.all()]
        }

    # CREATE
    def create(self, validated_data):
        tag_names = validated_data.pop('tags', [])
        task = Tasks.objects.create(**validated_data)

        # Tags erstellen oder holen
        for name in tag_names:
            tag, created = Tags.objects.get_or_create(name=name)
            task.tags.add(tag)

        return task

    # UPDATE
    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tags', None)

        # normale Felder updaten
        instance.content = validated_data.get('content', instance.content)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()

        # Tags ersetzen (wenn mitgegeben)
        if tag_names is not None:
            instance.tags.clear()

            for name in tag_names:
                tag, created = Tags.objects.get_or_create(name=name)
                instance.tags.add(tag)

        return instance