import json

from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import user as User, hobbies as Hobbies, friends as Friends
from .forms import LoginForm, SignupForm
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from django.middleware.csrf import get_token


## There should be a page where users can see a list of other users who have the most similar set of hobbies 
## (i.e. for each two users you should count how many hobbies in common they have) and then list those users 
## in descending order (users with most common hobbies first). Include some form of pagination, so that no more 
## than 10 users are displayed at any given time.
## From the list above users should be able to filter by age, e.g. only users with ages between 15 and 20. 
## Make sure that the frontend does not receive the full list of all users, but only the users that are needed 
## to be displayed on the page. So, changing the filter values should trigger an Ajax request for the new list of users.

def get_similar_users(request):
    if request.method == 'GET':
        user = request.user
        min_age = int(request.GET.get('min_age', 0))
        max_age = int(request.GET.get('max_age', 100))
        page_number = int(request.GET.get('page', 1))

        users = User.objects.all()
        similar_users = []
        for u in users:
            if u != user:
                age = u.calculate_age();
                if age is not None and min_age <= age <= max_age:
                    common_hobbies = set(user.hobbies.all()) & set(u.hobbies.all()) # intersection of two sets of hobbies 
                    similar_users.append({
                        'user': u.username,
                        'common_hobbies': len(common_hobbies),
                        'common_hobbies_list': [hobby.hobby for hobby in common_hobbies],
                        'age' : age
                    })
                    
        similar_users.sort(key=lambda x: x['common_hobbies'], reverse=True)

        paginator = Paginator(similar_users, 10)  # Show 10 users per page
        page_obj = paginator.get_page(page_number)

        return JsonResponse({
            'users': list(page_obj),
            'num_pages': paginator.num_pages,
            'current_page': page_number
        })
    return HttpResponse(status=405)

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@login_required
def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

# Sends over users profile details if they are logged in
def check_login(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        return JsonResponse({
            'loggedIn': True,
            'profile': user.as_dict()
        })
    return JsonResponse({'loggedIn': False, 'profile': None})


def login_view(request):
    # User is already logged in
    if request.user.is_authenticated:
        return redirect(reverse('mainapp:main'))

    form = LoginForm()

    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('mainapp:main'))
            else:
                error_message = "Invalid username or password."

        # invalid form
        return render(request, 'api/auth/login.html', {
            'form': form,
            'error_message': error_message
        })

    return render(request, 'api/auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('mainapp:login'))

def signup(request):
    '''
    Signup function
    Users creating an account
    '''
    # User is already logged in
    if request.user.is_authenticated:
        return redirect(reverse('mainapp:main'))

    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            date_of_birth = form.cleaned_data['date_of_birth']

            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                error_message = "User already exists."
                return render(request, 'api/auth/signup.html', {
                    'form': form,
                    'error_message': error_message
                })

            # create a new user
            new_user = User.objects.create_user(email, username, first_name, last_name, date_of_birth)
            # set user's password
            new_user.set_password(password)
            new_user.save()
            print('User created')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('mainapp:main'))
        else:
            print('Invalid form')

    return render(request, 'api/auth/signup.html', {'form': SignupForm})


@login_required
def users_api(request):
    users = User.objects.all()
    return JsonResponse({
        'profiles': [user.as_dict() for user in users]
    })

def user_api(request):
    POST = json.loads(request.body)

    if request.method == 'PUT':
        
        # Check if username already exists
        if User.objects.filter(username=POST['username']).exists():
            # Check if the username is the same as the current user
            if User.objects.get(id=POST['id']).username != POST['username']:
                return JsonResponse({'error': 'Username already exists'}, status=400)


        user = User.objects.get(id=POST['id'])
        user.username = POST['username']
        user.email = POST['email']
        user.first_name = POST['first_name']
        user.last_name = POST['last_name']
        user.date_of_birth = datetime.fromisoformat(POST['date_of_birth']).date()
        user.save()
        return JsonResponse({
            'profile': user.as_dict()
        })
    
def change_password(request):
    POST = json.loads(request.body)
    # Get the user by ID
    user = User.objects.get(id=POST['id'])

    # Verify current password
    if not user.check_password(POST['current_password']):
        return JsonResponse({'error': 'Current password is incorrect'}, status=400)

    # Set the new password
    user.set_password(POST['new_password'])
    user.save()

    authenticate(username=user.username, password=POST['new_password'])
    login(request, user)
    return JsonResponse({'profile': user.as_dict()})


