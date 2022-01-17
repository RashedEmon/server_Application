from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from api.serializers import BusSerializer, BusDetailsView, Bus_Details_From_Token_serializer
from rest_framework.authtoken.models import Token
# from django.db.models.utils import list_to_queryset

# Create your views here.
from core.models import Bus, Bus_Route


@api_view(["GET"])
def SearchView(request, source, destination):

    try:
        routes = Bus_Route.objects.filter(
            start_place__iexact=source, end_place__iexact=destination, is_on=True
        )
        if routes.exists():
            infoList = []
            for route in routes:
                info = {}
                info["bus_id"] = route.bus.bus_id
                info["bus_name"] = route.bus.bus_name
                info["bus_type"] = route.bus.bus_type
                info["bus_active_status"] = route.bus.bus_active_status
                info["source"] = route.start_place
                info["destination"] = route.end_place
                info["departureTime"] = route.departure_time
                info["is_on"] = route.is_on
                info["routes"] = route.routes
                infoList.append(info)

            # print(routes)
            # print(source)
            # print(destination)
            info = BusSerializer(infoList, many=True)
            return Response(info.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "No bus found for the given source and destination"},
                status=status.HTTP_404_NOT_FOUND,
            )
    except Bus_Route.DoesNotExist:
        return Response(
            data={"message": "No bus found for this query"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
def BusDetailsView(request, id):
    buses = Bus_Route.objects.filter(bus__bus_id=id)
    infoList = []

    for bus in buses:
        info = {}
        info["bus_name"] = bus.bus.bus_name
        info["bus_type"] = bus.bus.bus_type
        info["source"] = bus.start_place
        info["destination"] = bus.end_place
        info["departureTime"] = bus.departure_time
        info["routes"] = bus.routes
        infoList.append(info)

    # print(routes)
    # print(source)
    # print(destination)
    info = BusSerializer(infoList, many=True)
    return Response(info.data)


@api_view(["GET"])
def bus_from_token(request):
    bus_info = {

    }
    try:
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.split(' ')[1]
            print(token)
            bus = Token.objects.get(key=token).user.bus
            bus_info['bus_name'] = bus.bus_name.lower()
            bus_info['bus_id'] = bus.bus_id
            print(bus_info)
            info = Bus_Details_From_Token_serializer(bus_info)
            return Response(info.data, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "not registered"}, status=status.HTTP_404_NOT_FOUND)
    except Token.DoesNotExist:
        return Response({"msg": "not found"}, status=status.HTTP_404_NOT_FOUND)
