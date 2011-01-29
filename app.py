from datetime import datetime

from google.appengine.api import urlfetch
from google.appengine.api.labs.taskqueue import Task

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class DelayedJob(webapp.RequestHandler):
    def get(self):
        params = { 'url': self.request.get('url') }
        at = self.request.get('at')
        if at:
            params['at'] = datetime.utcfromtimestamp(float(at))
        Task(params=params).add()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('ok')

class JobRunner(webapp.RequestHandler):
    def post(self):
        urlfetch.fetch(url=self.request.get('url'), method=urlfetch.POST)

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/delay', DelayedJob),
        ('/_ah/queue/default', JobRunner)
    ]))

if __name__ == '__main__':
    main()