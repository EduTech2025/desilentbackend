from rest_framework import serializers
from .models import Blog, BlogDescription

class BlogDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogDescription
        fields = ['id', 'subheading', 'paragraph', 'images']

class BlogSerializer(serializers.ModelSerializer):
    description = BlogDescriptionSerializer(many=True)

    class Meta:
        model = Blog
        fields = '__all__'

    def create(self, validated_data):
        descriptions_data = validated_data.pop('description')
        blog = Blog.objects.create(**validated_data)
        for desc_data in descriptions_data:
            desc = BlogDescription.objects.create(**desc_data)
            blog.description.add(desc)
        return blog

    def update(self, instance, validated_data):
        descriptions_data = validated_data.pop('description')
        instance.header_image = validated_data.get('header_image', instance.header_image)
        instance.heading = validated_data.get('heading', instance.heading)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.save()

        # Clear and re-add descriptions
        instance.description.clear()
        for desc_data in descriptions_data:
            desc = BlogDescription.objects.create(**desc_data)
            instance.description.add(desc)

        return instance
