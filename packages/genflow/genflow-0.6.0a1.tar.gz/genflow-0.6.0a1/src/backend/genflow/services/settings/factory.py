from pathlib import Path
from genflow.services.settings.manager import SettingsService
from genflow.services.factory import ServiceFactory


class SettingsServiceFactory(ServiceFactory):
    def __init__(self):
        super().__init__(SettingsService)

    def create(self):
        # Here you would have logic to create and configure a SettingsService
        genflow_dir = Path(__file__).parent.parent.parent
        return SettingsService.load_settings_from_yaml(
            str(genflow_dir / "config.yaml")
        )
