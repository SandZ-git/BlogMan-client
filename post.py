class Post:
    def __init__(self, post_id, title, subtitle, body, author_id, country_id, date, image=''):
        self.id = post_id
        self.title = title
        self.subtitle = subtitle
        self.body = body
        self.author_id = author_id
        self.country_id = country_id
        self.date = date
        self.image = image
