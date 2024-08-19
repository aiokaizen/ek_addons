import json
import base64
import requests

from odoo import fields, models, api


class ProductTemplate(models.Model):

    _name = 'product.template'
    _inherit = 'product.template'

    COVER_SELECTION = [
        ('paper_cover', 'Papier'),
        ('hard_cover', 'Rigide'),
    ]

    is_book = fields.Boolean("Livre", default=False)
    barcode = fields.Char(
        'ISBN', copy=False, index='btree_not_null',
        help="International Standard Book Number"
    )
    google_books_volume_id = fields.Char("Google Books ID", copy=False, required=False)
    author_ids = fields.Many2many(
        'res.partner',
        string="Auteurs",
        domain="[('is_author', '=', True)]",
        relation='book_author_rel',  # The name of the relation table (optional)
        column1='book_id',  # Column name representing this model (optional)
        column2='author_id',  # Column name representing the related model (optional)
    )
    editor_id = fields.Many2one(
        'res.partner',
        string="Éditeur",
        domain="[('is_editor', '=', True)]",
        ondelete='restrict',  # corresponds to Django's PROTECT
        # ondelete='cascade',  # corresponds to Django's CASCADE
        required=False,
        help="Editor of the book",
    )
    page_count = fields.Integer("Nombre de pages", required=False)
    release_year = fields.Char( "Année de parution", required=False)
    cover = fields.Selection(
        COVER_SELECTION,
        string="Couverture",
        required=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        result = super().create(vals_list)
        if result.is_book:
            # Get book data by ISBN
            result.update_data_from_google_books()
        return result

    def update_data_from_google_books(self):
        """
            This method searches Google Books API for the cover picture and other
            information about the book using its ISBN and updates the book accordingly.
        """
        for book in self:

            isbn = book.barcode.split("_")[0]
            if not isbn:
                continue

            url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn

            response = requests.get(url)
            if response.status_code != 200:
                continue

            results = json.loads(response.content)
            book_data = results["items"][0]
            book_api_id = book_data["id"]

            book_data = book_data["volumeInfo"]

            authors_names = book_data.get("authors", [])
            publisher_name = book_data.get("publisher", "")
            release_year = book_data.get("publishedDate", "").split('-')[0]
            page_count = book_data.get("pageCount")

            # Get book cover
            image_links = book_data.get("imageLinks", {})
            image_link = image_links.get("thumbnail") or image_links.get(
                "smallThumbnail"
            )
            if image_link:
                image_response = requests.get(image_link)
                cover_picture = base64.b64encode(image_response.content).decode('utf-8')
                book.image_1920 = book.image_1920 or cover_picture

            # Handle Authors
            if not len(book.author_ids):
                author_ids = []
                for author_name in authors_names:
                    # Check if author already exists
                    author = self.env['res.partner'].search(
                        [('name', '=', author_name), ('is_author', '=', True)],
                        limit=1
                    )
                    if not author:
                        # If author doesn't exist, create one
                        author = self.env['res.partner'].create({
                            'name': author_name,
                            'is_company': False,
                            'is_author': True,
                        })
                    author_ids.append(author.id)
                # Update the authors for the book
                book.author_ids = [(6, 0, author_ids)]

            # Handle Publisher
            if publisher_name and not book.editor_id:
                # Check if the publisher already exists
                publisher = self.env['res.partner'].search(
                    [('name', '=', publisher_name), ('is_editor', '=', True)],
                    limit=1
                )
                if not publisher:
                    # If publisher doesn't exist, create one
                    publisher = self.env['res.partner'].create({
                        'name': publisher_name,
                        'is_company': True,
                        'is_editor': True,
                    })
                # Update the publisher for the book
                book.editor_id = publisher.id

            book.google_books_volume_id = book.google_books_volume_id or book_api_id
            book.release_year = book.release_year or release_year
            book.page_count = book.page_count or page_count


class BookProductProduct(models.Model):

    _name = 'product.product'
    _inherit = 'product.product'

    barcode = fields.Char(
        'ISBN', copy=False, index='btree_not_null',
        help="International Standard Book Number"
    )
