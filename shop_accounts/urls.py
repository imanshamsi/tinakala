from django.urls import path

from shop_accounts.views import (
    login_user,
    logout_user,
    register_user,
    user_reset_password,
    user_change_profile,
    user_verify_phone,
    user_send_otp,
    user_profile,
    user_address,
    user_address_detail,
    user_address_delete,
    user_get_cities_of_state,
    user_favorite,
    user_favorite_add,
    user_favorite_delete,
    user_comment,
    user_comment_positive_vote,
    user_comment_negative_vote,
    user_comment_delete,
    user_ticket,
    user_create_ticket,
    user_ticket_detail,
    user_orders,
    user_order_detail,
    LastVisitedView,
)

app_name = 'auth'
urlpatterns = [
    # User Authentication Methods
    path('auth/login', login_user, name='login'),
    path('auth/logout', logout_user, name='logout'),
    path('auth/register', register_user, name='register'),
    path('auth/reset-password', user_reset_password, name='reset-password'),
    # User Profile Methods
    path('account/user-panel', user_profile, name='user-profile'),
    path('account/user-change-profile', user_change_profile, name='change-profile'),
    path('account/user-send-otp', user_send_otp, name='send-otp'),
    path('account/user-verify-phone', user_verify_phone, name='verify-phone'),
    # User Profile Address Methods
    path('account/user-address', user_address, name='user-address'),
    path('account/user-address/<int:address_id>/edit', user_address_detail, name='user-address-edit'),
    path('account/user-address/<int:address_id>/delete', user_address_delete, name='user-address-delete'),
    path('account/user-get-cities-of-state', user_get_cities_of_state, name='user-get-cities-of-state'),
    # User Profile Favorite Methods
    path('account/user-favorite', user_favorite, name='user-favorite'),
    path('account/user-favorite/<slug>/add', user_favorite_add, name='user-favorite-add'),
    path('account/user-favorite/<slug>/delete', user_favorite_delete, name='user-favorite-delete'),
    # User Profile Comment Methods
    path('account/user-comment', user_comment, name='user-comment'),
    path('account/user-comment/<comment_id>/delete', user_comment_delete, name='user-comment-delete'),
    path('account/user-comment/<comment_id>/pos-vote', user_comment_positive_vote, name='user-comment-positive-vote'),
    path('account/user-comment/<comment_id>/neg-vote', user_comment_negative_vote, name='user-comment-negative-vote'),
    # User Profile Ticket Methods
    path('account/ticket', user_ticket, name='user-ticket'),
    path('account/ticket/add', user_create_ticket, name='user-add-ticket'),
    path('account/ticket/<ticket_id>', user_ticket_detail, name='user-ticket-show'),
    # User Orders Methods
    path('account/invoice', user_orders, name='user-invoice'),
    path('account/invoice/<str:order_code>', user_order_detail, name='user-invoice-detail'),
    # User Last Visited Product Methods
    path('recent-visits', LastVisitedView.as_view(), name='recent-visits'),
]

