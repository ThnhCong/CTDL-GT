class Course:
    def __init__(self, course_id, course_name, credit_hours):
        self.course_id = course_id
        self.course_name = course_name
        self.credit_hours = credit_hours

    def __str__(self):
        return f"{self.course_name} ({self.course_id}) - {self.credit_hours} tín chỉ"


class Student:
    def __init__(self, student_id, full_name, enrollment_year, major):
        self.student_id = student_id
        self.full_name = full_name
        self.enrollment_year = enrollment_year
        self.major = major
        self.registered_courses = []  # Danh sách các môn học đã đăng ký

    def __str__(self):
        return f"ID: {self.student_id}, Tên: {self.full_name}, Khóa học: {self.enrollment_year}, Ngành học: {self.major}"

    def register_course(self, course, grade=None):
        """Đăng ký môn học cho sinh viên"""
        registration = Registration(self, course, grade)
        self.registered_courses.append(registration)
        return registration

    def get_average_grade(self):
        """Tính điểm trung bình của sinh viên"""
        total_grades = sum(registration.grade for registration in self.registered_courses if registration.grade is not None)
        count = sum(1 for registration in self.registered_courses if registration.grade is not None)
        return total_grades / count if count > 0 else 0


class Registration:
    def __init__(self, student, course, grade=None):
        self.student = student
        self.course = course
        self.grade = grade

    def __str__(self):
        return f"{self.course.course_name} - Điểm: {self.grade}"

    def update_grade(self, grade):
        """Cập nhật điểm cho môn học"""
        self.grade = grade


class SchoolSystem:
    def __init__(self):
        self.students = []
        self.courses = []

    def add_student(self, student):
        """Thêm sinh viên vào hệ thống"""
        self.students.append(student)

    def remove_student(self, student_id):
        """Xóa sinh viên khỏi hệ thống"""
        self.students = [student for student in self.students if student.student_id != student_id]

    def add_course(self, course):
        """Thêm môn học vào hệ thống"""
        self.courses.append(course)

    def remove_course(self, course_id):
        """Xóa môn học khỏi hệ thống"""
        self.courses = [course for course in self.courses if course.course_id != course_id]

    def display_student_info(self, student_id):
        """Hiển thị thông tin sinh viên và các môn học đã đăng ký"""
        student = next((student for student in self.students if student.student_id == student_id), None)
        if student:
            print(student)
            for reg in student.registered_courses:
                print(f"  {reg}")
        else:
            print("Sinh viên không tồn tại.")

    def display_course_info(self, course_id):
        """Hiển thị thông tin môn học"""
        course = next((course for course in self.courses if course.course_id == course_id), None)
        if course:
            print(course)
            for student in self.students:
                for reg in student.registered_courses:
                    if reg.course.course_id == course_id:
                        print(f"  {student.full_name} - Điểm: {reg.grade}")
        else:
            print("Môn học không tồn tại.")