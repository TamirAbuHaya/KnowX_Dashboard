class User:
    """

    """
    def __init__(self, full_name, email, course_num, role, battalion, platoon=None, team=None):
        self.full_name = full_name
        self.email = email
        self.course_num = course_num
        self.role = role #מ"פ, מג"ד, סמג"ד, מפק"ץ, צוער
        self.battalion = battalion
        self.platoon = platoon
        self.team = team
        self.experience_roles = [] #הדרכתית + פיקודית


    def view_files(self):
        pass

    def delete_file(self):
        pass

    def add_file(self):
        pass

    def add_experience_role(self, role):
        pass

    def accept_experience_role(self, role):
        pass

    def submit_experience_role(self, role):
        pass

    def search_files(self):
        pass


