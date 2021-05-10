from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Produto
from django.contrib.auth import logout

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def set_produto(request):
    cidade = request.POST.get('cidade')
    email = request.POST.get('email')
    celular = request.POST.get('celular')
    descricao = request.POST.get('descrição')
    file = request.FILES.get('file')
    user = request.user
    produtos_id = request.POST.get('produtos_id')
    if produtos_id:
        produto = Produto.objects.get(id=produtos_id)
        if user == produto.user:
            produto.email = email
            produto.celular = celular
            produto.cidade = cidade
            produto.descricao = descricao
            if file:
                produto.photo = file
            produto.save()
    else:
        produto = Produto.objects.create(email=email, celular=celular, cidade=cidade, description=descricao, user=user, photo=file)
    url = '/produto/detail/{}/'.format(produto.id)
    return redirect(url)

@login_required(login_url='/login/')
def registro_produto(request):
    produtos_id = request.GET.get('id')
    if produtos_id:
        produto = Produto.objects.get(id=produtos_id)
        if produto.user == request.user:
            return render(request, 'registro.html', {'produto':produto})
    return render(request, 'registro.html')

@login_required(login_url='/login/')
def produto_detail(request, id):
    produto = Produto.objects.get(ativo=True, id=id)
    return render(request, 'produto.html', {'produto':produto})

@login_required(login_url='/login/')
def lista_all_produtos(request):
    produto = Produto.objects.filter(ativo=True)
    return render(request, 'lista.html', {'produto':produto})

@login_required(login_url='/login/')
def lista_usuario_produtos(request):
    produto = Produto.objects.filter(ativo=True, user=request.user)
    return render(request, 'lista.html', {'produto':produto})

@login_required(login_url='/login/')
def delete_produto(request, id):
    produto = Produto.objects.get(id=id)
    if produto.user == request.user:
        produto.delete()
    return redirect('/')

def loginuser(request):
    return render(request,'login.html')

@csrf_protect
def login_submit(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/produto/all')
        else:
            messages.error(request, 'Usuário/Senha inválidos. Favor tentar novamente.')
    return redirect('/login/')

