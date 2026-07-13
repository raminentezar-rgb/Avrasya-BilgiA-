from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
import json
import csv
from .models import Room, Topic, Message, User, Resource, Quiz, Question, QuizSubmission, Notification, Assignment, AssignmentSubmission, DEPARTMENT_CHOICES
from .forms import RoomForm, UserForm, MyUserCreationForm, ResourceForm, QuizForm, QuestionForm
from .proliz_obs import ProlizOBSClient

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        login_type = request.POST.get('login_type', 'teacher')

        # 1. Proliz OBS Entegrasyonu ile Öğrenci Girişi (Öğrenci Numarası ile)
        if login_type == 'student_obs' or request.POST.get('student_no'):
            student_no = request.POST.get('student_no', '').strip()
            obs_pass = request.POST.get('obs_password', '')
            res = ProlizOBSClient.get_student_info(student_no, obs_pass)
            if res.get('success'):
                email = res['email']
                user = User.objects.filter(Q(student_id=student_no) | Q(email=email)).first()
                if not user:
                    username_base = f"ogr_{student_no}"
                    user = User.objects.create_user(
                        email=email,
                        username=username_base,
                        password=obs_pass or 'AvrasyaOBS123',
                        name=res.get('full_name', f"Öğrenci {student_no}"),
                        student_id=student_no,
                        department=res.get('department', 'Bilgisayar Mühendisliği'),
                        role='student'
                    )
                login(request, user)
                messages.success(request, f"Proliz OBS Entegrasyonu ile hoş geldiniz, {user.name} ({user.department})!")
                return redirect('home')
            else:
                messages.error(request, res.get('error', 'Proliz OBS öğrenci doğrulaması başarısız! Öğrenci Numaranızı kontrol ediniz.'))

        # 2. Akademisyen / Öğretim Üyesi Girişi (Sadece @avrasya.edu.tr e-posta ile)
        else:
            email = request.POST.get('email', '').lower().strip()
            password = request.POST.get('password')

            if not email.endswith('@avrasya.edu.tr'):
                messages.error(request, 'Akademisyen / Öğretim Üyesi girişi için yalnızca resmi Avrasya Üniversitesi e-posta adresi (@avrasya.edu.tr) kullanılmalıdır!')
                return render(request, 'base/login_register.html', {'page': page})

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Akademisyen olarak giriş yapıldı: {user.name or user.username}")
                return redirect('home')
            else:
                messages.error(request, 'E-posta veya şifre hatalı! Lütfen resmi @avrasya.edu.tr bilgilerinizi kontrol ediniz.')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            if user.role == 'teacher' and not user.email.lower().strip().endswith('@avrasya.edu.tr'):
                messages.error(request, 'Akademisyen / Öğretim Üyesi kaydı için yalnızca resmi Avrasya Üniversitesi e-posta adresi (@avrasya.edu.tr) kullanılmalıdır!')
                return render(request, 'base/login_register.html', {'form': form})
            user.save()
            login(request, user)
            messages.success(request, 'Avrasya BilgiAğı platformuna kaydınız başarıyla tamamlandı!')
            return redirect('home')
        else:
            messages.error(request, 'Kayıt sırasında hata oluştu. Lütfen bilgilerinizi kontrol ediniz.')

    return render(request, 'base/login_register.html', {'form': form})


