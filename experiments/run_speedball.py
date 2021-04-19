from speedball import speedball

items = [
    {"is_completed": True, "description": "I am the Zohan!"},
    {"is_completed": False, "description": "Who are you!"},
    {"is_completed": True, "description": "I am nice!"},
    {"is_completed": False, "description": "Døne with this!"},]

hpg = speedball(items)
print("type hpg:", type(hpg))

html = hpg["html"]
print("type html:", type(html))
print("len:", len(html))
print()
print(html[:201])
