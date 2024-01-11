from policyengine_us.model_api import *


class ca_calworks_child_care_child_age_eligible(Variable):
    value_type = bool
    entity = Person
    label = (
        "Eligible child for the California CalWORKs Child Care based on age"
    )
    definition_period = YEAR
    defined_for = StateCode.CA
    reference = "http://epolicy.dpss.lacounty.gov/epolicy/epolicy/server/general/projects_responsive/ePolicyMaster/index.htm?&area=general&type=responsivehelp&ctxid=&project=ePolicyMaster#t=mergedProjects%2FChild%20Care%2FChild_Care%2F1210_Overview%2F1210_Overview.htm%23Backgroundbc-3&rhtocid=_3_3_0_2"

    def formula(person, period, parameters):
        p = parameters(period).gov.states.ca.cdss.tanf.child_care.eligibility
        age = person("age", period)
        is_disabled = person("is_disabled", period)
        age_limit = where(
            is_disabled, p.disabled_age_threshold, p.age_threshold
        )
        # Only children of citizens and legal permanent residents are eligible
        immigration_status = person("immigration_status", period)
        status = immigration_status.possible_values
        citizen = immigration_status == status.CITIZEN
        resident = immigration_status == status.LEGAL_PERMANENT_RESIDENT
        eligible_status = citizen | resident
        age_eligible = age <= age_limit
        return age_eligible & eligible_status
