from speedball import speedball

items = [
    {"is_completed": True, "description": "I am the Zohan!", "pk": 1},
    {"is_completed": False, "description": "Who are you!", "pk": 2},
    {"is_completed": True, "description": "I am nice!", "pk": 3},
    {"is_completed": False, "description": "Døne with this!", "pk": 4},]

hpg = speedball(items)
print(("type hpg:", type(hpg)))

print(("type event_handler_callbacks:", type(hpg["event_handler_callbacks"])))
print(("event_handler_callbacks:", hpg["event_handler_callbacks"]))

html = hpg["html"]
print(("type html:", type(html)))
print(("len:", len(html)))
print()
print((html[:1001]))
