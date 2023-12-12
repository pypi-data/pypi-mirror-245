# views.py
import glob
import logging
from django.db.models import Sum, Q
import pyshark
from django.db import transaction
from django.http import JsonResponse, HttpResponse, FileResponse, StreamingHttpResponse,HttpResponseServerError
import os
from django.utils.encoding import smart_str
from django.conf import settings
from django.shortcuts import render
import json
from .models import UploadedFile, Identifiers, Message,Stats,IdentifiersStats
from django.utils import timezone
from celery import shared_task
from drawranflow.servicelogic.handlers.processPackets import F1APHandlerE as fh
from django.views.decorators.csrf import csrf_exempt
from .servicelogic.handlers import stats_handler as sh

BASE_DIR = getattr(settings,'BASE_DIR',None )
MEDIA_ROOT=getattr(settings,'MEDIA_ROOT',None)

def home(request):
    return render(request, 'home.html')


def upload(request):
    messages = {}
    if request.method == 'POST':
        file = request.FILES.get('file_upload')
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)

        try:
            # Check if an UploadedFile record with the same filename already exists
            upload_table = UploadedFile.objects.get(filename=file.name)
            if upload_table:
                # If it exists, delete the associated records in the related tables
                main_table = Identifiers.objects.filter(uploadedFiles__id=upload_table.id)
                associations = Message.objects.filter(identifiers__id__in=main_table.values('id'))

                # Delete the records
                main_table.delete()
                associations.delete()

                # Finally, delete the UploadedFile record
                upload_table.delete()

                # Remove the file from the file system
                if os.path.exists(file_path):
                    delete_files(file_path)

        except UploadedFile.DoesNotExist:
            pass

        # Save the new file
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Create or update the UploadedFile record
        uploaded_file_record, created = UploadedFile.objects.get_or_create(filename=file.name, processed=False)
        uploaded_file_record.save()

        messages = {
            'message_type': 'success',
            'message_text': 'File uploaded successfully',
        }

    return JsonResponse(messages)




