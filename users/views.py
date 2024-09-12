from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Profile
from .utils import searchProfiles, paginateProfiles
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm

# Create your views here.


def profiles(request):
    profiles, search_query = searchProfiles(request)

    profiles, custom_range = paginateProfiles(request, profiles, 6)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range
    }

    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    # remove everything where description is empty
    topSkills = profile.skill_set.exclude(description__exact="")

    # add only where description is empty
    otherSkills = profile.skill_set.filter(description="")

    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills
    }

    return render(request, 'users/user_profile.html', context)


def registerUser(request):
    page = 'register'

    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # dont save the user now but after some processing
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'An error occurred during registration!')

    context = {
        'page': page,
        'form': form
    }

    return render(request, 'users/login_register.html', context)


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # create a session
            messages.success(request, "Logged in successfully!")
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username or Password is incorrect!')

    context = {
        'page': page
    }

    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)  # delete a session
    messages.info(request, "Logged out successfully!")
    return redirect('login')


@ login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile  # returns current user (username)

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects
    }

    return render(request, 'users/account.html', context)


@ login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()
            return redirect('account')

    context = {
        'form': form
    }

    return render(request, 'users/profile_form.html', context)


@ login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')

    context = {
        'form': form
    }

    return render(request, 'users/skill_form.html', context)


@ login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')

    context = {
        'form': form
    }

    return render(request, 'users/skill_form.html', context)


@ login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.info(request, 'Skill was deleted successfully!')
        return redirect('account')

    context = {
        'object': skill
    }

    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile

    # here 'messages' comes from models related_name of recipient
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()

    context = {
        'messageRequests': messageRequests,
        'unreadCount': unreadCount
    }

    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    # now the message is read so make it True
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {
        'message': message
    }

    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    sender = None

    # if user is authenticated
    if request.user.is_authenticated == True:
        sender = request.user.profile

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('user-profile', pk=recipient.id)

    context = {
        'recipient': recipient,
        'form': form
    }

    return render(request, 'users/message_form.html', context)
