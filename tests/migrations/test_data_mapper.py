"""Testes para o mapeador de dados."""
import pytest
from pytest_check import check
from src.migrations.data_mapper import DataMapper

@pytest.fixture
def sample_identification_data():
    """Fixture com dados de exemplo do IdentificationForm."""
    return {
        "name": "Test Process",
        "id": "PROC-001",
        "department": "IT",
        "owner": "John Doe",
        "participants": ["Alice", "Bob"],
        "created_at": "2024-01-01",
        "updated_at": "2024-01-02",
        "status": "draft"
    }

def test_map_identification_data(sample_identification_data):
    """Testa mapeamento de dados do IdentificationForm."""
    result = DataMapper.map_identification_data(sample_identification_data)
    
    assert result["process_name"] == sample_identification_data["name"]
    assert result["process_id"] == sample_identification_data["id"]
    assert result["department"] == sample_identification_data["department"]
    assert result["owner"] == sample_identification_data["owner"]
    assert result["participants"] == sample_identification_data["participants"]
    assert result["creation_date"] == sample_identification_data["created_at"]
    assert result["last_update"] == sample_identification_data["updated_at"]
    assert result["status"] == sample_identification_data["status"]

def test_map_identification_data_missing_fields():
    """Testa mapeamento com campos faltando."""
    old_data = {"name": "Test Process"}  # Dados incompletos
    
    result = DataMapper.map_identification_data(old_data)
    
    assert result["process_name"] == "Test Process"
    assert result["process_id"] == ""
    assert result["department"] == ""
    assert result["owner"] == ""
    assert result["participants"] == []
    assert result["creation_date"] == ""
    assert result["last_update"] == ""
    assert result["status"] == "draft" 

@pytest.fixture
def sample_process_details_data():
    """Fixture com dados de exemplo do ProcessDetailsForm."""
    return {
        "description": "Process description",
        "objective": "Process objective",
        "scope_in": ["Task 1", "Task 2"],
        "scope_out": ["Task 3"],
        "type": "manual",
        "frequency": "daily",
        "volume": 100,
        "peak_times": ["Morning", "Afternoon"],
        "complexity": "high",
        "complexity_factors": ["Multiple systems", "Complex rules"],
        "dependencies_upstream": ["Process A", "Process B"],
        "dependencies_downstream": ["Process C"],
        "additional_info": "Additional information"
    }

def test_map_process_details_data(sample_process_details_data):
    """Testa mapeamento de dados do ProcessDetailsForm."""
    result = DataMapper.map_process_details_data(sample_process_details_data)
    
    assert result["description"] == sample_process_details_data["description"]
    assert result["objective"] == sample_process_details_data["objective"]
    assert result["scope"]["in_scope"] == sample_process_details_data["scope_in"]
    assert result["scope"]["out_scope"] == sample_process_details_data["scope_out"]
    assert result["process_type"] == sample_process_details_data["type"]
    assert result["frequency"]["execution_frequency"] == sample_process_details_data["frequency"]
    assert result["frequency"]["volume"] == sample_process_details_data["volume"]
    assert result["frequency"]["peak_times"] == sample_process_details_data["peak_times"]
    assert result["complexity"]["level"] == sample_process_details_data["complexity"]
    assert result["complexity"]["factors"] == sample_process_details_data["complexity_factors"]
    assert result["dependencies"]["upstream"] == sample_process_details_data["dependencies_upstream"]
    assert result["dependencies"]["downstream"] == sample_process_details_data["dependencies_downstream"]
    assert result["additional_info"] == sample_process_details_data["additional_info"]

def test_map_process_details_data_missing_fields():
    """Testa mapeamento com campos faltando."""
    old_data = {"description": "Process description"}  # Dados incompletos
    
    result = DataMapper.map_process_details_data(old_data)
    
    assert result["description"] == "Process description"
    assert result["objective"] == ""
    assert result["scope"]["in_scope"] == []
    assert result["scope"]["out_scope"] == []
    assert result["process_type"] == "manual"
    assert result["frequency"]["execution_frequency"] == "daily"
    assert result["frequency"]["volume"] == 0
    assert result["frequency"]["peak_times"] == []
    assert result["complexity"]["level"] == "medium"
    assert result["complexity"]["factors"] == []
    assert result["dependencies"]["upstream"] == []
    assert result["dependencies"]["downstream"] == []
    assert result["additional_info"] == "" 

