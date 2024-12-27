from typing import List, Dict, Tuple

class DiagramValidator:
    """Validador para diagramas de processo."""
    
    @staticmethod
    def validate_diagram(nodes: List[Dict], edges: List[Dict]) -> Tuple[bool, List[str]]:
        """Valida o diagrama completo."""
        errors = []
        
        # Valida estrutura básica
        start_nodes = [n for n in nodes if n.get('type') == 'start']
        end_nodes = [n for n in nodes if n.get('type') == 'end']
        
        if not start_nodes:
            errors.append("O diagrama deve ter pelo menos um nó de início")
        elif len(start_nodes) > 1:
            errors.append("O diagrama deve ter apenas um nó de início")
            
        if not end_nodes:
            errors.append("O diagrama deve ter pelo menos um nó de fim")
        
        # Valida conexões
        node_ids = {n['id'] for n in nodes}
        for edge in edges:
            if edge['source'] not in node_ids:
                errors.append(f"Conexão inválida: nó fonte '{edge['source']}' não existe")
            if edge['target'] not in node_ids:
                errors.append(f"Conexão inválida: nó alvo '{edge['target']}' não existe")
        
        # Valida ciclos
        if DiagramValidator._has_cycles(nodes, edges):
            errors.append("O diagrama contém ciclos que podem causar loops infinitos")
        
        # Valida nós desconectados
        disconnected = DiagramValidator._find_disconnected_nodes(nodes, edges)
        if disconnected:
            errors.append(f"Nós desconectados encontrados: {', '.join(disconnected)}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def _has_cycles(nodes: List[Dict], edges: List[Dict]) -> bool:
        """Verifica se há ciclos no diagrama."""
        def dfs(node: str, visited: set, path: set) -> bool:
            visited.add(node)
            path.add(node)
            
            # Verifica todas as conexões saindo deste nó
            for edge in edges:
                if edge['source'] == node:
                    next_node = edge['target']
                    if next_node in path:
                        return True
                    if next_node not in visited:
                        if dfs(next_node, visited, path):
                            return True
            
            path.remove(node)
            return False
        
        visited = set()
        for node in nodes:
            if node['id'] not in visited:
                if dfs(node['id'], visited, set()):
                    return True
        return False
    
    @staticmethod
    def _find_disconnected_nodes(nodes: List[Dict], edges: List[Dict]) -> List[str]:
        """Encontra nós que não estão conectados ao fluxo principal."""
        connected = set()
        
        # Adiciona todos os nós que têm conexões
        for edge in edges:
            connected.add(edge['source'])
            connected.add(edge['target'])
        
        # Encontra nós desconectados
        all_nodes = {node['id'] for node in nodes}
        return list(all_nodes - connected) 