from django.db import models
# from users import models
# Create your models here.
class Template(models.Model):
	TEMPLATE_TYPES = (('Public','Public'),('Shared','Shared'))
	STATUS = (('Active','Active'),('Inactive','Inactive'))
	id = models.AutoField(primary_key = True,db_column = 'CG_MT_ID')
	name = models.CharField(max_length = 255,db_column = 'CG_MT_NAME')
	description = models.TextField(null = True,db_column = 'CG_MT_DESC')
	creation_date = models.DateField(db_column = 'CG_MT_CREATION_DATE')
	creator = models.ForeignKey('users.User',on_delete = models.CASCADE,db_column = 'CG_MT_CREATOR_ID',null = True,related_name = 'template_creator')
	modification_date = models.DateField(db_column = 'CG_MT_MODIFICATION_DATE',null = True)
	modifier = models.ForeignKey('users.User',on_delete = models.CASCADE,db_column = 'CG_MT_MODIFIER_ID',null = True,related_name = 'template_modifier')
	type_of_template = models.CharField(max_length = 20,choices = TEMPLATE_TYPES,db_column = 'CG_MT_TYPE')
	status = models.CharField(max_length = 20,choices = STATUS,db_column = 'CG_MT_STATUS')	

	class Meta:
		db_table = 'CM_Template_tbl'


class TemplateBody(models.Model):
	template = models.ForeignKey('Template',db_column = 'CG_MT_ID', on_delete = models.CASCADE)
	body = models.TextField(db_column = 'CG_MT_BODY')

	class Meta:
		db_table = 'CM_Template_body_tbl'

class TemplateUsers(models.Model):
	TEMPLATE_TYPES = (('Public','Public'),('Shared','Shared'))
	template = models.ForeignKey('Template',db_column = 'CG_MT_ID',on_delete = models.CASCADE)
	user = models.ForeignKey('users.User',db_column = 'CG_MT_USER_ID',on_delete = models.CASCADE)
	type_of_template = models.CharField(max_length = 20,choices = TEMPLATE_TYPES,db_column = 'CG_MT_TYPE')