@pytest.fixture
def sample_business_rules_data():
    """Fixture com dados de exemplo do BusinessRulesForm."""
    return {
        "rules": [
            {
                "id": "BR001",
                "description": "Rule 1 description",
                "type": "validation",
                "priority": "high",
                "exceptions": ["Exception 1", "Exception 2"]
            },
            {
                "id": "BR002",
                "description": "Rule 2 description",
                "type": "calculation",
                "priority": "medium",
                "exceptions": ["Exception 3"]
            }
        ],
        "validations": [
            {
                "field": "amount",
                "rule": "must be positive",
                "error_message": "Amount must be greater than zero"
            }
        ],
        "calculations": [
            {
                "name": "total",
                "formula": "quantity * price",
                "description": "Calculate total amount"
            }
        ],
        "conditions": [
            {
                "if": "amount > 1000",
                "then": "require_approval",
                "description": "Large amounts need approval"
            }
        ]
    }

def test_map_business_rules_data(sample_business_rules_data):
    """Testa mapeamento de dados do BusinessRulesForm."""
    result = DataMapper.map_business_rules_data(sample_business_rules_data)
    
    # Verifica regras de negócio
    assert len(result["business_rules"]) == 2
    assert result["business_rules"][0]["rule_id"] == "BR001"
    assert result["business_rules"][0]["description"] == "Rule 1 description"
    assert result["business_rules"][0]["rule_type"] == "validation"
    assert result["business_rules"][0]["priority"] == "high"
    assert len(result["business_rules"][0]["exceptions"]) == 2
    
    # Verifica validações
    assert len(result["validations"]) == 1
    assert result["validations"][0]["field_name"] == "amount"
    assert result["validations"][0]["validation_rule"] == "must be positive"
    assert result["validations"][0]["error_message"] == "Amount must be greater than zero"
    
    # Verifica cálculos
    assert len(result["calculations"]) == 1
    assert result["calculations"][0]["calculation_name"] == "total"
    assert result["calculations"][0]["formula"] == "quantity * price"
    assert result["calculations"][0]["description"] == "Calculate total amount"
    
    # Verifica condições
    assert len(result["conditions"]) == 1
    assert result["conditions"][0]["condition"] == "amount > 1000"
    assert result["conditions"][0]["action"] == "require_approval"
    assert result["conditions"][0]["description"] == "Large amounts need approval"

def test_map_business_rules_data_missing_fields():
    """Testa mapeamento com campos faltando."""
    old_data = {
        "rules": [
            {
                "id": "BR001",
                "description": "Rule 1 description"
            }
        ]
    }
    
    result = DataMapper.map_business_rules_data(old_data)
    
    # Verifica regras com campos faltando
    assert len(result["business_rules"]) == 1
    assert result["business_rules"][0]["rule_id"] == "BR001"
    assert result["business_rules"][0]["description"] == "Rule 1 description"
    assert result["business_rules"][0]["rule_type"] == "general"
    assert result["business_rules"][0]["priority"] == "medium"
    assert result["business_rules"][0]["exceptions"] == []
    
    # Verifica listas vazias para campos ausentes
    assert result["validations"] == []
    assert result["calculations"] == []
    assert result["conditions"] == [] 

@pytest.fixture
def sample_automation_goals_data():
    """Fixture com dados de exemplo do AutomationGoalsForm."""
    return {
        "goals": [
            {
                "id": "GOAL001",
                "description": "Reduce processing time",
                "type": "efficiency",
                "metrics": {
                    "current": "30 minutes",
                    "target": "5 minutes",
                    "unit": "time"
                }
            },
            {
                "id": "GOAL002",
                "description": "Improve accuracy",
                "type": "quality",
                "metrics": {
                    "current": "95%",
                    "target": "99.9%",
                    "unit": "percentage"
                }
            }
        ],
        "benefits": [
            {
                "type": "cost",
                "description": "Reduce operational costs",
                "value": "50000",
                "currency": "USD",
                "timeframe": "yearly"
            },
            {
                "type": "productivity",
                "description": "Increase throughput",
                "value": "200",
                "currency": "USD",
                "timeframe": "monthly"
            }
        ],
        "priority": "high"
    }

