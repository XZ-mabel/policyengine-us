from openfisca_us.model_api import *


class md_income_tax(Variable):
    value_type = float
    entity = TaxUnit
    label = "MD income tax"
    unit = USD
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        tax_after_non_refundable_credits = tax_unit(
            "md_income_tax_after_non_refundable_credits", period
        )
        refundable_credits = tax_unit("md_refundable_credits", period)
        return tax_after_non_refundable_credits - refundable_credits
