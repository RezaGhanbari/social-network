from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm


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