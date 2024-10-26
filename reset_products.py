books = env["product.product"].search(
    [
        ("is_book", "=", True),
    ]
)
quants = env["stock.quant"].search([("product_id", "in", books.ids)])
env["stock.picking"].search([("state", "=", "done")]).write({"state": "draft"})
env["stock.move.line"].search([("state", "=", "done")]).write({"state": "draft"})
env["stock.valuation.layer"].search([("product_id", "in", books.ids)]).unlink()
env["stock.move"].search([]).unlink()
quants.sudo().unlink()
books.sudo().unlink()
env.cr.commit()