def test_map_automation_goals_data(sample_automation_goals_data):
    """Testa mapeamento de dados do AutomationGoalsForm."""
    result = DataMapper.map_automation_goals_data(sample_automation_goals_data)

    # Verifica objetivos
    with check:
        assert len(result["automation_goals"]) == 2, "Número incorreto de objetivos"
    
    # Verifica primeiro objetivo
    with check:
        assert result["automation_goals"][0]["goal_id"] == "GOAL001", "ID do objetivo incorreto"
    with check:
        assert result["automation_goals"][0]["description"] == "Reduce processing time", "Descrição incorreta"
    with check:
        assert result["automation_goals"][0]["category"] == "efficiency", "Categoria incorreta"
    with check:
        assert result["automation_goals"][0]["priority_level"] == "high", "Prioridade incorreta"
    with check:
        assert result["automation_goals"][0]["metrics"]["current_value"] == "30 minutes", "Valor atual incorreto"
    with check:
        assert result["automation_goals"][0]["metrics"]["target_value"] == "5 minutes", "Valor alvo incorreto"
    with check:
        assert result["automation_goals"][0]["metrics"]["unit"] == "time", "Unidade incorreta"

    # Verifica segundo objetivo
    with check:
        assert result["automation_goals"][1]["goal_id"] == "GOAL002", "ID do segundo objetivo incorreto"
    with check:
        assert result["automation_goals"][1]["category"] == "quality", "Categoria do segundo objetivo incorreta"

    # Verifica benefícios
    with check:
        assert len(result["benefits"]) == 2, "Número incorreto de benefícios"
    with check:
        assert result["benefits"][0]["benefit_type"] == "cost", "Tipo de benefício incorreto"
    with check:
        assert result["benefits"][0]["description"] == "Reduce operational costs", "Descrição do benefício incorreta"
    with check:
        assert result["benefits"][0]["value"] == "50000", "Valor do benefício incorreto"
    with check:
        assert result["benefits"][0]["unit"] == "USD", "Unidade do benefício incorreta"
    with check:
        assert result["benefits"][0]["timeframe"] == "yearly", "Período do benefício incorreto"

    # Verifica campos obrigatórios
    with check:
        assert "implementation_timeline" in result, "Timeline de implementação ausente"
    with check:
        assert "success_criteria" in result, "Critérios de sucesso ausentes"
    with check:
        assert "dependencies" in result, "Dependências ausentes"
    with check:
        assert "constraints" in result, "Restrições ausentes"

def test_map_automation_goals_data_missing_fields():
    """Testa mapeamento com campos faltando."""
    old_data = {
        "goals": [
            {
                "id": "GOAL001",
                "description": "Basic goal"
            }
        ]
    }

    result = DataMapper.map_automation_goals_data(old_data)

    # Verifica objetivo com campos faltando
    with check:
        assert len(result["automation_goals"]) == 1, "Número incorreto de objetivos"
    with check:
        assert result["automation_goals"][0]["goal_id"] == "GOAL001", "ID do objetivo incorreto"
    with check:
        assert result["automation_goals"][0]["description"] == "Basic goal", "Descrição incorreta"
    with check:
        assert result["automation_goals"][0]["category"] == "general", "Categoria default incorreta"
    with check:
        assert result["automation_goals"][0]["metrics"] == {
            "current_value": "",
            "target_value": "",
            "unit": ""
        }, "Métricas default incorretas"

    # Verifica valores default para campos ausentes
    with check:
        assert result["benefits"] == [], "Lista de benefícios deveria estar vazia"
    with check:
        assert result["constraints"] == [], "Lista de restrições deveria estar vazia"
    with check:
        assert result["success_criteria"] == [], "Lista de critérios deveria estar vazia"
    with check:
        assert result["priority_level"] == "medium", "Prioridade default incorreta"
    with check:
        assert result["implementation_timeline"] == {
            "start_date": "",
            "end_date": "",
            "milestones": []
        }, "Timeline default incorreta" 

