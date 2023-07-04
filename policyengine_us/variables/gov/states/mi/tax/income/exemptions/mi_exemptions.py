from policyengine_us.model_api import *


class mi_exemptions(Variable):
    value_type = float
    entity = TaxUnit
    label = "Michigan Exemptions"
    defined_for = StateCode.MI
    unit = USD
    definition_period = YEAR
    reference = (
        "http://legislature.mi.gov/doc.aspx?mcl-206-30",
        "https://www.legislature.mi.gov/Publications/TaxpayerGuide.pdf",
    )

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.states.mi.tax.income.exemptions

        # Personal Exemptions
        person = tax_unit("head_spouse_count", period)
        personal_exemption = person * p.filer

        # Dependent exemptions
        dependent = tax_unit("tax_unit_dependents", period)
        dependent_exemption = dependent * p.dependent

        # Stillborn Exemptions
        stillborn = tax_unit("tax_unit_stillbirths", period)
        stillborn_exemption = stillborn * p.stillborn

        # Disabled exemptions
        disabled_people = add(tax_unit, period, ["is_disabled"])
        disabled_exemption = disabled_people * p.disabled

        # Disabled veteran exemptions
        disabled_veteran = add(
            tax_unit, period, ["is_fully_disabled_service_connected_veteran"]
        )
        disabled_veteran_exemption = disabled_veteran * p.disabled_veteran

        # Dependent on other return exemptions
        filing_status = tax_unit("filing_status", period)
        is_dependent_on_other_return = tax_unit("dsi", period).astype(int)
        is_dependent_exemption = (
            is_dependent_on_other_return
            * p.dependent_on_other_return[filing_status]
        )

        # Total exemptions
        return (
            personal_exemption
            + dependent_exemption
            + stillborn_exemption
            + disabled_exemption
            + disabled_veteran_exemption
            + is_dependent_exemption
        )
