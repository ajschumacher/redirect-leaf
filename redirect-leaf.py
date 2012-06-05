import webapp2, json, os
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template

class RootResponse(webapp2.RequestHandler):
    def get(self):
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
        path = os.path.join(os.path.dirname(__file__), 'leaf.html')
        self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([('/', RootResponse)],
                              debug=True)
