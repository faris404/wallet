from django.urls import path

from .views import TransactionView,PersonTransactionView,TransactionStatusView


urlpatterns = [
   path('',TransactionView.as_view()),
   path('person/<int:person_id>',PersonTransactionView.as_view()),
   path('<int:tran_id>',TransactionStatusView.as_view())
]