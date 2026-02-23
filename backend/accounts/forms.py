from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, FamilyGroup

class CustomUserCreationForm(UserCreationForm):
    family_group_name = forms.CharField(max_length=100, required=True, help_text="Nome do seu grupo familiar")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        group_name = self.cleaned_data.get('family_group_name')
        
        # Get or create the family group
        group, created = FamilyGroup.objects.get_or_create(name=group_name)
        user.family_group = group
        
        if commit:
            user.save()
        return user
