from django.http import JsonResponse
from django.shortcuts import redirect, render

from .models import History, User, UserRelation, UserState
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max, OuterRef, Subquery
from .forms import HistoryForm, SignUpForm, UserRelationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@csrf_exempt
def home(request):
    if request.user.is_authenticated:
        current_user_option = request.user.option
    else:
        current_user_option = None

    return render(request, 'home.html', {'current_user_option': current_user_option})

@csrf_exempt
def signup(request):  # 회원가입 /signup
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['id']
            if User.objects.filter(id=user_id).exists():
                return JsonResponse({'error': '이미 있는 아이디입니다.'}, status=400)
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)  # 비밀번호를 해쉬값으로 변경
            user.save()  # 회원가입 폼을 저장하고 생성된 사용자를 가져옴
            UserState.objects.create(user_id=user.id, state='Offline')  # 회원의 기본상태를 오프라인으로 설정
            return JsonResponse({'success': True, 'message': '회원가입이 성공적으로 완료되었습니다.'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def user_login(request):# /login
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['id']
            password = form.cleaned_data['password']
            user = authenticate(request, id=user_id, password=password)
            if user is not None:     # 로그인 성공 시 
                login(request, user)
                return JsonResponse({'option': user.option})
            else:  # 로그인 실패 시
                return JsonResponse({'error': '아이디 또는 비밀번호가 올바르지 않습니다.'}, status=400)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    

@csrf_exempt
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True, 'message': 'Successfully logged out.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
@login_required#로그인되어있어야함
def relations_view(request):# 보호자일때 피보호자 리스트및 상태 확인/relations
    
    # 현재 로그인된 사용자 아이디
    current_user_id = request.user.id
    
    # 현재 로그인된 사용자가 helper_id인 경우의 recipient_id 목록 가져오기
    user_relations = UserRelation.objects.filter(helper_id=current_user_id)
    
    # recipient_id 목록 추출
    recipient_ids = list(user_relations.values_list('recipient_id', flat=True))
    
    results = []
    for recipient_id in recipient_ids:
        # 최신 UserState 가져오기
        latest_state = UserState.objects.filter(user_id=recipient_id).order_by('-time').first()
        
        if latest_state:
            recipient = User.objects.get(id=recipient_id)
            results.append({
                'id': recipient_id,
                'name': recipient.name,
                'phoneNum': recipient.phoneNum,
                'latest_state': latest_state.state,
                #'latest_state_time': latest_state.time
            })
    
    return JsonResponse({'results': results})


@csrf_exempt
def makeRelations(request):# 보호자가 관계추가/makerelations
    if request.method == 'POST':
        form = UserRelationForm(request.POST)
        if form.is_valid():
            helper_id = form.cleaned_data['helper_id']
            recipient_id = form.cleaned_data['recipient_id']
            # UserRelation 테이블에 데이터 추가
            UserRelation.objects.create(helper_id=helper_id, recipient_id=recipient_id)
            return JsonResponse({'success': True, 'message': 'Relationship created successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    

@csrf_exempt
@login_required
def insertSearch(request):# 목적지검색 최근기록에 삽입 /routeSearch
    if request.method == 'POST':
        form = HistoryForm(request.POST)
        if form.is_valid():
            history = form.save(commit=False)  # Don't save to the database yet
            history.user_id = request.user.id  # Set the current user's ID
            history.save()  # Now save to the database
            return JsonResponse({'success': True, 'message': 'History saved successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
@login_required
def recentSearch(request):
    current_user_id = request.user.id
    user_history = History.objects.filter(user_id=current_user_id).order_by('-historyNum')[:10]

    history_data = []
    for history in user_history:
        history_data.append({
            'historyNum': history.historyNum,
            'user_id': history.user_id,
            'arrival': history.arrival,
            'time': history.time
        })

    return JsonResponse({'user_history': history_data})


@csrf_exempt
def startNavi(request):#네비시작 /startnavi
    current_user_id = request.user.id
    UserState.objects.create(user_id=current_user_id, state='Navigation')#회원의 상태를 네비게이션으로 설정
    return JsonResponse({'success': True, 'state': 'Navigation'})


@csrf_exempt
def startWalk(request):#도보시작 /startwalk
    current_user_id = request.user.id
    UserState.objects.create(user_id=current_user_id, state='Walking')#회원의 상태를 도보로 설정
    return JsonResponse({'success': True, 'state': 'Walking'})


@csrf_exempt
def DestinationArrival(request):#목적지 도착 /arrival
    current_user_id = request.user.id
    UserState.objects.create(user_id=current_user_id, state='Offline')#회원의 상태를 오프라인으로 설정
    return JsonResponse({'success': True, 'state': 'Offline'})