@pytest.fixture
def sample_systems_data():
    """Fixture com dados de exemplo do SystemsForm."""
    return {
        "systems": [
            {
                "id": "SYS001",
                "name": "SAP ERP",
                "type": "ERP",
                "version": "S/4HANA 2021",
                "modules": ["FI", "CO", "MM"],
                "access": {
                    "type": "API",
                    "credentials": "service_account",
                    "permissions": ["read", "write"]
                },
                "availability": {
                    "hours": "24/7",
                    "sla": "99.9%",
                    "maintenance_window": "Sunday 2-6 AM"
                }
            },
            {
                "id": "SYS002",
                "name": "Salesforce",
                "type": "CRM",
                "version": "Enterprise",
                "modules": ["Sales", "Service"],
                "access": {
                    "type": "REST API",
                    "credentials": "oauth2",
                    "permissions": ["read"]
                },
                "availability": {
                    "hours": "Business hours",
                    "sla": "99.5%",
                    "maintenance_window": "Saturday 10 PM"
                }
            }
        ],
        "integrations": [
            {
                "source": "SYS001",
                "target": "SYS002",
                "type": "batch",
                "frequency": "daily",
                "data_flow": ["orders", "customers"],
                "requirements": ["data mapping", "error handling"]
            }
        ],
        "data_flows": [
            {
                "name": "Customer Sync",
                "description": "Synchronize customer data between systems",
                "systems": ["SYS001", "SYS002"],
                "frequency": "real-time",
                "volume": "5000/day"
            }
        ],
        "technical_requirements": [
            {
                "category": "performance",
                "description": "Response time under 2 seconds",
                "priority": "high"
            },
            {
                "category": "security",
                "description": "Encrypted data transmission",
                "priority": "critical"
            }
        ]
    }

def test_map_systems_data(sample_systems_data):
    """Testa mapeamento de dados do SystemsForm."""
    result = DataMapper.map_systems_data(sample_systems_data)
    
    with check:
        assert len(result["systems"]) == 2, "Número incorreto de sistemas"
    
    # Verifica primeiro sistema
    with check:
        assert result["systems"][0]["system_id"] == "SYS001", "ID do sistema incorreto"
    with check:
        assert result["systems"][0]["name"] == "SAP ERP", "Nome do sistema incorreto"
    with check:
        assert result["systems"][0]["type"] == "ERP", "Tipo do sistema incorreto"
    
    # Verifica integrações
    with check:
        assert len(result["integrations"]) == 1, "Número incorreto de integrações"
    with check:
        assert result["integrations"][0]["source_system"] == "SYS001", "Sistema fonte incorreto"
    
    # Verifica requisitos técnicos
    with check:
        assert len(result["technical_requirements"]) == 2, "Número incorreto de requisitos"
    with check:
        assert result["technical_requirements"][0]["requirement_type"] == "performance", "Tipo de requisito incorreto"

def test_map_systems_data_missing_fields():
    """Testa mapeamento com campos faltando."""
    old_data = {
        "systems": [
            {
                "id": "SYS001",
                "name": "Basic System"
            }
        ]
    }
    
    result = DataMapper.map_systems_data(old_data)
    
    # Verifica sistema com campos faltando
    with check:
        assert len(result["systems"]) == 1, "Número incorreto de sistemas"
    with check:
        assert result["systems"][0]["system_id"] == "SYS001", "ID do sistema incorreto"
    with check:
        assert result["systems"][0]["name"] == "Basic System", "Nome do sistema incorreto"
    with check:
        assert result["systems"][0]["type"] == "", "Tipo do sistema deveria estar vazio"
    with check:
        assert result["systems"][0]["version"] == "", "Versão deveria estar vazia"
    with check:
        assert result["systems"][0]["modules"] == [], "Lista de módulos deveria estar vazia"
    
    # Verifica estruturas de acesso e disponibilidade
    with check:
        assert result["systems"][0]["access"] == {
            "type": "",
            "credentials": "",
            "permissions": []
        }, "Estrutura de acesso incorreta"
    with check:
        assert result["systems"][0]["availability"] == {
            "hours": "",
            "sla": "",
            "maintenance_window": ""
        }, "Estrutura de disponibilidade incorreta"
    
    # Verifica listas vazias para campos ausentes
    with check:
        assert result["integrations"] == [], "Lista de integrações deveria estar vazia"
    with check:
        assert result["technical_requirements"] == [], "Lista de requisitos deveria estar vazia" 

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

