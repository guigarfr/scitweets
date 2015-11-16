from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, TemplateView
from braces.views import LoginRequiredMixin
from tweets.models import Tweet


class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/home/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'login.html'

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
    url = '/users/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class MenuContextMixin(object):

    def get_context_data(self, **kwargs):
        context = dict()

        tasks = list()
        total_tweets = Tweet.objects.all().count()
        voted_tweets = Tweet.objects.all().answered_by_user(self.request.user.profile).count()
        tasks.append({
            'name': ugettext_lazy("Vote Tweets"),
            'percentage': voted_tweets * 100 / total_tweets,
            'href': reverse('tweets:vote')
        })
        context['tasks'] = tasks

        context.update(kwargs)

        print "Menu context: ", context

        return super(MenuContextMixin, self).get_context_data(**context)



