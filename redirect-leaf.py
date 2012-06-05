import webapp2, json, os
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Redirection(db.Model):
    url = db.StringProperty(required=True)
    # should really create new entities for each access, but...
    access_count = db.IntegerProperty(required=True, default=0)
    date = db.DateTimeProperty(auto_now_add=True)

class RootResponse(webapp2.RequestHandler):
    def get(self):
        redirections = Redirection.all().order('-date').fetch(40)
        template_values = { 'redirections': redirections }
        path = os.path.join(os.path.dirname(__file__), 'interface.html')
        self.response.out.write(template.render(path, template_values))
    def post(self):
        data = json.loads(self.request.body)
        redirection = Redirection(url = data['url'])
        redirection.put()
        self.response.out.write(json.dumps({'id': str(redirection.key())}))

class DoRedirect(webapp2.RequestHandler):
    def get(self, redirection_key_str):
        # get the URL and increment counter
        redirection = db.get(redirection_key_str)
        redirection.access_count = redirection.access_count + 1
        redirection.put()
        # report, if a report is possible
        response_data = {'score': 1}
        i_data = self.request.get_all('i')
        try:
            response_data['i'] = i_data[0]
        except:
            pass
        data_urls = self.request.get_all('d')
        try:
            data_url = data_urls[0]
            urlfetch.fetch(url = data_url,
                           payload = json.dumps(response_data),
                           method = urlfetch.PUT)
        except:
            pass
        # and redirect
        self.redirect(redirection.url.encode('utf-8'), permanent=True)
        # hmm... note that this fails with a redirect loop for dumb values

app = webapp2.WSGIApplication([('/', RootResponse),
                               (r'/go/(.+)', DoRedirect)],
                              debug=True)
