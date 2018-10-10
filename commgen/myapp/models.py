from django.db import models
from .utils import increment_campaign_id
from django.urls import reverse


class Campaign(models.Model):
	CAMPAIGN_STATUS = (('Draft','draft'),('Co-author Validation','co_author_validation'),('Approval Waiting','approval_waiting'),('Confirmed','confirmed'),('Scheduled','scheduled'),('Sent','sent'))
	id = models.CharField(primary_key = True,db_column = 'CG_CAMPAIGN_ID',default=increment_campaign_id,max_length=10)
	name = models.CharField(max_length = 255,db_column = 'CG_CAMPAIGN_NAME')
	description = models.TextField(null = True,db_column = 'CG_CAMPAIGN_DESC')
	creation_date = models.DateTimeField(db_column = 'CG_CAMPAIGN_CREATION_DT',auto_now_add=True)
	creator = models.ForeignKey('users.User',db_column = 'CG_CAMPAIGN_CREATOR_CUID',on_delete=models.CASCADE)
	mailing_list = models.ForeignKey('mailing_list.MailingList',null = True,db_column = 'CG_ML_ID',on_delete=models.CASCADE)
	status = models.CharField(max_length = 20,null = True,db_column = 'CG_CAMPAIGN_STATUS')
	clone = models.CharField(max_length = 15,null = True,db_column = 'CG_CAMPAIGN_CLONE_ID')
	template = models.ForeignKey('mailing_templates.Template',null = True,db_column = 'CG_MT_ID',on_delete=models.CASCADE)
	exclusion = models.TextField(null = True,db_column = 'CG_CAMPAIGN_EXC')
	inclusion = models.TextField(null = True,db_column = 'CG_CAMPAIGN_INC')
	campaign_from = models.CharField(null = True,max_length = 255,db_column = 'CG_CAMPAIGN_FROM')
	campaign_cc = models.CharField(null = True,max_length = 255,db_column = 'CG_CAMPAIGN_CC')
	campaign_bcc = models.CharField(null = True,max_length = 255,db_column = 'CG_CAMPAIGN_BCC')
	campaign_body = models.TextField(null = True,db_column = 'CG_CAMPAIGN_BODY')
	recurrence = models.CharField(null = True,max_length=120,db_column = 'CG_CAMPAIGN_REC_ID')

	def get_absolute_url(self):
		print("self...nmae",self.name)
		return reverse('audience',kwargs={"campaign":self.name})

	class Meta:
		db_table = 'CG_Campaign_tbl'


class CampaignAuthor(models.Model):
	campaign = models.ForeignKey('Campaign',on_delete = models.CASCADE,db_column = 'CG_CAMPAIGN_ID')
	user = models.ForeignKey('users.User',on_delete = models.CASCADE,db_column = 'CG_CAMPAIGN_USER_ID')
	role = models.ForeignKey('users.Group',on_delete = models.CASCADE,db_column = 'CG_CAMPAIGN_USER_ROLE')
	flag = models.CharField(max_length = 2,null = True,db_column = 'CG_CAMPAIGN_USER_EDIT_FLG')
	last_updated_date = models.DateTimeField(auto_now = True,db_column = 'CG_CAMPAIGN_USER_LAST_DATE')
	status = models.CharField(max_length = 20,null = True,db_column = 'CG_CAMPAIGN_USER_STATUS')

	class Meta:
		db_table = 'CG_Campaign_author_tbl'

class CampaignReader(models.Model):
	campaign = models.ForeignKey('Campaign',on_delete = models.CASCADE,db_column = 'CG_CAMPAIGN_ID')
	reader = models.ForeignKey('users.User',on_delete = models.CASCADE,db_column = 'CG_CAMPAIGN_READER_ID')
	status = models.CharField(max_length = 20,null = True,db_column = 'CG_CAMPAIGN_USER_STATUS')

	class Meta:
		db_table = 'CG_Campaign_reader_tbl'


