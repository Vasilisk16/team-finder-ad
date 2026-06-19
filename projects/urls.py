from django.urls import path

from . import views

urlpatterns = [
    path("list", views.project_list_view),
    path("list/", views.project_list_view, name="project_list"),
    path("create-project/", views.project_create_view),
    path("skills/", views.skill_autocomplete_view),
    path("<int:project_id>/", views.project_detail_view, name="project_detail"),
    path("<int:project_id>/edit", views.project_edit_view),
    path("<int:project_id>/complete/", views.project_complete_view),
    path("<int:project_id>/toggle-participate/", views.toggle_participate_view),
    path("<int:project_id>/skills/add/", views.skill_add_view),
    path(
        "<int:project_id>/skills/<int:skill_id>/remove/",
        views.skill_remove_view,
    ),
]
