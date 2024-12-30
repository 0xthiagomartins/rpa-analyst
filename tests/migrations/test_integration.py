"""Testes de integração para o processo de migração."""
import pytest
from pytest_check import check
from datetime import datetime
from src.migrations.migration_service import MigrationService
from src.migrations.data_mapper import DataMapper
from src.migrations.validators import DataValidator

@pytest.fixture
def migration_service():
    """Fixture que retorna uma instância do MigrationService."""
    return MigrationService(DataMapper(), DataValidator())

@pytest.fixture
def sample_old_identification_data():
    """Fixture com dados antigos de exemplo."""
    return {
        "name": "Processo de Vendas",
        "id": "PROC-001",
        "department": "Comercial",
        "owner": "João Silva",
        "participants": ["Maria Santos", "Pedro Costa"],
        "created_at": "2024-01-01",
        "updated_at": "2024-01-15",
        "status": "draft"
    }

@pytest.fixture
def sample_process_details_data():
    """Fixture com dados de exemplo do ProcessDetailsForm."""
    return {
        "description": "Processo de vendas completo",
        "objective": "Automatizar processo de vendas",
        "process_type": "automated",
        "frequency": {
            "type": "daily",
            "volume": "100"
        },
        "complexity": {
            "level": "medium",
            "factors": ["Multiple systems", "Business rules"]
        }
    }

@pytest.fixture
def sample_business_rules_data():
    """Fixture com dados de exemplo do BusinessRulesForm."""
    return {
        "business_rules": [
            {
                "rule_id": "BR001",
                "description": "Validação de limite de crédito",
                "rule_type": "validation",
                "priority": "high",
                "implementation": {
                    "condition": "credit_limit > order_value",
                    "action": "approve_order"
                }
            }
        ],
        "dependencies": [
            {
                "system": "CRM",
                "data": ["customer_credit_limit"]
            }
        ]
    }

@pytest.fixture
def sample_automation_goals_data():
    """Fixture com dados de exemplo do AutomationGoalsForm."""
    return {
        "automation_goals": [
            {
                "goal_id": "GOAL001",
                "description": "Reduzir tempo de processamento",
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
                "description": "Redução de custos operacionais",
                "value": "50000",
                "unit": "USD",
                "timeframe": "yearly"
            }
        ],
        "priority_level": "high"
    }

@pytest.fixture
def sample_data_form_data():
    """Fixture com dados de exemplo do DataForm."""
    return {
        "data_inputs": [
            {
                "input_id": "INP001",
                "name": "Customer Data",
                "type": "structured",
                "format": "CSV",
                "source": "CRM System",
                "fields": [
                    {
                        "name": "customer_id",
                        "type": "string",
                        "required": True,
                        "validation_rule": "length > 0"
                    }
                ]
            }
        ],
        "data_outputs": [
            {
                "output_id": "OUT001",
                "name": "Processed Orders",
                "type": "structured",
                "format": "JSON",
                "destination": "Order System"
            }
        ],
        "transformations": [
            {
                "transformation_id": "TR001",
                "name": "Data Validation",
                "description": "Validate customer data",
                "input_fields": ["customer_id"],
                "output_fields": ["validated_id"],
                "rules": ["validate_id_format"]
            }
        ],
        "data_quality": {
            "validation_rules": ["completeness", "accuracy"],
            "quality_metrics": {
                "accuracy_threshold": "98%",
                "completeness_threshold": "95%"
            },
            "error_handling": {
                "retry_attempts": 3,
                "error_notification": "email"
            }
        }
    }

@pytest.fixture
def sample_steps_data():
    """Fixture com dados de exemplo do StepsForm."""
    return {
        "steps": [
            {
                "id": "STEP001",
                "name": "Receive Request",
                "description": "Receive and validate customer request",
                "type": "manual",
                "role": "Analyst",
                "estimated_time": "10 minutes",
                "inputs": ["Customer Form", "ID Document"],
                "outputs": ["Validated Request"],
                "systems": ["CRM"],
                "instructions": [
                    "Check if form is complete",
                    "Validate customer ID"
                ],
                "validations": [
                    "All required fields filled",
                    "ID document is valid"
                ],
                "dependencies": {
                    "previous": [],
                    "next": ["STEP002"]
                }
            },
            {
                "id": "STEP002",
                "name": "Process Request",
                "description": "Process customer request in system",
                "type": "automated",
                "role": "System",
                "estimated_time": "2 minutes",
                "inputs": ["Validated Request"],
                "outputs": ["Processed Request"],
                "systems": ["CRM", "Processing System"],
                "instructions": [
                    "Submit request to processing queue",
                    "Update customer record"
                ],
                "validations": [
                    "Request successfully processed",
                    "Customer record updated"
                ],
                "dependencies": {
                    "previous": ["STEP001"],
                    "next": []
                }
            }
        ],
        "flow": {
            "start_step": "STEP001",
            "end_step": "STEP002",
            "parallel_steps": [],
            "conditional_steps": []
        },
        "roles": [
            {
                "name": "Analyst",
                "responsibilities": ["Validate requests", "Handle exceptions"],
                "skills": ["Data validation", "System knowledge"]
            },
            {
                "name": "System",
                "responsibilities": ["Process requests", "Update records"],
                "skills": ["Automated processing"]
            }
        ]
    }