def test_map_data_form_data(sample_data_form_data):
    """Testa mapeamento de dados do DataForm."""
    result = DataMapper.map_data_form_data(sample_data_form_data)

    # Verifica inputs
    with check:
        assert len(result["data_inputs"]) == 1, "Número incorreto de inputs"
    
    input_data = result["data_inputs"][0]
    with check:
        assert input_data["input_id"] == "INP001", "ID do input incorreto"
    with check:
        assert input_data["name"] == "Customer Data", "Nome do input incorreto"
    with check:
        assert input_data["type"] == "structured", "Tipo do input incorreto"
    with check:
        assert len(input_data["fields"]) == 1, "Número incorreto de campos"
    
    # Verifica outputs
    with check:
        assert len(result["data_outputs"]) == 1, "Número incorreto de outputs"
    
    output_data = result["data_outputs"][0]
    with check:
        assert output_data["output_id"] == "OUT001", "ID do output incorreto"
    with check:
        assert output_data["name"] == "Processed Orders", "Nome do output incorreto"
    with check:
        assert output_data["type"] == "structured", "Tipo do output incorreto"
    
    # Verifica transformações
    with check:
        assert len(result["transformations"]) == 1, "Número incorreto de transformações"
    
    transform = result["transformations"][0]
    with check:
        assert transform["id"] == "TR001", "ID da transformação incorreto"
    with check:
        assert transform["name"] == "Data Validation", "Nome da transformação incorreto"
    
    # Verifica qualidade de dados
    with check:
        assert "validation_rules" in result["data_quality"], "Regras de validação ausentes"
    with check:
        assert "quality_metrics" in result["data_quality"], "Métricas de qualidade ausentes"
    with check:
        assert "error_handling" in result["data_quality"], "Tratamento de erros ausente"

def test_map_data_form_data_missing_fields():
    """Testa mapeamento com campos faltando."""
    old_data = {
        "data_inputs": [
            {
                "input_id": "INP001",
                "name": "Basic Input"
            }
        ],
        "data_outputs": [
            {
                "output_id": "OUT001",
                "name": "Basic Output"
            }
        ],
        "transformations": [
            {
                "transformation_id": "TR001",
                "name": "Basic Transform"
            }
        ]
    }

    result = DataMapper.map_data_form_data(old_data)

    # Verifica input com campos faltando
    with check:
        assert len(result["data_inputs"]) == 1, "Número incorreto de inputs"
    
    input_data = result["data_inputs"][0]
    with check:
        assert input_data["input_id"] == "INP001", "ID do input incorreto"
    with check:
        assert input_data["name"] == "Basic Input", "Nome do input incorreto"
    with check:
        assert input_data["type"] == "", "Tipo deveria estar vazio"
    with check:
        assert input_data["fields"] == [], "Lista de campos deveria estar vazia"
    
    # Verifica output com campos faltando
    with check:
        assert len(result["data_outputs"]) == 1, "Número incorreto de outputs"
    with check:
        assert result["data_outputs"][0]["output_id"] == "OUT001", "ID do output incorreto"
    
    # Verifica transformação com campos faltando
    with check:
        assert len(result["transformations"]) == 1, "Número incorreto de transformações"
    with check:
        assert result["transformations"][0]["id"] == "TR001", "ID da transformação incorreto"

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
                "responsibilities": ["Request validation", "Customer service"],
                "skills": ["CRM System", "Document validation"]
            },
            {
                "name": "System",
                "responsibilities": ["Automated processing"],
                "skills": ["Request processing", "Data update"]
            }
        ],
        "metrics": {
            "total_time": "12 minutes",
            "manual_time": "10 minutes",
            "automated_time": "2 minutes",
            "handoffs": 1
        }
    }

