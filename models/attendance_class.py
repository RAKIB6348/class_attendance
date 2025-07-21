from odoo import models, fields, api

class AttendanceClass(models.Model):
    _name = 'attendance.class'
    _description = 'Class Attendance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'teacher_id'

    teacher_id = fields.Many2one(
        'hr.employee',
        string='Teacher',
        required=True,
        ondelete='cascade',
        tracking=True,
        help='Select the teacher taking the class.'
    )
    date = fields.Date(
        string='Date',
        default=fields.Date.context_today,
        tracking=True,
        help='Date when the class is scheduled.'
    )
    section_id = fields.Many2one(
        'class.section',
        string='Section',
        required=False,
        ondelete='cascade',
        tracking=True,
        help='Section under which this class falls.'
    )
    subject_id = fields.Many2one(
        'attendance.subject',
        string='Subject',
        required=True,
        ondelete='cascade',
        tracking=True,
        help='Subject being taught in the class.'
    )
    subject_code = fields.Char(
        related='subject_id.code',
        string='Subject Code',
        store=True,
        readonly=True,
        help='Code of the selected subject.'
    )
    start_time = fields.Float(
        string='Start Time',
        tracking=True,
        help='Class start time in float format (e.g., 9.5 for 9:30 AM).'
    )
    end_time = fields.Float(
        string='End Time',
        tracking=True,
        help='Class end time in float format (e.g., 11 for 11:00 AM, 11.5 for 11:30 AM).'
    )
    class_id = fields.Many2one(
        'class.class',
        string='Class',
        required=True,
        ondelete='cascade',
        tracking=True,
        help='Select the class for which attendance is being taken.'
    )

    attendance_line_ids = fields.One2many('attendance.student.line', 'attendance_id', string='Attendance Lines')
    # ... other fields ...

    @api.onchange('class_id')
    def _onchange_fetch_students(self):
        if self.class_id:
            students = self.env['class.student'].search([('class_id', '=', self.class_id.id)])
            lines = []
            for student in students:
                lines.append((0, 0, {'student_id': student.id}))
            self.attendance_line_ids = lines


    total_students = fields.Integer(string='Total Students', compute='_compute_total_students', store=True)

    @api.depends('attendance_line_ids')
    def _compute_total_students(self):
        for rec in self:
            rec.total_students = len(rec.attendance_line_ids)