from django import forms
from blog.models import Post,Comment

class PostForm(forms.ModelForm):

    class Meta():
        model = Post  #Connect the model for which this form is.
        fields = ('author','title','text')   #Fields which we want to edit or ask from user.

        #This widget is basically to give styling or extra formating to the form field using css.
        # format is key is field
        #value is forms.<<widget actual name>>(attrs={'class':'<<class_name>>'})
        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}) #postcontent is custom class rest are predefined classes from JS and CSS.
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        field = ('author','text')

        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
