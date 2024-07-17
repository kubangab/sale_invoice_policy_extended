from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sale_invoice_policy_required = fields.Boolean(
        help="This makes Invoice Policy required on Sale Orders"
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            sale_invoice_policy_required=self.env["ir.config_parameter"].sudo().get_param(
                "sale_invoice_policy.sale_invoice_policy_required", False
            )
        )
        return res

    def set_values(self):
        super().set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "sale_invoice_policy.sale_invoice_policy_required",
            self.sale_invoice_policy_required
        )