@login_required
def hobbies_api(request):
    hobbies_list = Hobbies.objects.all()
    hobbies_data = [hobby.as_dict() for hobby in hobbies_list]
    return JsonResponse({'hobbies': [hobby['hobby'] for hobby in hobbies_data]})

@login_required
def hobby_api(request):
    POST = json.loads(request.body)
    user = User.objects.get(id=POST['user_id'])
    if request.method == 'POST':
        hobby = POST['hobby']
        try:
            add_hobby = Hobbies.objects.get(hobby=hobby)
            user.hobbies.add(Hobbies.objects.get(hobby=hobby))
            return JsonResponse({
                'hobby': add_hobby.hobby
            })
        except Hobbies.DoesNotExist:
            new_hobby = Hobbies.objects.create(hobby=hobby)
            user.hobbies.add(new_hobby)
            return JsonResponse({
                'hobby': new_hobby.hobby
            })

    if request.method == 'DELETE':
        hobby = POST['hobby']
        hobby = Hobbies.objects.get(hobby=hobby)
        user.hobbies.remove(hobby)
        return JsonResponse({
            'hobbies': [hobby.as_dict() for hobby in user.hobbies.all()]
        })

    return JsonResponse({
        'hobbies': [hobby.as_dict() for hobby in user.hobbies.all()]
    })

@login_required
def friends(request, user_id):
    """Return a list of accepted friends."""
    if request.method == 'GET':
        user = User.objects.get(id=user_id)

        # Filter friends where the user is either the sender or receiver with accepted status
        friends_from = Friends.objects.filter(friend_request_from=user, friendship_status='accepted')
        friends_to = Friends.objects.filter(friend_request_to=user, friendship_status='accepted')

        # Combine the two querysets
        friends_list = friends_from | friends_to

        return JsonResponse({'friends': [friend.as_dict() for friend in friends_list]})

@login_required
def friend_requests_by_user(request, user_id):
    """Return a list of friend requests sent by the user."""
    if request.method == 'GET':
        user = User.objects.get(id=user_id)

        # Filter friend requests sent by the user with pending status
        sent_requests = Friends.objects.filter(friend_request_from=user, friendship_status='pending')

        return JsonResponse({'sent_requests': [request.as_dict() for request in sent_requests]})

@login_required
def friend_requests_to_user(request, user_id):
    """Return a list of friend requests received by the user."""
    if request.method == 'GET':
        user = User.objects.get(id=user_id)

        # Filter friend requests received by the user with pending status
        received_requests = Friends.objects.filter(friend_request_to=user, friendship_status='pending')

        return JsonResponse({'received_requests': [request.as_dict() for request in received_requests]})



@login_required
def send_friend_request(request, username):
    """Send a friend request."""
    if request.method == 'POST':
        try:
            user_to = User.objects.get(username=username)  # Use username instead of user_id
            if not Friends.objects.filter(friend_request_from=request.user, friend_request_to=user_to).exists():
                Friends.objects.create(friend_request_from=request.user, friend_request_to=user_to)
                return JsonResponse({'message': 'Friend request sent successfully!'}, status=200)
            return JsonResponse({'error': 'Friend request already exists!'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found!'}, status=404)
    return JsonResponse({'error': 'Invalid request method!'}, status=405)

@login_required
def accept_friend_request(request, friend_id):
    """Accept a friend request."""
    if request.method == 'POST':
        try:
            friend_request = Friends.objects.get(id=friend_id, friend_request_to=request.user, friendship_status='pending')
            friend_request.friendship_status = 'accepted'
            friend_request.save()
            return JsonResponse({'message': 'Friend request accepted.'}, status=200)
        except Friends.DoesNotExist:
            return JsonResponse({'error': 'Friend request not found or already accepted/rejected.'}, status=404)

@login_required
def reject_friend_request(request, friend_id):
    """Reject a friend request."""
    if request.method == 'DELETE':
        try:
            friend_request = Friends.objects.get(id=friend_id, friend_request_to=request.user, friendship_status='pending')
            friend_request.delete()
            return JsonResponse({'message': 'Friend request rejected.'}, status=200)
        except Friends.DoesNotExist:
            return JsonResponse({'error': 'Friend request not found or already accepted/rejected.'}, status=404)

@login_required
def remove_friend(request, friend_id):
    """Remove an existing friend."""
    if request.method == 'DELETE':
        try:
            friend = Friends.objects.get(id=friend_id, friendship_status='accepted')
            friend.delete()
            return JsonResponse({'message': 'Friend removed.'}, status=200)
        except Friends.DoesNotExist:
            return JsonResponse({'error': 'Friend not found.'}, status=404)