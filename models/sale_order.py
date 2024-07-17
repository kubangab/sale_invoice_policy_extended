from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_policy = fields.Selection(
        [("order", "Ordered quantities"), ("delivery", "Delivered quantities")],
        readonly=True,
        help="Ordered Quantity: Invoice based on the quantity the customer "
        "ordered.\n"
        "Delivered Quantity: Invoiced based on the quantity the vendor "
        "delivered (time or deliveries).",
    )
    
    invoice_policy_required = fields.Boolean(
        compute="_compute_invoice_policy_required",
        default=lambda self: self.env["ir.config_parameter"].sudo().get_param(
            "sale_invoice_policy.sale_invoice_policy_required", False
     )
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if "invoice_policy" not in res and self.partner_id:
            res["invoice_policy"] = self.partner_id.default_invoice_policy or self.env["res.config.settings"].sudo().default_get(["default_invoice_policy"]).get("default_invoice_policy", "order")
        return res

    @api.onchange('partner_id')
    def _onchange_partner_invoice_policy(self):
        if self.partner_id and self.partner_id.default_invoice_policy:
            self.invoice_policy = self.partner_id.default_invoice_policy

    @api.depends("partner_id")
    def _compute_invoice_policy_required(self):
        invoice_policy_required = (
            self.env["res.config.settings"]
            .sudo()
            .default_get(["sale_invoice_policy_required"])
            .get("sale_invoice_policy_required", False)
        )
        for sale in self:
            sale.invoice_policy_required = invoice_policy_required