def test_identification_form_migration_success(migration_service, sample_old_identification_data):
    """Testa migração bem sucedida do IdentificationForm."""
    # Executa migração
    result = migration_service.migrate_identification_form(sample_old_identification_data)
    
    # Verifica sucesso
    assert result["success"] is True
    assert result["errors"] == []
    
    # Verifica dados migrados
    migrated_data = result["data"]
    assert migrated_data["process_name"] == "Processo de Vendas"
    assert migrated_data["process_id"] == "PROC-001"
    assert migrated_data["department"] == "Comercial"
    assert migrated_data["owner"] == "João Silva"
    assert len(migrated_data["participants"]) == 2
    assert migrated_data["creation_date"] == "2024-01-01"
    assert migrated_data["last_update"] == "2024-01-15"
    assert migrated_data["status"] == "draft"

def test_identification_form_migration_invalid_data(migration_service):
    """Testa migração com dados inválidos."""
    invalid_data = {
        "name": "",  # Nome vazio (inválido)
        "id": "invalid-id",  # ID com formato inválido
        "status": "invalid"  # Status inválido
    }
    
    result = migration_service.migrate_identification_form(invalid_data)
    
    # Verifica falha
    assert result["success"] is False
    assert len(result["errors"]) > 0
    assert any("process_name" in error for error in result["errors"])
    assert any("process_id" in error for error in result["errors"])
    assert any("status" in error for error in result["errors"])

def test_identification_form_migration_rollback(migration_service, sample_old_identification_data):
    """Testa rollback da migração em caso de erro."""
    # Simula erro durante salvamento
    migration_service.save_error = True
    
    result = migration_service.migrate_identification_form(sample_old_identification_data)
    
    # Verifica falha e rollback
    assert result["success"] is False
    assert "rollback" in result
    assert result["rollback"]["success"] is True 

def test_process_details_migration_success(migration_service, sample_process_details_data):
    """Testa migração bem sucedida do ProcessDetailsForm."""
    process_id = "PROC-001"
    result = migration_service.migrate_process_details_form(sample_process_details_data, process_id)

    with check:
        assert result["success"] is True, "Migração deveria ter sucesso"
    with check:
        assert not result["errors"], "Não deveria ter erros"
    with check:
        assert result["data"] is not None, "Dados não deveriam ser nulos"

    # Verifica dados específicos
    migrated_data = result["data"]
    with check:
        assert migrated_data["description"] == "Processo de vendas completo", "Descrição incorreta"
    with check:
        assert migrated_data["process_type"] == "automated", "Tipo de processo incorreto"

def test_business_rules_migration_success(migration_service, sample_business_rules_data):
    """Testa migração bem sucedida do BusinessRulesForm."""
    process_id = "PROC-001"
    result = migration_service.migrate_business_rules_form(sample_business_rules_data, process_id)

    with check:
        assert result["success"] is True, "Migração deveria ter sucesso"
    with check:
        assert not result["errors"], "Não deveria ter erros"
    with check:
        assert result["data"] is not None, "Dados não deveriam ser nulos"

    # Verifica dados específicos
    migrated_data = result["data"]
    with check:
        assert len(migrated_data["business_rules"]) == 1, "Deveria ter uma regra"
    with check:
        assert migrated_data["business_rules"][0]["rule_id"] == "BR001", "ID da regra incorreto"
    with check:
        assert migrated_data["business_rules"][0]["type"] == "validation", "Tipo da regra incorreto"

def test_automation_goals_migration_success(migration_service, sample_automation_goals_data):
    """Testa migração bem sucedida do AutomationGoalsForm."""
    process_id = "PROC-001"
    result = migration_service.migrate_automation_goals_form(sample_automation_goals_data, process_id)

    with check:
        assert result["success"] is True, "Migração deveria ter sucesso"
    with check:
        assert not result["errors"], "Não deveria ter erros"
    with check:
        assert result["data"] is not None, "Dados não deveriam ser nulos"

    # Verifica dados específicos
    migrated_data = result["data"]
    with check:
        assert len(migrated_data["automation_goals"]) == 1, "Deveria ter um objetivo"
    with check:
        assert migrated_data["automation_goals"][0]["goal_id"] == "GOAL001", "ID do objetivo incorreto"
    with check:
        assert migrated_data["automation_goals"][0]["category"] == "efficiency", "Categoria incorreta"

def test_process_details_migration_invalid_data(migration_service):
    """Testa migração com dados inválidos no ProcessDetailsForm."""
    process_id = "PROC-001"
    invalid_data = {
        "description": "",  # Descrição vazia (inválido)
        "process_type": "invalid",  # Tipo inválido
        "frequency": {"execution_frequency": "invalid"}  # Frequência inválida
    }
    
    result = migration_service.migrate_process_details_form(invalid_data, process_id)
    
    assert result["success"] is False
    assert len(result["errors"]) > 0

