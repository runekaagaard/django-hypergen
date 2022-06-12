wrap context middleware:
    @liveview or @action decorator:
        handle perms
        init autourls
        wrap plugins.context():
            if liveview: maybe partial
            hypergen(template)
                    plugins.template_before()
                    run maybe_base_template() and template()
                    plugins.template_after()
                return html, commands
