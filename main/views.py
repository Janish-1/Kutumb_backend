from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.contrib.auth import authenticate,login
import random
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from django.conf import settings
from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.env import Env
import uuid  
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest

# from django.contrib.auth.hashers import check_password

class UserList(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            print("idsbgakusbg")
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error":"User DoesNotExist"})

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)        
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            new_password = serializer.validated_data['new_password']
            password = serializer.validated_data['password']            
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)            
            if not user.check_password(password):
                return Response({'message': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)            
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class loginview(APIView):
class UserLoginAPIView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.get(email=email)
        print(email,password,user)
        print(user)   
        
        if user is not None:
            otp = ''.join(random.choices('0123456789', k=6))  # Generate a 6-digit OTP
            print(otp)
            user.otp = otp
            user.save()
            authenticated_user = authenticate(request, username=user, password=password)
            print(authenticated_user)
            if authenticated_user is not None:
                login(request, authenticated_user)
                print("login")
                # return Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
            # user = authenticate(username=user.username,password=password)  
            subject = 'Password Reset OTP'
            message = f'Your OTP for password reset is: {otp}'
            print(message)
            from_email = 'sonalisharma7224@gmail.com'
            recipient_list = [user.email]
            # recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)
            # else:
            #     return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'message': user.id}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
    

class otpverify(APIView):
    def post(self, request, format=None):
        user_id = request.data.get('user_id')
        otp = request.data.get('otp')
        print(otp,user_id)
        try:
            user = CustomUser.objects.get(id=user_id)
            print(user.otp)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        print(type(otp),type(user.otp))
        if user.otp == otp:
            user.otp = None  # Set OTP to None after successful verification
            user.save()
            print(user,user.password)
            return Response({'message':"Logged In Successfully"},status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


# class otpverify(APIView):
#     def post(self, request,format=None):
#         id = request.data.get('user_id')
#         otp = request.data.get('otp')
#         user = CustomUser.objects.get(id=id)
#         print(id,otp,user.otp,user)
#         if int(user.otp) == otp:
#             print("efzfasdfasdfasdf")
#             username = user.username
#             print(user,username)
#             user.otp = None
#             user.save()   
#             return Response({'message':"Logged In Successfully"},status=status.HTTP_200_OK)
#         return Response({'Error':"Invalid OTP"},status=status.HTTP_400_BAD_REQUEST)
        # return Response({'Error':"Logged In Successfully"})

class PasswordUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordUpdateSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            user_id = serializer.validated_data['user_id']
            user = CustomUser.objects.get(id=user_id)
            print(user.otp,otp)
            # user = self.verify_otp(2, otp)
            # print(user)
            if user.otp == otp:
                # Update the password
                print("pkkooo")
                user.set_password(new_password)
                user.otp = None
                user.save()

                return Response({'ok': 'Password updated successfully'})
            else:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   


class ForgotPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)
            print(user)
            otp_code = get_random_string(length=6, allowed_chars='1234567890')
            # CustomUser.objects.create(user=user, otp=otp_code)
            print(type(otp_code))
            user.otp = int(otp_code)
            user.save()
            print(user.otp)
            subject = 'Password Reset OTP'
            message = f'Your OTP for password reset is: {otp_code}'
            print(message)
            from_email = 'sonalisharma7224@gmail.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            print("ok")
            return Response({'ok': f'OTP sent successfully {user.id}'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailAPIView(APIView):
    def patch(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CommentCreateAPIView(APIView):
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            post.comments_count += 1
            post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PostListAPIViews(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostsSerializer(posts, many=True)
        return Response(serializer.data)

class LikePostAPIView(APIView):
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)
        post.likes += 1
        post.save()
        return Response({'likes': post.likes}, status=status.HTTP_200_OK)
    

class UnLikePostAPIView(APIView):
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)
        post.likes -= 1
        post.save()
        return Response({'likes': post.likes}, status=status.HTTP_200_OK)

class ActionListDonationAPIView(APIView):
    def get(self, request):
        actions = Action.objects.filter(active=True,type='donation')
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)
    
class ActionListCelebrationAPIView(APIView):
    def get(self, request):
        actions = Action.objects.filter(active=True,type='celebration')
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)

class ActionListAPIView(APIView):
    def get(self, request):
        actions = Action.objects.filter(active=True)
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ActionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GalleryListAPIView(APIView):
    def get(self, request):
        galleries = Gallery.objects.filter(active=True)
        serializer = GallerySerializer(galleries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RequestTableAPIView(APIView):
    def post(self, request):
        
        serializer = RequestTableSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            main = CustomUser.objects.get(username=user)
            print(main.mobileno)
            serializer.save(requester_mobile_no=main.mobileno)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        galleries = Request_Table.objects.all()
        serializer = RequestTableSerializer(galleries,many=True)
        return Response(serializer.data)
        
        
        

class SubscriptionPaymentView(APIView):
    def post(self, request, *args, **kwargs):
        userid = request.data.get('userID') 
        typeid = request.data.get('actionID')
        unique_transaction_id = str(uuid.uuid4())[:-2]
        user = CustomUser.objects.get(id=userid)
        action = Action.objects.get(id=typeid)
        print(user,action)      
        payment_amount = action.amount  
        # Set other parameters for payment request
        ui_redirect_url = "http://kutumb.itpandit.in"  # Include redirect URL
        s2s_callback_url = "https://www.merchant.com/callback"  
        pay_page_request = PgPayRequest.pay_page_pay_request_builder(
            merchant_transaction_id=unique_transaction_id,
            amount=payment_amount,
            merchant_user_id=str(user.id),
            callback_url=s2s_callback_url,
            redirect_url=ui_redirect_url
        )
        merchant_id = settings.PHONEPE_MERCHANT_ID
        salt_key = settings.PHONEPE_SALT_KEY
        salt_index = 1  # Adjust this based on your PhonePe configuration
        env = Env.UAT  # Change to Env.PROD when you go live
        phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env)
        pay_page_response = phonepe_client.pay(pay_page_request)
        print(pay_page_response)
        pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
        payment = Transctions.objects.create(
            user=user,
            for_action=action,
            amount=action.amount,
            request_type=action.type,
            status="Pending",
            # transction_id= unique_transaction_id,

        )
        print(payment,unique_transaction_id)
        return Response({'payment_url': pay_page_url, 'payment_id': payment.id}, status=status.HTTP_200_OK)
    