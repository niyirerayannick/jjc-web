from django import forms

from apps.core.models import ContentPage, MinistryArea, SiteStatistic, TimelineMilestone


class DashboardModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                'class',
                'w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-blue-500',
            )


class ContentPageForm(DashboardModelForm):
    class Meta:
        model = ContentPage
        fields = [
            'slug', 'title', 'eyebrow', 'summary', 'featured_image',
            'featured_image_alt', 'body', 'closing_statement', 'is_published',
        ]


class SiteStatisticForm(DashboardModelForm):
    class Meta:
        model = SiteStatistic
        fields = ['key', 'value', 'label', 'detail', 'order', 'show_on_homepage', 'is_active']


class TimelineMilestoneForm(DashboardModelForm):
    class Meta:
        model = TimelineMilestone
        fields = ['year', 'title', 'description', 'order', 'is_active']


class MinistryAreaForm(DashboardModelForm):
    class Meta:
        model = MinistryArea
        fields = ['slug', 'title', 'summary', 'body', 'link_url', 'order', 'show_on_homepage', 'is_active']
