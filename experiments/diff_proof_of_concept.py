def delete(item_id):
    item = db.get_item(item_id)
    db.complete_item(item_id)
    # Either:
    the_page2(get_sections())
    # Or:
    hypergen.dom.remove(signature=[item, item.id, item.version])
    # Or:
    hypergen.dom.remove(signature=hpg_item.signature(item))
    # Or:
    hypergen.dom.remove(signature=hpg_item)

def move_up(item_id)
    prev_item, item = db.move_up(item_id)
    hypergen.dom.switch(hpg_item.signature(prev_item), hpg_item.signature(item))

def move_up(item_id)
    next_item, item = db.move_down(item_id)
    hypergen.dom.switch(hpg_item.signature(next_item), hpg_item.signature(item))

def complete(item_id):
    item = db.complete_item(item_id)
    hpg_item(item)


def hpg_item(item):
    with li_cm(item.title, " - ", signature=[item, item.id, item.version]):
        span("Complete", onclick=(complete, item.id))
        span("Delete", onclick=(delete, item.id))
        span("Move up", onclick=(move_up, item.id))
        span("Move Down", onclick=(move_down, item.id))


# OR:


@li(text=lambda item: item.title,
    signature=lambda func, item: [func, item.id, item.version])
def hpg_item(item):
    span("Complete", onclick=(complete, item.id))
    span("Delete", onclick=(delete, item.id))
    span("Move up", onclick=(move_up, item.id))
    span("Move Down", onclick=(move_down, item.id))


# OR:
    
def hpg_item(item):
    with li_cm(item.title, " - ", signature=hpg_item.signature(item)):
        span("Complete", onclick=(complete, item.id))
        span("Delete", onclick=(delete, item.id))
        span("Move up", onclick=(move_up, item.id))
        span("Move Down", onclick=(move_down, item.id))
hpg_item.signature = lambda item: [hpg_item, item.id, item.version]

def the_page2(sections):
    for section in sections:
        with div_cm(
                class_="section",
                signature=[the_page2, section.id, section.version]):
            for sub_section in section:
                with ul_cm(signature[the_page2, sub_section.id,
                                     sub_section.version]):
                    for item in sub_section:
                        hpg_item(item)

                    div("Add new item", onclick=(add_item, subsection.id))


def the_page(sections):
    for section in sections:
        with skippable(), diffing(), caching(), hashing(
                section=section) as hashed, div_cm(class_="section"):
            p(hashed.section.title, height=hashed.section.height)


first_html, _ = hypergen(get_sections(), diffing=True, previous_html=None)

print first_html
{
    47109385: '<div class="section">Section1</p>',
    39582039: '<div class="section">Section2</p>',
    35203802: '<div class="section">Section3</p>',
}

# Fails if extends is called outside of a diffing context manager.
next_html, diff = hypergen(
    get_sections(), diffing=True, previous_html=first_html)

print next_html
{
    47109385: '<div class="section">Section1</p>',
    30948594: '<div class="section">Section4</p>',
    83592891: '<div class="section">Section5</p>',
}

print diff
(
    ('-', 39582039),
    ('-', 35203802),
    ('+', 30948594),
    ('+', 83592891), )
