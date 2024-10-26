ProductTemplate = env["product.template"]

products = ProductTemplate.search([])

for product in products:
    if product.author:
        author_record = env["librarian.author"].search(
            [("name", "=", product.author)], limit=1
        )
        if not author_record:
            author_record = env["librarian.author"].create({"name": product.author})
        product.author_ids = [(4, author_record.id)]
    if product.editor:
        editor_record = env["librarian.editor"].search(
            [("name", "=", product.editor)], limit=1
        )
        if not editor_record:
            editor_record = env["librarian.editor"].create({"name": product.editor})
        product.editor_id = editor_record.id

env.cr.commit()
