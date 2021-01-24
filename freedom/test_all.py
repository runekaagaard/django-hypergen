from freedom.core import context


def test_context():
    def inc(ctx):
        ctx["i"] = ctx.get("i", 0) + 1
        return ctx

    with context(inc) as ctx:
        assert ctx["i"] == 1

        with context(inc, foo=9) as ctx2:
            assert ctx2["foo"] == 9
            assert ctx2["i"] == 2
            with context(bar=42) as ctx3:
                assert ctx3["i"] == 2
                assert ctx3["bar"] == 42
            assert ctx2["i"] == 2

        assert ctx["i"] == 1
        assert "foo" not in ctx
