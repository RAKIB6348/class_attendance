from odoo import models, fields, api

class Student(models.Model):
    _name = 'class.student'
    _description = 'Class Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'roll_number asc'

    image = fields.Binary(
        string='Image',
        help='Upload a photo of the student for identification.',
        tracking=True,
    )
    name = fields.Char(
        string='Name',
        required=True,
        help='Enter the full name of the student.',
        tracking=True,
    )
    roll_number = fields.Integer(
        string='Roll Number',
        required=True,
        help='Enter the student\'s roll number.',
        tracking=True,
    )
    present = fields.Boolean(
        string='Present',
        default=False,
        help='Mark this checkbox if the student is present.',
        tracking=True,
    )
    absent = fields.Boolean(
        string='Absent',
        default=False,
        help='Mark this checkbox if the student is absent.',
        tracking=True,
    )
    remarks = fields.Text(
        string='Remarks',
        help='Additional comments or notes about the student\'s attendance.',
        tracking=True,
    )
    attendance_id = fields.Many2one(
        comodel_name='attendance.class',
        string='Attendance',
        help='Select the attendance record for this student.',
        tracking=True,
    )

    class_id = fields.Many2one(
        'class.class',
        string='Class',
        ondelete="cascade",
    )


    _sql_constraints = [
        ('unique_roll_number', 'unique(roll_number)', 'Roll number must be unique!'),
    ]
