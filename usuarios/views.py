from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Perfil  
from .forms import OnboardingForm

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loga automaticamente após cadastrar
            
            # Pega o parâmetro 'next' se existir (ex: vindo de sugerir evento)
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('onboarding')
    else:
        form = UserCreationForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def onboarding(request):
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        form = OnboardingForm(request.POST, instance=perfil)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.primeiro_acesso = False
            perfil.save()
            return redirect('mapa_eventos')
    else:
        form = OnboardingForm(instance=perfil)
    
    return render(request, 'usuarios/onboarding.html', {'form': form})