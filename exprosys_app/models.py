from datetime import timezone

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        # user.is_active = True
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, unique=True)
    job_title = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    location_information = models.BooleanField(default=False)
    data_sharing = models.BooleanField(default=False)
    data_retention = models.BooleanField(default=False)
    data_storage = models.BooleanField(default=False)
    usage_analytics = models.BooleanField(default=False)
    payment_information = models.BooleanField(default=False)
    preferred_terminal_team = models.CharField(max_length=150)
    language_preference = models.CharField(max_length=150)
    accessibility_preference = models.JSONField(
        default=dict
    )  # storing fontsize, font type, mode
    account_recovery_email = models.EmailField()
    account_recovery_phone = models.CharField(max_length=15)
    account_recovery_question = models.CharField(max_length=255)
    account_recovery_answer = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Container(models.Model):
    CONTAINER_SIZES = [("20", "20 feet"), ("40", "40 feet")]
    CONTAINER_TYPES = [("standard", "Standard"), ("reefer", "Reefer")]
    STATUS_CHOICES = [
        ("in transit", "In Transit"),
        ("at port", "At Port"),
        ("delivered", "Delivered"),
    ]

    container_id = models.AutoField(primary_key=True)
    container_size = models.CharField(max_length=200, null=True, blank=True)
    container_type = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    export_type = models.CharField(max_length=200, null=True, blank=True)
    import_type = models.CharField(max_length=200, null=True, blank=True)
    origin = models.CharField(max_length=100, null=True, blank=True)
    booking_number = models.CharField(max_length=50, blank=True, null=True)
    shipping_line = models.CharField(max_length=100, null=True, blank=True)
    arrival_date = models.DateField(null=True, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    vessel_name = models.CharField(max_length=100, null=True, blank=True)
    exporter = models.ForeignKey(
        "Exporter", on_delete=models.CASCADE, null=True, blank=True
    )
    destination = models.CharField(max_length=100, null=True, blank=True)
    vessel_assignment = models.CharField(
        max_length=100, default="Not assigned", null=True, blank=True
    )
    cargo_type = models.CharField(
        max_length=50, default="general", null=True, blank=True
    )
    last_update = models.DateTimeField(auto_now=True, null=True, blank=True)
    estimated_time_of_arrival = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.container_id


class ContainerEvent(models.Model):
    container = models.ForeignKey(
        Container, related_name="events", on_delete=models.CASCADE
    )
    event_date = models.DateField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.container.container_id} - {self.description}"


class ContainerTransfer(models.Model):
    container = models.ForeignKey(
        "Container", related_name="transfers", on_delete=models.CASCADE
    )
    transfer_from = models.CharField(max_length=100)
    transfer_to = models.CharField(max_length=100)
    transfer_date = models.DateField()
    confirmation_code = models.CharField(max_length=50)
    reasons_for_transfer = models.TextField()

    def __str__(self):
        return f"Transfer of {self.container.container_id} from {self.transfer_from} to {self.transfer_to}"


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ("invoice", "Invoice"),
        ("payment", "Payment"),
    ]
    exporter = models.ForeignKey(
        "Exporter", on_delete=models.CASCADE, related_name="transactions"
    )
    date = models.DateTimeField()
    invoice_number = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.invoice_number} - {self.transaction_type}"


class Agency(models.Model):
    agency_id = models.AutoField(primary_key=True)
    agency_name = models.CharField(max_length=255, null=True, blank=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state_province = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    billing_address = models.CharField(max_length=255, null=True, blank=True)
    letter_of_authority = models.FileField(
        upload_to="authorities/", null=True, blank=True
    )

    # Services Offered
    container_handling = models.BooleanField(default=False, null=True, blank=True)
    cargo_handling = models.BooleanField(default=False, null=True, blank=True)
    customs_clearance = models.BooleanField(default=False, null=True, blank=True)
    warehousing = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.agency_name


class Agent(models.Model):
    agent_id = models.AutoField(primary_key=True)
    agent_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    agency_name = models.CharField(max_length=255)
    agency_id = models.ForeignKey(
        "Agency", related_name="agents", on_delete=models.CASCADE
    )
    email = models.EmailField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to="profile_pics/")
    services_offered = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.agent_name


class GateAccessControl(models.Model):
    time_of_access = models.DateTimeField()
    gate_entry_point = models.CharField(max_length=100)
    security_officer_name = models.CharField(max_length=100)
    security_officer_id = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=50)
    booking_verification_number = models.CharField(max_length=100)
    access_type = models.CharField(max_length=50)
    authorized_exit_time = models.DateTimeField(null=True, blank=True)
    authorized_areas = models.TextField()
    reason_for_access = models.TextField()
    purpose_of_visit = models.TextField()
    destination = models.TextField()
    security_checkpoints = models.CharField(max_length=250, null=True, blank=True)
    inspection_result = models.CharField(max_length=100, null=True, blank=True)
    access_granted = models.BooleanField(default=False)
    access_denied_reason = models.TextField(blank=True, null=True)
    security_code = models.CharField(max_length=100, null=True, blank=True)
    vehicle_type = models.CharField(max_length=50, null=True, blank=True)
    drivers = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.vehicle_number


