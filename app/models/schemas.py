from pydantic import BaseModel
from typing import List, Optional

class PeakHourItem(BaseModel):
    hour: int
    count: int

class PeakHoursResponse(BaseModel):
    data: List[PeakHourItem]
    orgId: str

class NoShowRateResponse(BaseModel):
    total: int
    cancelled: int
    noShowRate: float
    orgId: str

class StaffUtilisationItem(BaseModel):
    staffId: str
    firstName: str
    lastName: str
    email: str
    totalAppointments: int
    completedAppointments: int
    totalMinutesBooked: int

class StaffUtilisationResponse(BaseModel):
    data: List[StaffUtilisationItem]
    orgId: str

class VolumeTrendItem(BaseModel):
    date: str
    count: int

class VolumeTrendResponse(BaseModel):
    data: List[VolumeTrendItem]
    orgId: str

class RevenueItem(BaseModel):
    appointmentType: str
    count: int
    pricePerAppointment: float
    totalRevenue: float

class RevenueEstimateResponse(BaseModel):
    data: List[RevenueItem]
    totalEstimatedRevenue: float
    orgId: str

class SummaryResponse(BaseModel):
    totalAppointments: int
    completedAppointments: int
    cancelledAppointments: int
    noShowRate: float
    peakHour: Optional[int]
    totalStaff: int
    totalEstimatedRevenue: float
    orgId: str