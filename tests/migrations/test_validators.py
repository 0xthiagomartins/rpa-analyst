"""Testes para os validadores de dados."""
import pytest
from src.migrations.validators import DataValidator

@pytest.fixture
def sample_identification_data():
    """Fixture com dados de exemplo do IdentificationForm."""
    return {
        "process_name": "Test Process",
        "process_id": "PROC-001",
        "department": "IT",
        "owner": "John Doe",
        "participants": ["Alice", "Bob"],
        "creation_date": "2024-01-01",
        "last_update": "2024-01-02",
        "status": "draft"
    }

@pytest.fixture
def sample_process_details_data():
    """Fixture com dados de exemplo do ProcessDetailsForm."""
    return {
        "description": "Process description",
        "objective": "Process objective",
        "process_type": "automated",
        "frequency": {"execution_frequency": "daily"},
        "complexity": {"level": "medium"}
    }

@pytest.fixture
def sample_automation_goals_data():
    """Fixture com dados de exemplo do AutomationGoalsForm."""
    return {
        "automation_goals": [
            {
                "goal_id": "GOAL001",
                "description": "Reduce processing time",
                "category": "efficiency",
                "metrics": {
                    "current_value": "30 minutes",
                    "target_value": "5 minutes",
                    "unit": "time"
                }
            }
        ],
        "benefits": [
            {
                "benefit_type": "cost",
                "description": "Reduce operational costs",
                "value": "50000",
                "unit": "USD",
                "timeframe": "yearly"
            }
        ],
        "priority_level": "high"
    }

@pytest.fixture
def sample_systems_data():
    """Fixture com dados de exemplo do SystemsForm."""
    return {
        "systems": [
            {
                "system_id": "SYS001",
                "system_name": "SAP ERP",
                "system_type": "ERP",
                "version": "S/4HANA",
                "access_details": {
                    "access_type": "API",
                    "credentials_type": "service_account",
                    "permissions": ["read", "write"]
                }
            }
        ],
        "integrations": [
            {
                "source_system": "SYS001",
                "target_system": "SYS002",
                "integration_type": "batch",
                "sync_frequency": "daily"
            }
        ]
    }

@pytest.fixture
def sample_data_form_data():
    """Fixture com dados de exemplo do DataForm."""
    return {
        "data_inputs": [
            {
                "input_id": "INP001",
                "input_name": "Customer Data",
                "data_type": "structured",
                "field_definitions": [
                    {
                        "field_name": "customer_id",
                        "data_type": "string",
                        "is_required": True
                    }
                ]
            }
        ],
        "data_outputs": [
            {
                "output_id": "OUT001",
                "output_name": "Processed Data",
                "data_type": "structured"
            }
        ]
    }

@pytest.fixture
def sample_steps_data():
    """Fixture com dados de exemplo do StepsForm."""
    return {
        "process_steps": [
            {
                "step_id": "STEP001",
                "step_name": "Receive Request",
                "description": "Receive and validate customer request",
                "step_type": "manual",
                "assigned_role": "Analyst",
                "time_estimate": "10 minutes",
                "step_inputs": ["Customer Form"],
                "step_outputs": ["Validated Request"],
                "required_systems": ["CRM"],
                "dependencies": {
                    "previous_steps": [],
                    "next_steps": ["STEP002"]
                }
            }
        ],
        "process_flow": {
            "initial_step": "STEP001",
            "final_step": "STEP002",
            "parallel_execution": []
        },
        "process_roles": [
            {
                "role_name": "Analyst",
                "role_responsibilities": ["Request validation"],
                "required_skills": ["CRM System"]
            }
        ]
    }

@pytest.fixture
def sample_risks_data():
    """Fixture com dados de exemplo do RisksForm."""
    return {
        "identified_risks": [
            {
                "risk_id": "RISK001",
                "description": "System downtime",
                "risk_category": "technical",
                "probability_level": "medium",
                "impact_level": "high",
                "severity_level": "critical",
                "mitigation_strategy": {
                    "planned_actions": ["Implement redundancy"],
                    "responsible_party": "IT Team",
                    "target_date": "2024-06-30"
                }
            }
        ],
        "risk_assessment_matrix": {
            "probability_scale": ["low", "medium", "high"],
            "impact_scale": ["low", "medium", "high"]
        }
    }

@pytest.fixture
def sample_documentation_data():
    """Fixture com dados de exemplo do DocumentationForm."""
    return {
        "process_documentation": {
            "document_version": "1.0",
            "last_updated": "2024-01-15",
            "document_author": "John Doe",
            "document_status": "draft",
            "content_sections": [
                {
                    "section_id": "SEC001",
                    "section_title": "Overview",
                    "section_content": "Process overview content"
                }
            ]
        },
        "training_materials": [
            {
                "material_id": "TRN001",
                "material_title": "User Guide",
                "file_type": "document",
                "file_format": "PDF"
            }
        ]
    }

def test_validate_identification_data_success(sample_identification_data):
    """Testa validação bem sucedida dos dados do IdentificationForm."""
    validator = DataValidator()
    result, errors = validator.validate_identification_data(sample_identification_data)
    
    assert result is True
    assert not errors

def test_validate_identification_data_missing_required():
    """Testa validação com campos obrigatórios faltando."""
    data = {
        "process_name": "",  # Campo obrigatório vazio
        "process_id": "PROC-001",
        "department": "IT"
    }
    
    validator = DataValidator()
    result, errors = validator.validate_identification_data(data)
    
    assert result is False
    assert "process_name" in errors
    assert "owner" in errors  # Campo obrigatório ausente

