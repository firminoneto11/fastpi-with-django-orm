from fastapi import FastAPI


def reverse_url[**P](
    app_name: str, controller_name: str, *_: P.args, **kwargs: P.kwargs
):
    from src.presentation.api.http.asgi import ASGIFactory

    for mount in ASGIFactory.latest_app().state.mounted_applications:
        if mount.name != app_name:
            continue

        if isinstance(mount.app, FastAPI):
            for route in mount.app.routes:
                if getattr(route, "name", None) == controller_name:
                    return mount.path + route.url_path_for(controller_name, **kwargs)

    raise ValueError(f"The {app_name!r} app wasn't mounted in the main application")
