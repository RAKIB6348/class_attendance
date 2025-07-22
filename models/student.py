from odoo import models, fields, api

class Student(models.Model):
    _name = 'class.student'
    _description = 'Class Student'
    _order = 'roll_number asc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    image = fields.Binary()
    name = fields.Char(required=True)
    roll_number = fields.Char()
    class_id = fields.Many2one('class.class', required=True)
    # ... other fields ...


    _sql_constraints = [
        ('unique_roll_number_per_class', 'unique(roll_number, class_id)', 'Roll number must be unique per class!'),
    ]


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
                vals['roll_number'] = self.env['ir.sequence'].next_by_code('class.attendance.roll')
        return super().create(vals_list)