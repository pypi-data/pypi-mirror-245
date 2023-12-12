from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


def convert_to_numeric(value):
    try:
        value = float(value)

    except ValueError as exc:
        raise ValidationError(
            _("Invalid number."),
            "invalid_number",
        ) from exc

    return value


def check_bounds(value, bottom, top):
    if any(
        [
            bottom is None and value > top,
            top is None and value < bottom,
            bottom is not None and value < bottom,
            top is not None and value > top,
        ],
    ):
        raise ValidationError(
            _("The value must be between the minimum and maximum allowed value."),
            "out_of_bounds_value",
        )
