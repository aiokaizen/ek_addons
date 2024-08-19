# -*- coding: utf-8 -*-
################################################################################
#
#    EKBlocks
#
#    Copyright (C) 2024-TODAY EKBlocks(<https://www.ekblocks.com>).
#    Author: EKBlocks (Contact : insightsphere@ekblocks.com)
#
#    This program is under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
#    Version 3 (AGPL v3)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the
#    Software or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
#    USE OR OTHER DEALINGS IN THE SOFTWARE.
#
################################################################################
{
    'name': 'Image Preview Widget',
    'version': '17.0.1.0.0',
    'category': 'Extra Tools',
    'summary': """Enables preview of the image""",
    'description': """This module enables to enlarge image while clicking on it
    to see the preview in the products,partners and etc.""",
    'author': 'EKBlocks',
    'company': 'EKBlocks',
    'maintainer': 'EKBlocks',
    'website': 'https://www.ekblocks.com',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': {
            'widget_preview_image/static/src/js/image_preview_widget.js',
            'widget_preview_image/static/src/xml/widget_image_preview.xml',
        }
    },
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False
}
