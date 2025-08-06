from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    related_vendor_bill_ids = fields.One2many(
        'account.move', 'invoice_origin_ref_id', string="Related Vendor Bills",
        domain=[('move_type', '=', 'in_invoice')]
    )

    invoice_origin_ref_id = fields.Many2one('account.move', string="Customer Invoice Reference")

    vendor_id = fields.Many2one(
        'res.partner',
        string="Vendor",
        domain="[('supplier_rank', '>', 0)]",
        help="Select the vendor from whom you want to buy the invoiced items."
    )

    def action_generate_vendor_bill(self):
        for invoice in self:
            if invoice.move_type != 'out_invoice' or invoice.state != 'posted':
                raise UserError(_("Vendor Bill can only be generated from a posted Customer Invoice."))

            # Use the vendor field directly from the invoice
            vendor = invoice.vendor_id
            if not vendor:
                raise UserError(_("Please select a vendor before generating the vendor bill."))

            company = invoice.company_id

            # Create the vendor bill using standard_price from products
            vendor_bill = self.env['account.move'].create({
                'move_type': 'in_invoice',
                'partner_id': vendor.id,
                'invoice_date': fields.Date.today(),
                'invoice_origin_ref_id': invoice.id,
                'company_id': company.id,
                'invoice_line_ids': [(0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'quantity': line.quantity,
                    'price_unit': line.product_id.standard_price,
                    'account_id': line.account_id.id or line.product_id.categ_id.property_account_expense_categ_id.id,
                }) for line in invoice.invoice_line_ids if line.product_id]
            })

            return {
                'name': _('Vendor Bill'),
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': vendor_bill.id,
            }

    def action_open_related_vendor_bills(self):
        self.ensure_one()
        tree_view_id = self.env.ref('nspl_create_vendor_bill_from_invoice.view_vendor_bill_list_custom').id
        form_view_id = self.env.ref('account.view_move_form').id  # or your custom form view

        return {
            'name': _('Vendor Bills'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'views': [
                (tree_view_id, 'list'),
                (form_view_id, 'form')
            ],
            'domain': [('id', 'in', self.related_vendor_bill_ids.ids)],
            'context': {'default_move_type': 'in_invoice'},
            'target': 'current',
        }


