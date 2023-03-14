from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import requests
import json
from ABHA import abha_cred
from .models import AbhaDetails,CustomUser
from django.http import HttpResponse,JsonResponse

def generate_token():
    endpoint = abha_cred.endpoint_login
    payload = json.dumps(abha_cred.credential)
    headers = {
    'Content-Type': 'application/json',
    }
    response = requests.request("POST", endpoint, headers=headers, data=payload)
    try:
        token_response=response.json()
        print("--token_response-",token_response)
        token_response['status'] = True
        return token_response
    except Exception as e:
        context = {'status': False, 'message': "Something went wrong."}
        return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def refresh_token(token):
    endpoint = abha_cred.refresh
    data = {"refreshToken":token}
    payload = json.dumps(data)
    token_response = generate_token()
    headers = {
    'Content-Type': 'application/json',
    'Authorization':'Bearer ' + str(token_response['accessToken']),
    }
    response = requests.request("POST", endpoint, headers=headers, data=payload)
    try:
        tokenresponse=response.json()
        tokenresponse['status'] = True
        return tokenresponse
    except Exception as e:
        context = {'status': False, 'message': "Something went wrong."}
        return context


class AAdharVerify(APIView):
    def post(self, request):
        try:
            token_response = generate_token()
            if token_response['status'] == True:
                endpoint = abha_cred.adhar_verify
                payload = json.dumps(request.data)
                print('Bearer ' + str(token_response['accessToken']),"======>")
                headers = {
                'Content-Type': 'application/json',
                'Authorization':'Bearer ' + str(token_response['accessToken']),
                }
                response = requests.request("POST", endpoint, headers=headers, data=payload)
                adhar_value=response.json()
                adhar = CustomUser(txnid=adhar_value['txnId'])
                adhar.save()
                return Response(response.json())

            else:
                return Response({"message": "invalid token"})
        except Exception as e:
            context = {'status': False, 'message': "Something went wrong."}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AAdharOTPVerify(APIView):
    def post(self, request):
        try:
            token_response = generate_token()
            if token_response['status'] == True:
                endpoint = abha_cred.adhar_otp_verify
                payload = json.dumps(request.data)
                print('Bearer ' + str(token_response['accessToken']),"======>")
                headers = {
                'Content-Type': 'application/json',
                'Authorization':'Bearer ' + str(token_response['accessToken'])
                }
                response = requests.request("POST", endpoint, headers=headers, data=payload)
                return Response(response.json())
            else:
                return Response({"message": "invalid token"})
        except Exception as e:
            context = {'status': False, 'message': "Something went wrong."}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MobileVerify(APIView):
    def post(self, request):
        try:
            token_response = generate_token()
            if token_response['status'] == True:
                endpoint = abha_cred.mobile_verify
                payload = json.dumps(request.data)
                print('Bearer ' + str(token_response['accessToken']),"======>")
                headers = {
                'Content-Type': 'application/json',
                'Authorization':'Bearer ' + str(token_response['accessToken'])
                }
                response = requests.request("POST", endpoint, headers=headers, data=payload)
                adhar_value = response.json()
                adhar = CustomUser.objects.filter(txnid=request.data['txnId'])
                adhar.update(mobile=request.data.get('mobile'))
                return Response(response.json())

            else:
                return Response({"message": "invalid token"})
        except Exception as e:
            context = {'status': False, 'message': "Something went wrong."}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MobileOtpVerify(APIView):
    def post(self, request):
        try:
            token_response = generate_token()
            if token_response['status'] == True:
                endpoint = abha_cred.mobile_otp_verify
                payload = json.dumps(request.data)
                print('Bearer ' + str(token_response['accessToken']),"======>")
                headers = {
                'Content-Type': 'application/json',
                'Authorization':'Bearer ' + str(token_response['accessToken'])
                }
                response = requests.request("POST", endpoint, headers=headers, data=payload)
                return Response(response.json())

            else:
                return Response({"message": "invalid token"})
        except Exception as e:
            context = {'status': False, 'message': "Something went wrong."}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateHealthId(APIView):
    def post(self, request):
        try:
            token_response = generate_token()
            if token_response['status'] == True:
                endpoint = abha_cred.create_healthid
                payload = json.dumps(request.data)
                headers = {
                'Content-Type': 'application/json',
                'Authorization':'Bearer ' + str(token_response['accessToken'])
                }
                response = requests.request("POST", endpoint, headers=headers, data=payload)
                health_response=response.json()
                healthid = str(health_response['healthId'])
                print("healthId",str(health_response['healthId']))
                x_token =  'Bearer '  + str(health_response['token'])
                refreshToken =  str(health_response['refreshToken'])
                abha_detail = CustomUser.objects.filter(txnid=request.data['txnId']).first()
                if abha_detail:
                    abha_details = AbhaDetails(health_id=healthid,token=x_token,refreshtoken=refreshToken,user=abha_detail)
                    abha_details.save()
                    return Response(response.json())
                else:
                    return Response({"message": "invalid user"})
            else:
                return Response({"message": "invalid token"})
        except Exception as e:
            context = {'status': False, 'message': "Something went wrong."}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QrCodeAPI(APIView):
    def get(self, request):
        try:
            token_response = generate_token()
            if token_response['status'] == True:
                endpoint = abha_cred.qrCode
                payload = ""
                qr_token_response = AbhaDetails.objects.filter(health_id= request.GET.get('health_id')).last()
                refresh = refresh_token(qr_token_response.refreshtoken)
                qr= 'Bearer ' + str(refresh['accessToken'])
                x_tokens=qr_token_response.token
                if x_tokens:
                    headers = {
                            'Content-Type': 'application/json',
                            'Authorization':'Bearer ' + str(token_response['accessToken']),
                            'X-Token':qr,
                            }
                    response = requests.request("GET", endpoint, headers=headers, data=payload)

                return HttpResponse(response, content_type="image/png") 

        except Exception as e:
            context = {'status': False, 'message': "Something went wrong."}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetCardAPI(APIView):
     def get(self, request):
        try:
            token_response = generate_token()
            if token_response['status'] == True:
                endpoint = abha_cred.getcard
                payload = ""
                qr_token_response = AbhaDetails.objects.filter(health_id= request.GET.get('health_id')).last()
                refresh = refresh_token(qr_token_response.refreshtoken)
                qr= 'Bearer ' + str(refresh['accessToken'])
                headers = {
                        'Content-Type': 'application/json',
                        'Authorization':'Bearer ' + str(token_response['accessToken']),
                        'X-Token':qr,
                        }
                response = requests.request("GET", endpoint, headers=headers, data=payload)
                return HttpResponse(response,content_type="application/pdf")
        except Exception as e:
            context = {'status': False, 'message': "Something went wrong."}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class searchByHealthId(APIView):
    def post(self, request):
        try:
            token_response = generate_token()
            if token_response['status'] == True:
                endpoint = abha_cred.searchByHealthId
                payload = json.dumps(request.data)
                print('Bearer ' + str(token_response['accessToken']),"======>")
                headers = {
                'Content-Type': 'application/json',
                'Authorization':'Bearer ' + str(token_response['accessToken'])
                }

                response = requests.request("POST", endpoint, headers=headers, data=payload)
                return Response(response.json())
            else:
                return Response({"message": "invalid token"})
        except Exception as e:
            context = {'status': False, 'message': "Something went wrong."}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class existsByHealthId(APIView):
    def post(self, request):
        try:
            token_response = generate_token()
            if token_response['status'] == True:
                endpoint = abha_cred.existsByHealthId
                payload = json.dumps(request.data)
                print('Bearer ' + str(token_response['accessToken']),"======>")
                headers = {
                'Content-Type': 'application/json',
                'Authorization':'Bearer ' + str(token_response['accessToken'])
                }

                response = requests.request("POST", endpoint, headers=headers, data=payload)
                return Response(response.json())
            else:
                return Response({"message": "invalid token"})
        except Exception as e:
            context = {'status': False, 'message': "Something went wrong."}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class AuthCert(APIView):
     def get(self, request):
        try:
            token_response = generate_token()
            if token_response['status'] == True:
                endpoint = abha_cred.authcert
                payload = ""
                headers = {
                            'Content-Type': 'application/json',
                            'Authorization':'Bearer ' + str(token_response['accessToken']),
                            }
                response = requests.request("GET", endpoint, headers=headers, data=payload)
                data =response.text
                return HttpResponse(data, content_type='text/plain')
        except Exception as e:
            context = {'status': False, 'message': "Something went wrong."}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MobileLogin(APIView):
    def post(self, request):
        try:
            token_response = generate_token()
            if token_response['status'] == True:
                endpoint = abha_cred.mobilelogin
                payload = json.dumps(request.data)
                print('Bearer ' + str(token_response['accessToken']),"======>")
                headers = {
                'Content-Type': 'application/json',
                'Authorization':'Bearer ' + str(token_response['accessToken'])
                }

                response = requests.request("POST", endpoint, headers=headers, data=payload)
                return Response(response.json())

            else:
                return Response({"message": "invalid token"})
        except Exception as e:
            context = {'status': False, 'message': e}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MobileAPi(APIView):
    def post(self, request):
        print("--MobileOtpVrify--")
        try:
            token_response = generate_token()
            if token_response['status'] == True:
                endpoint = abha_cred.loginverifyOtp
                payload = json.dumps(request.data)
                print("============",payload)
                print('Bearer ' + str(token_response['accessToken']),"======>")
                headers = {
                'Content-Type': 'application/json',
                'Authorization':'Bearer ' + str(token_response['accessToken'])
                }

                response = requests.request("POST", endpoint, headers=headers, data=payload)
                return Response(response.json())

            else:
                return Response({"message": "invalid token"})
        except Exception as e:
            context = {'status': False, 'message': e}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetResponseAPI(APIView):
    def post(self, request):
        data = request.data
        return Response({"data":data})