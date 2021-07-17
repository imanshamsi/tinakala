import socket


def get_visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.splite(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    try:
        socket.inet_aton(ip)
        ip_valid = True
    except socket.error:
        ip_valid = False

    result = {
        'ip': ip,
        'valid': ip_valid,
    }
    return result