class InboundPreGateEntry(models.Model):
    container_id = models.CharField(max_length=100, blank=True, null=True)
    eto_gate_pass_no = models.CharField(max_length=100, blank=True, null=True)
    gate_in_date = models.DateField(blank=True, null=True)
    license_plate_number = models.CharField(max_length=50, blank=True, null=True)
    driver_name = models.CharField(max_length=50, blank=True, null=True)
    driver_number = models.CharField(max_length=50, blank=True, null=True)
    company_organization = models.CharField(max_length=100)
    hazardous_material_check = models.BooleanField(default=False)
    security_clearance_check = models.BooleanField(default=False)
    temperature_senstive_cargo = models.BooleanField(default=False)
    entry_date_time = models.DateTimeField(null=True, blank=True)
    truck_id = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    cargo_description = models.CharField(max_length=50, blank=True, null=True)
    arrival_date_time = models.DateTimeField(null=True, blank=True)
    gate_pass_status = models.CharField(max_length=50, blank=True, null=True)
    special_instructions = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.container_id


class OutboundGateExit(models.Model):
    container_id = models.CharField(max_length=100, blank=True, null=True)
    truck_number = models.CharField(max_length=50, blank=True, null=True)
    driver_name = models.CharField(max_length=100, blank=True, null=True)
    driver_contact = models.CharField(max_length=50, blank=True, null=True)
    documentation_verification = models.BooleanField(default=False)
    cargo_inspection = models.BooleanField(default=False)
    driver_verification = models.BooleanField(default=False)
    destination = models.CharField(max_length=300, blank=True, null=True)
    journey_code = models.CharField(max_length=100, blank=True, null=True)
    last_payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    validity_date = models.DateField(blank=True, null=True)
    gate_out_officer = models.CharField(max_length=100, null=True, blank=True)
    seal_information = models.CharField(max_length=100, null=True, blank=True)
    seal_condition = models.CharField(max_length=50, null=True, blank=True)
    security_check = models.BooleanField(default=False, null=True, blank=True)
    security_check_note = models.CharField(max_length=100, null=True, blank=True)
    security_code = models.CharField(max_length=100, null=True, blank=True)
    date_time = models.DateTimeField(null=True, blank=True)
    attachments = models.FileField(null=True, blank=True, upload_to = 'gate_uploads/')

    def __str__(self):
        return f"{self.truck_number} - {self.container_id}"


class TruckQueueManagement(models.Model):
    truck_id = models.CharField(max_length=50, unique=True)
    company_organization = models.CharField(max_length=100)
    driver_name = models.CharField(max_length=100, null=True, blank=True)
    driver_phone_number = models.CharField(max_length=50, null=True, blank=True)
    priority = models.CharField(
        max_length=10, null=True, blank=True
    )  # e.g., High, Medium, Low
    status = models.CharField(max_length=50)  # e.g., Waiting, Loading, Departed
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    merge_containers = models.CharField(max_length=255, null=True, blank=True)
    assigned_terminal = models.CharField(max_length=100, null=True, blank=True)
    notes = models.CharField(max_length=100, null=True, blank=True)
    instruction = models.TextField(null=True, blank=True)
    container_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.truck_id} - {self.driver_name}"


class ContainerCycleManagement(models.Model):
    CYCLE_TYPES = [
        ("Export Delivery", "Export Delivery"),
        ("Import Receipt", "Import Receipt"),
        ("Empty Return", "Empty Return"),
    ]
    cycle_type = models.CharField(max_length=50, choices=CYCLE_TYPES)
    destination_terminal = models.CharField(max_length=100)
    booking_number = models.CharField(max_length=50)
    delivery_date = models.DateField()
    eir_number = models.CharField(max_length=50)
    container_list = models.TextField()
    update_container_cycle = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cycle_type} - {self.booking_number}"


class ProcessEquipmentInterchange(models.Model):
    CONTAINER_PART_CHOICES = [
        ("All Over", "All Over"),
        ("Top", "Top"),
        ("Side", "Side"),
    ]
    EXPORT_TYPE_CHOICES = [
        ("Full", "Full"),
        ("Empty", "Empty"),
    ]
    container_id = models.CharField(max_length=50)
    container_part = models.CharField(max_length=50, choices=CONTAINER_PART_CHOICES)
    transport_id = models.CharField(max_length=50)
    driver_id = models.CharField(max_length=50)
    export_type = models.CharField(max_length=50, choices=EXPORT_TYPE_CHOICES)
    damage_status = models.CharField(max_length=50)
    exporter = models.ForeignKey("Exporter", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.container_id} - {self.exporter.exporter_name}"


