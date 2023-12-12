from datetime import datetime

from b2_utils.helpers import get_nested_attr
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.managers import SoftDeletableManager
from model_utils.models import SoftDeletableModel, TimeStampedModel
from rest_framework.exceptions import ValidationError
from validate_docbr import CNPJ, CPF

from b2_forms.helpers import check_bounds, convert_to_numeric
from b2_forms.mixins import CustomFieldMixin, FormFieldMixin


class Form(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CustomField(CustomFieldMixin, SoftDeletableModel, TimeStampedModel):
    objects = SoftDeletableManager()

    class Meta:
        verbose_name = _("Custom field")
        verbose_name_plural = _("Custom fields")
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"

    def format_answer(self, answer):
        if self.input_type in self.BINARY_TYPES:
            return None, False

        if not answer:
            return [], True

        if not isinstance(answer, list):
            answer = [answer]

        format = getattr(
            self,
            f"_format_{self.input_type.lower()}",
            self._format_default,
        )

        return format(answer), True

    def _format_default(self, answer: list):
        return [{"value": value} for value in answer]

    def _format_checkbox(self, answers):
        return [d for d in self.values if d.get("ID") in map(int, answers)]

    def _format_radio(self, answers):
        return self._format_checkbox(answers)[:1]

    def get_values_list(self, values=None, key="value") -> list:
        return [value.get(key) for value in values or self.values]

    def get_bounds(self) -> list:
        return [float(bound) if bound else None for bound in self.get_values_list()]

    def get_errors(self, func, answers: list):
        error_list = []
        error = False

        ids_mapping = {value.get("ID"): value for value in self.values}
        for index, answer in enumerate(answers):
            try:
                answers[index] = func(
                    answer,
                    ids_mapping=ids_mapping,
                )
                error_list.append([])

            except ValidationError as exc:
                error_list.append(exc.detail)
                error = True

        if error:
            raise ValidationError(error_list)

        return answers

    def validate_input(self, answers: list):
        if not answers:
            return []

        if len(answers) > 1:
            is_checkbox = self.input_type == self.Type.CHECKBOX
            if not (self.multiple or is_checkbox):
                raise ValidationError(
                    _("This field does not support multiple values"),
                    "non_multiple_field_with_multiple_values",
                )

            is_radio = self.input_type == self.Type.RADIO
            if is_radio:
                raise ValidationError(
                    _(
                        "The 'radio' field type requires none or exactly one answer.",
                    ),
                    "radio_multiple_values",
                )

        if validate := getattr(self, f"_validate_{self.input_type.lower()}", None):
            return self.get_errors(validate, answers)

        return answers

    def _validate_checkbox(self, answer, ids_mapping, **kwargs):
        id = answer["ID"]
        if id not in ids_mapping:
            raise ValidationError(
                _("Invalid option."),
                "invalid_option",
            )

        return ids_mapping[id]

    def _validate_radio(self, answer, **kwargs):
        return self._validate_checkbox(answer, **kwargs)

    def _validate_link(self, answer, **kwargs):
        link = answer["value"]
        try:
            validator = URLValidator()
            validator(link)

        except DjangoValidationError as exc:
            raise ValidationError(_("Invalid link"), "invalid_link") from exc

        return answer

    def _validate_number(self, answer, **kwargs):
        number = answer["value"]
        value = convert_to_numeric(number)
        if bounds := self.get_bounds():
            check_bounds(value, bounds[0], bounds[1])

        return answer

    def _validate_slider(self, answer, **kwargs):
        return self._validate_number(answer, **kwargs)

    def _validate_date(self, answer, **kwargs):
        date = answer["value"]
        try:
            datetime.strptime(date, "%Y-%m-%d")  # noqa: DTZ007

        except ValueError as exc:
            raise ValidationError(
                _("Invalid date format."),
                "invalid_date_format",
            ) from exc

        return answer

    def _validate_datetime(self, answer, **kwargs):
        date = answer["value"]
        try:
            datetime.fromisoformat(date)

        except ValueError as exc:
            raise ValidationError(
                _("Invalid datetime format."),
                "invalid_datetime_format",
            ) from exc

        return answer

    def _validate_document(self, answer, **kwargs):
        document = answer["value"]
        if not any(
            [
                CPF().validate(document),
                CNPJ().validate(document),
            ],
        ):
            raise ValidationError(
                _("Invalid CPF or CNPJ."),
                "invalid_cpf_or_cnpj",
            )

        return answer

    def _validate_cpf(self, answer, **kwargs):
        document = answer["value"]
        if not CPF().validate(document):
            raise ValidationError(
                _("Invalid CPF."),
                "invalid_cpf",
            )

        return answer

    def _validate_cnpj(self, answer, **kwargs):
        document = answer["value"]
        if not CNPJ().validate(document):
            raise ValidationError(
                _("Invalid CNPJ."),
                "invalid_cnpj",
            )

        return answer


class Section(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name="sections",
    )

    class Meta:
        verbose_name = _("Form section")
        verbose_name_plural = _("Form sections")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Field(FormFieldMixin, SoftDeletableModel, TimeStampedModel):
    custom_field = models.ForeignKey(
        CustomField,
        related_name="+",
        on_delete=models.CASCADE,
    )
    section = models.ForeignKey(
        Section,
        related_name="fields",
        on_delete=models.CASCADE,
    )

    objects = SoftDeletableManager()

    class Meta:
        verbose_name = _("Form field")
        verbose_name_plural = _("Form fields")
        ordering = ["section__form", "section", "index"]

    def __str__(self) -> str:
        return f"{self.form}|{self.custom_field}"

    def is_valid_answer(self, answers):
        valid = len(answers) >= 1 and all(
            answer.get("ID") or answer["value"].strip() for answer in answers
        )

        if not any([not (self.required ^ valid), valid]):
            raise ValidationError(
                _("answer is required for this field"),
                "answer_is_required",
            )


class Answer(
    CustomFieldMixin,
    FormFieldMixin,
    SoftDeletableModel,
    TimeStampedModel,
):
    field = models.ForeignKey(
        Field,
        on_delete=models.SET_NULL,
        null=True,
        related_name="answers",
    )
    answer = ArrayField(
        models.JSONField(blank=True, null=True),
        blank=True,
        default=list,
    )

    mutable = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Answer field")
        verbose_name_plural = _("Answer fields")
        ordering = ["index"]

    def set_answer(self, answer):
        if custom_field := get_nested_attr(self, "field.custom_field"):
            answer, formatted = custom_field.format_answer(answer)
            if formatted:
                self.answer = answer
                self.save(update_fields=["answer"])
