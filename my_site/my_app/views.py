from django.shortcuts import render
from models import Whatsapp, WhatsappDetail
import pandas as pd
from django.http import HttpResponse ,response
from io import BytesIO  
from datetime import datetime   
from openpyxl import Workbook   

# Create your views here.

def get_whatsapp_message_report(request):
    # Retrieve date range from query parameters
    start_date_raw = request.GET.get('start_date')
    end_date_raw = request.GET.get('end_date')

    # Validate and parse dates
    if start_date_raw and end_date_raw:
        try:
            # Parse dates using dd-mm-yyyy format
            start_date = datetime.strptime(start_date_raw.strip(), "%d-%m-%Y")
            end_date = datetime.strptime(end_date_raw.strip(), "%d-%m-%Y")
        except ValueError:
            return HttpResponse("Invalid date format. Please use DD-MM-YYYY.")
    else:
        return HttpResponse("Please provide a valid date range.")




    whatsapp_users = Whatsapp.objects.select_related('id')
    whatsapp_dict = {whatsapp_user.id: whatsapp_user for whatsapp_user in whatsapp_users}

    if start_date and end_date:
        whatsapp_messages = WhatsappDetail.objects.filter(
        created_on_date_gte=start_date,
        created_on_date_lte=end_date
        ).order_by('whatsapp', 'created_on')
    else:
        whatsapp_messages = WhatsappDetail.objects.all().order_by('message_id', 'created_on')

    data = []
    last_chat_id = None

    for message in whatsapp_messages:
        whatsapp_chat_id = message.id
        whatsapp_user = whatsapp_dict.get(whatsapp_chat_id)

        created_on = message.created_on.strftime("%d/%m/%Y %H:%M:%S")
        from_user = message.from_user
        message_text = message.text
        sender = 'Bilinmiyor'
    

        if whatsapp_user:
            if from_user == 'AGENT' and whatsapp_user.id:
                sender = whatsapp_user.sender_name
            elif from_user == 'CLIENT' and whatsapp_user.sender_name:
                sender = whatsapp_user.sender_name

        if last_chat_id and whatsapp_chat_id:
            data.append({'Tarih': '---------------------------------', 'Gönderen': '---------------------------------', 'Mesaj': '---------------------------------'})
            if whatsapp_user:
                data.append({'Tarih': f'{whatsapp_user.sender_name} | {whatsapp_user.sender_phone}','Gönderen': '', 'Mesaj': ''})


        data.append({
            'Tarih': created_on,
            'Gönderen': f'{from_user} ({sender})',
            'Mesaj': message_text
        })

        last_chat_id = whatsapp_chat_id                            

    df = pd.DataFrame(data)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Whatsapp Messages')

    writer.close()
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Whatsapp_messages.xlsx"'
    return render(request, 'whatsapp_report.html', {'response': response})