@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    dept = request.GET.get('dept') if request.GET.get('dept') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(course_code__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q) |
        Q(host__department__icontains=q)
    ).distinct()

    if dept:
        rooms = rooms.filter(
            Q(host__department__icontains=dept) |
            Q(topic__name__icontains=dept) |
            Q(name__icontains=dept) |
            Q(description__icontains=dept) |
            Q(course_code__icontains=dept)
        ).distinct()

    # Öğrenciler SADECE kendi bölümlerine ait odaları, konuları ve materyalleri görebilir
    topics = Topic.objects.all()
    if request.user.role == 'student' and request.user.department:
        dept = request.user.department
        dept_keywords = [w for w in dept.split() if len(w) > 3 and w not in ['Mühendisliği', 'Fakültesi', 'Bölümü', 'Programı', 'Teknolojisi', 'Hizmetleri']]
        query = Q(host__department=dept) | Q(topic__name__iexact=dept)
        for kw in dept_keywords:
            query |= Q(topic__name__icontains=kw) | Q(name__icontains=kw) | Q(course_code__icontains=kw)
        rooms = rooms.filter(query).distinct()

        # Sol menüdeki konuları da öğrencinin görebildiği odaların konuları veya kendi bölümüyle sınırla
        topics = Topic.objects.filter(
            Q(room__in=rooms) | Q(name__iexact=dept)
        ).distinct()

    room_count = rooms.count()

    room_messages_query = Message.objects.filter(
        Q(room__topic__name__icontains=q))
    if request.user.role == 'student' and request.user.department:
        room_messages_query = room_messages_query.filter(room__in=rooms).distinct()
    room_messages = room_messages_query[0:5]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages,
               'departments': DEPARTMENT_CHOICES, 'selected_dept': dept}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def room(request, pk):
    room_obj = Room.objects.get(id=pk)

    # Öğrencilerin diğer bölüm odalarına yetkisiz erişimini engelle
    if request.user.role == 'student' and request.user.department:
        if room_obj.host and room_obj.host.department not in [request.user.department, 'Genel / Diğer']:
            if request.user not in room_obj.participants.all():
                messages.error(request, f"Güvenlik Kısıtlaması: Bu oda '{room_obj.host.department}' bölümüne aittir. Sadece kendi bölümünüze ({request.user.department}) ait çalışma odalarına erişebilirsiniz.")
                return redirect('home')

    room_messages = room_obj.message_set.all()
    participants = room_obj.participants.all()
    resources = room_obj.resources.all()

    resource_form = ResourceForm()

    if request.method == 'POST':
        if 'resource_submit' in request.POST:
            if not request.user.is_authenticated:
                return redirect('login')
            form = ResourceForm(request.POST, request.FILES)
            if form.is_valid():
                res = form.save(commit=False)
                res.user = request.user
                res.room = room_obj
                res.save()
                messages.success(request, 'Ders materyali / sesli anons başarıyla eklendi!')
                return redirect('room', pk=room_obj.id)
            else:
                file_obj = request.FILES.get('file')
                title_str = request.POST.get('title') or 'Ders Materyali / Sesli Anons'
                if file_obj or request.POST.get('link'):
                    Resource.objects.create(
                        user=request.user,
                        room=room_obj,
                        title=title_str,
                        file=file_obj,
                        link=request.POST.get('link', ''),
                        description=request.POST.get('description', '')
                    )
                    messages.success(request, 'Ders materyali / sesli anons başarıyla eklendi!')
                    return redirect('room', pk=room_obj.id)
        elif 'body' in request.POST:
            if not request.user.is_authenticated:
                return redirect('login')
            body_text = request.POST.get('body', '').strip()
            if body_text:
                Message.objects.create(
                    user=request.user,
                    room=room_obj,
                    body=body_text
                )
                room_obj.participants.add(request.user)
            return redirect('room', pk=room_obj.id)

    context = {'room': room_obj, 'room_messages': room_messages,
               'participants': participants, 'resources': resources,
               'resource_form': resource_form, 'quizzes': room_obj.quizzes.all()}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    if request.user.role not in ['faculty', 'teacher'] and not request.user.is_superuser:
        messages.error(request, 'Ders odası oluşturma yetkisi yalnızca Öğretim Üyeleri / Akademisyenlere aittir.')
        return redirect('home')
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            course_code=request.POST.get('course_code', ''),
            room_type=request.POST.get('room_type', 'general'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.course_code = request.POST.get('course_code', '')
        room.room_type = request.POST.get('room_type', 'general')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def deleteResource(request, pk):
    resource = Resource.objects.get(id=pk)

    if request.user != resource.user and request.user != resource.room.host:
        return HttpResponse('Bu işlemi yapmaya yetkiniz yok!!')

    if request.method == 'POST':
        room_id = resource.room.id
        resource.delete()
        return redirect('room', pk=room_id)
    return render(request, 'base/delete.html', {'obj': resource})


def roomMessagesAjax(request, pk):
    room_obj = Room.objects.get(id=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            body_text = data.get('body', '').strip()
        except:
            body_text = request.POST.get('body', '').strip()

        if body_text:
            msg = Message.objects.create(
                user=request.user,
                room=room_obj,
                body=body_text
            )
            room_obj.participants.add(request.user)
            return JsonResponse({
                'status': 'ok',
                'message': {
                    'id': msg.id,
                    'body': msg.body,
                    'user': msg.user.username,
                    'name': msg.user.name or msg.user.username,
                    'avatar': msg.user.avatar.url if msg.user.avatar else '/static/images/avatar.svg',
                    'created': msg.created.strftime("%H:%M")
                }
            })
        return JsonResponse({'status': 'error', 'msg': 'Boş mesaj gönderilemez'}, status=400)

    # GET messages
    messages_list = []
    for msg in room_obj.message_set.all():
        messages_list.append({
            'id': msg.id,
            'body': msg.body,
            'user': msg.user.username,
            'name': msg.user.name or msg.user.username,
            'avatar': msg.user.avatar.url if msg.user.avatar else '/static/images/avatar.svg',
            'created': msg.created.strftime("%H:%M"),
            'is_owner': (request.user.is_authenticated and request.user == msg.user)
        })
    return JsonResponse({'status': 'ok', 'messages': messages_list})



@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


@login_required(login_url='login')
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    if request.user.role == 'student' and request.user.department:
        dept = request.user.department
        dept_keywords = [w for w in dept.split() if len(w) > 3 and w not in ['Mühendisliği', 'Fakültesi', 'Bölümü', 'Programı', 'Teknolojisi', 'Hizmetleri']]
        query = Q(name__iexact=dept)
        for kw in dept_keywords:
            query |= Q(name__icontains=kw)
        topics = topics.filter(query).distinct()
    return render(request, 'base/topics.html', {'topics': topics})


@login_required(login_url='login')
def activityPage(request):
    room_messages = Message.objects.all()
    if request.user.role == 'student' and request.user.department:
        dept = request.user.department
        dept_keywords = [w for w in dept.split() if len(w) > 3 and w not in ['Mühendisliği', 'Fakültesi', 'Bölümü', 'Programı', 'Teknolojisi', 'Hizmetleri']]
        query = Q(room__host__department=dept) | Q(room__topic__name__iexact=dept)
        for kw in dept_keywords:
            query |= Q(room__topic__name__icontains=kw) | Q(room__name__icontains=kw) | Q(room__course_code__icontains=kw)
        room_messages = room_messages.filter(query).distinct()
    return render(request, 'base/activity.html', {'room_messages': room_messages})


@login_required(login_url='login')
def create_quiz(request, pk):
    if request.user.role == 'student':
        messages.error(request, "Öğrencilerin sınav oluşturma yetkisi bulunmamaktadır.")
        return redirect('quizzes')

    room = Room.objects.get(id=pk)
    if request.user != room.host and request.user.role != 'faculty':
        return HttpResponse("Bu odaya sınav ekleme yetkiniz bulunmamaktadır.")

    form = QuizForm()
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.room = room
            quiz.creator = request.user
            quiz.save()
            for p in room.participants.all():
                if p != request.user:
                    Notification.objects.create(
                        recipient=p,
                        sender=request.user,
                        message=f"'{room.name}' odasında yeni çevrimiçi sınav yayınlandı: {quiz.title} 📝",
                        link=f"/quiz/{quiz.id}/"
                    )
            messages.success(request, "Sınav başarıyla oluşturuldu. Şimdi soru ekleyebilirsiniz.")
            return redirect('quiz-detail', pk=quiz.id)

    context = {'form': form, 'room': room}
    return render(request, 'base/quiz_form.html', context)


@login_required(login_url='login')
def create_quiz_general(request):
    if request.user.role == 'student':
        messages.error(request, "Öğrencilerin sınav oluşturma yetkisi bulunmamaktadır.")
        return redirect('quizzes')

    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        room = Room.objects.get(id=room_id)
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        duration_minutes = request.POST.get('duration_minutes', 30)
        
        quiz = Quiz.objects.create(
            room=room,
            creator=request.user,
            title=title,
            description=description,
            duration_minutes=duration_minutes
        )
        for p in room.participants.all():
            if p != request.user:
                Notification.objects.create(
                    recipient=p,
                    sender=request.user,
                    message=f"'{room.name}' odasında yeni çevrimiçi sınav yayınlandı: {quiz.title} 📝",
                    link=f"/quiz/{quiz.id}/"
                )
        messages.success(request, "Sınav başarıyla oluşturuldu! Şimdi aşağıdan soruları ekleyebilir ve sınavı yönetebilirsiniz.")
        return redirect('quiz-detail', pk=quiz.id)

    rooms = Room.objects.all()
    form = QuizForm()
    return render(request, 'base/quiz_form_general.html', {'rooms': rooms, 'form': form})


@login_required(login_url='login')
def quiz_detail(request, pk):
    quiz = Quiz.objects.get(id=pk)

    # Öğrencilerin diğer bölüm sınavlarına yetkisiz erişimini engelle
    if request.user.role == 'student' and request.user.department:
        room_obj = quiz.room
        if room_obj.host and room_obj.host.department not in [request.user.department, 'Genel / Diğer']:
            if request.user not in room_obj.participants.all():
                messages.error(request, f"Güvenlik Kısıtlaması: Bu sınav '{room_obj.host.department}' bölümüne aittir. Sadece kendi bölümünüze ({request.user.department}) ait sınavlara erişebilirsiniz.")
                return redirect('home')

    questions = quiz.questions.all()
    user_submission = QuizSubmission.objects.filter(quiz=quiz, student=request.user).first()
    question_form = QuestionForm()

    # Öğretim Üyesi / Sınav Sahibi Soru Ekleme
    if request.method == 'POST' and 'add_question' in request.POST:
        if request.user != quiz.creator and request.user != quiz.room.host:
            return HttpResponse("Soru ekleme yetkiniz yok.")
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            q = question_form.save(commit=False)
            q.quiz = quiz
            q.save()
            messages.success(request, "Soru başarıyla sınav listesine eklendi.")
            return redirect('quiz-detail', pk=quiz.id)

    # Öğrenci Sınav Gönderimi (Cevaplama)
    if request.method == 'POST' and 'submit_quiz' in request.POST:
        if user_submission:
            messages.error(request, "Bu sınavı daha önce cevapladınız.")
            return redirect('quiz-detail', pk=quiz.id)

        score = 0
        total = questions.count()
        for q in questions:
            ans = request.POST.get(f'question_{q.id}')
            if ans and ans == q.correct_option:
                score += 1

        submission = QuizSubmission.objects.create(
            quiz=quiz,
            student=request.user,
            score=score,
            total_questions=total
        )
        messages.success(request, f"Sınavı tamamladınız. Sonucunuz: {score} / {total} Doğru.")
        return redirect('quiz-detail', pk=quiz.id)

    submissions = quiz.submissions.all()
    context = {
        'quiz': quiz,
        'questions': questions,
        'question_form': question_form,
        'user_submission': user_submission,
        'submissions': submissions,
        'is_creator': (request.user == quiz.creator or request.user == quiz.room.host)
    }
    return render(request, 'base/quiz_detail.html', context)


@login_required(login_url='login')
def delete_quiz(request, pk):
    quiz = Quiz.objects.get(id=pk)
    room_id = quiz.room.id
    if request.user != quiz.creator and request.user != quiz.room.host:
        return HttpResponse("Sınav silme yetkiniz bulunmuyor.")
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, "Sınav silindi.")
        return redirect('room', pk=room_id)
    return render(request, 'base/delete.html', {'obj': quiz.title})


@login_required(login_url='login')
def delete_question(request, pk):
    question = Question.objects.get(id=pk)
    quiz_id = question.quiz.id
    if request.user != question.quiz.creator and request.user != question.quiz.room.host:
        return HttpResponse("Soru silme yetkiniz yok.")
    question.delete()
    messages.success(request, "Soru sınavdan kaldırıldı.")
    return redirect('quiz-detail', pk=quiz_id)


@login_required(login_url='login')
def quizzesPage(request):
    quizzes = Quiz.objects.all()
    if request.user.role == 'student' and request.user.department:
        dept = request.user.department
        dept_keywords = [w for w in dept.split() if len(w) > 3 and w not in ['Mühendisliği', 'Fakültesi', 'Bölümü', 'Programı', 'Teknolojisi', 'Hizmetleri']]
        query = Q(room__host__department=dept) | Q(room__topic__name__iexact=dept)
        for kw in dept_keywords:
            query |= Q(room__topic__name__icontains=kw) | Q(room__name__icontains=kw) | Q(room__course_code__icontains=kw)
        quizzes = quizzes.filter(query).distinct()
    return render(request, 'base/quizzes.html', {'quizzes': quizzes})


@login_required(login_url='login')
def export_quiz_results(request, pk):
    quiz = Quiz.objects.get(id=pk)
    if request.user != quiz.creator and request.user != quiz.room.host and request.user.role != 'faculty':
        return HttpResponse("Bu sınavın sonuçlarını indirme yetkiniz yoktur.")

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename="sinav_sonuclari_quiz_{quiz.id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Öğrenci Adı Soyadı', 'Kullanıcı Adı', 'Bölümü', 'Puan', 'Toplam Soru', 'Yüzde (%)', 'Teslim Tarihi'])

    for sub in quiz.submissions.all():
        pct = round((sub.score / sub.total_questions) * 100, 1) if sub.total_questions > 0 else 0
        writer.writerow([
            sub.student.name or sub.student.username,
            sub.student.username,
            sub.student.department or '-',
            sub.score,
            sub.total_questions,
            f"%{pct}",
            sub.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    return response


@login_required(login_url='login')
def verify_message(request, pk):
    message = Message.objects.get(id=pk)
    room_id = message.room.id
    if request.user == message.room.host or request.user.role == 'faculty':
        message.is_verified_answer = not message.is_verified_answer
        message.save()
        status_txt = "onaylandı" if message.is_verified_answer else "onayı kaldırıldı"
        messages.success(request, f"Cevap öğretim üyesi tarafından {status_txt}.")
        # Create notification for message author if verified
        if message.is_verified_answer and message.user != request.user:
            Notification.objects.create(
                recipient=message.user,
                sender=request.user,
                message=f"'{message.room.name}' odasındaki cevabınız Öğretim Üyesi tarafından Doğru Cevap olarak onaylandı! ✅",
                link=f"/room/{room_id}/"
            )
    else:
        messages.error(request, "Bu işlem için öğretim üyesi yetkiniz olmalıdır.")
    return redirect('room', pk=room_id)


@login_required(login_url='login')
def toggle_save_resource(request, pk):
    resource = Resource.objects.get(id=pk)
    if request.user in resource.saved_by.all():
        resource.saved_by.remove(request.user)
        messages.info(request, "Materyal kütüphanenizden çıkarıldı.")
    else:
        resource.saved_by.add(request.user)
        messages.success(request, "Materyal kişisel kütüphanenize kaydedildi! 🔖")
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')
def saved_resources(request):
    resources = request.user.saved_resources.all()
    return render(request, 'base/saved_resources.html', {'resources': resources})


@login_required(login_url='login')
def create_assignment(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host and request.user.role != 'faculty':
        return HttpResponse("Ödev oluşturma yetkiniz yok.")

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        if title and deadline:
            assignment = Assignment.objects.create(
                room=room,
                creator=request.user,
                title=title,
                description=description or '',
                deadline=deadline
            )
            messages.success(request, "Ödev başarıyla oluşturuldu!")
            # Notify room participants
            for p in room.participants.all():
                if p != request.user:
                    Notification.objects.create(
                        recipient=p,
                        sender=request.user,
                        message=f"'{room.name}' odasında yeni ödev eklendi: {title} (Son Teslim: {deadline})",
                        link=f"/room/{room.id}/"
                    )
    return redirect('room', pk=room.id)


@login_required(login_url='login')
def submit_assignment(request, pk):
    assignment = Assignment.objects.get(id=pk)
    if request.method == 'POST':
        notes = request.POST.get('notes', '')
        file = request.FILES.get('file')
        sub, created = AssignmentSubmission.objects.get_or_create(
            assignment=assignment,
            student=request.user,
            defaults={'notes': notes, 'file': file}
        )
        if not created:
            sub.notes = notes
            if file:
                sub.file = file
            sub.save()
        if assignment.creator and assignment.creator != request.user:
            Notification.objects.create(
                recipient=assignment.creator,
                sender=request.user,
                message=f"@{request.user.username} öğrencisi '{assignment.title}' ödevini teslim etti! 📂",
                link=f"/room/{assignment.room.id}/"
            )
        messages.success(request, "Ödeviniz başarıyla teslim edildi! 🎉")
    return redirect('room', pk=assignment.room.id)


@login_required(login_url='login')
def read_notification(request, pk):
    try:
        notif = Notification.objects.get(id=pk, recipient=request.user)
        link = notif.link or '/'
        notif.is_read = True
        notif.save()
    except Notification.DoesNotExist:
        link = '/'
    return redirect(link)


@login_required(login_url='login')
def clear_all_notifications(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', 'home'))
