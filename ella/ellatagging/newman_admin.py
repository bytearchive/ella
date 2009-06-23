from django.forms import models as modelforms
from django.contrib.contenttypes.models import ContentType
from django.forms.models import save_instance

from ella import newman
from ella.newman.generic import BaseGenericInlineFormSet
from ella.core.models import Publishable

from tagging.models import TaggedItem, Tag

CT_PUBLISHABLE = ContentType.objects.get_for_model(Publishable)

class TaggingInlineFormset(BaseGenericInlineFormSet):
    def save_new(self, form, commit=True):
        kwargs = {
            self.ct_field.get_attname(): CT_PUBLISHABLE.pk,
            self.ct_fk_field.get_attname(): self.instance.pk,
        }
        new_obj = self.model(**kwargs)
        return save_instance(form, new_obj, commit=commit)

    def get_queryset(self):
        if self.instance is None:
            return self.model._default_manager.none()
        return self.model._default_manager.filter(**{
            self.ct_field.name: CT_PUBLISHABLE,
            self.ct_fk_field.name: self.instance.pk,
        })

class TaggingInlineAdmin(newman.GenericTabularInline):
    model = TaggedItem
    max_num = 3
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    suggest_fields = {'tag': ('name',)}
    formset = TaggingInlineFormset

class TagAdmin(newman.NewmanModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

class TaggedItemAdmin(newman.NewmanModelAdmin):
    list_display = ('object', 'tag',)
    list_filter = ('content_type',)
    search_fields = ('tag',)
    suggest_fields = {'tag': ('name',)}

newman.site.register(Tag, TagAdmin)
newman.site.register(TaggedItem, TaggedItemAdmin)
newman.site.append_inline(newman.config.TAGGED_MODELS, TaggingInlineAdmin)
