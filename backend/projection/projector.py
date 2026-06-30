from typing import Dict, Any

class Projector:
    def project(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Projects data based on a configuration schema.
        Example Config:
        {
            "fields": [
                {"path": "full_name"},
                {"path": "primary_email", "from": "emails[0]"}
            ]
        }
        """
        if not config or "fields" not in config:
            return data # Return as is if no config

        result = {}
        for field_config in config.get("fields", []):
            path = field_config.get("path")
            from_path = field_config.get("from", path)
            
            if not path:
                continue
                
            # Basic path resolution (supports single level array index like emails[0])
            value = self._resolve_path(data, from_path)
            if value is not None:
                result[path] = value
                
        return result
        
    def _resolve_path(self, data: Dict[str, Any], path: str) -> Any:
        try:
            if "[" in path and path.endswith("]"):
                key, index_str = path.split("[")
                index = int(index_str[:-1])
                array_val = data.get(key, [])
                if isinstance(array_val, list) and len(array_val) > index:
                    return array_val[index]
                return None
            else:
                return data.get(path)
        except Exception:
            return None
