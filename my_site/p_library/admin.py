from django.contrib import admin
from .models import Redaction, Book, Authors, Inspiration, Reader


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    @staticmethod
    def author_full_name(obj):
        return obj.author.full_name

    list_display = (
        'title',
        'author_full_name',
    )
    fields = (
        'ISBN',
        'title',
        'description',
        'year_release',
        'author',
        'price',
        'copy_count',
        'redaction',
        'reader',
        'image'
    )


@admin.register(Authors)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Inspiration)
class InspirationAdmin(admin.ModelAdmin):
    pass


@admin.register(Redaction)
class RedactionAdmin(admin.ModelAdmin):
    pass


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    pass
