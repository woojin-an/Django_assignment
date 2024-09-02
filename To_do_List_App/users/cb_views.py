from django.contrib.auth import get_user_model, login
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from users.forms import SignupForm, LoginForm
from utils.email import send_email

User = get_user_model()


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('signup_done')

    def form_valid(self, form):
        user = form.save()
        # 이메일 발송
        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)

        url = f'{self.request.scheme}://{self.request.META["HTTP_HOST"]}/users/verify/?code={signer_dump}'

        subject = '[To Do List App] 이메일 인증을 완료해주세요!'
        message = f'다음 링크를 클릭해주세요. <a href="{url}"></a>'
        send_email(subject, message, from_email=None, to_email=user.email)

        return render(
            self.request,
            template_name='registration/signup_done.html',
            context={'user': user, }
        )


def verify_email(request):
    code = request.GET.get('code', '')

    signer = TimestampSigner()
    try:
        decoded_user_email = signing.loads(code)
        email = signer.unsign(decoded_user_email, max_age=60 * 30)
    except (TypeError, SignatureExpired):
        return render(request, 'registration/verify_failed.html')

    user = get_object_or_404(User, email=email, is_active=False)
    user.is_active = True
    user.save()
    return render(request, 'registration/verify_success.html', {'user': user})


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('cbv_todo_list')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user=user)

        next_page = self.request.GET.get('next')
        if next_page:
            return HttpResponseRedirect(next_page)

        return HttpResponseRedirect(self.get_success_url())
