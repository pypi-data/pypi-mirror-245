from __future__ import annotations

from functools import partial

from hx_markup import Element, functions
from markupsafe import Markup


def init_element(tag, /, *args, **kwargs) -> Element:
    booleans = [*args]
    children = kwargs.pop('children', [])
    dataset = kwargs.pop('dataset', {})
    classlist = kwargs.pop('classlist', [])
    styles = kwargs.pop('styles', {})
    htmx = kwargs.pop('htmx', {})
    id = kwargs.pop('id', None)
    for item in booleans[:]:
        if item.startswith('#'):
            if not id:
                id = item[1:]
            booleans.remove(item)
        elif item.startswith('.'):
            classlist.append(item[1:])
            booleans.remove(item)
    return Element(tag, id, booleans, classlist, kwargs, htmx, dataset, styles, children)


h1 = partial(init_element, 'h1')
h2 = partial(init_element, 'h2')
h3 = partial(init_element, 'h3')
h4 = partial(init_element, 'h4')
h5 = partial(init_element, 'h5')
h6 = partial(init_element, 'h6')


def dropdown_login_form():
    text = """
    <div class="dropdown">
      <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false" data-bs-auto-close="outside">
        Login de Usuário
      </button>
      <form class="dropdown-menu p-4">
        <div class="mb-3">
          <label for="username" class="form-label">Usuário</label>
          <input type="email" class="form-control" id="username" placeholder="email do usuário">
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" class="form-control" id="password" placeholder="senha de usuário">
        </div>
        <button type="submit" class="btn btn-primary">login</button>
      </form>
    </div>
    """
    return Markup(text)

def nav_list(children, /, *args, **kwargs) -> Element:
    return init_element('ul', '.navbar-nav', *args, children=children, **kwargs)
    # classlist = functions.string_to_list(kwargs.pop('classlist', []))
    # classlist.append('navbar-nav')
    # content = kwargs.pop('content', [])
    # styles = kwargs.pop('styles', dict())
    # htmx = kwargs.pop('htmx', dict())
    # id = kwargs.pop('id', None)
    # return Element('ul', classlist=classlist, content=content, keywords=kwargs, htmx=htmx, styles=styles, id=id, booleans=[*args])

def nav_item(children: str, *args, **kwargs) -> Element:
    return init_element('li', '.nav-item', *args, children=children, **kwargs)


def nav_link(children: str, href: str, *args, **kwargs) -> Element:
    return init_element('a', '.nav-link', *args, href=href, children=children, **kwargs)