def delete_files(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

        file_path = os.path.basename(file_path)

        file_path = file_path.split('.')[0]

        # Find and delete associated files with the same prefix
        for file_name in os.listdir(settings.MEDIA_ROOT):
            if file_name.startswith(file_path + '_'):
                file_to_delete = os.path.join(settings.MEDIA_ROOT, file_name)
                logging.debug(f"Filese deleting {file_to_delete}")
                os.remove(file_to_delete)

            if file_name.startswith(file_path + '.'):
                file_to_delete = os.path.join(settings.MEDIA_ROOT, file_name)
                logging.debug(f"Filese deleting {file_to_delete}")

                os.remove(file_to_delete)

def delete_item(request, item_id):
    try:
        print(item_id)
        item = UploadedFile.objects.get(id=item_id)
        print(item)
        # Delete the associated file from the media path
        if item:
            file_path = item.filename
            print(item.filename)
            file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            logging.debug(f"files to be deleted {file_path}")
            if os.path.exists(file_path):
                delete_files(file_path)

                # Delete the item from the database
                item.delete()

        return JsonResponse({'message_type': 'success', 'message_text': f'{item.filename} deleted successfully'},
                            status=200)
    except UploadedFile.DoesNotExist:
        return JsonResponse({'message': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': f'Error: {str(e)}'}, status=500)


# Process files

def process_item(request, item_id):
    try:
        item = UploadedFile.objects.get(id=item_id)
        # Delete the associated file from the media path
        if item:
            file_path = item.filename
            print(item.filename)
            file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            print(settings.MEDIA_ROOT, file_path)
            if os.path.exists(file_path):
                print("inside if")
                f = f'{file_path}'
                tmp = f'{item.filename}'.split('.')[0]
                csv = f'{settings.MEDIA_ROOT}/{tmp}.csv'
                async_process_file(f, csv, item_id)

        return JsonResponse(
            {'message_type': 'success', 'message_text': f'{item.filename} process started successfully'}, status=200)
    except UploadedFile.DoesNotExist:
        return JsonResponse({'message_type': 'error', 'message': 'file not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message_type': 'error', 'message': f'Error: {str(e)}'}, status=500)


@shared_task
def async_process_file(filename, csv, item_id):
    print("Im in async_process_file")
    # Run the file processing asynchronously
    fh(input_pcap=filename, output_csv=csv, item_id=item_id).capture_packets_and_save_to_csv()


def tmp_check_file_existence(request):
    file_exists = False
    if request.method == "POST":
        file_name = request.POST.get('file_name')
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        print(os.path.exists(file_path), file_path)
        try:
            if os.path.exists(file_path):
                # File exists, do something
                file_exists = True
            else:
                # File doesn't exist, log an error
                print("File does not exist:", file_path)
        except Exception as e:
            # Log the exception for debugging
            print("Error checking file existence:", str(e))
    return JsonResponse({'file_exists': file_exists})


def check_file_existence(request):
    file_exists = False
    if request.method == "POST":
        file_name = request.POST.get('file_name')
        print(file_name, "========")
        try:
            if UploadedFile.objects.filter(filename=file_name).exists():
                # File exists in the database
                file_exists = True
        except Exception as e:
            # Handle any exceptions or errors
            print("Error checking file existence:", str(e))
        print(file_exists)
    return JsonResponse({'file_exists': file_exists})


def streaming_table_view(request):
    # Retrieve data from the MainTable model
    id = request.GET.get('id')
    identifiers_table_data = Identifiers.objects.filter(uploadedFiles_id=id).values()

    # Convert the data to a list
    data = list(identifiers_table_data)
    print(data)
    return JsonResponse(data, safe=False)


def display_streaming_table(request, id):
    context = {
        'id': id,
        # Include other context data if needed...
    }
    return render(request, 'streaming_table.html', context)


def fetch_associated_data(request, main_id):
    try:
        messages = Message.objects.filter(identifiers=main_id)
        messages_list = []  # List to store all associated data for the main_id

        for message in messages:
            message_data = {
                'message_key': message.id,
                'FrameNumber': message.FrameNumber,
                'FrameTime': str(message.FrameTime),
                'IpSrc': message.IpSrc,
                'IpDst': message.IpDst,
                'Protocol': message.Protocol,
                'F1_Proc': message.F1_Proc,
                'E1_Proc': message.E1_Proc,
                'NG_Proc': message.NG_Proc,
                'C1_RRC': message.C1_RRC,
                'C2_RRC': message.C2_RRC,
                'MM_Message_Type': message.MM_Message_Type,
                'SM_Message_Type': message.SM_Message_Type,
                'Message': message.Message,
                'srcNode': message.srcNode,
                'dstNode': message.dstNode,
                'message_json': message.message_json,
            }
            messages_list.append(message_data)

        return messages_list

    except Message.DoesNotExist:
        # Handle the case where the message with the given id is not found
        return None
    except Exception as e:
        # Handle other exceptions
        raise e


@csrf_exempt
def prepare_download_pcap(request):
    try:
        # Retrieve main_id from the request's GET parameters
        main_id = request.GET.get('main_id')
        logging.debug(f"main id: {main_id}")

        # Fetch data based on the main_id from the Identifiers table
        identifier_data = fetch_identifier_data(main_id)

        # Construct a filter based on the identifier data
        if identifier_data:
            pcap_filter = construct_pcap_filter(identifier_data)
            logging.debug(f"identifier_data: {identifier_data}")

            if pcap_filter:
                uploadfile = UploadedFile.objects.get(id=identifier_data.uploadedFiles_id)

                filename = uploadfile.filename
                f = filename.split('.')
                # Filter the original pcap file and save the filtered file
                original_pcap_path = os.path.join(settings.MEDIA_ROOT, filename)

                outputfile = os.path.join(settings.MEDIA_ROOT,
                                          f"{f[0]}_{identifier_data.C_RNTI}_{identifier_data.GNB_DU_UE_F1AP_ID}.pcap")
                logging.debug(f'original_pcap_path={original_pcap_path}, outputfile={outputfile}')
                outputfile = filter_pcap(original_pcap_path, pcap_filter, outputfile)

                # Check if the file exists before trying to open it
                if os.path.exists(outputfile) and outputfile:
                    response = FileResponse(open(outputfile, 'rb'), content_type="application/vnd.tcpdump.pcap")
                    response[
                        "Content-Disposition"] = f'attachment; filename="{smart_str(os.path.basename(outputfile))}"'
                    return response
                else:
                    return JsonResponse({'error': 'Filtered file not found'}, status=404)
        else:
            return JsonResponse({'error': 'Identifier data not found'}, status=404)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


def fetch_identifier_data(row_id):
    logging.debug(f'identifier_data in fetch_identifier_data: {row_id}')

    identifier_data = Identifiers.objects.get(id=row_id)

    return identifier_data


def construct_pcap_filter(identifier_data):
    filter_conditions = []

    if identifier_data.C_RNTI is not None and identifier_data.GNB_DU_UE_F1AP_ID is not None:
        filter_conditions.append(f"(f1ap.C_RNTI=={identifier_data.C_RNTI} && "
                                 f"f1ap.GNB_DU_UE_F1AP_ID=={identifier_data.GNB_DU_UE_F1AP_ID})")

    if identifier_data.GNB_DU_UE_F1AP_ID is not None and identifier_data.GNB_CU_UE_F1AP_ID is not None:
        filter_conditions.append(f"(f1ap.GNB_CU_UE_F1AP_ID=={identifier_data.GNB_CU_UE_F1AP_ID}) or "
                                 f"(f1ap.GNB_CU_UE_F1AP_ID=={identifier_data.GNB_CU_UE_F1AP_ID} && "
                                 f"f1ap.GNB_DU_UE_F1AP_ID=={identifier_data.GNB_DU_UE_F1AP_ID})")

    if identifier_data.GNB_DU_UE_F1AP_ID is not None and identifier_data.GNB_CU_UE_F1AP_ID is None:
        filter_conditions.append(f"(f1ap.GNB_CU_UE_F1AP_ID=={identifier_data.GNB_CU_UE_F1AP_ID})")

    if identifier_data.GNB_CU_CP_UE_E1AP_ID is not None and identifier_data.GNB_CU_UP_UE_E1AP_ID is not None:
        filter_conditions.append(f"(e1ap.GNB_CU_CP_UE_E1AP_ID=={identifier_data.GNB_CU_CP_UE_E1AP_ID}) or "
                                 f"(e1ap.GNB_CU_CP_UE_E1AP_ID=={identifier_data.GNB_CU_CP_UE_E1AP_ID} && "
                                 f"e1ap.GNB_CU_UP_UE_E1AP_ID=={identifier_data.GNB_CU_UP_UE_E1AP_ID})")

    if identifier_data.GNB_CU_CP_UE_E1AP_ID is not None and identifier_data.GNB_CU_UP_UE_E1AP_ID is None:
        filter_conditions.append(f"(e1ap.GNB_CU_CP_UE_E1AP_ID=={identifier_data.GNB_CU_CP_UE_E1AP_ID})")

    if identifier_data.RAN_UE_NGAP_ID is not None and identifier_data.AMF_UE_NGAP_ID is not None:
        filter_conditions.append(f"(ngap.RAN_UE_NGAP_ID=={identifier_data.RAN_UE_NGAP_ID}) or "
                                 f"(ngap.RAN_UE_NGAP_ID=={identifier_data.RAN_UE_NGAP_ID} && "
                                 f"ngap.AMF_UE_NGAP_ID=={identifier_data.AMF_UE_NGAP_ID})")

    if identifier_data.RAN_UE_NGAP_ID is not None and identifier_data.AMF_UE_NGAP_ID is None:
        filter_conditions.append(f"ngap.RAN_UE_NGAP_ID =={identifier_data.RAN_UE_NGAP_ID}")

    if identifier_data.XNAP_SRC_RAN_ID is not None:
        filter_conditions.append(f"(xnap.NG_RANnodeUEXnAPID=={identifier_data.XNAP_SRC_RAN_ID})")

    if identifier_data.XNAP_TRGT_RAN_ID is not None:
        filter_conditions.append(f"(xnap.NG_RANnodeUEXnAPID=={identifier_data.XNAP_TRGT_RAN_ID})")

    filter_string = " or ".join(filter_conditions)
    logging.debug(f'Filter string - {filter_string}')
    # Log or use the generated filter_string as needed

    return filter_string


def filter_pcap(input_file, filter_string, output_file):
    print(input_file,filter_string,output_file)
    capture = pyshark.FileCapture(input_file, display_filter=f"{filter_string}", output_file=f'{output_file}')
    capture.set_debug()
    filtered_packets = [packet for packet in capture]
    logging.debug(f'filtered_packets,{filtered_packets} - output: {output_file}')

    return output_file


def fetch_packet_data(request):
    main_id = request.GET.get('main_id')
    logging.debug(f"main id: {main_id}")

    # Fetch data based on the main_id from the Identifiers table
    identifier_data = fetch_identifier_data(main_id)

    # Construct a filter based on the identifier data
    if identifier_data:
        pcap_filter = construct_pcap_filter(identifier_data)
        logging.debug(f"identifier_data: {identifier_data}")
        uploadfile = UploadedFile.objects.get(id=identifier_data.uploadedFiles_id)
        filename = uploadfile.filename
        f = filename.split('.')
        update_stats(uploadfile.id)
        # outputfile = os.path.join(settings.MEDIA_ROOT,
        #                           f"{f[0]}_{identifier_data.C_RNTI}_{identifier_data.GNB_DU_UE_F1AP_ID}.pcap")
        original_pcap_path = os.path.join(settings.MEDIA_ROOT, filename)
        # Future use if required.
        # if not os.path.exists(outputfile):
        #     try:
        #         # Filter the original pcap file and save the filtered file
        #         outputfile = filter_pcap(original_pcap_path, pcap_filter, outputfile)
        #         logging.debug(f'original_pcap_path={original_pcap_path}, outputfile={outputfile}')
        #     except Exception as e:
        #         logging.error(f"Error filtering pcap: {e}")
        #         # Handle the error as needed, e.g., return an error response

    frame_numbers = [message.FrameNumber for message in Message.objects.filter(identifiers_id=identifier_data.id)]

    if frame_numbers:
        frame_filter = '||'.join([f'frame.number=={fn}' for fn in frame_numbers])
        logging.debug(f"frame_filter - {frame_filter}")

        try:
            # Use PyShark to filter packets based on frame numbers
            if os.path.exists(original_pcap_path):
                with pyshark.FileCapture(original_pcap_path, display_filter=frame_filter) as packets:
                    packets.set_debug()
                    print("=========>", packets)
                    for packet in packets:
                        print(packet)
                        pduType = packetLayers(packet=packet)
                        test = sh.packet_to_dict(pduType)
                        if test:
                            # Find the message associated with the current frame number
                            matching_message = next(
                                (message for message in Message.objects.filter(identifiers_id=identifier_data.id) if
                                 message.FrameNumber == int(packet.frame_info.number)), None)
                            if matching_message:
                                matching_message.message_json = test
                                matching_message.save()
        except Exception as e:
            logging.error(f"Error capturing packets: {e}")
            # Handle the error as needed, e.g., return an error response

    associated_data = fetch_associated_data(request, main_id)
    logging.debug(f"associated_data- {associated_data}")

    # Render the draw-sequence view with the associated data
    if associated_data:
        associated_data = json.dumps(associated_data)

        context = {'main_id': main_id, 'associated_data': associated_data}

        return render(request, 'draw_sequence.html', context)
    else:
        return render(request, 'draw_sequence.html')


def packetLayers(packet):
    f1ap = packet.f1ap._all_fields if 'F1AP' in packet else {}
    e1ap = packet.e1ap._all_fields if 'E1AP' in packet else {}
    ngap = packet.ngap._all_fields if 'NGAP' in packet else {}
    xnap = packet.xnap._all_fields if 'XNAP' in packet else {}
    ipadd = packet.ip._all_fields if 'IP' in packet else {}
    filtered_ipdata = {key: value for key, value in ipadd.items() if key in ["ip.src", "ip.dst"]}
    del packet
    return {**filtered_ipdata, **f1ap, **ngap, **e1ap, **xnap}


def packet_to_dict(packet):
    # Extract IP layer if it exists
    new_dict = {}

    for key in packet:
        # split the key by the first dot and get the top-level key and the second-level key suffix
        if key != "" and "per" not in key:
            if "." in key:
                top_level_key, suffix = key.split(".", 1)
            else:
                top_level_key = key
                suffix = ""

            # create a new dictionary with the top-level key if it doesn't exist
            if top_level_key not in new_dict:
                new_dict[top_level_key] = {}

                # add the second-level key suffix and its value to the new dictionary
            new_dict[top_level_key][suffix] = packet[key]
            # convert the output dictionary to a pretty-printed JSON string
    return new_dict


def draw_sequence_view(request, main_id):
    if main_id is not None:
        filter_string = ""
        # Fetch associated data using  fetch_associated_data function
        associated_data = fetch_associated_data(request, main_id)
        identifier_data = fetch_identifier_data(main_id)
        if identifier_data:
            filter_string= construct_pcap_filter(identifier_data)
        # Render the draw-sequence view with the associated data
        associated_data = json.dumps(associated_data)
        context = {'main_id': main_id, 'associated_data': associated_data, 'filter_string': filter_string}

        return render(request, 'draw_sequence.html', context)
    else:
        return render(request, 'draw_sequence.html')


def get_updated_table_data(request):
    # Query the UploadedFile model and prepare data to send as JSON
    data = UploadedFile.objects.values('id', 'filename', 'upload_date', 'proces_date', 'processed')
    return JsonResponse(list(data), safe=False)

def showCucpWiseStats(request,id):
    print("id",id)
    unique_cucp_ips = Identifiers.objects.filter(
                        uploadedFiles_id=id,
                        CUCP_F1C_IP__isnull=False).values_list("CUCP_F1C_IP", flat=True).distinct()


    context = {'cucp_ips': unique_cucp_ips}
    return  render(request,'show_stats.html',context)

def update_stats(upload_file_id):
    # Define the time window for considering ServiceRequest or RegistrationRequest
    time_window = timezone.timedelta(seconds=1)
    unique_ips = Identifiers.objects.filter(uploadedFiles_id=upload_file_id).values_list('CUCP_F1C_IP', flat=True).distinct()


    # Retrieve all Identifiers associated with the given Upload File ID
    identifiers = Identifiers.objects.filter(uploadedFiles_id=upload_file_id)

    with transaction.atomic():
        for ip in unique_ips:
            if ip is not None or ip != '':
                # Reset stats for the current IP
                cumulative_stats.attempts = 0
                cumulative_stats.success = 0
                cumulative_stats.fails = 0
                cumulative_stats.timeouts = 0
                # Initialize cumulative stats
                cumulative_stats, created = Stats.objects.get_or_create(category='RRC', uploadedFiles_id=upload_file_id, cucp_f1c_ip=ip)

                for identifier in identifiers:
                    # Retrieve RRC Setup messages for the current Identifier
                    rrc_setup_messages = Message.objects.filter(
                        identifiers_id=identifier.id,
                        Message='RRC Setup'
                    )

                    for rrc_setup in rrc_setup_messages:
                        # Get related messages within the time window
                        related_messages = Message.objects.filter(
                            identifiers_id=identifier.id,
                            FrameTime__gte=rrc_setup.FrameTime,
                            FrameTime__lte=rrc_setup.FrameTime + time_window
                        )

                        # Check for ServiceRequest or RegistrationRequest
                        has_service_request = related_messages.filter(Message='Service request').exists()
                        has_registration_request = related_messages.filter(Message='Registration Request').exists()

                        # Update cumulative stats based on conditions
                        cumulative_stats.attempts += 1

                        if has_service_request or has_registration_request:
                            cumulative_stats.success += 1
                        elif related_messages.filter(Message='RRC Reject').exists():
                            cumulative_stats.fails += 1
                        else:
                            cumulative_stats.timeouts += 1

                cumulative_stats.save()



def update_stats_by_id(file_id):

    time_window = timezone.timedelta(seconds=1)
    upload_file = UploadedFile.objects.get(id=file_id)
    unique_ips = Identifiers.objects.filter(uploadedFiles_id=file_id).values_list('CUCP_F1C_IP', flat=True).distinct()

    if not upload_file.is_analysis_complete:
        with transaction.atomic():
            for ip in unique_ips:
                identifiers = Identifiers.objects.filter(uploadedFiles_id=file_id, CUCP_F1C_IP=ip)
                for identifier in identifiers:
                    # Get all RRC Setup messages from a perticular identifier
                    stats, created = IdentifiersStats.objects.get_or_create(category='RRC', identifier_id=identifier.id,
                                                                            uploadedFiles_id=file_id, cucp_f1c_ip=ip)
                    ctxt, ctxt_created = IdentifiersStats.objects.get_or_create(category='InitialCtxt', identifier_id=identifier.id,
                                                                            uploadedFiles_id=file_id,cucp_f1c_ip=ip)
                    rrc_setup_messages = Message.objects.filter(
                        identifiers_id=identifier.id,
                        Message='RRC Setup'
                    )
                    for rrc_setup in rrc_setup_messages:
                        # Get related messages within the time window
                        related_messages = Message.objects.filter(
                            identifiers_id=identifier.id,
                            FrameTime__gte=rrc_setup.FrameTime,
                            FrameTime__lte=rrc_setup.FrameTime + time_window
                        )
                          # Check for ServiceRequest or RegistrationRequest
                        has_service_request = related_messages.filter(Message='Service request',Protocol__icontains='f1ap').exists()
                        has_registration_request = related_messages.filter(Message='Registration request',Protocol__icontains='f1ap').exists()
                        has_tracking_request = related_messages.filter(Message='Tracking area update request',Protocol__icontains='f1ap').exists()
                        logging.debug(f"table id: {related_messages}, has_service_request: {has_service_request}, "
                                      f"has_registration_request: {has_registration_request}, "
                                      f"has_tracking_request: {has_tracking_request}")

                        if created:
                            stats.attempts += 1
                            if has_service_request or has_registration_request or has_tracking_request:
                                stats.success += 1
                                print(stats, stats.success)

                            if related_messages.filter(Message='Registration reject', Protocol__icontains='f1ap').exists():
                                stats.fails += 1
                                print(stats, stats.fails)

                            if not has_service_request and not has_registration_request and not has_tracking_request:
                                stats.timeouts += 1
                                print(stats, stats.timeouts)
                        stats.save()

                    has_initial_context_request = Message.objects.filter(Message='InitialContextSetupRequest',
                                                                         identifiers_id=identifier.id).exists()
                    has_initial_context_response = Message.objects.filter(Message='InitialContextSetupResponse',
                                                                          identifiers_id=identifier.id).exists()
                    has_initial_context_failure = Message.objects.filter(Message='InitialContextSetupFailure',
                                                                         identifiers_id=identifier.id).exists()
                    logging.debug(
                        f"has_initial_context_request: {has_initial_context_request}, "
                        f"has_initial_context_response: {has_initial_context_response},"
                        f"has_initial_context_failure: {has_initial_context_failure}"
                    )

                    if ctxt_created:
                    # Update stats based on conditions
                        if has_initial_context_request:
                            # Update stats for InitialContext category
                            ctxt.attempts += 1
                        if has_initial_context_response:

                            ctxt.success += 1

                        if has_initial_context_failure:
                            ctxt.fails += 1

                        if has_initial_context_request and not has_initial_context_failure and not has_initial_context_response:
                            ctxt.timeouts += 1
                        ctxt.save()



                update_cumulative_stats_for_category(file_id, 'InitialCtxt',ip)
                update_cumulative_stats_for_category(file_id, 'RRC',ip)

                # Check if analysis is complete and update the flag in UploadFiles model

                identifiers_ctxt_count = Message.objects.filter(identifiers__uploadedFiles_id=file_id, Message='InitialContextSetupRequest').count()
                processed_identifiers_ctxt_count = IdentifiersStats.objects.filter(
                        uploadedFiles_id=file_id,
                        category='InitialCtxt',
                    ).count()
                identifiers_rrc_count = Message.objects.filter(identifiers__uploadedFiles_id=file_id, Message='RRC Setup').count()
                processed_identifiers_rrc_count = IdentifiersStats.objects.filter(
                        uploadedFiles_id=file_id,
                        category='RRC',
                    ).count()

                if identifiers_rrc_count == processed_identifiers_ctxt_count and identifiers_rrc_count==processed_identifiers_rrc_count:
                    upload_file.is_analysis_complete = True
                    upload_file.save()
                logging.debug(f"Actual RRC Setup Count: {identifiers_rrc_count}, "
                              f"Processed Count: {processed_identifiers_rrc_count}, "
                              f"Actual InitalCtxt Count: {identifiers_ctxt_count}, "
                              f"Processed InitalCtxt Count: {processed_identifiers_ctxt_count}")

# def update_cummulative_stats(upload_file_id):
#     identifiers = Identifiers.objects.filter(uploadedFiles_id=upload_file_id)
#     cumulative_stats,created = Stats.objects.get_or_create(category='RRC', uploadedFiles_id=upload_file_id)
#     if cumulative_stats.attempts == 0 and created:
#         print("=======Ugandhar", identifiers,cumulative_stats,created)
#
#         # with transaction.atomic():
#         for identifier in identifiers:
#             update_stats_by_id(upload_file_id)
#
#         identifier_stats = IdentifiersStats.objects.filter(category='RRC',uploadedFiles_id=upload_file_id)
#
#         for identifier_stat in identifier_stats:
#             cumulative_stats.attempts += 1
#
#             if identifier_stat.success:
#                 cumulative_stats.success += 1
#                 print("succss", identifier_stat, cumulative_stats.success)
#
#             if identifier_stat.fails:
#                 cumulative_stats.fails += 1
#                 print("Fail", identifier_stat, cumulative_stats.fails)
#
#             if identifier_stat.timeouts:
#
#                 cumulative_stats.timeouts += 1
#                 print("Timeout", identifier_stat, cumulative_stats.timeouts)
#
#             cumulative_stats.save()

def update_cumulative_stats_for_category(upload_file_id, category,ip):

    # Get UploadFiles object

    # Update cumulative stats using annotation and aggregation
    identifier_stats_summary = IdentifiersStats.objects.filter(
        uploadedFiles_id=upload_file_id, category=category, cucp_f1c_ip=ip
    ).aggregate(
        attempts_count=Sum('attempts'),
        success_count=Sum('success'),
        fails_count=Sum('fails'),
        timeouts_count=Sum('timeouts')
    )

    cumulative_stats,created = Stats.objects.get_or_create(category=category, uploadedFiles_id=upload_file_id,cucp_f1c_ip=ip)
    if identifier_stats_summary:
    # Update cumulative stats for the specified category in UploadFiles model
        cumulative_stats.attempts = identifier_stats_summary['attempts_count'] or 0
        cumulative_stats.success = identifier_stats_summary['success_count'] or 0
        cumulative_stats.fails = identifier_stats_summary['fails_count'] or 0
        cumulative_stats.timeouts = identifier_stats_summary['timeouts_count'] or 0

        cumulative_stats.save()


def show_stats(request,id):
    try:
        upload_file_id = id
        cumulative_stat_list =[]
        identifier_stat_list = []
        print(upload_file_id)
        update_stats_by_id(upload_file_id)
        cumulative_stats = Stats.objects.filter(uploadedFiles_id=upload_file_id)
        for cumulative_stat in cumulative_stats:
            cumulative_stat_list.append ({
                'category': cumulative_stat.category,
                'attempts': cumulative_stat.attempts,
                'success': cumulative_stat.success,
                'fails': cumulative_stat.fails,
                'timeouts': cumulative_stat.timeouts,
                'cucp': cumulative_stat.cucp_f1c_ip
            })
        identifiers = IdentifiersStats.objects.filter(uploadedFiles_id=upload_file_id)
        identifier_stat_list = []
        for identifier in identifiers:
            identifier_stat_list.append({
                    'identifier_id': identifier.identifier_id,
                    'identifier_attempt': identifier.attempts,
                    'identifier_success': identifier.success,
                    'identifier_timeout': identifier.timeouts,
                    "identifier_category": identifier.category,
                    'identifier_fails': identifier.fails,
                    'cucp_ip': identifier.cucp_f1c_ip

            })

        print(cumulative_stat_list)

        context= {
            'cumulative_stat_list': cumulative_stat_list,
            'identifier_stats_list':identifier_stat_list
        }
        return render(request,'show_stats.html',context)
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error in show_stats view: {e}")
        return HttpResponseServerError("An error occurred while processing your request.")
