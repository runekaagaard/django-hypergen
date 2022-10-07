from hypergen.imports import *
from django.templatetags.static import static
from contextlib import contextmanager

@contextmanager
def lander_base_template():
    with html(lang="en-us", dir_="ltr"):
        with head():
            meta(charset="utf-8")
            title("The install worked successfully! Congratulations!")
            meta(name="viewport", content="width=device-width, initial-scale=1")
            link(href=static('djangolander/animations.css'))
            link(href=static("admin/css/fonts.css"))
        with body():
            with header():
                a("""
        django
    """, class_="logo", href="https://www.djangoproject.com/", target="_blank", rel="noopener")
                with p():
                    a("release notes", href="https://docs.djangoproject.com/en/4.1/releases/", target="_blank", rel="noopener")
            with main():
                with svg(class_="figure", viewbox="0 0 508 268", aria_hidden="true"):
                    path(class_="black-stroke fill-grey", d="M305.2 156.6c0 4.6-.5 9-1.6 13.2-2.5-4.4-5.6-8.4-9.2-12-4.6-4.6-10-8.4-16-11.2 2.8-11.2 4.5-22.9 5-34.6 1.8 1.4 3.5 2.9 5 4.5 10.5 10.3 16.8 24.5 16.8 40.1zm-75-10c-6 2.8-11.4 6.6-16 11.2-3.5 3.6-6.6 7.6-9.1 12-1-4.3-1.6-8.7-1.6-13.2 0-15.7 6.3-29.9 16.6-40.1 1.6-1.6 3.3-3.1 5.1-4.5.6 11.8 2.2 23.4 5 34.6z", fill="#2E3B39", fill_rule="nonzero")
                    path(class_="black-stroke", d="M282.981 152.6c16.125-48.1 6.375-104-29.25-142.6-35.625 38.5-45.25 94.5-29.25 142.6h58.5z", stroke="#FFF", stroke_width="3.396", fill="#6DDCBD")
                    path(class_="black-stroke", d="M271 29.7c-4.4-10.6-9.9-20.6-16.6-29.7-6.7 9-12.2 19-16.6 29.7H271z", stroke="#FFF", stroke_width="3", fill="#2E3B39")
                    circle(fill="#FFF", cx="254.3", cy="76.8", r="15.5")
                    circle(stroke="#FFF", stroke_width="7", fill="#6DDCBD", cx="254.3", cy="76.8", r="12.2")
                    path(class_="smoke", d="M507.812 234.24c0-2.16-.632-4.32-1.58-6.24-3.318-6.72-11.85-11.52-21.804-11.52-1.106 0-2.212.12-3.318.24-.474-11.52-12.956-20.76-28.282-20.76-3.318 0-6.636.48-9.638 1.32-4.74-6.72-14.062-11.28-24.806-11.28-.79 0-1.58 0-2.37.12-.79 0-1.58-.12-2.37-.12-10.744 0-20.066 4.56-24.806 11.28a35.326 35.326 0 00-9.638-1.32c-15.642 0-28.282 9.6-28.282 21.48 0 1.32.158 2.76.474 3.96a26.09 26.09 0 00-4.424-.36c-8.058 0-15.01 3.12-19.118 7.8-3.476-1.68-7.742-2.76-12.324-2.76-12.008 0-21.804 7.08-22.752 15.96h-.158c-9.322 0-17.38 4.32-20.856 10.44-4.108-3.6-10.27-6-17.222-6h-1.264c-6.794 0-12.956 2.28-17.222 6-3.476-6.12-11.534-10.44-20.856-10.44h-.158c-.948-9-10.744-15.96-22.752-15.96-4.582 0-8.69.96-12.324 2.76-4.108-4.68-11.06-7.8-19.118-7.8-1.422 0-3.002.12-4.424.36.316-1.32.474-2.64.474-3.96 0-11.88-12.64-21.48-28.282-21.48-3.318 0-6.636.48-9.638 1.32-4.74-6.72-14.062-11.28-24.806-11.28-.79 0-1.58 0-2.37.12-.79 0-1.58-.12-2.37-.12-10.744 0-20.066 4.56-24.806 11.28a35.326 35.326 0 00-9.638-1.32c-15.326 0-27.808 9.24-28.282 20.76-1.106-.12-2.212-.24-3.318-.24-9.954 0-18.486 4.8-21.804 11.52-.948 1.92-1.58 4.08-1.58 6.24 0 4.8 2.528 9.12 6.636 12.36-.79 1.44-1.264 3.12-1.264 4.8 0 7.2 7.742 13.08 17.222 13.08h462.15c9.48 0 17.222-5.88 17.222-13.08 0-1.68-.474-3.36-1.264-4.8 4.582-3.24 7.11-7.56 7.11-12.36z", fill="#E6E9EE")
                    path(fill="#6DDCBD", d="M239 152h30v8h-30z")
                    path(class_="exhaust__line", fill="#E6E9EE", d="M250 172h7v90h-7z")
                    path(class_="flame", d="M250.27 178.834l-5.32-8.93s-2.47-5.7 3.458-6.118h10.26s6.232.266 3.306 6.194l-5.244 8.93s-3.23 4.37-6.46 0v-.076z", fill="#AA2247")
                h1("The install worked successfully! Congratulations!")
                with p():
                    a("DEBUG=True", href="https://docs.djangoproject.com/en/4.1/ref/settings/#debug", target="_blank", rel="noopener")
            with footer():
                with a(class_="option", href="https://docs.djangoproject.com/en/4.1/", target="_blank", rel="noopener"):
                    with svg(viewbox="0 0 24 24", aria_hidden="true"):
                        path(d="M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7zm2.85 11.1l-.85.6V16h-4v-2.3l-.85-.6A4.997 4.997 0 017 9c0-2.76 2.24-5 5-5s5 2.24 5 5c0 1.63-.8 3.16-2.15 4.1z")
                    with p():
                        span("Django Documentation", class_="option__heading")
                        span(".", class_="sr-only")
                        br()
                with a(class_="option", href="https://docs.djangoproject.com/en/4.1/intro/tutorial01/", target="_blank", rel="noopener"):
                    with svg(viewbox="0 0 24 24", aria_hidden="true"):
                        path(d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z")
                    with p():
                        span("Tutorial: A Polling App", class_="option__heading")
                        span(".", class_="sr-only")
                        br()
                with a(class_="option", href="https://www.djangoproject.com/community/", target="_blank", rel="noopener"):
                    with svg(viewbox="0 0 24 24", aria_hidden="true"):
                        path(d="M16.5 13c-1.2 0-3.07.34-4.5 1-1.43-.67-3.3-1-4.5-1C5.33 13 1 14.08 1 16.25V19h22v-2.75c0-2.17-4.33-3.25-6.5-3.25zm-4 4.5h-10v-1.25c0-.54 2.56-1.75 5-1.75s5 1.21 5 1.75v1.25zm9 0H14v-1.25c0-.46-.2-.86-.52-1.22.88-.3 1.96-.53 3.02-.53 2.44 0 5 1.21 5 1.75v1.25zM7.5 12c1.93 0 3.5-1.57 3.5-3.5S9.43 5 7.5 5 4 6.57 4 8.5 5.57 12 7.5 12zm0-5.5c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm9 5.5c1.93 0 3.5-1.57 3.5-3.5S18.43 5 16.5 5 13 6.57 13 8.5s1.57 3.5 3.5 3.5zm0-5.5c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2z")
                    with p():
                        span("Django Community", class_="option__heading")
                        span(".", class_="sr-only")
                        br()
                        yield