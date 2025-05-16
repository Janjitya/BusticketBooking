from django.urls import path, include
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="regsiter"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('bus/create/', views.BusCreateView.as_view(), name="create_bus"),
    path('bus/update/<int:bus_id>', views.BusUpdateDeleteView.as_view(), name='bus_detail'),
    path('schedule/create/', views.CreateScheduleView.as_view(), name="create_schedule"),
    path('schedule/update/<int:schedule_id>', views.UpdateDeleteScheduleView.as_view(), name="schedule_detail"),
    path('bus/search/', views.BusSearchView.as_view(), name="bus_search"),
    path('bus/book/', views.BookSeatView.as_view(), name="book_seat"),
    path('bookings/history/', views.BookingHistoryView.as_view(), name="booking_history"),
    path('bus/seat-layout/<int:schedule_id>', views.SeatLayoutView.as_view(), name="seat-layout"),
    path('bookings/<int:booking_id>/cancel/', views.CancelBookingView.as_view(), name="cancel_booking"),

    #documentation urls
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    


    

]