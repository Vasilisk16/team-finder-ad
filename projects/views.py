import json
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from team_finder.pagination import get_page

from .forms import ProjectForm
from .models import (
    STATUS_CLOSED,
    STATUS_OPEN,
    Project,
    Skill,
)

SKILL_AUTOCOMPLETE_LIMIT = 10


def project_list_view(request):
    projects = (
        Project.objects.select_related("owner")
        .prefetch_related("participants", "skills")
        .order_by("-created_at")
    )
    active_skill = request.GET.get("skill", "")
    if active_skill:
        projects = projects.filter(skills__name=active_skill).distinct()
    page_obj = get_page(request, projects)
    all_skills = Skill.objects.order_by("name").values_list("name", flat=True)
    return render(
        request,
        "projects/project_list.html",
        {
            "projects": page_obj.object_list,
            "page_obj": page_obj,
            "all_skills": all_skills,
            "active_skill": active_skill,
        },
    )


@login_required
def project_create_view(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect("project_detail", project_id=project.id)
    else:
        form = ProjectForm()
    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": False},
    )


def project_detail_view(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related(
            "participants", "skills"
        ),
        pk=project_id,
    )
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def project_edit_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("project_detail", project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": True},
    )


@login_required
@require_POST
def project_complete_view(request, project_id):
    project = Project.objects.filter(pk=project_id, owner=request.user).first()
    if project is None:
        return JsonResponse(
            {"status": "error", "message": "Проект не найден"},
            status=HTTPStatus.NOT_FOUND,
        )
    if project.status != STATUS_OPEN:
        return JsonResponse({"status": "error"}, status=HTTPStatus.BAD_REQUEST)
    project.status = STATUS_CLOSED
    project.save(update_fields=["status"])
    return JsonResponse({"status": "ok", "project_status": STATUS_CLOSED})


@login_required
@require_POST
def toggle_participate_view(request, project_id):
    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return JsonResponse(
            {"status": "error", "message": "Проект не найден"},
            status=HTTPStatus.NOT_FOUND,
        )
    if project.owner == request.user:
        return JsonResponse({"status": "error"}, status=HTTPStatus.FORBIDDEN)
    if project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
        return JsonResponse({"status": "ok", "participant": False})
    project.participants.add(request.user)
    return JsonResponse({"status": "ok", "participant": True})


@require_GET
def skill_autocomplete_view(request):
    query = request.GET.get("q", "")
    skills = Skill.objects.filter(name__istartswith=query).order_by("name")[
        :SKILL_AUTOCOMPLETE_LIMIT
    ]
    data = [{"id": skill.id, "name": skill.name} for skill in skills]
    return JsonResponse(data, safe=False)


@login_required
@require_POST
def skill_add_view(request, project_id):
    project = Project.objects.filter(pk=project_id, owner=request.user).first()
    if project is None:
        return JsonResponse(
            {"status": "error", "message": "Проект не найден"},
            status=HTTPStatus.NOT_FOUND,
        )
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error"}, status=HTTPStatus.BAD_REQUEST)

    created = False
    skill_id = body.get("skill_id")
    name = body.get("name")

    if skill_id:
        skill = Skill.objects.filter(pk=skill_id).first()
        if skill is None:
            return JsonResponse(
                {"status": "error", "message": "Навык не найден"},
                status=HTTPStatus.NOT_FOUND,
            )
    elif name:
        skill, created = Skill.objects.get_or_create(name=name.strip())
    else:
        return JsonResponse({"status": "error"}, status=HTTPStatus.BAD_REQUEST)

    added = False
    if not project.skills.filter(pk=skill.pk).exists():
        project.skills.add(skill)
        added = True

    return JsonResponse({"skill_id": skill.id, "created": created, "added": added})


@login_required
@require_POST
def skill_remove_view(request, project_id, skill_id):
    project = Project.objects.filter(pk=project_id, owner=request.user).first()
    if project is None:
        return JsonResponse(
            {"status": "error", "message": "Проект не найден"},
            status=HTTPStatus.NOT_FOUND,
        )
    skill = Skill.objects.filter(pk=skill_id).first()
    if skill is None:
        return JsonResponse(
            {"status": "error", "message": "Навык не найден"},
            status=HTTPStatus.NOT_FOUND,
        )
    if project.skills.filter(pk=skill.pk).exists():
        project.skills.remove(skill)
    return JsonResponse({"status": "ok"})
