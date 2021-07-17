from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from pure_pagination import Paginator, PageNotAnInteger

from shop_accounts.forms import UserTicketAnswerForm, UserTicketForm
from shop_accounts.models import UserProfile
from shop_contact.models import (
    UserTicket,
    UserTicketAnswer,
    set_read_mark_for_answers,
)
from tinakala.utils import profile_completion_required


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_ticket(request):
    ticket_form = UserTicketForm(request.POST or None)
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    tickets = []
    for ticket in UserTicket.objects.filter(user=request.user).order_by('-timestamp'):
        tickets.append({
            'id': ticket.id,
            'title': ticket.title,
            'timestamp': ticket.timestamp,
            'answers': UserTicketAnswer.objects.get_ticket_answers(ticket=ticket).count(),
            'unread': UserTicketAnswer.objects.get_unread_answer_count(user=request.user, ticket=ticket),
            'active': ticket.active,
        })
    context = {
        'tickets': Paginator(tickets, request=request, per_page=5).page(page),
        'ticket_form': ticket_form,
    }
    return render(request, 'accounts/SiteUserTicket.html', context)


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_create_ticket(request):
    ticket_form = UserTicketForm(request.POST or None)
    if ticket_form.is_valid():
        ticket = UserTicket.objects.create(
            user=request.user,
            title=ticket_form.cleaned_data.get('title'),
            question=ticket_form.cleaned_data.get('question')
        )
        ticket.save()
        messages.success(request, 'تیکت شما با موفقیت ایجاد شد.')
        return redirect('auth:user-ticket')
    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'accounts/SiteUserTicketAdd.html', context)


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_ticket_detail(request, ticket_id):
    ticket = get_object_or_404(UserTicket, user=request.user, id=ticket_id)
    answers = UserTicketAnswer.objects.get_ticket_answers(ticket=ticket)
    set_read_mark_for_answers(answers)
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    context = {
        'ticket': ticket,
        'answers': Paginator(answers, request=request, per_page=5).page(page),
    }
    # control ticket activate/deactivate
    if ticket.active:
        answer_form = UserTicketAnswerForm(request.POST or None)
        context['answer_form'] = answer_form
        if answer_form.is_valid():
            answer = UserTicketAnswer.objects.create(
                ticket=ticket,
                user=request.user,
                answer=answer_form.cleaned_data.get('answer')
            )
            answer.save()
            messages.success(request, 'تیکت شما با موفقیت ارسال شد.')
    return render(request, 'accounts/SiteUserTicketDetail.html', context)
