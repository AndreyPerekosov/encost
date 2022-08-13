from django.shortcuts import render
from .service.filters import Filter

# Создаем словарь для элементов выпадающих списков и начальный контент. В случае небольшного объема данных считаю допустимым
# Можно также использовать сессии и хранить в кэше (redis, mongoDB)
f = Filter()
DICT_ITEMS = {'clients': f.get_clients(), 'equipments': f.get_equips(),
              'modes': f.get_modes(), 'content': '',
              'row_names': ['Client', 'Equipment', 'Start', 'Stop', 'Minutes', 'Mode']}


def main_context(view):
    def wrapper(request):
        f = Filter()
        context = DICT_ITEMS
        return view(request, context, f)

    return wrapper


@main_context
def index(*args, **kwargs):
    request, context, f = args
    return render(request, 'filter/index.html', context=context)


@main_context
def client_filter(*args, **kwargs):
    request, context, f = args
    client = request.POST['client_filter']
    context['content'] = f.client_filter(client)
    return render(request, 'filter/index.html', context=context)


@main_context
def equipment_filter(*args, **kwargs):
    request, context, f = args
    equipment = request.POST['equipment_filter']
    context['content'] = f.equipment_filter(equipment)
    return render(request, 'filter/index.html', context=context)


@main_context
def mode_filter(*args, **kwargs):
    request, context, f = args
    mode = request.POST['mode_filter']
    context['content'] = f.mode_filter(mode)
    return render(request, 'filter/index.html', context=context)


@main_context
def minute_filter(*args, **kwargs):
    request, context, f = args
    minute = request.POST['minute_filter']
    context['content'] = f.minute_filter(minute)
    return render(request, 'filter/index.html', context=context)


@main_context
def start_date_filter(*args, **kwargs):
    request, context, f = args
    start_date = request.POST['start_date_filter']
    context['content'] = f.start_date_filter(start_date)
    return render(request, 'filter/index.html', context=context)


@main_context
def start_time_filter(*args, **kwargs):
    request, context, f = args
    start_time = request.POST['start_time_filter']
    context['content'] = f.start_time_filter(start_time)
    return render(request, 'filter/index.html', context=context)


@main_context
def end_date_filter(*args, **kwargs):
    request, context, f = args
    end_date = request.POST['end_date_filter']
    context['content'] = f.end_date_filter(end_date)
    return render(request, 'filter/index.html', context=context)


@main_context
def end_time_filter(*args, **kwargs):
    request, context, f = args
    end_time = request.POST['end_time_filter']
    context['content'] = f.end_time_filter(end_time)
    return render(request, 'filter/index.html', context=context)
