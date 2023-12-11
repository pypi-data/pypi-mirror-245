import io
from functools import wraps

from starlette.datastructures import QueryParams
from starlette.requests import Request

from spacestar.model import SpaceModel
from spacestar.component import init_element


def list_component_route(_model: type[SpaceModel] = None):

    def wrapper(model: type[SpaceModel]):
        @wraps(model)
        def wrapped():
            async def list_component_endpoint(request: Request):
                return request.app.response(request,
                                            model=model,
                                            instances=model.sorted_instances_list(query={**request.query_params}),
                                            template=f'component/list.html')
            return list_component_endpoint
        model._list_component_route = wrapped()
        return model
    if _model:
        return wrapper(_model)
    return wrapper
                # with io.StringIO() as f:
                #     container = init_element('div', f'#{model.item_name()}__list__container .card-box')
                #     container.children.append(init_element('h3', children=f'Lista de {model.plural()}'))
                #     group = init_element('ul', 'nav')
                #     for item in items:
                #         group.children.append(init_element('li', f'#{model.item_name()}__{item.key} .nav-item'))
                #     container.children.append(group)
                #     f.write(str(container))
                #     text = f.getvalue()