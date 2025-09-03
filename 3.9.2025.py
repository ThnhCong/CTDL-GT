class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id  # ID sinh viên
        self.name = name  # Tên sinh viên
        self.courses = []  # Danh sách môn học đã đăng ký
        self.grades = {}  # Điểm số của các môn học (key: môn học, value: điểm)

    def register_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            course.add_student(self)  # Thêm sinh viên vào danh sách môn học
        else:
            print(f"{self.name} đã đăng ký môn {course.name} rồi.")

    def unregister_course(self, course):
        if course in self.courses:
            self.courses.remove(course)
            course.remove_student(self)  # Xóa sinh viên khỏi danh sách môn học
        else:
            print(f"{self.name} chưa đăng ký môn {course.name}.")

    def add_grade(self, course, grade):
        if course in self.courses:
            self.grades[course] = grade
        else:
            print(f"{self.name} chưa đăng ký môn {course.name}. Không thể ghi điểm.")

    def calculate_gpa(self):
        total_points = 0
        total_credits = 0
        for course in self.courses:
            grade = self.grades.get(course, 0)
            total_points += grade * course.credits
            total_credits += course.credits

        if total_credits > 0:
            return total_points / total_credits
        return 0

    def calculate_grade(self):
        gpa = self.calculate_gpa()
        if gpa >= 9:
            return "A"
        elif gpa >= 7.5:
            return "B"
        elif gpa >= 5.0:
            return "C"
        elif gpa >= 3.0:
            return "D"
        else:
            return "F"

    def list_courses(self):
        if self.courses:
            print(f"{self.name} đã đăng ký các môn học sau:")
            for course in self.courses:
                print(f"- {course.name}")
        else:
            print(f"{self.name} chưa đăng ký môn học nào.")

class Course:
    def __init__(self, course_id, name, credits):
        self.course_id = course_id  # Mã môn học
        self.name = name  # Tên môn học
        self.credits = credits  # Số tín chỉ của môn học
        self.students = []  # Danh sách sinh viên đã đăng ký môn học

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)
        else:
            print(f"Sinh viên {student.name} đã đăng ký môn {self.name}.")

    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)
        else:
            print(f"Sinh viên {student.name} không có trong danh sách môn {self.name}.")

class System:
    def __init__(self):
        self.accounts = []  # Danh sách tài khoản sinh viên
        self.courses = []  # Danh sách môn học
        self.logged_in_account = None  # Tài khoản sinh viên hiện tại đã đăng nhập

    def add_account(self, student_id, name, password):
        account = StudentAccount(student_id, name, password)
        self.accounts.append(account)

    def add_course(self, course_id, name, credits):
        course = Course(course_id, name, credits)
        self.courses.append(course)

    def login(self, student_id, password):
        for account in self.accounts:
            if account.student_id == student_id:
                if account.authenticate(password):
                    self.logged_in_account = account
                    account.student = Student(account.student_id, account.name)  # Liên kết tài khoản với đối tượng sinh viên
                    print(f"Đăng nhập thành công! Chào {account.name}.")
                    return True
                else:
                    print("Mật khẩu sai.")
                    return False
        print("ID sinh viên không tồn tại.")
        return False

    def logout(self):
        if self.logged_in_account:
            print(f"Đã đăng xuất tài khoản {self.logged_in_account.name}.")
            self.logged_in_account = None
        else:
            print("Chưa đăng nhập.")

    def register_course_for_logged_in_student(self, course_id):
        if self.logged_in_account:
            course = None
            for c in self.courses:
                if c.course_id == course_id:
                    course = c
                    break
            if course:
                self.logged_in_account.student.register_course(course)
                print(f"{self.logged_in_account.name} đã đăng ký môn {course.name}.")
            else:
                print("Môn học không tồn tại.")
        else:
            print("Chưa đăng nhập.")

    def unregister_course_for_logged_in_student(self, course_id):
        if self.logged_in_account:
            course = None
            for c in self.courses:
                if c.course_id == course_id:
                    course = c
                    break
            if course:
                self.logged_in_account.student.unregister_course(course)
                print(f"{self.logged_in_account.name} đã hủy đăng ký môn {course.name}.")
            else:
                print("Môn học không tồn tại.")
        else:
            print("Chưa đăng nhập.")

    def add_grade_for_student(self, course_id, grade):
        if self.logged_in_account:
            course = None
            for c in self.courses:
                if c.course_id == course_id:
                    course = c
                    break
            if course:
                self.logged_in_account.student.add_grade(course, grade)
                print(f"{self.logged_in_account.name} đã được ghi điểm môn {course.name} với điểm {grade}.")
            else:
                print("Môn học không tồn tại.")
        else:
            print("Chưa đăng nhập.")

    def calculate_gpa_for_logged_in_student(self):
        if self.logged_in_account:
            gpa = self.logged_in_account.student.calculate_gpa()
            print(f"GPA của {self.logged_in_account.name} là {gpa:.2f}.")
        else:
            print("Chưa đăng nhập.")

    def calculate_grade_for_logged_in_student(self):
        if self.logged_in_account:
            grade = self.logged_in_account.student.calculate_grade()
            print(f"{self.logged_in_account.name} có xếp loại học lực: {grade}.")
        else:
            print("Chưa đăng nhập.")

    def list_student_info(self):
        if self.logged_in_account:
            print(f"Thông tin sinh viên: {self.logged_in_account.name} (ID: {self.logged_in_account.student_id})")
            self.logged_in_account.student.list_courses()
        else:
            print("Chưa đăng nhập.")

    def list_course_info(self, course_id):
        course = None
        for c in self.courses:
          if c.course_id == course_id:
            course = c
            break

        if course:
            print(f"Thông tin môn học: {course.name} (Mã: {course.course_id}, Số tín chỉ: {course.credits})")
            print("Danh sách sinh viên đã đăng ký:")
            for student in course.students:
                print(f"- {student.name} (ID: {student.student_id})")
        else:
            print("Môn học không tồn tại.")

# if __name__ ==

system = System()