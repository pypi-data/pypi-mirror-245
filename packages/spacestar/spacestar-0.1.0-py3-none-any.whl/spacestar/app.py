from __future__ import annotations

import os.path
from functools import partial, wraps
from typing import Any

import uvicorn
from starlette.applications import Starlette

from hx_markup import Element
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from spacestar import component as cp
from spacestar.middleware import session_middleware


def app_context(request: Request) -> dict[str, Any]:
    return {'app': request.app}
    
def add_staticfiles(_app: SpaceStar = None, *, path: str = '/static', directory: str = 'static'):
    def decorator(app):
        @wraps(app)
        def wrapper():
            app.routes.append(
                Mount(path, app=StaticFiles(directory=os.path.join(os.getcwd(), directory)), name='static'))
            return app
        return wrapper()
    
    if _app is None:
        return decorator
    else:
        return decorator(_app)

bootstrap_sript = Element('script', keywords=dict(
        src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js",
        integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL",
        crossorigin="anonymous"
))

bootstrap_link = Element('link', keywords=dict(
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
                    rel="stylesheet",
                    integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",
                    crossorigin="anonymous"
))

def page_head(title: str = None, content: list[Element | str] = None) -> Element:
    
    head = Element('head', content=[
            Element('meta', keywords=dict(charset='utf-8')),
            Element('meta', keywords=dict(content="width=device-width, initial-scale=1", name='viewport')),
            Element('title', content=title),
            bootstrap_link,
            bootstrap_sript
    ])
    
    if isinstance(content, list):
        head.children.extend(content)
    elif isinstance(content, str):
        head.children.append(content)
        
    return head
    

class SpaceStar(Starlette):
    """SpaceStar class is a mix of Starlette and Uvicorn for faster run of HTTP server configured for Deta Space.
    Parameters:
    module - A string with the module name running the application. Defaults to "main".
    app_name - A string with the SpaceStar instance name. Defaults to "app".
    lang - Language of the application. Defaults to "en".
    title - The title for home page. Defaults to "SpaceStar".
    static - A string indicating the location of static folder, relative to working directory.
    style_path - A string indicating the location of css file, relative to static folder.
    templates_directory - A string indicating the location of jinja2 templates_directory.
    debug - Boolean indicating if debug tracebacks should be returned on errors.
    routes - A list of routes to serve incoming HTTP and WebSocket requests.
    middleware - A list of middleware to run for every request. A starlette application will always automatically include two middleware classes. ServerErrorMiddleware is added as the very outermost middleware, to handle any uncaught errors occurring anywhere in the entire stack. ExceptionMiddleware is added as the very innermost middleware, to deal with handled exception cases occurring in the routing or endpoints.
    exception_handlers - A mapping of either integer status codes, or exception class types onto callables which handle the exceptions. Exception handler callables should be of the form handler(request, exc) -> response and may be either standard functions, or async functions.
    on_startup - A list of callables to run on application startup. Startup handler callables do not take any arguments, and may be either standard functions, or async functions.
    on_shutdown - A list of callables to run on application shutdown. Shutdown handler callables do not take any arguments, and may be either standard functions, or async functions.
    lifespan - A lifespan context function, which can be used to perform startup and shutdown tasks. This is a newer style_path that replaces the on_startup and on_shutdown handlers. Use one or the other, not both.
    """
    def __init__(self, **kwargs):
        middleware = kwargs.pop('middleware', [])
        middleware.insert(0, session_middleware)
        self.module = kwargs.pop('module', 'main')
        self.app_name = kwargs.pop('app_name', 'app')
        self.lang = kwargs.pop('lang', 'en')
        self.title = kwargs.pop('title', 'SpaceStar')
        self.static_directory = kwargs.pop('static_directory', None)
        if self.static_directory:
            self.static_path = kwargs.pop('static_path', '/static')
        else:
            self.static_path = None
        self.script_path = kwargs.pop('script_path', None)
        self.style_path = kwargs.pop('style_path', None)
        self.templates_directory = kwargs.pop('templates_directory', None)
        if self.templates_directory:
            self.templates = self._templates_engine()
            self.templates.env.globals['partial'] = partial
            self.templates.env.globals['elm'] = cp.init_element
            self.templates.env.globals['element'] = cp.init_element
            self.templates.env.globals['nav_list'] = cp.nav_list
            self.templates.env.globals['nav_item'] = cp.nav_item
            self.templates.env.globals['nav_link'] = cp.nav_link
            self.templates.env.globals['h1'] = cp.h1
            self.templates.env.globals['h2'] = cp.h2
            self.templates.env.globals['h3'] = cp.h3
            self.templates.env.globals['h4'] = cp.h4
            self.templates.env.globals['h5'] = cp.h5
            self.templates.env.globals['h6'] = cp.h6
        super().__init__(middleware=middleware, **kwargs)
        self.routes.insert(0, self._home_route())
        if self.static_path:
            self.routes.insert(1, Mount(self.static_path, app=StaticFiles(directory=os.path.join(os.getcwd(), self.static_directory)), name='static'))

    def _home_route(self):
        return Route('/', self.home_page, name='home')
    
    async def home_page(self, request: Request, title: str | None = None):
        return self.response(request, title=title or self.title)
    
    def _templates_engine(self):
        return Jinja2Templates(directory=os.path.join(os.getcwd(), self.templates_directory), context_processors=[app_context])
    
    def index_template(self):
        return self.templates.get_template('index.html')
    
    @staticmethod
    def element(tag, *args, **kwargs):
        return cp.init_element(tag, *args, **kwargs)
    
    def render(self, request, / , **kwargs):
        if template:= kwargs.pop('template', None):
            print(f'template is {template}')
            return self.templates.get_template(template).render(request=request, **kwargs)
        return self.index_template().render(request=request, **kwargs)
    
    def response(self, request: Request, /, **kwargs) -> HTMLResponse:
        return HTMLResponse(self.render(request, **kwargs))
    
    def run(self, *args, **kwargs):
        uvicorn.run(f'{self.module}:{self.app_name}', *args, **kwargs)
    
    def create_route(self, _endpoint=None, *, path: str = None, name: str = None, methods: list[str] = None):
        def decorator(endpoint):
            @wraps(endpoint)
            def wrapper():
                self.routes.append(Route(path=path, endpoint=endpoint, name=name, methods=methods or ['GET']))
                return self
            return wrapper()
            
        if _endpoint is None:
            return decorator
        else:
            return decorator(_endpoint)
            



if __name__ == '__main__':
    print(page_head('essencia', content=[
            Element('link', keywords=dict(rel='stylesheet', href="/static/css/style_path.css"))
    ]))