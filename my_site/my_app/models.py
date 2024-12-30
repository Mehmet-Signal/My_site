from django.db import models
import uuid

class Whatsapp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    version = models.IntegerField()
    sender_phone = models.CharField(max_length=255)
    sender_name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255)
    dial_code = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now=True)

    def latest_detail(self):
        return self.whatsappdetail_set.order_by('-created_on').first()


    class Meta:
            db_table = "Whatsapp"


class WhatsappDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    whatsapp = models.ForeignKey(Whatsapp, on_delete=models.CASCADE)
    recevier_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user = models.CharField(max_length=255)
    message_id = models.CharField(max_length=500)
    type = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    image_type = models.CharField(max_length=255, null=True, blank=True)
    image_expiry = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "WhatsappDetail"