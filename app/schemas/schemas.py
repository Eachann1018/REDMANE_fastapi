from typing import List, Optional
from pydantic import BaseModel, validator

# =====================
# Project Schema
# =====================
class Project(BaseModel):
    id: int
    name: str
    status: str


# =====================
# Dataset Schemas
# =====================
class Dataset(BaseModel):
    id: int
    project_id: int
    name: str


class DatasetMetadata(BaseModel):
    id: int
    dataset_id: int
    key: str
    value: str


class DatasetWithMetadata(Dataset):
    metadata: List[DatasetMetadata] = []


class MetadataUpdate(BaseModel):
    dataset_id: int
    file_size: Optional[str] = None
    last_size_update: Optional[str] = None


# =====================
# Patient Schemas
# =====================
class Patient(BaseModel):
    id: int
    project_id: int
    ext_patient_id: str
    ext_patient_url: str
    public_patient_id: Optional[str]


class PatientMetadata(BaseModel):
    id: int
    patient_id: int
    key: str
    value: str


class PatientWithMetadata(Patient):
    metadata: List[PatientMetadata] = []


class PatientWithSampleCount(Patient):
    sample_count: int


# =====================
# Sample Schemas
# =====================
class SampleMetadata(BaseModel):
    id: int
    sample_id: int
    key: str
    value: str


class Sample(BaseModel):
    id: int
    patient_id: int
    ext_sample_id: str
    ext_sample_url: str
    metadata: List[SampleMetadata] = []
    patient: Patient


class SampleWithoutPatient(BaseModel):
    id: int
    patient_id: int
    ext_sample_id: str
    ext_sample_url: str
    metadata: List[SampleMetadata] = []


class PatientWithSamples(PatientWithMetadata):
    samples: List[SampleWithoutPatient] = []


# =====================
# File Schemas
# =====================
class FileMetadataCreate(BaseModel):
    metadata_key: str
    metadata_value: str


class FileCreate(BaseModel):
    dataset_id: int
    path: str
    file_type: str  # 'raw', 'processed', or 'summarised'
    metadata: Optional[List[FileMetadataCreate]] = []

    @validator('file_type')
    def validate_file_type(cls, v):
        allowed = ['raw', 'processed', 'summarised']
        if v not in allowed:
            raise ValueError(f"file_type must be one of {allowed}, got '{v}'")
        return v


class FileResponse(BaseModel):
    id: int
    path: str
    sample_id: Optional[int] = None
    ext_sample_id: Optional[str] = None
    sample_metadata: Optional[List[SampleMetadata]] = None
