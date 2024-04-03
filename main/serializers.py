from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

class RequestTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request_Table
        fields = ['user','requested_for','request_type','request_to_date']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
class ForgotPasswordSerializer(serializers.Serializer):
    # phone_number = serializers.CharField(max_length=15)
    email = serializers.EmailField()

class PasswordUpdateSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    otp = serializers.CharField(max_length=6, min_length=6)
    new_password = serializers.CharField(write_only=True)




class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']

class PostsSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id','name','photo','content','category', 'likes', 'comments_count', 'comments']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        comments = Comment.objects.filter(post_id=instance.id)
        data['comments'] = [comment.comment for comment in comments]
        return data