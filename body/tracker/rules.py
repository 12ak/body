import rules

def is_measurement_owner(user, measurement):
    return measurement.owner == user

rules.add_perm('tracker.view_measurement', is_measurement_owner)
rules.add_perm('tracker.change_measurement', is_measurement_owner)
rules.add_perm('tracker.delete_measurement', is_measurement_owner)
