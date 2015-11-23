from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, authenticate, login
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, FormView, RedirectView, TemplateView
from braces.views import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from tweets.models import Tweet
from django.http import HttpResponseRedirect

from .forms import UserCreateForm


class ScitweetsContextMixin(object):

    def get_context_data(self, **kwargs):
        context = dict()

        tasks = list()
        total_tweets = Tweet.objects.all().count()
        voted_tweets = percentage_tweets = 0
        if total_tweets:
            voted_tweets = Tweet.objects.all().answered_by_user(self.request.user.profile).count()
            if voted_tweets:
                percentage_tweets = voted_tweets * 100 / total_tweets

        tasks.append({
            'name': ugettext_lazy("Vote Tweets"),
            'percentage': percentage_tweets,
            'href': reverse("tweets:tweet_question_list")
        })
        context['tasks'] = tasks

        context.update(kwargs)

        print "Menu context: ", context

        return context


class DashboardView(LoginRequiredMixin, ScitweetsContextMixin, TemplateView):
    template_name = 'home.html'


class AccountRegistrationView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(self.get_success_url())
        return super(AccountRegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        valid = super(AccountRegistrationView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        if new_user:
            # Is the account active? It could have been disabled.
            if new_user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(self.request, new_user)
            else:
                # An inactive account was used - no logging in!
                # return HttpResponse("Your Rango account is disabled.")
                pass
        return valid


class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = reverse_lazy('dashboard')
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'accounts/login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.REQUEST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = reverse_lazy('accounts:login')

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


