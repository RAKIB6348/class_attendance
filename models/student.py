from odoo import models, fields

class Student(models.Model):
    _name = 'class.student'
    _description = 'Class Student'
    _order = 'roll_number asc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    image = fields.Binary()
    name = fields.Char(required=True)
    roll_number = fields.Integer(required=True)
    class_id = fields.Many2one('class.class', required=True)
    # ... other fields ...

    _sql_constraints = [
        ('unique_roll_number_per_class', 'unique(roll_number, class_id)', 'Roll number must be unique per class!'),
    ]