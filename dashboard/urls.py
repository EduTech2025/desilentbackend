from django.urls import path
from dashboard.views.chat_message_view import SaveMessageView, MarkMessagesReadView

urlpatterns = [
    path('save-message/', SaveMessageView.as_view(), name='save_message'),
    path('mark-as-read/', MarkMessagesReadView.as_view(), name='mark_as_read'),
]
