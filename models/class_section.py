from odoo import models, fields


class SectionClass(models.Model):
    _name = 'class.section'
    _description = 'Class Section'

    name = fields.Char(string='Section Name', required=True)