class ManifestService:
    def __init__(self, manifest: dict) -> None:
        self.manifest = manifest

    @property
    def version(self) -> str:
        return self.manifest.get("Response", "unknown").get("version", "unknown")

    @version.setter
    def version(self, new_version: str) -> None:
        if not isinstance(new_version, str):
            raise ValueError("Version must be a string")
        self.manifest["Response"]["version"] = new_version

    @property
    def mobile_world_content_paths(self) -> dict:
        return self.manifest.get("Response", {}).get("mobileWorldContentPaths", {})

    @mobile_world_content_paths.setter
    def mobile_world_content_paths(self, paths: dict) -> None:
        if not isinstance(paths, dict):
            raise ValueError("mobileWorldContentPaths must be a dictionary")
        self.manifest["Response"]["mobileWorldContentPaths"] = paths

    @property
    def json_world_component_content_paths(self) -> dict:
        return self.manifest.get("Response", {}).get(
            "jsonWorldComponentContentPaths", {}
        )

    @json_world_component_content_paths.setter
    def json_world_component_content_paths(self, paths: dict) -> None:
        if not isinstance(paths, dict):
            raise ValueError("jsonWorldComponentContentPaths must be a dictionary")
        self.manifest["Response"]["jsonWorldComponentContentPaths"] = paths

    def get_json_world_component_content_path(self, table_name: str, lang: str) -> str:
        if table_name not in self.json_world_component_content_paths[lang]:
            raise KeyError(f"{table_name} not found in jsonWorldComponentContentPaths")
        return self.json_world_component_content_paths[lang][table_name]

    def get_mobile_world_content_path(self, lang: str) -> str:
        if lang not in self.mobile_world_content_paths:
            raise KeyError(f"{lang} not found in mobileWorldContentPaths")
        return self.mobile_world_content_paths[lang]

    def json_world_component_content_path_toList(self, lang: str) -> list[str]:
        components = self.json_world_component_content_paths.get(lang, {})
        return [f"{key}: {value}" for key, value in components.items()]

    def json_world_component_content_keys_toList(self, lang: str) -> list[str]:
        return [
            x
            for x in self.manifest["Response"]["jsonWorldComponentContentPaths"]
            .get(lang, {})
            .keys()
        ]

    def json_world_component_content_values_toList(self, lang: str) -> list[str]:
        return [
            x
            for x in self.manifest["Response"]["jsonWorldComponentContentPaths"]
            .get(lang, {})
            .values()
        ]

    def json_world_component_content_paths_toTuple(self, lang: str) -> tuple:
        components = self.json_world_component_content_paths.get(lang, {})
        return tuple((key, value) for key, value in components.items())
