class MigrationLogger:
    def log_migration_step(self, step: str, status: str, details: Dict[str, Any]) -> None:
        """Registra passo da migração com detalhes."""
        self.logger.info(f"Migration step: {step}")
        self.logger.info(f"Status: {status}")
        self.logger.info(f"Details: {json.dumps(details, indent=2)}") 