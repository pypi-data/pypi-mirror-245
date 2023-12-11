from __future__ import annotations

import io

from ormspace import model as md
from hx_markup import functions
from spacestar.component import init_element, Element


@md.modelmap
class SpaceModel(md.Model):
    
    @classmethod
    def htmx(cls, **kwargs):
        return functions.join_htmx_attrs(**kwargs)
    
    async def display(self):
        with io.StringIO() as f:
            container: Element = init_element('div', id=self.table_key)
            container.children.append(init_element('h3', children=str(self)))
            container.children.append(init_element('ul', '.nav', children=[init_element('li','.nav-item', children=f'{k}: {v}') for k, v in dict(self).items()]))
            f.write(str(container))
            return f.getvalue()
        
    async def heading(self, tag: str, *args, **kwargs):
        with io.StringIO() as f:
            kwargs['children'] = str(self)
            f.write(str(init_element(tag, *args, **kwargs)))
            return f.getvalue()
        

        
    
    
