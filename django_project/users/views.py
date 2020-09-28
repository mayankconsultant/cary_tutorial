from django.shortcuts import render,redirect
# from django.contrib.auth.forms import  UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,ProfileUpdateForm,UserUpdateForm

# Create your views here.

def register(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            # username = form.cleaned_data.get('username')
            messages.success(request,f' Your Account has been Created , You can Login!')
            form.save()
            return redirect('login')
        # else :
        #     messages.error(request, f'Account not Created {form.error_messages.values()}')
        #     return render(request, 'users/register.html', {'form': form})
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f' Your Profile has been Updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form':u_form,
        'p_form' :p_form
    }

    return render(request,'users/profile.html',context)

