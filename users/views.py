from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm
from .forms import UserUpdateForm
from django.contrib.auth import logout

from blog.models import Article

class RegisterView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'users/register.html', {'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('index')

class ProfileView(View):
	def get(self, request):
		form = UserUpdateForm(instance=request.user)

		return render(request, 'users/user-profile.html', {
			'title': 'Profile  - Everything Of Life',
			'form': form
		})

	def post(self, request):
		if request.method == 'POST':
			form = UserUpdateForm(request.POST, instance=request.user)
			if form.is_valid():
				form.save()
				return redirect('/account/profile/')
		else:
			form = UserUpdateForm(instance=request.user)

		return render(request, 'users/user-profile.html', {
			'title': 'Profile  - Everything Of Life',
			'form': form
		})

class PostCollectionView(View):
	def get(self, request):

		user_id = request.user.id
		articles = Article.objects.filter(author_id=user_id)

		context = {
			'title': 'Post Collection  - Everything Of Life',
			'articles': articles
		}

		return render(request, 'users/post-collection.html', context)

def logout_user (request):
	logout(request=request)
	return redirect('/')