def test_business_rules_migration_invalid_data(migration_service):
    """Testa migração com dados inválidos no BusinessRulesForm."""
    process_id = "PROC-001"
    invalid_data = {
        "rules": [
            {
                "rule_id": "",  # ID vazio (inválido)
                "rule_type": "invalid"  # Tipo inválido
            }
        ]
    }
    
    result = migration_service.migrate_business_rules_form(invalid_data, process_id)
    
    assert result["success"] is False
    assert len(result["errors"]) > 0

def test_automation_goals_migration_invalid_data(migration_service):
    """Testa migração com dados inválidos no AutomationGoalsForm."""
    process_id = "PROC-001"
    invalid_data = {
        "automation_goals": [
            {
                "goal_id": "",  # ID vazio (inválido)
                "category": "invalid",  # Categoria inválida
                "metrics": {}  # Métricas vazias (inválido)
            }
        ],
        "priority_level": "invalid"  # Prioridade inválida
    }

    result = migration_service.migrate_automation_goals_form(invalid_data, process_id)

    with check:
        assert result["success"] is False, "Deveria falhar com dados inválidos"
    with check:
        assert result["errors"], "Deveria ter mensagens de erro"
    with check:
        assert result["data"] is None, "Dados deveriam ser nulos" 

def test_data_form_migration_success(migration_service, sample_data_form_data):
    """Testa migração bem sucedida do DataForm."""
    process_id = "PROC-001"
    result = migration_service.migrate_data_form(sample_data_form_data, process_id)

    with check:
        assert result["success"] is True, "Migração deveria ter sucesso"
    with check:
        assert not result["errors"], "Não deveria ter erros"
    with check:
        assert result["data"] is not None, "Dados não deveriam ser nulos"

    # Verifica dados específicos
    migrated_data = result["data"]
    
    # Verifica inputs
    with check:
        assert len(migrated_data["data_inputs"]) == 1, "Número incorreto de inputs"
    with check:
        assert migrated_data["data_inputs"][0]["input_id"] == "INP001", "ID do input incorreto"
    with check:
        assert migrated_data["data_inputs"][0]["name"] == "Customer Data", "Nome do input incorreto"
    with check:
        assert migrated_data["data_inputs"][0]["type"] == "structured", "Tipo do input incorreto"
    
    # Verifica outputs
    with check:
        assert len(migrated_data["data_outputs"]) == 1, "Número incorreto de outputs"
    with check:
        assert migrated_data["data_outputs"][0]["output_id"] == "OUT001", "ID do output incorreto"
    with check:
        assert migrated_data["data_outputs"][0]["name"] == "Processed Orders", "Nome do output incorreto"
    
    # Verifica transformações
    with check:
        assert len(migrated_data["transformations"]) == 1, "Número incorreto de transformações"
    with check:
        assert migrated_data["transformations"][0]["id"] == "TR001", "ID da transformação incorreto"
    
    # Verifica qualidade de dados
    with check:
        assert "validation_rules" in migrated_data["data_quality"], "Regras de validação ausentes"
    with check:
        assert "quality_metrics" in migrated_data["data_quality"], "Métricas de qualidade ausentes"
    with check:
        assert "error_handling" in migrated_data["data_quality"], "Tratamento de erros ausente"

def test_steps_form_migration_success(migration_service, sample_steps_data):
    """Testa migração bem sucedida do StepsForm."""
    process_id = "PROC-001"
    result = migration_service.migrate_steps_form(sample_steps_data, process_id)

    with check:
        assert result["success"] is True, "Migração deveria ter sucesso"
    with check:
        assert not result["errors"], "Não deveria ter erros"
    with check:
        assert result["data"] is not None, "Dados não deveriam ser nulos"

    # Verifica dados específicos
    migrated_data = result["data"]
    with check:
        assert len(migrated_data["process_steps"]) == 2, "Número incorreto de passos"
    with check:
        assert migrated_data["process_steps"][0]["step_id"] == "STEP001", "ID do passo incorreto"
    with check:
        assert migrated_data["process_steps"][0]["step_type"] == "manual", "Tipo do passo incorreto"
    
    # Verifica fluxo
    with check:
        assert migrated_data["process_flow"]["initial_step"] == "STEP001", "Passo inicial incorreto"
    with check:
        assert migrated_data["process_flow"]["final_step"] == "STEP002", "Passo final incorreto"

def test_steps_form_migration_invalid_data(migration_service):
    """Testa migração com dados inválidos no StepsForm."""
    process_id = "PROC-001"
    invalid_data = {
        "steps": [
            {
                "step_id": "",  # ID vazio (inválido)
                "step_type": "invalid",  # Tipo inválido
                "dependencies": "invalid"  # Deveria ser dict (inválido)
            }
        ],
        "flow": {
            "start_step": "",  # Passo inicial vazio (inválido)
            "end_step": ""  # Passo final vazio (inválido)
        }
    }

    result = migration_service.migrate_steps_form(invalid_data, process_id)

    with check:
        assert result["success"] is False, "Deveria falhar com dados inválidos"
    with check:
        assert result["errors"], "Deveria ter mensagens de erro"
    with check:
        assert result["data"] is None, "Dados deveriam ser nulos" 