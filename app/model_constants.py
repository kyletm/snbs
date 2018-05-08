BROAD_CATEGORIES_FORM = [('service', 'Service'), ('item', 'Item')]
SERVICES_FORM = [('ironing', 'Ironing'), ('driving', 'Driving'),
                 ('survey', 'Survey'), ('miscellaneous', 'Miscellaneous')]
ITEMS_FORM = [('cleaning', 'Cleaning'), ('household', 'Household'), ('tickets', 'Tickets'),
              ('party', 'Party'), ('music', 'Music'), ('miscellaneous', 'Miscellaneous')]
SERVICE_TYPES_FORM = [('sup', 'I want to supply something'), ('dem', 'I need something fulfilled')]
POSSIBLE_INSTUTIONS = ['Carnegie Mellon University', 'New York University',
                       'Princeton University', 'Rutgers University',
                       'University of Alabama', 'University of Michigan']
INSTITUTIONS_FORM = [('', 'Select an institution')] + [(inst, inst) for inst in POSSIBLE_INSTUTIONS]

HIERARCHICAL_CATEGORIES = {'service': SERVICES_FORM, 'item': ITEMS_FORM}
