
def increment_campaign_id():
  from .models import Campaign
  last_campaign = Campaign.objects.all().order_by('id').last()
  if not last_campaign:
    return 'CAM' + '00000'
  campaign_id = last_campaign.id
  campaign_int = int(campaign_id[3:8])
  new_campaign_int = campaign_int + 1
  new_campaign_id = 'CAM' + str(new_campaign_int)
  return new_campaign_id


