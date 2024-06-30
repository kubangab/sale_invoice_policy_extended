from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_default_invoice_policy(self):
        # Get from sales setting
        sale_config = self.env['res.config.settings'].sudo().search([], order='id desc', limit=1)
        default_policy = sale_config.default_invoice_policy if hasattr(sale_config, 'default_invoice_policy') else 'order'
        
        return default_policy

    default_invoice_policy = fields.Selection([
        ('order', 'Ordered quantities'),
        ('delivery', 'Delivered quantities')],
        string=_('Default Invoicing Policy'),
        default=_get_default_invoice_policy,
        help=_("This will be the default invoicing policy for this partner when creating new sales orders."))

    @api.depends('is_company', 'parent_id')
    def _compute_company_type(self):
        super()._compute_company_type()
        for partner in self:
            if not partner.is_company and partner.default_invoice_policy:
                partner.default_invoice_policy = False
