import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from .forms import ProjectForm
from .models import Project, Skill


def project_list_view(request):
    projects = Project.objects.select_related("owner").prefetch_related(
        "participants", "skills"
    ).order_by("-created_at")
    active_skill = request.GET.get("skill", "")
    if active_skill:
        projects = projects.filter(skills__name=active_skill).distinct()
    paginator = Paginator(projects, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
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
            return redirect(f"/projects/{project.id}/")
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
            return redirect(f"/projects/{project.id}/")
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
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    if project.status != "open":
        return JsonResponse({"status": "error"}, status=400)
    project.status = "closed"
    project.save(update_fields=["status"])
    return JsonResponse({"status": "ok", "project_status": "closed"})


@login_required
@require_POST
def toggle_participate_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner == request.user:
        return JsonResponse({"status": "error"}, status=403)
    if project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
        return JsonResponse({"status": "ok", "participant": False})
    project.participants.add(request.user)
    return JsonResponse({"status": "ok", "participant": True})


@require_GET
def skill_autocomplete_view(request):
    query = request.GET.get("q", "")
    skills = Skill.objects.filter(name__istartswith=query).order_by("name")[:10]
    data = [{"id": skill.id, "name": skill.name} for skill in skills]
    return JsonResponse(data, safe=False)


@login_required
@require_POST
def skill_add_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error"}, status=400)

    created = False
    skill_id = body.get("skill_id")
    name = body.get("name")

    if skill_id:
        skill = get_object_or_404(Skill, pk=skill_id)
    elif name:
        skill, created = Skill.objects.get_or_create(name=name.strip())
    else:
        return JsonResponse({"status": "error"}, status=400)

    added = False
    if not project.skills.filter(pk=skill.pk).exists():
        project.skills.add(skill)
        added = True

    return JsonResponse(
        {"skill_id": skill.id, "created": created, "added": added}
    )


@login_required
@require_POST
def skill_remove_view(request, project_id, skill_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    skill = get_object_or_404(Skill, pk=skill_id)
    if project.skills.filter(pk=skill.pk).exists():
        project.skills.remove(skill)
    return JsonResponse({"status": "ok"})
