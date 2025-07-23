# # -*- coding: utf-8 -*-
# from odoo import http
# from odoo.http import request
# from datetime import datetime, date
# import logging

# _logger = logging.getLogger(__name__)

# class AttendanceAPIController(http.Controller):

#     @http.route('/api/student/mark_present', type='json', auth='public', methods=['POST'], csrf=False)
#     def mark_student_present(self, **kwargs):
#         _logger.info("📥 API Request: %s", kwargs)

#         student_id = kwargs.get('student_id')
#         classroom_number = kwargs.get('classroom_number')
#         input_date = kwargs.get('date')  # Optional: '2025-07-23'
#         input_time = kwargs.get('time')  # Optional: '14:30'

#         if not student_id or not classroom_number:
#             return {"status": "error", "message": "Missing student_id or classroom_number"}

#         # Date & time setup
#         try:
#             today = datetime.strptime(input_date, "%Y-%m-%d").date() if input_date else date.today()
#         except ValueError:
#             return {"status": "error", "message": "Invalid date format. Use YYYY-MM-DD"}

#         if input_time:
#             try:
#                 hour, minute = map(int, input_time.split(":"))
#                 current_float_time = hour + minute / 60.0
#             except:
#                 return {"status": "error", "message": "Invalid time format. Use HH:MM"}
#         else:
#             now = datetime.now().time()
#             current_float_time = now.hour + now.minute / 60.0

#         # Fetch student
#         student = request.env['class.student'].sudo().search([('id', '=', student_id)], limit=1)
#         if not student:
#             return {"status": "error", "message": "No student found with ID %s" % student_id}
#         if not student.class_id or not student.section_id:
#             return {"status": "error", "message": "Student must have class & section assigned"}

#         section_id = student.section_id.id

#         # Fetch timetable
#         timetable = request.env['time.table'].sudo().search([
#             ('class_id', '=', student.class_id.id),
#             ('section_id', '=', section_id)
#         ], limit=1)

#         if not timetable:
#             return {"status": "error", "message": "No timetable found for class & section"}

#         # Map weekday to schedule field
#         weekday = str(today.weekday())
#         day_mapping = {
#             '0': 'schedule_monday_ids',
#             '1': 'schedule_tuesday_ids',
#             '2': 'schedule_wednesday_ids',
#             '3': 'schedule_thursday_ids',
#             '4': 'schedule_friday_ids',
#             '5': 'schedule_saturday_ids',
#             '6': 'schedule_sunday_ids',
#         }
#         schedule_field = day_mapping.get(weekday)
#         if not schedule_field:
#             return {"status": "error", "message": "Invalid weekday mapping"}

#         schedules = getattr(timetable, schedule_field)
#         matched_schedule = None
#         matched_attendance = None

#         for sched in schedules:
#             if sched.classroom_number == classroom_number:
#                 if sched.time_from <= current_float_time <= sched.time_to:
#                     attendance = request.env['attendance.class'].sudo().search([
#                         ('class_id', '=', student.class_id.id),
#                         ('section_id', '=', section_id),
#                         ('subject_id', '=', sched.subject_id.id),
#                         ('date', '=', today),
#                         ('start_time', '=', sched.time_from),
#                         ('end_time', '=', sched.time_to),
#                     ], limit=1)

#                     if not attendance:
#                         students = request.env['class.student'].sudo().search([
#                             ('class_id', '=', student.class_id.id),
#                             ('section_id', '=', section_id)
#                         ])
#                         attendance_lines = [(0, 0, {'student_id': s.id}) for s in students]
#                         attendance = request.env['attendance.class'].sudo().create({
#                             'teacher_id': sched.teacher_id.id,
#                             'date': today,
#                             'section_id': section_id,
#                             'subject_id': sched.subject_id.id,
#                             'start_time': sched.time_from,
#                             'end_time': sched.time_to,
#                             'class_id': student.class_id.id,
#                             'attendance_line_ids': attendance_lines,
#                         })
#                         _logger.info("✅ Created new attendance record ID %s", attendance.id)

#                     matched_schedule = sched
#                     matched_attendance = attendance
#                     break

#         if not matched_attendance:
#             return {"status": "error", "message": "No running class found at this time"}

#         # Mark student as present
#         line = request.env['attendance.student.line'].sudo().search([
#             ('attendance_id', '=', matched_attendance.id),
#             ('student_id', '=', student.id),
#         ], limit=1)

#         if not line:
#             return {"status": "error", "message": "Student not found in attendance line"}

#         line.write({'present': True, 'absent': False})
#         _logger.info("🎯 Student %s marked present in %s", student.name, matched_schedule.subject_id.name)

#         return {
#             "status": "success",
#             "message": f"✅ {student.name} marked present for subject {matched_schedule.subject_id.name}"
#         }
