from django.db import models

# from users import models

# Create your models here.

class MailingList(models.Model):
	LIST_TYPES = (('Public','Public'),('Shared','Shared'))
	STATUS = (('Active','Active'),('Inactive','Inactive'))
	id = models.AutoField(primary_key = True,db_column = 'CG_ML_ID')
	name = models.CharField(max_length = 255,db_column = 'CG_ML_NAME')
	description = models.TextField(null = True,db_column = 'CG_ML_DESC')
	creation_date = models.DateField(db_column = 'CG_ML_CREATION_DATE')
	creator = models.ForeignKey('users.User',on_delete = models.CASCADE,db_column = 'CG_ML_CREATOR_ID',null = True,related_name = 'mailing_list_creator')
	modification_date = models.DateField(db_column = 'CG_ML_MODIFICATION_DATE',null = True)
	modifier = models.ForeignKey('users.User',on_delete = models.CASCADE,db_column = 'CG_ML_MODIFIER_ID',null = True, related_name = 'mailing_list_modifier')
	type_of_list = models.CharField(max_length = 20,choices = LIST_TYPES,db_column = 'CG_ML_TYPE')
	status = models.CharField(max_length = 20,choices = STATUS,db_column = 'CG_ML_STATUS')

	class Meta:
		db_table = 'CM_Mailing_list_tbl'

class MailingListUser(models.Model):
	ACCESS_TYPES = (('Public','Public'),('Shared','Shared'))
	mailing_list = models.ForeignKey('MailingList',on_delete = models.CASCADE,db_column = 'CG_ML_ID')
	mailing_user = models.ForeignKey('users.User',on_delete = models.CASCADE, db_column = 'CG_ML_USER_ID')
	access_type = models.CharField(max_length = 20,choices = ACCESS_TYPES)

	class Meta:
		db_table = 'CM_Mailing_list_usr_tbl'


class MailingListCustomerUpload(models.Model):
	list_id = models.ForeignKey('MailingList',on_delete = models.CASCADE,db_column = 'CG_ML_CU_ID')
	emails = models.TextField(null = True,db_column = 'CG_ML_CU_EMAILS')

	class Meta:
		db_table = 'CM_Mailing_list_custupl_tbl'


class MailingListSetup(models.Model):
	STATUS = (('Active','Active'),('Inactive','Inactive'))
	mailing_list = models.ForeignKey('MailingList',on_delete = models.CASCADE,db_column = 'CG_ML_STP_ID')
	parameter = models.CharField(max_length = 255,db_column = 'CG_ML_STP_PARAMETER')
	value = models.CharField(max_length = 500,null = True,db_column = 'CG_ML_STP_VALUE')
	inclusion_flag = models.BooleanField(default = False,db_column = 'CG_ML_STP_INC_FLG')
	status = models.CharField(max_length = 20,null = True,choices = STATUS,db_column = 'CG_ML_STATUS')

	class Meta:
		db_table = 'CM_Mail_list__Setup_tbl'

# class DepartmentSetup(models.Model):
# 	source = models.CharField(max_length = 10,db_column = 'CM_STP_SOURCE')
# 	status = models.CharField(max_length = 255,db_column = 'CM_STP_STATUS')
# 	department_id = models.CharField(max_length =10 ,db_column = 'CM_STP_DEPTID')
# 	department_name = models.CharField(max_length = 255 ,db_column = 'CM_STP_DEPTNAME')
# 	level = models.CharField(max_length = 4,db_column = 'CM_STP_LEVEL')
# 	m1_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M1_DEPT_ID')
# 	m1_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M1_DEPT_NAME')
# 	m2_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M2_DEPT_ID')
# 	m2_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M2_DEPT_NAME')
# 	m3_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M3_DEPT_ID')
# 	m3_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M3_DEPT_NAME')
# 	m4_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M4_DEPT_ID')
# 	m4_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M4_DEPT_NAME')
# 	m5_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M5_DEPT_ID')
# 	m5_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M5_DEPT_NAME')
# 	m6_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M6_DEPT_ID')
# 	m6_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M6_DEPT_NAME')
# 	m7_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M7_DEPT_ID')
# 	m7_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M7_DEPT_NAME')

# 	class Meta:
# 	db_table = 'CM_Department_Setup_tbl'




