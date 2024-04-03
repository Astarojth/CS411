import openpyxl
import random
import string

# 创建新的Excel工作簿
wb = openpyxl.Workbook()
ws = wb.active

# 添加标题行
headers = ["UserID", "UserAccount", "UserPassword", "UserName", "UserPhonenumber", "UserEmail", "UserJoinYear"]
ws.append(headers)

# 为每项数据定义随机取值的池

# UserID: 从1到1000
user_ids = list(range(1, 1600))

# UserAccount: 4到8位数字
def random_account():
    return ''.join(random.choices(string.digits, k=random.randint(6,10)))

# UserPassword: 8个字符组成的随机字符串
def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# UserName: 从一个预定义的名字列表中选择
firstnames = [
    # Anglo-Saxon names
    "John", "Emily", "Michael", "Jessica", "David", "Sarah",
    # France
    "Pierre", "Marie", "Jean", "Claudette", "Louis", "Sophie",
    # Spain
    "Jose", "Maria", "Carlos", "Carmen", "Miguel", "Isabel",
    # Germany
    "Hans", "Anna", "Heinrich", "Claudia", "Friedrich", "Helga",
    # Italy
    "Luigi", "Isabella", "Giovanni", "Sofia", "Marco", "Francesca",
    # Russia
    "Ivan", "Anastasia", "Sergei", "Olga", "Dmitry", "Yulia",
    # China (These are first names, but Chinese surnames usually come first)
    "Li", "Wang", "Zhang", "Liu", "Chen", "Yang",
    # India
    "Raj", "Priya", "Vijay", "Lakshmi", "Rohit", "Anjali",
    # Japan
    "Hiroshi", "Sakura", "Kenji", "Yumi", "Taro", "Hana",
    # Brazil
    "João", "Maria", "Paulo", "Teresa", "Antonio", "Clara",
    # Mexico/Latin America
    "Fernando", "Juanita", "Alberto", "Rosa", "Diego", "Gabriela",
    # Middle East
    "Ahmed", "Fatima", "Mahmoud", "Layla", "Omar", "Aisha",
    # Africa
    "Kwame", "Nneka", "Jomo", "Amara", "Chijioke", "Zanele"
]

lastnames = [
    # Anglo-Saxon names
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller",
    # France
    "Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard",
    # Spain
    "García", "Rodríguez", "Martínez", "Hernández", "López", "González",
    # Germany
    "Müller", "Schmidt", "Weber", "Meyer", "Wagner", "Schulz",
    # Italy
    "Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano",
    # Russia
    "Ivanov", "Smirnov", "Kuznetsov", "Popov", "Vasiliev", "Petrov",
    # China (These are surnames)
    "Wang", "Li", "Zhang", "Liu", "Chen", "Yang",
    # India (Using pan-Indian surnames as specific region-based surnames can be numerous)
    "Sharma", "Patel", "Singh", "Kumar", "Reddy", "Gupta",
    # Japan
    "Sato", "Suzuki", "Takahashi", "Tanaka", "Watanabe", "Ito",
    # Brazil
    "Silva", "Santos", "Oliveira", "Lima", "Pereira", "Fernandes",
    # Mexico/Latin America
    "Hernández", "García", "Martínez", "López", "González", "Pérez",
    # Middle East (Using common surnames across Arabic-speaking countries)
    "Al-Salem", "Husseini", "Abdallah", "Al-Nasser", "Malik", "Qureshi",
    # Africa (Using names from various regions, as Africa is very diverse)
    "Nguyen", "Patel", "Kumar", "Ali", "Singh", "Hussain"
]


names = [f"{random.choice(firstnames)} {random.choice(lastnames)}" for _ in range(1800)]
def random_name():
    return random.choice(names)

# UserPhonenumber: 10位数字组成
def random_phone():
    return ''.join(random.choices(string.digits, k=10))

# UserEmail: 使用UserAccount和一些常见的邮箱域名
domains = ["gmail.com", "yahoo.com", "outlook.com"]

def random_email(account):
    return f"{account}@{random.choice(domains)}"

# UserJoinYear: 2010到2022年之间的年份
join_years = list(range(2010, 2023))

for user_id in user_ids:
    user_account = random_account()
    user_password = random_password()
    user_name = random_name()
    user_phone = random_phone()
    user_email = random_email(user_account)
    user_join_year = random.choice(join_years)
    
    ws.append([user_id, user_account, user_password, user_name, user_phone, user_email, user_join_year])

# 保存到Excel文件中
wb.save("random_users.xlsx")

