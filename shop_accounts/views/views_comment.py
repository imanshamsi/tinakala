"""
shop_accounts -> views -> user comment manager methods
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from pure_pagination import Paginator, PageNotAnInteger

from shop_accounts.models import UserProfile, UserCommentVote
from shop_products.models import ProductComment
from tinakala.utils import profile_completion_required, get_total_average


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_comment(request):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    comments = []
    for comment in ProductComment.objects.filter(user=request.user, promote=True):
        total_avg = ProductComment.objects.filter(product=comment.product).values_list('worth', 'quality', 'function')
        comments.append({
            'id': comment.id,
            'title': comment.title,
            'comment': comment.comment,
            'verified': comment.verified,
            'positive': comment.usercommentvote_set.filter(vote=True).count(),
            'negative': comment.usercommentvote_set.filter(vote=False).count(),
            'product_code': comment.product.code,
            'product_slug': comment.product.slug,
            'product_avatar': comment.product.avatar.url,
            'product_avg': get_total_average(total_avg),
        })

    context = {
        'comments': Paginator(comments, request=request, per_page=8).page(page),
    }
    return render(request, 'accounts/SiteUserComment.html', context)


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_comment_delete(request, *args, **kwargs):
    comment_id = kwargs.get('comment_id')
    comment = get_object_or_404(ProductComment, id=comment_id)
    if not comment.promote:
        raise Http404('کامنتی یافت نشد')
    comment.promote = False
    comment.save()
    messages.success(request, f'نظر شما با موفقیت حذف شد.')
    return redirect('auth:user-comment')


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_comment_positive_vote(request, *args, **kwargs):
    comment_id = kwargs.get('comment_id')
    comment = get_object_or_404(ProductComment, id=comment_id)
    existed_user_vote: UserCommentVote = UserCommentVote.objects.filter(user=request.user, comment=comment).first()
    if existed_user_vote:
        existed_user_vote.positive_comment_vote()
    else:
        existed_user_vote = UserCommentVote.objects.create(user=request.user, comment=comment, vote=True)
        existed_user_vote.save()
    messages.success(request, f'نظر مثبت شما برای کامنت ({comment.user.get_full_name()}) با موفقیت ثبت شد.')
    return redirect('auth:user-profile')


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_comment_negative_vote(request, *args, **kwargs):
    comment_id = kwargs.get('comment_id')
    comment = get_object_or_404(ProductComment, id=comment_id)
    existed_user_vote: UserCommentVote = UserCommentVote.objects.filter(user=request.user, comment=comment).first()
    if existed_user_vote:
        existed_user_vote.negative_comment_vote()
    else:
        existed_user_vote = UserCommentVote.objects.create(user=request.user, comment=comment, vote=False)
        existed_user_vote.save()
    messages.success(request, f'نظر منفی شما برای کامنت ({comment.user.get_full_name()}) با موفقیت ثبت شد.')
    return redirect('auth:user-profile')
