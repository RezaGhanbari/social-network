from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm


def user_login(requset):
    if requset.method == 'POST':
        form = LoginForm(requset.POST)

        '''
        Note the difference between authenticate and login:
        authenticate() checks user credentials and returns a user object
        if they are right; login() sets the user in the current session.
        '''
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(requset, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    form = LoginForm()
    return render(requset, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object but avoid saving this
            new_user = user_form.save(commit=False)
            # set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # save the user object
            new_user.save()
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})
