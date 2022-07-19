# Server-side is back, baby!
\- take a break from Javascript, write your apps with liveviews instead 🚀

In this workshop, we explore *liveviews* as an alternative to “traditional” client-side rendering – a new way of building dynamic user interfaces for the web.

First, we give an introduction to liveviews using examples from established frameworks like [Phonix Liveview](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html) for Elixir and [StimulusReflex](https://docs.stimulusreflex.com/) for Ruby. We also touch on the emergent space of Django liveviews. Then, we showcase our interpretation of a Django liveview called [Hypergen](https://hypergen.it). Last, in the main part of the workshop, we build an example app in [Hypergen](https://github.com/runekaagaard/django-hypergen) while constrasting its architectural choices to other liveviews.

So are you looking for a break from Javascript, or if you’re just curious about what else is possible with Django, this talk is for you!

## Outline

1. About Liveviews
    - From PHP, over jQuery, then React to liveviews. The evolution of web development.
    - Liveview basics - the what, why, who, where and when.
    - Performance considerations.
    - Examples from liveviews such as [Phonix Liveview](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html), [StimulusReflex](https://docs.stimulusreflex.com/), [Unicorn](https://www.django-unicorn.com/), [django-htmx](https://github.com/adamchainz/django-htmx) and [Tetra](https://www.tetraframework.com/).
2. Hypergen
    - Introduction and examples.
    - Architecture and design choices.
    - Our experiences after building with it for two years.
3. We build an example app in Hypergen together, showcasing
    - Pure Python HTML templates
    - Base templates and template composition
    - Liveviews
    - Binding to DOM events
    - Actions
    - Partial DOM updates and other client commands
    - Forms
    - Tips and tricks
