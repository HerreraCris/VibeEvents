from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Perfil  
from .forms import OnboardingForm
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