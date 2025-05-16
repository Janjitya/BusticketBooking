from django.shortcuts import render, get_object_or_404
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ProfileSerializer, BusSerializer, ScheduleSerializer, BookingSerializer
from django.conf import settings 
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from .models import Profile, Bus, Schedule, Booking
from datetime import datetime
from django.utils import timezone

User = get_user_model()
# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)

            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'detail': 'invalid credentials'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class BusCreateView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BusSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BusUpdateDeleteView(APIView):

    permission_classes = [IsAdminUser]
    def get(self, request, bus_id):
        bus = get_object_or_404(Bus, id=bus_id)
        serializer = BusSerializer(bus)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, bus_id):
        bus = get_object_or_404(Bus, id=bus_id)
        serializer = BusSerializer(bus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, bus_id):
        bus = get_object_or_404(Bus, id=bus_id)
        bus.delete()

        return Response({"message":"Bus deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class CreateScheduleView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ScheduleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UpdateDeleteScheduleView(APIView):

    permission_classes = [IsAdminUser]
    def get(self, request, schedule_id):
        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            return Response({"error":"Schedule not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ScheduleSerializer(schedule)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, schedule_id):
        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            return Response({"error":"Schedule not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ScheduleSerializer(schedule, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, schedule_id):
        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            return Response({"error":"Schedule not found"}, status=status.HTTP_404_NOT_FOUND)
        
        schedule.delete()
        
        return Response({"message":"Schedule deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class BusSearchView(APIView):

    def get(self, request):
        source = request.query_params.get('source')
        destination = request.query_params.get('destination')
        travel_date = request.query_params.get('date')

        if not(source and destination and travel_date):
            return Response({"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            date_obj = datetime.strptime(travel_date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error":"Invalid date format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        

        buses = Bus.objects.filter(source__iexact=source, destination__iexact=destination)
        result = []

        for bus in buses:
            schedule = Schedule.objects.filter(bus=bus, travel_date=date_obj).first()
            if schedule:
                serializer = BusSerializer(bus)
                bus_data = serializer.data
                bus_data['available_seats'] = schedule.available_seats
                bus_data['travel_date'] = str(schedule.travel_date)
                result.append(bus_data)

        return Response(result, status=status.HTTP_200_OK)
    
class BookSeatView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        bus_id = request.data.get('bus_id')
        schedule_id = request.data.get('schedule_id')
        seat_numbers = request.data.get('seat_numbers')

        if not all([bus_id, schedule_id, seat_numbers]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            schedule = Schedule.objects.get(id=schedule_id, bus_id = bus_id)
        except Schedule.DoesNotExist:
            return Response({"error": "Invalid schedule or bus"}, status=status.HTTP_400_BAD_REQUEST)
        
        if schedule.available_seats < len(seat_numbers):
            return Response({"error": "Not enough seats available"}, status=status.HTTP_400_BAD_REQUEST)
        
        fare = schedule.bus.fare
        total_amount = fare * len(seat_numbers)

        booking = Booking.objects.create(
            passenger = user,
            bus_id = bus_id,
            schedule_id = schedule_id,
            seat_numbers = seat_numbers,
            total_amount = total_amount
        )

        schedule.available_seats -= len(seat_numbers)
        schedule.save()

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BookingHistoryView(generics.ListAPIView):

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(passenger=self.request.user).order_by('-booking_time')
    

class SeatLayoutView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, schedule_id):

        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            return Response({"error":"Schedule not found"}, status=status.HTTP_404_NOT_FOUND)
        

        booked_seats = Booking.objects.filter(schedule=schedule, is_cancelled=False).values_list('seat_numbers',flat=True)

        all_booked = [seat for sublist in booked_seats for seat in sublist]

        return Response(
            {
                "bus": schedule.bus.name,
                "travel_date": schedule.travel_date,
                "total_seats": schedule.bus.total_seats,
                "booked_seats": all_booked,
                "available_seats": schedule.available_seats
            }
        )
    
class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request, booking_id):

        try:
            booking = Booking.objects.get(id=booking_id, passenger= request.user)
        except Booking.DoesNotExist:
            return Response({"error":"Booking not found"},status=status.HTTP_404_NOT_FOUND)
        

        if booking.is_cancelled:
            return Response({"message":"Booking is already cancelled"}, status=status.HTTP_400_BAD_REQUEST)
        

        booking.is_cancelled = True
        booking.cancelled_at = timezone.now()
        booking.save()

        return Response({"message":"Booking cancelled successfully"})



