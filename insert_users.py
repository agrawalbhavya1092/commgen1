from users.models import User

User.objects.create_user(email='cd@orange.com',emp_id='cd1234',password='!1bhavya')
user = User.objects.filter(email = 'cd@orange.com')

user_info = {'first_name':'Johna','pref_first_name':'Jo','last_name':'Doe','pref_last_name':'De','middle_name':'Pal','pref_language':'fr','title':'Mr'}

user.update(**user_info)

