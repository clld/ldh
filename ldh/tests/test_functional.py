def test_home(app):
    app.get_html('/legal', status=200)
