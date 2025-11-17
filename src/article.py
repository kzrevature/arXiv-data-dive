class Article:
    # later consider: abs_link, pdf_link, cat, subcat
    def __init__(self, id_, title, created_at, updated_at):
        self.id = id_
        self.title = title
        self.created_at = created_at
        self.updated_at = updated_at
