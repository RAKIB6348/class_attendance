from odoo import models, fields


class AttendanceStudentLine(models.Model):
    _name = 'attendance.student.line'
    _description = 'Attendance Line'

    attendance_id = fields.Many2one('attendance.class')
    student_id = fields.Many2one('class.student', required=True)
    roll_number = fields.Integer(related='student_id.roll_number')
    present = fields.Boolean()
    absent = fields.Boolean()
    remarks = fields.Char()