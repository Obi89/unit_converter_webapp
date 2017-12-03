#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("main.html")


class Ergebnis(BaseHandler):
    def get(self):
        return self.render_template("result.html")

    def post(self):
        num = float(self.request.get("num"))
        unit = self.request.get("unit")
        result = None
        if unit == "km/miles":
            result = str(num) + " km are " + str(num * 0.621371) + " miles"
        elif unit == "miles/km":
            result = str(num) + " miles are " + str(num * 1.60934) + " km"
        elif unit == "km/seemile":
            result = str(num) + " km are " + str(num * 0.539957) + " seemiles"
        elif unit == "km/yard":
            result = str(num) + " km are " + str(num * 1093.61) + " yards"
        params = {"result": result}
        return self.render_template("result.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/result', Ergebnis),
], debug=True)
