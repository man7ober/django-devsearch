from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import Project, Tag, Review
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects

# Create your views here.


def projects(request):
    # concept of searching (projects) in utils.py
    projects, search_query = searchProjects(request)

    # concept of pagination (projects) in utils.py
    projects, custom_range = paginateProjects(request, projects, 6)

    print(custom_range)

    context = {
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range
    }

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, 'Review was successfully submitted!')

        # redirect to same project
        return redirect('project', pk=projectObj.id)

    context = {
        'project': projectObj,
        'form': form
    }

    return render(request, 'projects/single_project.html', context)


@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        new_tags = request.POST.get('newtags').replace(
            ',', ' ').lower().split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            messages.success(request, 'Project was added successfully!')
            return redirect('account')

    context = {
        'form': form,
    }

    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        new_tags = request.POST.get('newtags').replace(
            ',', ' ').lower().split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            messages.success(request, 'Project was updated successfully!')
            return redirect('account')

    context = {
        'form': form,
        'project': project
    }

    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        messages.info(request, 'Project was deleted successfully!')
        return redirect('account')

    context = {
        'object': project
    }

    return render(request, 'delete_template.html', context)