class EquipmentInterchangeReceipt(models.Model):
    INTERCHANGE_TYPES = [
        ("Incoming", "Incoming"),
        ("Outgoing", "Outgoing"),
    ]
    INTERCHANGE_PARTIES = [
        ("Carrier", "Carrier"),
        ("Shipper", "Shipper"),
        ("Receiver", "Receiver"),
        ("Other", "Other"),
    ]
    voyage_details_vessel_name = models.CharField(max_length=100)
    voyage_details_voyage_number = models.CharField(max_length=50)
    voyage_details_port_of_loading = models.CharField(max_length=100)
    voyage_details_port_of_discharge = models.CharField(max_length=100)
    voyage_details_estimated_arrival_date = models.DateField()
    voyage_details_estimated_departure_date = models.DateField()
    shipper_name = models.CharField(max_length=100)
    shipper_address = models.CharField(max_length=255)
    shipper_contact_person = models.CharField(max_length=100)
    interchange_type = models.CharField(max_length=50, choices=INTERCHANGE_TYPES)
    interchange_party = models.CharField(max_length=50, choices=INTERCHANGE_PARTIES)
    interchange_contact = models.CharField(max_length=100)
    interchange_reference_number = models.CharField(max_length=50)
    condition_inspection_overall_condition = models.CharField(max_length=100)
    condition_inspection_inspection_result = models.CharField(max_length=100)
    condition_inspection_inspection_date = models.DateField()
    equipment_id_number = models.CharField(max_length=50)
    equipment_type = models.CharField(max_length=50)
    equipment_size = models.CharField(max_length=50)
    equipment_status = models.CharField(max_length=100)
    equipment_condition_exterior = models.CharField(max_length=100)
    equipment_condition_interior = models.CharField(max_length=100)
    equipment_condition_floor = models.CharField(max_length=100)
    location_terminal_name = models.CharField(max_length=100)
    location_terminal_location = models.CharField(max_length=255)
    location_date_of_interchange = models.DateField()
    prepared_by = models.ForeignKey("Exporter", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.equipment_id_number} - {self.interchange_reference_number}"


class BookedContainer(models.Model):
    container_number = models.CharField(max_length=20)
    exporter = models.ForeignKey("Exporter", on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)


class PostExportInvoice(models.Model):
    container_number = models.CharField(max_length=20)
    exporter = models.ForeignKey("Exporter", on_delete=models.CASCADE)
    invoice_date = models.DateField()
    export_handling_fees = models.DecimalField(max_digits=10, decimal_places=2)
    storage_charges = models.DecimalField(max_digits=10, decimal_places=2)
    haulage = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_number = models.CharField(max_length=50)
    total_amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    services_type = models.CharField(max_length=100)
    discounts_or_adjustments = models.DecimalField(max_digits=10, decimal_places=2)
    rated_upto_date = models.DateField()


class PostPayment(models.Model):
    container_number = models.CharField(max_length=20)
    exporter = models.ForeignKey("Exporter", on_delete=models.CASCADE)
    payment_date = models.DateField()
    invoice_number = models.CharField(max_length=50)
    total_amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    services_type = models.CharField(max_length=100)
    confirmation_officer = models.CharField(max_length=100)
    payment_remarks = models.TextField()
    payment_receipt = models.FileField(upload_to="payment_receipts/")


class InvoicePostingReport(models.Model):
    container_number = models.CharField(max_length=20)
    exporter = models.ForeignKey("Exporter", on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    amount_payment_status = models.CharField(max_length=50)


class ExportDelivery(models.Model):
    edo_number = models.AutoField(primary_key=True)
    booking_number = models.CharField(max_length=100, null=True, blank=True)
    delivery_date = models.DateField()
    container_list = models.TextField(null=True, blank=True)
    container_part = models.TextField(null=True, blank=True)
    damage_status = models.TextField(null=True, blank=True)
    exporter_id = models.ForeignKey(
        "Exporter",
        on_delete=models.CASCADE,
        related_name="deliveries",
        null=True,
        blank=True,
    )
    bellington_annexes = models.TextField(null=True, blank=True)
    validate_truck = models.BooleanField(default=False)
    validate_booking = models.BooleanField(default=False)
    agent_id = models.ForeignKey(
        "Agent", on_delete=models.CASCADE, null=True, blank=True
    )
    contact_number = models.CharField(max_length=50, null=True, blank=True)
    shipping_line = models.TextField(null=True, blank=True)
    vessel_name = models.TextField(null=True, blank=True)
    vessel_departure_date = models.DateField(null=True, blank=True)
    port_of_loading = models.TextField(null=True, blank=True)
    truck_to_port = models.BooleanField(default=False)
    stuffing = models.BooleanField(default=False)
    weightbridge = models.BooleanField(default=False)
    cbm_weight = models.CharField(max_length=50, null=True, blank=True)
    truck_driver_name = models.CharField(max_length=100, null=True, blank=True)
    truck_id = models.CharField(max_length=100, null=True, blank=True)
    delivery_status = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.edo_number)


class Exporter(models.Model):
    exporter_id = models.AutoField(primary_key=True)
    exporter_name = models.TextField()
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=50)
    contact_person = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
