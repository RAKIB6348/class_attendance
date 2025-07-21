from odoo import models, fields

class ClassClass(models.Model):
    _name = 'class.class'
    _description = 'Class'

    name = fields.Char(string='Class Name', required=True)
   
