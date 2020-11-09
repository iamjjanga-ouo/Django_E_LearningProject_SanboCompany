import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

# Authentication
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import  LoginRequiredMixin, PermissionRequiredMixin

from e_learning.models import Lecture, Professor, LectureInstance, Language, Major, Assignment

@login_required
def index(request):
    num_lectures = Lecture.objects.all().count()
    num_lecture_instances = LectureInstance.objects.all().count()
    num_streamings = LectureInstance.objects.filter(status__exact='s').count()
    num_professors = Professor.objects.count()

    # session별 방문횟수
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_lectures' : num_lectures,
        'num_lecture_intance' : num_lecture_instances,
        'num_streamings' : num_streamings,
        'num_professors' : num_professors,
        'num_visits' : num_visits,
    }

    return render(request, 'index.html', context=context)

"""
Lecture View
"""
class LectureListView(LoginRequiredMixin, generic.ListView):
    model = Lecture
    paginate_by = 5

class LectureDetailView(LoginRequiredMixin, generic.DetailView):
    model = Lecture

"""
Professor View
"""
class ProfessorListView(LoginRequiredMixin, generic.ListView):
    model = Professor
    paginate_by = 5

class ProfessorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Professor

"""
Lecture instance View
"""
class LectureInstanceListView(LoginRequiredMixin, generic.ListView):
    model = LectureInstance
    template_name = 'e_learning/lectureinst_list.html'
    paginate_by = 10

    def get_queryset(self):
        return LectureInstance.objects.filter(status__exact='o').order_by('remain_time')

class LectureInstanceStreamingListView(LoginRequiredMixin, generic.ListView):
    model = LectureInstance
    template_name = 'e_learning/lectureinst_streaming_list.html'
    paginate_by = 10

    def get_queryset(self):
        return LectureInstance.objects.filter(status__exact='s').order_by('remain_time')

class LectureInstanceMyListView(LoginRequiredMixin, generic.ListView):
    model = LectureInstance
    template_name = 'e_learning/lectureinst_my_list.html'
    paginate_by = 10

    def get_queryset(self):
        return LectureInstance.objects.filter(enroll_student=self.request.user).filter(status__exact='o').order_by('remain_time')

"""
form
"""
from .forms import RenewLectureForm

@permission_required('e_learning.can_modified_remain_time')
def renew_lecture_staff(request, pk):
    lecture_instance = get_object_or_404(LectureInstance, pk=pk)

    if request.method == 'POST':
        form = RenewLectureForm(request.POST)

        if form.is_vaild():
            lecture_instance.due_date = form.cleaned_data['renewal_date']
            lecture_instance.save()

            ## return HttpResponseRedirect(reverse('all-borrowed')) 수정필요
    else: # GET request
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=2)
        form = RenewLectureForm(initial={'renewal_date': proposed_renewal_date})

        context = {
            'form' : form,
            'lecture_instance' : lecture_instance,
        }

        return render(request, 'catalog/lecture_renew_staff.html', context)

"""
Lecture Create / Update /Delete
"""
from .models import Lecture

class LectureCreate(PermissionRequiredMixin, CreateView):
    model = Lecture
    fields = '__all__'
    permission_required = 'e_learning.can_modified_remain_time'

class LectureUdpate(PermissionRequiredMixin, UpdateView):
    model = Lecture
    fields = '__all__'
    permission_required = 'e_learning.can_modified_remain_time'

class LectureDelete(PermissionRequiredMixin, DeleteView):
    model = Lecture
    success_url = reverse_lazy('lectures')
    permission_required = 'e_learning.can_modified_remain_time'

"""
Professor Create / Update / Delete
"""
from .models import Professor

class ProfessorCreate(PermissionRequiredMixin, CreateView):
    model = Professor
    fields = '__all__'
    initial = {'date_of_birth' : '01/01/2020',}
    permission_required = 'e_learning.can_modified_remain_time'

class ProfessorUpdate(PermissionRequiredMixin, UpdateView):
    model = Professor
    fields = ['fist_name', 'last_name', 'date_of_birth', 'major'] ## '__all__'은 안되나?
    permission_required = 'e_learning.can_modified_remain_time'

class ProfessorDelete(PermissionRequiredMixin, DeleteView):
    model = Professor
    success_url = reverse_lazy('professors')
    permission_required = 'e_learning.can_modified_remain_time'