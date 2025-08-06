from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    vendor_id = fields.Many2one(
        'res.partner',
        string="Vendor",
        domain="[('supplier_rank', '>', 0)]",
        help="Select default vendor for this customer."
    )
