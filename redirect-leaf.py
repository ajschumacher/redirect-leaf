import webapp2, json, os
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext import db

# going to need a model up here...

class RootResponse(webapp2.RequestHandler):
    def get(self):
        # all this needs to be moved/redone!
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
            template_values = { 'data_url': data_url }
        except:
            template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'interface.html')
        self.response.out.write(template.render(path, template_values))
    def post(self):
        # make new redirect objects via a json interface here
        self.response.out.write('POST!')

class DoRedirect(webapp2.RequestHandler):
    def get(self, redirect_key):
        # get redirect location
        # send report request to d if it exists
        # redirect (not to this, but...)
        self.redirect(redirect_key, permanent=True)
        # hmm... note that this fails with a redirect loop for dumb values

app = webapp2.WSGIApplication([('/', RootResponse),
                               (r'/go/(.+)', DoRedirect)],
                              debug=True)
