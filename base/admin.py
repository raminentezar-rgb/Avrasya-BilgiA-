from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Room, Topic, Message, User, Resource, Quiz, Question,
    QuestionBankItem, QuizSubmission, QuizSubmissionAnswer,
    Notification, Assignment, AssignmentSubmission,
    AttendanceSession, AttendanceRecord
)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'name', 'get_role_display', 'department', 'student_id', 'email', 'is_staff', 'is_active')
    list_filter = ('role', 'department', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'name', 'email', 'student_id', 'department')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Kişisel Bilgiler (Ad Soyad, E-Posta, Biyografi)', {'fields': ('name', 'email', 'bio', 'avatar')}),
        ('Akademik Bilgiler & Rol (Öğrenci / Öğretim Üyesi)', {'fields': ('role', 'department', 'student_id')}),
        ('Sosyal Medya Linkleri', {'fields': ('github_link', 'linkedin_link')}),
        ('İzinler & Yetkiler', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Önemli Tarihler', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'role', 'department', 'student_id', 'password1', 'password2'),
        }),
    )

    def get_role_display(self, obj):
        role_map = {
            'student': 'Öğrenci (Student)',
            'faculty': 'Öğretim Üyesi / Akademisyen (Faculty)',
            'ta': 'Asistan / TA'
        }
        return role_map.get(obj.role, obj.role)
    get_role_display.short_description = 'Akademik Rol'
    get_role_display.admin_order_field = 'role'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'topic', 'course_code', 'room_type', 'updated')
    list_filter = ('room_type', 'topic', 'host__department')
    search_fields = ('name', 'course_code', 'description', 'host__username', 'host__name')
    ordering = ('-updated',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'get_short_body', 'is_verified_answer', 'created')
    list_filter = ('is_verified_answer', 'room__topic', 'created')
    search_fields = ('body', 'user__username', 'room__name')
    
    def get_short_body(self, obj):
        return obj.body[:60] + '...' if len(obj.body) > 60 else obj.body
    get_short_body.short_description = 'Mesaj İçeriği'


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'room', 'user', 'created')
    list_filter = ('room__topic', 'created')
    search_fields = ('title', 'description', 'user__username', 'room__name')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'room', 'creator', 'duration_minutes', 'created')
    list_filter = ('room__topic', 'created')
    search_fields = ('title', 'description', 'creator__username', 'room__name')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('get_short_text', 'quiz', 'question_type', 'points')
    list_filter = ('question_type', 'quiz__room__topic')
    search_fields = ('text', 'quiz__title')

    def get_short_text(self, obj):
        return obj.text[:60] + '...' if len(obj.text) > 60 else obj.text
    get_short_text.short_description = 'Soru Metni'


@admin.register(QuestionBankItem)
class QuestionBankItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'question_type', 'points', 'created_at')
    list_filter = ('question_type', 'created_at')
    search_fields = ('title', 'text', 'creator__username')


@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'total_questions', 'is_graded', 'submitted_at')
    list_filter = ('is_graded', 'quiz__room__topic', 'submitted_at')
    search_fields = ('student__username', 'student__name', 'quiz__title')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'room', 'creator', 'deadline', 'created_at')
    list_filter = ('room__topic', 'deadline')
    search_fields = ('title', 'description', 'creator__username', 'room__name')


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'grade', 'submitted_at')
    list_filter = ('assignment__room__topic', 'submitted_at')
    search_fields = ('student__username', 'student__name', 'assignment__title')


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('room', 'created_at', 'is_active', 'require_ip_check', 'allow_qr_check')
    list_filter = ('is_active', 'require_ip_check', 'allow_qr_check', 'room__topic')
    search_fields = ('room__name', 'room__course_code')


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'status', 'client_ip', 'timestamp')
    list_filter = ('status', 'timestamp', 'session__room__topic')
    search_fields = ('student__username', 'student__name', 'session__room__name', 'client_ip')