def test_validate_identification_data_invalid_format():
    """Testa validação com formatos inválidos."""
    data = {
        "process_name": "Test Process",
        "process_id": "invalid-id",  # Formato inválido
        "department": "IT",
        "owner": "John Doe",
        "creation_date": "invalid-date"  # Formato inválido
    }
    
    validator = DataValidator()
    result, errors = validator.validate_identification_data(data)
    
    assert result is False
    assert "process_id" in errors
    assert "creation_date" in errors

def test_validate_identification_data_invalid_status():
    """Testa validação com status inválido."""
    data = {
        "process_name": "Test Process",
        "process_id": "PROC-001",
        "department": "IT",
        "owner": "John Doe",
        "status": "invalid"  # Status inválido
    }
    
    validator = DataValidator()
    result, errors = validator.validate_identification_data(data)
    
    assert result is False
    assert "status" in errors
    assert "Invalid status" in errors["status"]

def test_validate_identification_data_invalid_participants():
    """Testa validação com participantes inválidos."""
    data = {
        "process_name": "Test Process",
        "process_id": "PROC-001",
        "department": "IT",
        "owner": "John Doe",
        "participants": "John Doe"  # Deveria ser uma lista
    }
    
    validator = DataValidator()
    result, errors = validator.validate_identification_data(data)
    
    assert result is False
    assert "participants" in errors
    assert "Must be a list" in errors["participants"]

def test_validate_process_details_success(sample_process_details_data):
    """Testa validação bem sucedida do ProcessDetailsForm."""
    validator = DataValidator()
    result, errors = validator.validate_process_details_data(sample_process_details_data)
    assert result is True
    assert not errors

def test_validate_process_details_invalid_type():
    """Testa validação com tipo de processo inválido."""
    data = {
        "description": "Process description",
        "objective": "Process objective",
        "process_type": "invalid"
    }
    validator = DataValidator()
    result, errors = validator.validate_process_details_data(data)
    assert result is False
    assert "process_type" in errors

def test_validate_automation_goals_success(sample_automation_goals_data):
    """Testa validação bem sucedida do AutomationGoalsForm."""
    validator = DataValidator()
    result, errors = validator.validate_automation_goals_data(sample_automation_goals_data)
    assert result is True
    assert not errors

def test_validate_automation_goals_invalid_priority():
    """Testa validação com prioridade inválida."""
    data = {
        "automation_goals": [],
        "priority_level": "invalid"
    }
    validator = DataValidator()
    result, errors = validator.validate_automation_goals_data(data)
    assert result is False
    assert "priority_level" in errors

def test_validate_systems_data_success(sample_systems_data):
    """Testa validação bem sucedida do SystemsForm."""
    validator = DataValidator()
    result, errors = validator.validate_systems_data(sample_systems_data)
    assert result is True
    assert not errors

def test_validate_systems_data_missing_required():
    """Testa validação com campos obrigatórios faltando."""
    data = {
        "systems": [
            {
                "system_id": "SYS001"
                # system_name faltando
            }
        ]
    }
    validator = DataValidator()
    result, errors = validator.validate_systems_data(data)
    assert result is False
    assert "systems[0].system_name" in errors

def test_validate_data_form_success(sample_data_form_data):
    """Testa validação bem sucedida do DataForm."""
    validator = DataValidator()
    result, errors = validator.validate_data_form_data(sample_data_form_data)
    assert result is True
    assert not errors

def test_validate_data_form_invalid_type():
    """Testa validação com tipo de dado inválido."""
    data = {
        "data_inputs": [
            {
                "input_id": "INP001",
                "field_definitions": [
                    {
                        "field_name": "field1",
                        "data_type": "invalid_type"
                    }
                ]
            }
        ]
    }
    validator = DataValidator()
    result, errors = validator.validate_data_form_data(data)
    assert result is False
    assert "data_inputs[0].field_definitions[0].data_type" in errors

def test_validate_steps_data_success(sample_steps_data):
    """Testa validação bem sucedida do StepsForm."""
    validator = DataValidator()
    result, errors = validator.validate_steps_data(sample_steps_data)
    assert result is True
    assert not errors

def test_validate_steps_data_missing_required():
    """Testa validação com campos obrigatórios faltando."""
    data = {
        "process_steps": [
            {
                "step_id": "STEP001"
                # step_name faltando
            }
        ]
    }
    validator = DataValidator()
    result, errors = validator.validate_steps_data(data)
    assert result is False
    assert "process_steps[0].step_name" in errors

def test_validate_risks_data_success(sample_risks_data):
    """Testa validação bem sucedida do RisksForm."""
    validator = DataValidator()
    result, errors = validator.validate_risks_data(sample_risks_data)
    assert result is True
    assert not errors

def test_validate_risks_data_invalid_levels():
    """Testa validação com níveis inválidos."""
    data = {
        "identified_risks": [
            {
                "risk_id": "RISK001",
                "description": "Test risk",
                "probability_level": "invalid",
                "impact_level": "invalid"
            }
        ]
    }
    validator = DataValidator()
    result, errors = validator.validate_risks_data(data)
    assert result is False
    assert "identified_risks[0].probability_level" in errors
    assert "identified_risks[0].impact_level" in errors

def test_validate_documentation_data_success(sample_documentation_data):
    """Testa validação bem sucedida do DocumentationForm."""
    validator = DataValidator()
    result, errors = validator.validate_documentation_data(sample_documentation_data)
    assert result is True
    assert not errors

def test_validate_documentation_data_invalid_status():
    """Testa validação com status inválido."""
    data = {
        "process_documentation": {
            "document_version": "1.0",
            "document_status": "invalid"
        }
    }
    validator = DataValidator()
    result, errors = validator.validate_documentation_data(data)
    assert result is False
    assert "process_documentation.document_status" in errors 