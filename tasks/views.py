from django.shortcuts import render, HttpResponseRedirect
from .forms import reg_add
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from .forms import PasswordResetRequestForm
from django.db.models import Q, F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from tasks.models import Task, Photo 
from .forms import TaskForm, PhotoForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .serializers import TaskSerializer
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView





#registration
def reg_form(request):
    if request.method == "POST":
        frm = reg_add(request.POST)
        if frm.is_valid():
            frm.save()
    else:
        frm = reg_add
    return render(request, 'register.html', {'form' : frm})


#login
def login_form(request):
    if request.method == "POST":
        frm = AuthenticationForm(request=request, data=request.POST)
        if frm.is_valid():
            usern = frm.cleaned_data['username']
            userp = frm.cleaned_data['password']
            user = authenticate(username = usern, password = userp)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/tasklist')
    else:
        frm = AuthenticationForm()
    return render(request, 'login.html', {'form' : frm})
    


#login success
def login_success(request):
    return render(request, 'success.html')



#logout
def logout_form(request):
    logout(request)
    return HttpResponseRedirect('/login')



#change password
def change_pass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            frm = PasswordChangeForm(user=request.user, data=request.POST)
            if frm.is_valid():
                frm.save()
                update_session_auth_hash(request, frm.user)
                return HttpResponseRedirect('/success')
        else:
            frm = PasswordChangeForm(user = request.user)
        return render(request, 'changepass.html', {'form':frm})
    else:
        return HttpResponseRedirect('/login')



#reset password
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            # Check if the input corresponds to a valid user by username or email
            username_or_email = form.cleaned_data.get("username_or_email")
            User = get_user_model()
            try:
                user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
            except User.DoesNotExist:
                user = None

            if user:
                # Generate and send a password reset email
                PasswordResetForm(user=user).save(request=request)
                # Redirect to a success page or display a message
            else:
                # No user found with the provided input, display an error message
                form.add_error('username_or_email', 'No user found with this username or email.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'reset.html', {'form': form})



#task list
class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['priorities'] = ['Low', 'Medium', 'High']
        return context

    def get_queryset(self):
        queryset = Task.objects.all().order_by(F('priority').desc())
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
            )

        creation_date = self.request.GET.get('creation_date')
        if creation_date:
            queryset = queryset.filter(
                creation_date__date=creation_date
            )

        due_date = self.request.GET.get('due_date')
        if due_date:
            queryset = queryset.filter(
                due_date__date=due_date
            )

        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(
                priority=priority
            )

        is_complete = self.request.GET.get('is_complete')
        if is_complete == '1':
            queryset = queryset.filter(is_complete=True)
        elif is_complete == '0':
            queryset = queryset.filter(is_complete=False)

        return queryset



#create new task
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



#view task details
class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'



#task update
class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')



#delete task
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task_list')



#photo add
class AddPhotoToTaskView(CreateView):
    model = Task  # Model associated with the view
    form_class = PhotoForm  # Form for uploading photos
    template_name = 'add_photo_to_task.html'  # Template to render

    def form_valid(self, form):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        photo = form.save(commit=False)
        photo.task = task
        photo.save()
        messages.success(self.request, 'Photo added successfully.')
        return redirect('task_detail', pk=task.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=self.kwargs['pk'])
        return context



#photo delete
class DeletePhotoView(DeleteView):
    model = Photo  # Model associated with the view
    template_name = 'photo_confirm_delete.html'  # Template for confirmation

    def get_success_url(self):
        task_pk = self.object.task.pk
        messages.success(self.request, 'Photo deleted successfully.')
        return reverse_lazy('task_detail', kwargs={'pk': task_pk})
    



#rest api view
class TaskApi_list_create(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class TaskApi_retrieve_update_destroy(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
