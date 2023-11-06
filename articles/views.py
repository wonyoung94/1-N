from django.shortcuts import render, redirect
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

# Create your views here.
def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)

def detail(request, id):
    article = Article.objects.get(id=id)
    form = CommentForm()

    # 1. comment 목록을 조회하는 법 : 댓글을 기준으로 filter
    # comments = Comment.objects.filter(article=article)

    # 2. comment 목록을 조회하는 법 : article을 기준으로 댓글 취합(python에서 실행)
    # comments = article.comment_set.all()

    # 3. comment 목록을 조회하는 법 : html 코드에서 만드는 방법(자주 쓸 예정, html에서 실행)
    # HTML에서 comments = article.comment_set.all()
    # detail.html에서 17번째 줄에서 {% for comment in comments %} 
    #   -> {% for comment in article.comment_set.all %}
    # 이 방법을 사용하려면 밑의 context 딕셔너리의 comments줄도 주석처리 필요


    context = {
        'article': article,
        'form': form,
        # 'comments': comments,
    }

    return render(request, 'detail.html', context)

def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', id=article.id)
    else:
        form = ArticleForm()

    context = {
        'form': form
    }

    return render(request, 'form.html', context)

def comment_create(request, article_id):
    form = CommentForm(request.POST)

    if form.is_valid():
        # form을 저장하되 추가로 넣어야 하는 데이터(article정보) 를 넣기 위해 잠시 멈춰봐!
        comment = form.save(commit=False)

        # # 1-1. article찾기 : article_id를 기준으로 article obj 가져오기
        # #                 (db를 호출해서 게시물을 찾아야 하므로 시간이 좀 걸림)
        # article = Article.objects.get(id=article_id)
        # # 1-2. article찾기 : article 컬럼에 추가
        # comment.article = article
        # comment.save()

        # 2-1. article찾기 : integer를 저장하는 방법(데이터 양이 많을 수록 2번이 효율적)
        comment.article_id = article_id
        comment.save()

        return redirect('articles:detail', id=article_id)

def comment_delete(request, article_id, id):
    comment = Comment.objects.get(id=id)
    comment.delete()

    return redirect('articles:detail', id=article_id)


