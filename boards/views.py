from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Board
from .forms import BoardForm

# Create your views here.
def index(request):
    boards = Board.objects.order_by('-pk')
    context = {
        'boards' : boards
    }
    return render(request, 'boards/index.html', context)
    
# 로그인 되어있으면 실행
@login_required
def create(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            # board를 바로 저장하지 않고, 현재 user를 넣고 저장
            # 실제 DB에 반영 전까지의 단계를 진행하고, 그 중간에 user 정보를
            # request.user에서 가져와서 그 후에 저장한다.
            board = form.save(commit=False)
            board.user = request.user
            board.save()
            return redirect('boards:detail', board.pk)
    # GET 요청(혹은 다른 메서드)이면 기본 폼을 생성한다.
    else:
        form = BoardForm()
    # indentation 주의
    context = {'form' : form}
    return render(request, 'boards/forms.html', context)
        
def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    # 객체 가져오는 방식 다르게 함, 없는 게시물 번호 url로 이동하면 404메세지
    board = get_object_or_404(Board, pk=board_pk)
    context = {
        'board' : board,
    }
    return render(request, 'boards/detail.html', context)
    
def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:   # 유저가 같으면
        if request.method == 'POST':
            board.delete()
            return redirect('boards:index')
        else:
            return redirect('boards:detail', board.pk)
    else:
        return redirect('boards:index')

@login_required
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:
        
        if request.method == 'POST':
            form = BoardForm(request.POST, instance=board)   # 1
            if form.is_valid():
                board = form.save()                          # 2
                return redirect('boards:detail', board.pk)
        else:
            form = BoardForm(instance=board)                 # 3
            
    else:
        return redirect('boards:index')
    context = {
            'form' : form, 
            'board' : board,
    }
    return render(request, 'boards/forms.html', context)