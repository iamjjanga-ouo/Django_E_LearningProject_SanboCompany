from django.urls import path
from e_learning import views

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    path('lectures/', views.LectureListView.as_view(), name='lecture-list'),
    path('lecture/<int:pk>', views.LectureDetailView.as_view(), name='lecture-detail'),
    path('professors/', views.ProfessorListView.as_view(), name='professor-list'),
    path('professor/<int:pk>', views.ProfessorDetailView.as_view(), name='professor-detail'),
]

urlpatterns += [
    path('streamings/', views.LectureInstanceStreamingListView.as_view(), name='streaming-list'),
    path('enrolledlectures/', views.LectureInstanceMyListView.as_view(), name='my-enroll'),
]

urlpatterns += [
    path('lecture/create/', views.LectureCreate.as_view(), name='lecture_create'),
    path('lecture/<int:pk>/update/', views.LectureUdpate.as_view(), name='lecture_update'),
    path('lecture/<int:pk>/delete/', views.LectureDelete.as_view(), name='lecture_delete'),
]

urlpatterns += [
    path('professor/create', views.ProfessorCreate.as_view(), name='professor_create'),
    path('professor/<int:pk>/update/', views.ProfessorUpdate.as_view(), name='professor_update'),
    path('professor/<int:pk>/delete/', views.ProfessorDelete.as_view(), name='professor_delete'),
]