if 'region' in request.GET:
    units = models.Unit.objects.none()
    regions = request.GET['region'].split(',')
    for i in range(0, len(regions)):
        units |= units_all.filter(region__icontains=regions[i])
else:
    units = units_all
if 'search' in request.GET and len(request.GET['search']) > 0:
    units = units.filter(
        Q(name__icontains=request.GET['search']) |
        Q(model_name__icontains=request.GET['search']) |
        Q(services__name__icontains=request.GET['search']) |
        Q(category__name__icontains=request.GET['search'])
    ).distinct()

if 'min_rating' in request.GET and 'max_rating' in request.GET:
    units = units.filter(
        rating__gte=request.GET['min_rating'],
        rating__lte=request.GET['max_rating']
    )

if 'min_price_UAH_from' in request.GET:
    units = units.filter(minimal_price_UAH__gte=request.GET['min_price_UAH_from'])
if 'min_price_UAH_to' in request.GET:
    units = units.filter(minimal_price_UAH__lte=request.GET['min_price_UAH_to'])
if 'min_price_USD_from' in request.GET:
    units = units.filter(minimal_price_USD__gte=request.GET['min_price_USD_from'])
if 'min_price_USD_to' in request.GET:
    units = units.filter(minimal_price_USD__lte=request.GET['min_price_USD_to'])
if 'min_price_EUR_from' in request.GET:
    units = units.filter(minimal_price_EUR__gte=request.GET['min_price_EUR_from'])
if 'min_price_EUR_to' in request.GET:
    units = units.filter(minimal_price_EUR__lte=request.GET['min_price_EUR_to'])

if 'calendar_ranges' in request.GET:
    ids = []
    calendars_qs = models.UnitCalendar.objects.all()
    for date in request.GET['calendar_ranges'].split(' '):
        dates = date.split(',')
        calendars = calendars_qs.filter(
            start_date__gte=dates[0], end_date__lte=dates[1]
        )
        if not calendars.exists():
            errors.append({
                'date_error': f'There are no units in this range: {dates[0]} - {dates[1]}'
            })
        ids += [unit.id for unit in calendars]
    if ids:
        units = units.exclude(id__in=ids)

if 'sort_price' in request.GET:
    if request.GET['sort_price'] == 'inc':
        units = units.order_by('minimal_price_UAH')
    if request.GET['sort_price'] == 'dec':
        units = units.order_by('-minimal_price_UAH')

if 'category' in request.GET:
    units = units.filter(category__in=request.GET['category'].split(',')).distinct()

if 'model_name' in request.GET:
    units = units.filter(model_name__in=request.GET['model_name'].split(',')).distinct()

if 'manufacturers' in request.GET:
    units = units.filter(manufacturer__name__in=request.GET['manufacturers'].split(',')).distinct()

if 'services' in request.GET:
    units = units.filter(services__in=request.GET['services'].split(',')).distinct()