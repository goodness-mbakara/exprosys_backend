from ..models import TruckQueueManagement, Container
from ..serializers.truck_serializers import TruckQueueManagementSerializer
from django.db.models import Avg, Count, F, Q
import datetime
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


class TruckQueueManagementListCreateView(generics.ListCreateAPIView):
    queryset = TruckQueueManagement.objects.all()
    serializer_class = TruckQueueManagementSerializer
    
    def get_queryset(self):
       return TruckQueueManagement.objects.exclude(status="Departed")
   
    def post(self, request, *args, **kwargs):
        merge_containers = request.data.get('merge_containers', '')
        assigned_terminal = request.data.get('assigned_terminal', '')

        # Split merge_containers string into individual container IDs
        container_ids = merge_containers.split(',') if merge_containers else []

        # Get or create Container instances for each container ID
        containers = []
        for container_id in container_ids:
            container, _ = Container.objects.get_or_create(container_id=container_id.strip())
            containers.append(container)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Assign containers to the TruckQueueManagement instance
        instance = serializer.instance
        instance.merge_containers = merge_containers
        instance.assigned_terminal = assigned_terminal
        instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class TruckQueueManagementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TruckQueueManagement.objects.all()
    serializer_class = TruckQueueManagementSerializer
    lookup_field = 'truck_id'
    
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        merge_containers = request.data.get('merge_containers', '')
        assigned_terminal = request.data.get('assigned_terminal', '')

        # Split merge_containers string into individual container IDs
        container_ids = merge_containers.split(',') if merge_containers else []

        # Get or create Container instances for each container ID
        containers = []
        for container_id in container_ids:
            container, _ = Container.objects.get_or_create(container_id=container_id.strip())
            containers.append(container)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Assign containers to the TruckQueueManagement instance
        instance.merge_containers = merge_containers
        instance.assigned_terminal = assigned_terminal
        instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

def format_time(time_delta):
    if time_delta is None:
        return None
    total_seconds = abs(time_delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    return formatted_time

def calculate_queue_metrics():
    # Total trucks in queue (excluding those that have departed)
    total_trucks_in_queue = TruckQueueManagement.objects.exclude(status='Departed').count()

    # Average queue waiting time (from creation to departure)
    trucks_with_departure_time = TruckQueueManagement.objects.filter(status='Departed')
    average_queue_waiting_time = None
    if trucks_with_departure_time.exists():
        average_queue_waiting_time = trucks_with_departure_time.aggregate(avg_waiting_time=Avg(F('created_at') - F('updated_at')))
        average_queue_waiting_time = average_queue_waiting_time['avg_waiting_time']

    # Average container processing time (assuming this is the time from Loading to Departed)
    trucks_with_processing_time = TruckQueueManagement.objects.filter(status='Departed')
    average_container_processing_time = None
    if trucks_with_processing_time.exists():
        average_container_processing_time = trucks_with_processing_time.aggregate(avg_processing_time=Avg(F('updated_at') - F('created_at')))
        average_container_processing_time = average_container_processing_time['avg_processing_time']

    # Estimated time of next container assignment (this is more complex and depends on various factors)
    # A simple approach could be to use the average waiting time as a proxy
    estimated_time_of_next_container_assignment = average_queue_waiting_time

    data =  {
        'total_trucks_in_queue': total_trucks_in_queue,
        'average_queue_waiting_time': average_queue_waiting_time,
        'average_container_processing_time': average_container_processing_time,
        'estimated_time_of_next_container_assignment': estimated_time_of_next_container_assignment,
    }
    
    formatted_data = {
    "total_trucks_in_queue": data["total_trucks_in_queue"],
    "average_queue_waiting_time": format_time(data["average_queue_waiting_time"]),
    "average_container_processing_time": format_time(data["average_container_processing_time"]),
    "estimated_time_of_next_container_assignment": format_time(data["estimated_time_of_next_container_assignment"])
    }
    
    return formatted_data


@api_view(['GET'])
def get_queue_metrics(request):
    try:
        metrics = calculate_queue_metrics()
        return Response(metrics, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
