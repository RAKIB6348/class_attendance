from odoo import models, fields, api
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)



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

    
    @api.model
    def create_attendance_for_today(self):
        today = fields.Date.context_today(self)
        weekday = str(today.weekday())  # Get the weekday as a string (0=Monday, 6=Sunday)

        day_mapping = {
            '0': 'schedule_monday_ids',
            '1': 'schedule_tuesday_ids',
            '2': 'schedule_wednesday_ids',
            '3': 'schedule_thursday_ids',
            '4': 'schedule_friday_ids',
            '5': 'schedule_saturday_ids',
            '6': 'schedule_sunday_ids',
        }

        schedule_field = day_mapping.get(weekday)
        if not schedule_field:
            _logger.warning("❌ No schedule field found for weekday: %s", weekday)
            return False

        _logger.info("🗓️ Creating attendance for %s (Weekday: %s, Schedule field: %s)", today, weekday, schedule_field)

        timetables = self.env['time.table'].search([])

        for timetable in timetables:
            _logger.info("📚 Processing timetable for Class: %s | Section: %s", timetable.class_id.name, timetable.section_id.name)

            schedules = getattr(timetable, schedule_field)

            for schedule in schedules:
                _logger.info("➡️ Schedule: Subject=%s, Teacher=%s, Time=%s-%s",
                             schedule.subject_id.name,
                             schedule.teacher_id.name,
                             schedule.time_from,
                             schedule.time_to)

                existing = self.search([
                    ('class_id', '=', timetable.class_id.id),
                    ('section_id', '=', timetable.section_id.id),
                    ('subject_id', '=', schedule.subject_id.id),
                    ('date', '=', today),
                    ('start_time', '=', schedule.time_from),
                    ('end_time', '=', schedule.time_to),
                ], limit=1)

                if existing:
                    _logger.info("⚠️ Already exists: attendance for %s [%s] on %s", 
                                 timetable.class_id.name, schedule.subject_id.name, today)
                    continue

                students = self.env['class.student'].search([
                    ('class_id', '=', timetable.class_id.id)
                ])

                _logger.info("👥 Found %s students for class %s", len(students), timetable.class_id.name)

                attendance_lines = [(0, 0, {'student_id': student.id}) for student in students]

                self.create({
                    'teacher_id': schedule.teacher_id.id,
                    'date': today,
                    'section_id': timetable.section_id.id,
                    'subject_id': schedule.subject_id.id,
                    'start_time': schedule.time_from,
                    'end_time': schedule.time_to,
                    'class_id': timetable.class_id.id,
                    'attendance_line_ids': attendance_lines,
                })

                _logger.info("✅ Created attendance for class: %s | subject: %s | teacher: %s",
                             timetable.class_id.name, schedule.subject_id.name, schedule.teacher_id.name)

        _logger.info("🎉 Attendance creation completed for date: %s", today)
        return True