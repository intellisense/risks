from django.db import transaction

from rest_framework import serializers

from .models import RiskType, RiskField


class RiskFieldSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='get_field_type_name')
    id = serializers.ModelField(model_field=RiskField()._meta.get_field('id'))

    class Meta:
        model = RiskField
        fields = ('id', 'label', 'field_type', 'required', 'help_text', 'options', 'name')


class RiskTypeSerializer(serializers.ModelSerializer):
    DATE_TIME_FORMAT = '%d %b %Y %I:%M:%S %p'
    fields = RiskFieldSerializer(many=True)
    fields_count = serializers.ReadOnlyField(source='get_fields_count')
    created = serializers.DateTimeField(format=DATE_TIME_FORMAT, required=False, read_only=True)
    modified = serializers.DateTimeField(format=DATE_TIME_FORMAT, required=False, read_only=True)

    class Meta:
        model = RiskType
        fields = ('id', 'name', 'fields', 'fields_count', 'created', 'modified')
        read_only_fields = ('created', 'modified')

    def validate(self, data):
        """
        Check that there is at-least one risk field for risk type.
        """
        fields = data.get('fields', [])
        if not fields:
            raise serializers.ValidationError('Specify at-least one Risk Field for Risk Type.')
        return data

    def create(self, validated_data):
        with transaction.atomic():
            fields_data = validated_data.pop('fields')
            risk_type = RiskType.objects.create(**validated_data)
            for field_data in fields_data:
                if field_data['field_type'] != RiskField.TYPE_SELECT:
                    field_data.pop('options', None)
                field_data.pop('id', None)
                RiskField.objects.create(risk_type=risk_type, **field_data)
        return risk_type

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            instance.save()

            # update existing risk fields
            existing_fields = validated_data.get('fields', [])
            new_fields_ids = []
            for f in existing_fields:
                field_data = f.copy()
                is_new = False
                if field_data['field_type'] != RiskField.TYPE_SELECT:
                    field_data.pop('options', None)
                field_id = field_data.pop('id', None)
                if field_id:
                    field = instance.fields.get(id=field_id)
                else:
                    field = RiskField(
                        risk_type=instance,
                        field_type=field_data['field_type'],
                    )
                    is_new = True
                field.label = field_data['label']
                field.required = field_data.get('required', False)
                field.help_text = field_data.get('help_text', '')
                if field_data['field_type'] == RiskField.TYPE_SELECT:
                    field.options = field_data.get('options', '')
                field.save()
                if is_new:
                    new_fields_ids.append(field.id)

            # check stale risk fields
            new_fields_ids = set([int(f['id']) for f in existing_fields if f.get('id')] + new_fields_ids)
            curr_fields_ids = set(instance.fields.values_list('id', flat=True))
            to_delete = [i for i in curr_fields_ids if i not in new_fields_ids]
            if to_delete:
                instance.fields.filter(id__in=to_delete).delete()
                # sanity check, make sure we have at-least one field associated
                assert instance.fields.count() > 0

        return instance
