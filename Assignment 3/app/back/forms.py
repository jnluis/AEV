from django import forms
from .models import Images,Profile,Likepost, CommentPost

class ImageForm(forms.ModelForm):
    class Meta:
        
        model = Images
        fields = ('file',)

class liker(forms.ModelForm):
    class Meta:
        
        model = Likepost
        fields = ('postid','username',)

class commentBox(forms.ModelForm):
    class Meta:
        
        model = CommentPost
        fields = ('postid','username','comment',)