from django import forms

from users.validators import validate_github_url

from .models import Project


class ProjectForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=[("open", "Открыт"), ("closed", "Закрыт")],
        label="Статус",
    )

    class Meta:
        model = Project
        fields = ("name", "description", "github_url", "status")

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url", "")
        validate_github_url(url)
        return url
