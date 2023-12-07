from odoo import api, fields, models, _

from datetime import datetime, time, timedelta
from collections import defaultdict
from odoo.tools import float_utils

ROUNDING_FACTOR = 16


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def _get_number_of_days(self, date_from, date_to, employee_id):
        """Returns a float equals to the timedelta between two dates given as string."""
        total_days = 0
        current_day = date_from.date()
        limit_day = date_to.date()
        while current_day <= limit_day:
            not_weekend = current_day.weekday() < 5
            not_holiday = not self.env["hr.holidays.public"].is_public_holiday(
                current_day
            )
            if not_weekend and not_holiday:
                total_days += 1
            current_day += timedelta(days=1)

        hours_per_day = (
            self.env["hr.employee"]
            .browse(employee_id)
            .resource_calendar_id.hours_per_day
        )

        if self.request_unit_hours and total_days != 0:
            custom_hours = float_utils.float_round(
                (date_to - date_from).seconds / 3600.0, precision_rounding=1
            )
            total_days = 1
            hours_per_day = custom_hours

        elif self.request_unit_half and total_days != 0:
            total_days = 0.5

        return {"days": total_days, "hours": total_days * hours_per_day}

    @api.depends("number_of_days")
    def _compute_number_of_hours_display(self):
        for holiday in self:
            calendar = holiday._get_calendar()
            if holiday.date_from and holiday.date_to:
                number_of_hours = holiday._get_number_of_days(
                    holiday.date_from, holiday.date_to, holiday.employee_id.id
                )["hours"]
                holiday.number_of_hours_display = number_of_hours
            else:
                holiday.number_of_hours_display = 0
