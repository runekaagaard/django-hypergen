# yapf: disable

### Django query langugage ###

from dql import dql, load, meta, hash_query
from music.models import Album, Artist, Track

album_query = dql([
    Album.name, Album.year,
    {Album.artist: [Artist.name]},
    {Album.tracks: [Track.name]},
], cache=True, ttl=3600)

assert load(Album.objects.get(pk=1), album_query) == {
    Album.name: "Magical Mystery Tour",
    Album.artist: {Artist.name: "The Beatles"},
    Album.tracks: [
        {Track.name: "The Fool On The Hill"},
        {Track.name: "All You Need Is Love"},
    ]
}

assert load(Album.objects.filter(pk=1), album_query) == [{
    Album.name: "Magical Mystery Tour",
    Album.artist: {Artist.name: "The Beatles"},
    Album.tracks: [
        {Track.name: "The Fool On The Hill"},
        {Track.name: "All You Need Is Love"},
    ]
}]

assert hash_query(album_query) == "134f837d-3ef6-4ce1-b1a7-2ad8af231e01"

query_a = dql([MyModel.field_a])
query_b = dql([MyModel.field_b])
query_c = dql([MyModel.field_a, MyModel.field_b])

assert query_a + query_b == query_c
assert query_c - query_a == query_b
assert query_a[0] == MyModel.field_a
assert album_query[2][0] == Artist.name
