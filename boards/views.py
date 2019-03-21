from django.shortcuts import render, redirect, get_object_or_404
from .models import Board
from .forms import BoardForm

# Create your views here.
def index(request):
    boards = Board.objects.order_by('-pk')
    context = {
        'boards' : boards
    }
    return render(request, 'boards/index.html', context)
    
def create(request):

    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save()
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
    if request.method == 'POST':
        board.delete()
        return redirect('boards:index')
    else:
        return redirect('boards:detail', board.pk)
    
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)   # 1
        if form.is_valid():
            board = form.save()                          # 2
            return redirect('boards:detail', board.pk)
    else:
        form = BoardForm(instance=board)                 # 3
    context = {
            'form' : form, 
            'board' : board,
    }
    return render(request, 'boards/forms.html', context)