def test_map_steps_data(sample_steps_data):
    """Testa mapeamento de dados do StepsForm."""
    result = DataMapper.map_steps_data(sample_steps_data)
    
    # Verifica passos
    assert len(result["process_steps"]) == 2
    step1 = result["process_steps"][0]
    assert step1["step_id"] == "STEP001"
    assert step1["step_name"] == "Receive Request"
    assert step1["description"] == "Receive and validate customer request"
    assert step1["step_type"] == "manual"
    assert step1["assigned_role"] == "Analyst"
    assert step1["time_estimate"] == "10 minutes"
    assert len(step1["step_inputs"]) == 2
    assert len(step1["step_outputs"]) == 1
    assert len(step1["required_systems"]) == 1
    assert len(step1["execution_instructions"]) == 2
    assert len(step1["validation_points"]) == 2
    assert step1["dependencies"]["previous_steps"] == []
    assert step1["dependencies"]["next_steps"] == ["STEP002"]
    
    # Verifica fluxo
    assert result["process_flow"]["initial_step"] == "STEP001"
    assert result["process_flow"]["final_step"] == "STEP002"
    assert result["process_flow"]["parallel_execution"] == []
    assert result["process_flow"]["conditional_execution"] == []
    
    # Verifica papéis
    assert len(result["process_roles"]) == 2
    role1 = result["process_roles"][0]
    assert role1["role_name"] == "Analyst"
    assert len(role1["role_responsibilities"]) == 2
    assert len(role1["required_skills"]) == 2
    
    # Verifica métricas
    assert result["process_metrics"]["total_processing_time"] == "12 minutes"
    assert result["process_metrics"]["manual_processing_time"] == "10 minutes"
    assert result["process_metrics"]["automated_processing_time"] == "2 minutes"
    assert result["process_metrics"]["number_of_handoffs"] == 1

def test_map_steps_data_missing_fields():
    """Testa mapeamento com campos faltando."""
    old_data = {
        "steps": [
            {
                "id": "STEP001",
                "name": "Basic Step",
                "description": "Basic step description"
            }
        ]
    }
    
    result = DataMapper.map_steps_data(old_data)
    
    # Verifica passo com campos faltando
    assert len(result["process_steps"]) == 1
    step = result["process_steps"][0]
    assert step["step_id"] == "STEP001"
    assert step["step_name"] == "Basic Step"
    assert step["description"] == "Basic step description"
    assert step["step_type"] == "manual"
    assert step["assigned_role"] == ""
    assert step["time_estimate"] == ""
    assert step["step_inputs"] == []
    assert step["step_outputs"] == []
    assert step["required_systems"] == []
    assert step["execution_instructions"] == []
    assert step["validation_points"] == []
    assert step["dependencies"] == {
        "previous_steps": [],
        "next_steps": []
    }
    
    # Verifica valores default para campos ausentes
    assert result["process_flow"] == {
        "initial_step": "",
        "final_step": "",
        "parallel_execution": [],
        "conditional_execution": []
    }
    assert result["process_roles"] == []
    assert result["process_metrics"] == {
        "total_processing_time": "",
        "manual_processing_time": "",
        "automated_processing_time": "",
        "number_of_handoffs": 0
    } 

@pytest.fixture
def sample_risks_data():
    """Fixture com dados de exemplo do RisksForm."""
    return {
        "risks": [
            {
                "id": "RISK001",
                "description": "System downtime",
                "category": "technical",
                "probability": "medium",
                "impact": "high",
                "severity": "critical",
                "affected_areas": ["operations", "customer service"],
                "current_controls": [
                    "Backup systems",
                    "Monitoring alerts"
                ],
                "mitigation_plan": {
                    "actions": [
                        "Implement redundancy",
                        "Improve monitoring"
                    ],
                    "responsible": "IT Team",
                    "deadline": "2024-06-30",
                    "status": "in_progress"
                }
            },
            {
                "id": "RISK002",
                "description": "Data quality issues",
                "category": "data",
                "probability": "high",
                "impact": "medium",
                "severity": "high",
                "affected_areas": ["data processing"],
                "current_controls": [
                    "Data validation rules"
                ],
                "mitigation_plan": {
                    "actions": [
                        "Enhance validation",
                        "Implement data cleansing"
                    ],
                    "responsible": "Data Team",
                    "deadline": "2024-05-15",
                    "status": "planned"
                }
            }
        ],
        "risk_matrix": {
            "probability_levels": ["low", "medium", "high"],
            "impact_levels": ["low", "medium", "high"],
            "severity_mapping": {
                "high_high": "critical",
                "high_medium": "high",
                "medium_medium": "medium"
            }
        },
        "monitoring": {
            "frequency": "weekly",
            "responsible": "Risk Manager",
            "metrics": [
                "Number of active risks",
                "Mitigation effectiveness"
            ],
            "reporting": {
                "format": "dashboard",
                "recipients": ["management", "team_leads"]
            }
        },
        "contingency_plans": [
            {
                "risk_id": "RISK001",
                "trigger_conditions": ["System unavailable > 1 hour"],
                "actions": [
                    "Activate backup system",
                    "Notify stakeholders"
                ],
                "resources_needed": ["Backup infrastructure", "Communication channels"],
                "recovery_time_objective": "2 hours"
            }
        ]
    }

