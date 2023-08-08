from policyengine_us.model_api import *


class la_cdcc(Variable):
    value_type = float
    entity = TaxUnit
    label = "Louisiana Chil and Dependent Care Credit"
    unit = USD
    definition_period = YEAR
    reference = "http://legis.la.gov/Legis/Law.aspx?d=101769"
    defined_for = StateCode.LA

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.states.la.tax.income.credits.cdcc
        # determine LA cdcc amount
        us_cdcc = tax_unit("cdcc", period)
        us_agi = tax_unit("adjusted_gross_income", period)
        return us_cdcc * p.rate.calc(us_agi, right=True)