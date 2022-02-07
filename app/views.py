from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages


def index(request):
    return render (request, 'index.html')

def register (request):
    return render (request, 'register.html')

def home (request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'category': Category.objects.all(),
        'protocols': Protocol.objects.all(),
    }
    return render (request, 'home.html', context)

def new_reg (request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/register')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            facility = request.POST['facility'],
            password = pw_hash
        )
        request.session.flush()
        this_user=User.objects.filter(email = request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect ('/build')

def login (request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/')
    else:
        request.session.flush()
        this_user = User.objects.filter(email = request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect ('/build')

def build (request):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'category': Category.objects.all(),
            'protocols': Protocol.objects.all(),
        }
        return render (request, 'build.html', context)

def new_category(request):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        Category.objects.create(
            name = request.POST['new_category']
        )
        return redirect ('/build')

def select_category(request):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        selected = Category.objects.get(id=request.POST['category'])
        category_name = selected.name
        return redirect (f'/select_category/{category_name}')

def new_protocol(request,category_name):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        selected_category = category_name
        this_category = Category.objects.get(name=selected_category)
        request.session['this_category'] = this_category.name
        request.session['category_id'] = this_category.id
        context = {
            'this_category': this_category.name,
            'category': Category.objects.all(),
            'protocols': Protocol.objects.all(),
            'sequences': Sequence.objects.all(),
            'current_category': request.session['this_category'],
            'category_id': request.session['category_id']
        }
        return render (request, 'sequences.html', context)

def create_protocol (request):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        Protocol.objects.create(
            name = request.POST['name'],
            category = Category.objects.get(id=request.session['category_id'])
        )
        new_protocol = Protocol.objects.last()
        new_protocol_id = new_protocol.id
        return redirect (f'/add_sequences/{new_protocol_id}')


def add_sequences (request,id):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        protocol_id=id
        selected = Protocol.objects.get(id=protocol_id)
        request.session['current_protocol'] = Protocol.objects.get(id=protocol_id).id
        context = {
            'protocols': Protocol.objects.all(),
            'categories': Category.objects.all(),
            'user': User.objects.get(id=request.session['user_id']),
            'current_protocol': selected
        }
        return render (request, 'add_sequences.html', context)

def add_to_protocol (request):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        current_protocol = request.session['current_protocol']
        this_protocol = Protocol.objects.get(id=current_protocol)
        Sequence.objects.create(
            plane = request.POST['plane'],
            weighting = request.POST['weighting'],
            slice = request.POST['slice'],
            gap = request.POST['gap'],
            fat_sat = request.POST['fat_sat'],
            fov = request.POST['FOV'],
            notes = request.POST['notes'],
            protocol = Protocol.objects.get(id=current_protocol)
        )
        context = {
            'sequences': Sequence.objects.all(),
            'this_protocol': this_protocol
        }
        return redirect (f'/add_sequences/{current_protocol}', context)

def review (request,id):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        protocol_id = id
        selected = Protocol.objects.get(id=protocol_id)
        context = {
            'protocols': Protocol.objects.all(),
            'category': Category.objects.all(),
            'user': User.objects.get(id=request.session['user_id']),
            'current_protocol': selected
        }
        return render (request, 'review.html', context)

def details (request,id):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        protocol_id = id
        selected = Protocol.objects.get(id=protocol_id)
        context = {
            'protocols': Protocol.objects.all(),
            'category': Category.objects.all(),
            'user': User.objects.get(id=request.session['user_id']),
            'current_protocol': selected
        }
        return render (request, 'details.html', context)

def edit (request,id):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        protocol_id = id
        selected = Protocol.objects.get(id=protocol_id)
        context = {
            'protocols': Protocol.objects.all(),
            'category': Category.objects.all(),
            'user': User.objects.get(id=request.session['user_id']),
            'current_protocol': selected
        }
        return render (request, 'edit.html', context)

def edit_sequence(request,id):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        sequence_id = id
        selected = Sequence.objects.get(id=sequence_id)
        context = {
            'protocols': Protocol.objects.all(),
            'category': Category.objects.all(),
            'user': User.objects.get(id=request.session['user_id']),
            'selected': selected
        }
        return render (request, 'edit_sequence.html', context)

def edit_sequence_submit(request):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        sequence_edit = Sequence.objects.get(id=request.POST['id'])
        sequence_edit.plane = request.POST['plane']
        sequence_edit.weighting = request.POST['weighting']
        sequence_edit.slice = request.POST['slice']
        sequence_edit.gap = request.POST['gap']
        sequence_edit.fat_sat = request.POST['fat_sat']
        sequence_edit.fov = request.POST['FOV']
        sequence_edit.notes = request.POST['notes']
        sequence_edit.save()
        return redirect (f'/details/{sequence_edit.protocol.id}')

def delete_sequence(request):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        delete_sequence = Sequence.objects.get(id=request.POST['id'])
        delete_sequence.delete()
        return redirect (f'/edit/{delete_sequence.protocol.id}')

def edit_to_protocol (request):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        current_protocol = request.POST['id']
        this_protocol = Protocol.objects.get(id=current_protocol)
        Sequence.objects.create(
            plane = request.POST['plane'],
            weighting = request.POST['weighting'],
            slice = request.POST['slice'],
            gap = request.POST['gap'],
            fat_sat = request.POST['fat_sat'],
            fov = request.POST['FOV'],
            notes = request.POST['notes'],
            protocol = Protocol.objects.get(id=current_protocol)
        )

        return redirect (f'/details/{current_protocol}')

def delete_protocol (request):
    if 'user_id' not in request.session:
        return redirect ('/')
    else:
        delete_protocol = Protocol.objects.get(id=request.POST['id'])
        delete_protocol.delete()
        return redirect ('/build')

def logout (request):
    request.session.flush()
    return redirect ('/')