class CampaignApprover(models.Model):
	ACTION = (('Approve','approve'),('Reject','reject'),('Pending','pending'))
	campaign = models.ForeignKey('Campaign',on_delete = models.CASCADE,db_column = 'CG_CAMPAIGN_ID')
	level = models.CharField(max_length = 2,db_column = 'CG_CAMPAIGN_APV_LVL')
	approver = models.CharField(max_length = 255,db_column = 'CG_CAMPAIGN_APV_NAME')
	cuid = models.CharField(max_length = 2,db_column = 'CG_CAMPAIGN_APV_CUID')
	action = models.CharField(max_length = 50,db_column = 'CG_CAMPAIGN_APV_ACTN')
	date_of_action = models.DateTimeField(db_column = 'CG_CAMPAIGN_APV_ACTNDT')
	comment = models.TextField(null = True,db_column = 'CG_CAMPAIGN_APV_COMMENTS')
	status = models.CharField(max_length = 20,db_column = 'CG_CAMPAIGN_APV_STATUS')

	class Meta:
		db_table = 'CG_Campaign_approver_tbl'


class DepartmentSetup(models.Model):
    source = models.CharField(max_length = 10,db_column = 'CM_STP_SOURCE',null = True,blank=True)
    status = models.CharField(max_length = 50,db_column = 'CM_STP_STATUS',null = True,blank=True)
    department_id = models.CharField(max_length =10 ,db_column = 'CM_STP_DEPTID',null = True,blank=True)
    department_name = models.CharField(max_length = 255 ,db_column = 'CM_STP_DEPTNAME',null = True,blank=True)
    level = models.CharField(max_length = 4,db_column = 'CM_STP_LEVEL',null = True,blank=True)
    m1_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M1_DEPT_ID',null = True,blank=True)
    m1_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M1_DEPT_NAME',null = True,blank=True)
    m2_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M2_DEPT_ID',null = True,blank=True)
    m2_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M2_DEPT_NAME',null = True,blank=True)
    m3_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M3_DEPT_ID',null = True,blank=True)
    m3_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M3_DEPT_NAME',null = True,blank=True)
    m4_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M4_DEPT_ID',null = True,blank=True)
    m4_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M4_DEPT_NAME',null = True,blank=True)
    m5_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M5_DEPT_ID',null = True,blank=True)
    m5_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M5_DEPT_NAME',null = True,blank=True)
    m6_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M6_DEPT_ID',null = True,blank=True)
    m6_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M6_DEPT_NAME',null = True,blank=True)
    m7_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M7_DEPT_ID',null = True,blank=True)
    m7_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M7_DEPT_NAME',null = True,blank=True)
    m8_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M8_DEPT_ID',null = True,blank=True)
    m8_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M8_DEPT_NAME',null = True,blank=True)
    m9_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M9_DEPT_ID',null = True,blank=True)
    m9_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M9_DEPT_NAME',null = True,blank=True)
    m10_department_id = models.CharField(max_length = 10,db_column = 'CM_STP_M10_DEPT_ID',null = True,blank=True)
    m10_department_name = models.CharField(max_length = 255,db_column = 'CM_STP_M10_DEPT_NAME',null = True,blank=True)
    class Meta:
        db_table = 'CM_Department_Setup_tbl'


class LocationSetup(models.Model):
	generic_company = models.CharField(max_length=20,db_column='CM_STP_GEN_COMP',null=True)
	region = models.CharField(max_length=20,db_column='CM_STP_REGION',null=True)
	country = models.CharField(max_length=20,db_column='CM_STP_COUNTRY',null=True)
	location = models.CharField(max_length=20,db_column='CM_STP_LOCATION',null=True)
	status = models.CharField(max_length=20,db_column='CM_STP_STATUS',null=True)

	class Meta:
		db_table = 'CM_Location_Setup_tbl'