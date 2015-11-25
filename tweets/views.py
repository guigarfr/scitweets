# -*- coding: utf-8 -*-
# from django.contrib import messages
import json
from django.views.generic import CreateView, ListView, FormView
from braces.views import LoginRequiredMixin
from django.utils.translation import ugettext_lazy
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from django.contrib.contenttypes.models import ContentType

from . import models
from . import forms
from accounts.views import ScitweetsContextMixin


class TweetListView(LoginRequiredMixin, ListView, ScitweetsContextMixin):
    model = models.Tweet
    template_name = 'tweets/list.html'

    # TODO: Agrupar por question, y poner cada una en una caja? o poner columna question


class TrendingTopicListView(LoginRequiredMixin, ListView, ScitweetsContextMixin):
    model = models.TrendingTopic
    template_name = 'tweets/list_trendingtopic.html'

    # TODO: Agrupar por question, y poner cada una en una caja? o poner columna question


class TweetAnswerListView(LoginRequiredMixin, ScitweetsContextMixin, ListView):
    model = models.Answer
    template_name = 'tweets/answer_list.html'

    def get_queryset(self):
        tweet_type = ContentType.objects.get_for_model(models.Tweet)
        return self.model.objects.filter(content_type=tweet_type, user=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = {
            'tweet': True
        }
        context.update(kwargs)
        return super(TweetAnswerListView, self).get_context_data(**context)


class TrendingTopicAnswerListView(LoginRequiredMixin, ScitweetsContextMixin, ListView):
    model = models.Answer
    template_name = 'tweets/answer_list.html'

    def get_queryset(self):
        trendingtopic_type = ContentType.objects.get_for_model(models.TrendingTopic)
        return self.model.objects.filter(content_type=trendingtopic_type, user=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = {
            'trendingtopic': True
        }
        context.update(kwargs)
        return super(TrendingTopicAnswerListView, self).get_context_data(**context)



class QuestionListView(ListView):
    model = models.Question
    template_name = 'tweets/question-list.html'


class CreateAnswerView(LoginRequiredMixin, ScitweetsContextMixin, CreateView):
    model = models.Answer
    template_name = 'tweets/vote.html'
    form_class = forms.CreateAnswerForm
    redirect_unauthenticated_users = True
    question = None
    about_object = None
    about_object_class = None
    object = None

    def dispatch(self, request, *args, **kwargs):
        # Get question to answer to
        question_id = self.kwargs.get("question_id")
        try:
            self.question = models.Question.objects.get(id=question_id)
        except:
            raise ValueError("There is no question with id " + str(question_id))

        # Get first unanswered tweet or trendingtopic
        self.about_object_class = self.question.content_type.model_class()
        self.about_object = self.about_object_class.objects.exclude(answers__user=request.user.profile).first()

        return super(CreateAnswerView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initials = dict()
        if self.about_object:
            initials.update({
                "object_id": self.about_object.pk,
                "question": self.question,
            })

            initials.update(super(CreateAnswerView, self).get_initial())

        return initials

    def get_success_url(self):
        return reverse('tweets:tweet_answer_new', kwargs={
            'question_id': self.question.pk
        })

    def form_valid(self, form):
        tweet_answer = form.save(commit=False)
        tweet_answer.user = self.request.user.profile
        # tweet_answer.question = self.question
        # tweet_answer.object_id = self.about_object.pk
        tweet_answer.value_type = self.question.answer_value_type
        tweet_answer.content_type = self.question.content_type
        tweet_answer.save()
        return redirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context = super(CreateAnswerView, self).get_context_data(*args, **kwargs)
        context['question'] = self.question
        context['object'] = self.about_object
        context['unanswered_count'] = self.about_object_class.objects.exclude(
            answers__user=self.request.user.profile).count()
        context['answered_count'] = self.about_object_class.objects.filter(
            answers__user=self.request.user.profile).count()
        assert(self.about_object_class.objects.all().count() ==
               (context['unanswered_count'] + context['answered_count']))
        return context


class TweetImportFormView(FormView, LoginRequiredMixin):
    template_name = 'tweets/import_tweets.html'
    form_class = forms.UploadFileForm

    def get_success_url(self):
        return reverse('tweets:tweet_list')

    def parse_json_text(self, text):
        try:
            return json.loads(text)
        except ValueError as e:
            print('invalid json: %s' % e)
            return None # or: raise

    def parse_json_file(self, json_file):
        raw_data = json_file.read()

        # Check if file is a correct json
        json_data = self.parse_json_text(raw_data)

        # File might be json data for each row
        if not json_data:
            raw_data = raw_data.split('\n')

            json_data = list()
            for row_data in raw_data:
                if row_data:
                    parsed_row_data = self.parse_json_text(row_data)
                    if not parsed_row_data:
                        return None
                    json_data.append(parsed_row_data)

        return json_data

    def parse_tweet_data_from_json_data_array(self, json_data_array):

        tweet_imported = tweet_found = tweet_failure_format = tweet_failure_other = 0
        for json_tweet in json_data_array:
            tweet_text = json_tweet.get('text', None)
            tweet_id = json_tweet.get('id', None)

            # Check for needed fields
            if tweet_text is None or tweet_id is None:
                tweet_failure_format += 1
                continue

            # Check for existing tweet or create new one
            try:
                _ = models.Tweet.objects.get(id_twitter=int(json_tweet['id']))
                tweet_found += 1
            except models.Tweet.DoesNotExist:
                try:
                    new_tweet = models.Tweet(id_twitter=int(tweet_id), text=unicode(tweet_text))
                    new_tweet.save()
                    tweet_imported += 1
                except:
                    tweet_failure_other += 1

        imported_tweets = {
            'imported': tweet_imported,
            'existing': tweet_found,
            'failure_format': tweet_failure_format,
            'failure_other': tweet_failure_other
        }

        failure_text = u''
        if tweet_imported:
            if not tweet_found:
                success_text = u"%(imported)d tweets were imported from file" % imported_tweets
            else:
                success_text = u'%(imported)d tweets were imported from file and ' \
                               u'%(existing)d already existed in the database' % imported_tweets
            messages.success(self.request, ugettext_lazy(success_text))
        else:
            warning_text = u'No new tweets were created.'

        if tweet_failure_format:
            failure_text = u'There were %(failure_format)d tweets with format errors' % imported_tweets
        if tweet_failure_other:
            failure_text += u' and %(failure_other)s led to unexpected errors' % imported_tweets

        if failure_text:
            messages.error(self.request, ugettext_lazy(failure_text))
        elif warning_text:
            messages.warning(self.request, ugettext_lazy(warning_text))

        return tweet_imported

    def form_valid(self, form):

        form_file = form.cleaned_data.get('file', None)

        if form_file is None:
            messages.error(self.request, ugettext_lazy("File field is required"))

        json_data = self.parse_json_file(form_file)

        if json_data is None:
            failure_text = ugettext_lazy(u'There was no data we could process in this file')
            messages.error(self.request, failure_text)
            return super(TweetImportFormView, self).form_invalid(form)

        imported_tweets = self.parse_tweet_data_from_json_data_array(json_data)

        if not imported_tweets:
            return super(TweetImportFormView, self).form_invalid(form)

        return super(TweetImportFormView, self).form_valid(form)


# def distribuidores_csv_process(request):
#     """Lista todos los activos del cliente"""
#
#     log.info('distribuidores_csv_process')
#
#     result = {
#         'res': 'ok',
#         'error': [],
#         'ok': []
#     }
#     if not request.is_ajax():
#         # Si no es ajax se devuelve el contenido normal para el template
#         return HttpResponse(json.dumps(result))
#     else:
#         if request.FILES and 'file' in request.FILES:
#             file = request.FILES['file']
#             mime = magic.from_buffer(file.read(), mime=True)
#             if mime != 'text/csv' and mime != 'text/plain':
#                 result['res'] = 'error'
#                 result['error'] = 'Tipo de fichero incorrecto'
#                 return HttpResponseBadRequest(json.dumps(result))
#
#             file.seek(0)
#             # data = [row for row in csv.reader(file.read().splitlines(), delimiter=';')]
#             data = [row for row in csv.reader(file.read().splitlines(), delimiter=',')]
#
#             file.seek(0)
#             m = magic.Magic(mime_encoding=True)
#             blob = file.read()
#             encoding = m.from_buffer(blob)
#
#             rownum = 0
#
#             for row in data:
#                 if rownum >= 0 and row and len(row) > 0:
#
#                     # Verifica que la fila no esté vacía
#                     valid_row = False
#                     for col in row:
#                         if col:
#                             valid_row = True
#                             break
#
#                     if valid_row:
#
#                         log.info("Row = " + str(row))
#                         log.info("Cols in row = " + str(len(row)))
#
#                         asset = {
#                             'nombre': '',
#                             'contacto': '',
#                             'direccion': '',
#                             'telefono': '',
#                             'email': '',
#                             'cif_nif': '',
#                             'pais': '',
#                             'territorio': ''
#                         }
#                         # Ponemos que el pais tambien apunte al campo del csv con el code2 de territorio
#                         pais_str = row[8].decode(encoding)
#                         pais = get_possible_country_code_from_string(pais_str)
#
#                         try:
#                             asset['nombre'] = row[0].decode(encoding)
#                             asset['contacto'] = row[1].decode(encoding)
#                             asset['direccion'] = row[2].decode(encoding)
#                             asset['telefono'] = row[3].decode(encoding)
#                             asset['email'] = row[4].decode(encoding)
#                             asset['cif_nif'] = row[5].decode(encoding)
#                             asset['pais'] = pais.code2 if pais else ''
#                             asset['territorio'] = row[8].decode(encoding)
#
#                             result['ok'].append(asset)
#                         except:
#                             result['error'].append(','.join(row))
#                 rownum += 1
#
#             return HttpResponse(json.dumps(result))
#
#
# def distribuidores_csv_save(request):
#     if request.method == 'POST':
#
#         assets = request.POST.get('assets_to_save')
#
#         cliente = request.user.groups.all().first()
#
#         assets = json.loads(assets)
#         guardados = 0
#         for asset in assets:
#
#             # TODO Hace falta guardar territorio y pais
#
#             country = None
#             if asset['pais']:
#                 country = get_possible_country_code_from_string(asset['pais'])
#                 if not country:
#                     # request.messages.error("Couldn't find country '" +
#                     #                        str(asset['pais']) +
#                     #                        " for distributor " + asset['nombre'])
#                     print "Couldnt find country", asset['pais']
#                     pass
#
#             territorio = None
#             if asset['territorio']:
#                 country = get_possible_country_code_from_string(asset['territorio'])
#                 if country:
#                     territorio, created = models.ZonasDistribuidor.objects.get_or_create(nombre=country.name,
#                                                                                          cliente=cliente)
#                     if created:
#                         territorio.save()
#
#                     territorio.paises.add(country)
#
#             # Miramos si no existe un distribuidor con el mismo nombre para ese cliente en BD, para no duplicados
#             # instances = models.Distribuidor.objects.filter(nombre=asset['nombre'], cliente=cliente).count()
#             # if instances == 0:
#             instance = models.Distribuidor(nombre=asset['nombre'],
#                                            direccion=asset['direccion'],
#                                            telefono=asset['telefono'],
#                                            cif_nif=asset['cif_nif'],
#                                            email=asset['email'],
#                                            pais=country,
#                                            cliente=cliente,
#                                            territorio=territorio,
#                                            )
#             try:
#                 instance.save()
#                 if instance.pk:
#                     guardados += 1
#             except Exception as e:
#                 print("Couldn't save distributor " + asset['nombre'])
#                 print e
#                 print "#################################################################"
#                 # pass
#             # else:
#             #     print("Duplicado distributor-> " + asset['nombre'])
#
#         # messages.success(request, u'Se han cargado correctamente %s activos.' % guardados)
#         # return redirect('frontal.views.assets_list')
#         return redirect(reverse('affiliates_partners:distributor-list'))
#
#     else:
#         print 'ONLY POST ALLOWED!!'

