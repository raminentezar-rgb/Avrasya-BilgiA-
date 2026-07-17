from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('delete-resource/<str:pk>/', views.deleteResource, name="delete-resource"),

    path('ajax/room/<str:pk>/messages/', views.roomMessagesAjax, name="ajax-room-messages"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

    path('room/<str:pk>/create-quiz/', views.create_quiz, name="create-quiz"),
    path('quiz/<str:pk>/', views.quiz_detail, name="quiz-detail"),
    path('delete-quiz/<str:pk>/', views.delete_quiz, name="delete-quiz"),
    path('delete-question/<str:pk>/', views.delete_question, name="delete-question"),
    path('create-quiz/', views.create_quiz_general, name="create-quiz-general"),
    path('quizzes/', views.quizzesPage, name="quizzes"),
    path('quiz/<str:pk>/export-results/', views.export_quiz_results, name="export-quiz-results"),
    path('message/<str:pk>/verify/', views.verify_message, name="verify-message"),
    path('resource/<str:pk>/save/', views.toggle_save_resource, name="toggle-save-resource"),
    path('my-saved-resources/', views.saved_resources, name="saved-resources"),
    path('room/<str:pk>/create-assignment/', views.create_assignment, name="create-assignment"),
    path('assignment/<str:pk>/submit/', views.submit_assignment, name="submit-assignment"),
    path('notification/<str:pk>/read/', views.read_notification, name="read-notification"),
    path('notifications/clear/', views.clear_all_notifications, name="clear-notifications"),
    path('quiz/<str:quiz_id>/add-from-bank/<str:bank_id>/', views.add_from_bank_to_quiz, name="add-from-question-bank"),
    path('question-bank/', views.question_bank_view, name="question-bank"),
    path('submission/quiz/<str:submission_id>/grade/', views.grade_quiz_submission, name="grade-quiz-submission"),
    path('submission/assignment/<str:submission_id>/grade/', views.grade_assignment_submission, name="grade-assignment-submission"),
    path('room/<str:pk>/gradebook/', views.room_gradebook, name="room-gradebook"),
    path('room/<str:pk>/gradebook/export/', views.export_room_gradebook, name="export-room-gradebook"),

    # Classroom Attendance System URLs
    path('attendance/room/<str:room_id>/start/', views.start_attendance_session, name="start-attendance-session"),
    path('attendance/projector/<str:session_id>/', views.projector_view, name="projector_view"),
    path('attendance/api/projector/<str:session_id>/token/', views.api_projector_token, name="api_projector_token"),
    path('attendance/api/projector/<str:session_id>/live/', views.api_projector_live, name="api_projector_live"),
    path('attendance/api/projector/<str:session_id>/toggle-ip/', views.toggle_ip_check, name="toggle_ip_check"),
    path('attendance/api/projector/<str:session_id>/toggle-qr/', views.toggle_qr_check, name="toggle_qr_check"),
    path('attendance/session/<str:session_id>/close/', views.close_attendance_session, name="close_attendance_session"),
    path('attendance/session/<str:session_id>/export/', views.export_attendance_report, name="export_attendance_report"),
    path('attendance/scan/', views.student_scan, name="student_scan"),
    path('attendance/check-ip/', views.student_ip_checkin, name="student_ip_checkin"),

    # Excel Bulk Student & Grade/Attendance Import/Export URLs
    path('student-template/download/', views.download_student_template, name="download-student-template"),
    path('bulk-import/students/<str:room_id>/', views.bulk_import_students, name="bulk-import-students-room"),
    path('bulk-import/students/', views.bulk_import_students, name="bulk-import-students-general"),
]