def test_map_risks_data(sample_risks_data):
    """Testa mapeamento de dados do RisksForm."""
    result = DataMapper.map_risks_data(sample_risks_data)
    
    # Verifica riscos
    assert len(result["identified_risks"]) == 2
    risk1 = result["identified_risks"][0]
    assert risk1["risk_id"] == "RISK001"
    assert risk1["description"] == "System downtime"
    assert risk1["risk_category"] == "technical"
    assert risk1["probability_level"] == "medium"
    assert risk1["impact_level"] == "high"
    assert risk1["severity_level"] == "critical"
    assert len(risk1["affected_areas"]) == 2
    assert len(risk1["existing_controls"]) == 2
    assert len(risk1["mitigation_strategy"]["planned_actions"]) == 2
    assert risk1["mitigation_strategy"]["responsible_party"] == "IT Team"
    
    # Verifica matriz de risco
    matrix = result["risk_assessment_matrix"]
    assert len(matrix["probability_scale"]) == 3
    assert len(matrix["impact_scale"]) == 3
    assert matrix["severity_calculation"]["high_high"] == "critical"
    
    # Verifica monitoramento
    monitoring = result["risk_monitoring"]
    assert monitoring["monitoring_frequency"] == "weekly"
    assert monitoring["responsible_party"] == "Risk Manager"
    assert len(monitoring["monitoring_metrics"]) == 2
    assert monitoring["reporting_config"]["report_format"] == "dashboard"
    
    # Verifica planos de contingência
    assert len(result["contingency_plans"]) == 1
    plan = result["contingency_plans"][0]
    assert plan["associated_risk"] == "RISK001"
    assert len(plan["trigger_events"]) == 1
    assert len(plan["response_actions"]) == 2
    assert len(plan["required_resources"]) == 2
    assert plan["recovery_target"] == "2 hours"

def test_map_risks_data_missing_fields():
    """Testa mapeamento com campos faltando."""
    old_data = {
        "risks": [
            {
                "id": "RISK001",
                "description": "Basic risk"
            }
        ]
    }
    
    result = DataMapper.map_risks_data(old_data)
    
    # Verifica risco com campos faltando
    assert len(result["identified_risks"]) == 1
    risk = result["identified_risks"][0]
    assert risk["risk_id"] == "RISK001"
    assert risk["description"] == "Basic risk"
    assert risk["risk_category"] == "general"
    assert risk["probability_level"] == "low"
    assert risk["impact_level"] == "low"
    assert risk["severity_level"] == "low"
    assert risk["affected_areas"] == []
    assert risk["existing_controls"] == []
    assert risk["mitigation_strategy"] == {
        "planned_actions": [],
        "responsible_party": "",
        "target_date": "",
        "status": "planned"
    }
    
    # Verifica valores default para campos ausentes
    assert result["risk_assessment_matrix"] == {
        "probability_scale": ["low", "medium", "high"],
        "impact_scale": ["low", "medium", "high"],
        "severity_calculation": {}
    }
    assert result["risk_monitoring"] == {
        "monitoring_frequency": "monthly",
        "responsible_party": "",
        "monitoring_metrics": [],
        "reporting_config": {
            "report_format": "",
            "report_recipients": []
        }
    }
    assert result["contingency_plans"] == [] 

