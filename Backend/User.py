class User:
    """

    """
    def __init__(self, full_name, email, course_num, battalion, platoon=None, team=None):
        self.full_name = full_name
        self.email = email
        self.battalion = battalion
        self.platoon = platoon
        self.team = team
        self.course_num = course_num



class Staff (User):
    """

    """
    def __init__(self, full_name, email, course_num, staff_role, battalion, platoon=None, team=None):
        User.__init__(self, full_name, email, battalion, platoon, team, course_num)
        self.staff_experience_roles = [] #
        self.staff_role = staff_role #Staff role - platoon_commander, battalion_commander, battalion_second_in_command, team_commander


class Cadet (User):
    """

    """
    def __init__(self, full_name, email, course_num, battalion, platoon=None, team=None):
        User.__init__(self, full_name, email, battalion, platoon, team, course_num)
        self.cadet_roles = []

