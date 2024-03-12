from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Article, Category, Comment
from django.db.models import Q
from django.views.generic.edit import UpdateView, CreateView
from .forms import ArticleForm

class Index(ListView):
	model = Article
	queryset = Article.objects.all().order_by('-date')
	template_name = 'blog/index.html'
	paginate_by = 6

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		context['title'] = 'Home - Everything Of Life'
		return context

class SearchView(ListView):
	model = Article
	template_name = 'blog/index.html'
	paginate_by = 6
  
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["categories"] = Category.objects.all()
		return context

	def get_queryset(self):
		query = self.request.GET.get('q')
			
		if query:
			queryset = Article.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
		else:
			queryset = Article.objects.all()

		return queryset

class SearchViewTitle(ListView):
	model = Article
	template_name = 'blog/index.html'
	paginate_by = 6
  
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["categories"] = Category.objects.all()
		return context

	def get_queryset(self):
		queryset = Article.objects.all().order_by('title')
		return queryset

class SearchViewDate(ListView):
	model = Article
	template_name = 'blog/index.html'
	paginate_by = 6
  
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["categories"] = Category.objects.all()
		return context

	def get_queryset(self):
		queryset = Article.objects.all().order_by('date')
		return queryset

class SearchViewLike(ListView):
	model = Article
	template_name = 'blog/index.html'
	paginate_by = 6
  
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["categories"] = Category.objects.all()
		return context

	def get_queryset(self):
		queryset = Article.objects.all().order_by('likes')
		return queryset

class ArticlesByCategory(ListView):
	model = Article
	template_name = 'blog/index.html'
	paginate_by = 6

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		category = Category.objects.get(name=self.kwargs.get('category'))
		context['title'] = category.name + ' - Everything Of Life'
		return context

	def get_queryset(self, *args, **kwargs):
		return Article.objects.filter(category=self.kwargs.get('category')).order_by('-date')

class Featured(ListView):
	model = Article
	queryset = Article.objects.filter(featured=True).order_by('title')
	template_name = 'blog/featured.html'
	paginate_by = 6

class DetailArticleView(DetailView):
	model = Article
	template_name = 'blog/detail_post.html'

	def get_context_data(self, *args, **kwargs):
		context = super(DetailArticleView, self).get_context_data(*args, **kwargs)
		context['liked_by_user'] = False
		article = Article.objects.get(id=self.kwargs.get('pk'))
		if article.likes.filter(pk=self.request.user.id).exists():
			context['liked_by_user'] = True
		context['title'] = article.title + ' - Everything Of Life'
		return context

class LikeArticle(View):
	def post(self, request, pk):
		article = Article.objects.get(id=pk)
		if article.likes.filter(pk=self.request.user.id).exists():
			article.likes.remove(request.user.id)
		else:
			article.likes.add(request.user.id)

		article.save()
		return redirect('detail_article', pk)

class CommentArticle(View):
	def post(self, request, pk):
		comment_text = request.POST.get('comment_text')
		if comment_text:
			article = Article.objects.get(id=pk)
			comment = Comment.objects.create(content=comment_text, user=request.user, article=article)
			article.comments.add(comment)

		return redirect('detail_article', pk)

class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Article
	template_name = 'blog/blog_delete.html'
	success_url = reverse_lazy('post-collection')

	def test_func(self):
		article = Article.objects.get(id=self.kwargs.get('pk'))
		return self.request.user.id == article.author.id

class EditArticleView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/blog_edit.html'
    success_url = reverse_lazy('post-collection')

    def form_valid(self, form):
        return super().form_valid(form)

class CreateArticleView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/blog_create.html'
    success_url = reverse_lazy('post-collection')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)