from odoo import _

LEGAL_CASE_COURT_TYPE_CHOICES = [
    ("first_instance", _("Première instance")),
    ("appeal_court", _("Cours d'appel")),
    ("cassation_court", _("Cour de cassation")),
]


LEGAL_CASE_STATUS_CHOICES = [
    ("pending", _("En cours")),
    ("paied", _("Payé")),
    ("archived", _("Archivé")),
]

LEGAL_CASE_TYPE_CHOICES = [
    ("civile", "Civile"),
    ("correctionel", "Correctionel"),
    ("commircial", "Commercial"),
    ("work_accident", "Accident de travail (AT)"),
    ("incentive_payment_disputes ", "Contentieux prime (CP)"),
    ("divers", "Divers")
]

# LEGAL_CASE_TYPE_CHOICES = [
#     ("civile", _("Civile")),
#     ("correctionel", _("Correctionel")),
#     ("commircial", _("Commercial")),
#     ("work_accident", _("Accident de travail (AT)")),
#     ("incentive_payment_disputes ", _("Contentieux prime (CP)")),
#     ("divers", "Divers")
# ]
TRIAL_TYPE_CHOICES = [
    ("civile", _("Civile")),
    ("correctionel", _("Correctionelle")),
    ("commircial", _("Commercial")),
    ("work_accident", _("Accident de travail (AT)")),
    ("incentive_payment_disputes ", _("Contentieux prime (CP)")),
    ("divers", "Divers")
]

TRIBUNAL_CHOICES = [
    ("marrakech", _("Marrakech")),
    ("kelaa", _("Kelâa")),
    ("benguerir", _("Benguerir")),
    ("imintanoute", _("Imintanoute")),
]

PAYMENT_TYPE_CHOICES = [
    ("Indemnité", _("Indemnité")),
    ("Dépense", _("Dépense")),
]



EXPENSES_TYPE = [
    ("personal_expenses", _("Frais personnel")),
    ("tax", _("Impôts, Droit et taxes déductibles")),
    ("Loyers", _("Rents")),
    ("costs_management", _("Frais divers de gestion")),
    ("travelling", _("Frais de déplacement")),
    ("car_costs", _("Frais de voiture")),
    ("proffessional_fees", _("Frais professionnels")),
    ("taxes_provisions", _("Taxes provisions"))
]