@pytest.fixture
def sample_documentation_data():
    """Fixture com dados de exemplo do DocumentationForm."""
    return {
        "process_documentation": {
            "version": "1.0",
            "last_update": "2024-01-15",
            "author": "John Doe",
            "status": "draft",
            "sections": [
                {
                    "id": "SEC001",
                    "title": "Overview",
                    "content": "Process overview content",
                    "attachments": [
                        {
                            "name": "diagram.png",
                            "type": "image",
                            "url": "/attachments/diagram.png",
                            "description": "Process flow diagram"
                        }
                    ]
                },
                {
                    "id": "SEC002",
                    "title": "Detailed Steps",
                    "content": "Step by step instructions",
                    "attachments": []
                }
            ]
        },
        "training_materials": [
            {
                "id": "TRN001",
                "title": "User Guide",
                "type": "document",
                "format": "PDF",
                "url": "/training/user_guide.pdf",
                "target_audience": ["end users"],
                "version": "1.0"
            },
            {
                "id": "TRN002",
                "title": "Video Tutorial",
                "type": "video",
                "format": "MP4",
                "url": "/training/tutorial.mp4",
                "target_audience": ["new employees"],
                "version": "1.1"
            }
        ],
        "change_history": [
            {
                "date": "2024-01-15",
                "author": "John Doe",
                "type": "creation",
                "description": "Initial documentation"
            },
            {
                "date": "2024-01-20",
                "author": "Jane Smith",
                "type": "update",
                "description": "Added video tutorial"
            }
        ],
        "references": [
            {
                "title": "Company Policy",
                "type": "internal",
                "url": "/policies/process_policy.pdf",
                "description": "Related company policies"
            },
            {
                "title": "Regulatory Guidelines",
                "type": "external",
                "url": "https://regulations.gov/guidelines",
                "description": "Industry regulations"
            }
        ],
        "review_cycle": {
            "frequency": "quarterly",
            "last_review": "2024-01-10",
            "next_review": "2024-04-10",
            "reviewers": ["Process Owner", "Quality Team"]
        }
    }

def test_map_documentation_data(sample_documentation_data):
    """Testa mapeamento de dados do DocumentationForm."""
    result = DataMapper.map_documentation_data(sample_documentation_data)
    
    # Verifica documentação do processo
    doc = result["process_documentation"]
    assert doc["document_version"] == "1.0"
    assert doc["last_updated"] == "2024-01-15"
    assert doc["document_author"] == "John Doe"
    assert doc["document_status"] == "draft"
    assert len(doc["content_sections"]) == 2
    
    # Verifica seção da documentação
    section = doc["content_sections"][0]
    assert section["section_id"] == "SEC001"
    assert section["section_title"] == "Overview"
    assert len(section["section_attachments"]) == 1
    attachment = section["section_attachments"][0]
    assert attachment["file_name"] == "diagram.png"
    assert attachment["file_type"] == "image"
    
    # Verifica materiais de treinamento
    assert len(result["training_materials"]) == 2
    training = result["training_materials"][0]
    assert training["material_id"] == "TRN001"
    assert training["material_title"] == "User Guide"
    assert training["file_type"] == "document"
    assert training["file_format"] == "PDF"
    
    # Verifica histórico de alterações
    assert len(result["change_history"]) == 2
    change = result["change_history"][0]
    assert change["change_date"] == "2024-01-15"
    assert change["change_author"] == "John Doe"
    assert change["change_type"] == "creation"
    
    # Verifica referências
    assert len(result["references"]) == 2
    ref = result["references"][0]
    assert ref["reference_title"] == "Company Policy"
    assert ref["reference_type"] == "internal"
    
    # Verifica ciclo de revisão
    review = result["review_cycle"]
    assert review["review_frequency"] == "quarterly"
    assert review["last_review_date"] == "2024-01-10"
    assert len(review["review_team"]) == 2

def test_map_documentation_data_missing_fields():
    """Testa mapeamento com campos faltando."""
    old_data = {
        "process_documentation": {
            "version": "1.0",
            "sections": [
                {
                    "id": "SEC001",
                    "title": "Basic Section"
                }
            ]
        }
    }
    
    result = DataMapper.map_documentation_data(old_data)
    
    # Verifica documentação com campos faltando
    doc = result["process_documentation"]
    assert doc["document_version"] == "1.0"
    assert doc["last_updated"] == ""
    assert doc["document_author"] == ""
    assert doc["document_status"] == "draft"
    assert len(doc["content_sections"]) == 1
    
    section = doc["content_sections"][0]
    assert section["section_id"] == "SEC001"
    assert section["section_title"] == "Basic Section"
    assert section["section_content"] == ""
    assert section["section_attachments"] == []
    
    # Verifica valores default para campos ausentes
    assert result["training_materials"] == []
    assert result["change_history"] == []
    assert result["references"] == []
    assert result["review_cycle"] == {
        "review_frequency": "annual",
        "last_review_date": "",
        "next_review_date": "",
        "review_team": []
    } 