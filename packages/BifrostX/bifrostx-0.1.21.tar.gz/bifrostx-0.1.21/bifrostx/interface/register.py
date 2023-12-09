from pydantic import BaseModel
from .base import BaseInterface
from .profile import InterfaceProfile
from typing import Dict, List, Type, Union
from bifrostx.utils.logger import logger
from bifrostx.adapter.register import AdapterInfo
from bifrostx.core.data_model import ValidationError


class InterfaceInfo(BaseModel):
    module_name: str
    interface: Type[BaseInterface]
    profile: InterfaceProfile
    adapters: Dict[str, AdapterInfo] = {}

    def get_adapter_instance(
        self, adapter_name=None, instance_id=None
    ) -> BaseInterface:
        if not adapter_name:
            for adapter in self.adapters.values():
                if adapter.instance_configs:
                    if not instance_id:
                        instance_id = list(adapter.instance_configs.keys())[0]
                        return adapter.adapter(
                            adapter.instance_configs[instance_id],
                            instance_id=instance_id,
                        )
                    elif instance_id in adapter.instance_configs:
                        return adapter.adapter(
                            adapter.instance_configs[instance_id],
                            instance_id=instance_id,
                        )
            raise ValueError(f"未找到 Interface[{self.module_name}] 的实例")
        adapter_info = self.adapters.get(adapter_name)
        if not adapter_info:
            raise ValueError(
                f"未找到 Interface[{self.module_name}] 的 Adapter[{adapter_name}]"
            )
        if instance_id:
            instance_config = adapter_info.instance_configs.get(instance_id)
            if not instance_config:
                raise ValueError(
                    f"未找到 Interface[{self.module_name}] 的 Adapter[{adapter_name}] 的实例[{instance_id}]"
                )
            return adapter_info.adapter(instance_config, instance_id)
        else:
            instance_keys = list(adapter_info.instance_configs.keys())
            if not instance_keys:
                raise ValueError(
                    f"未找到 Interface[{self.module_name}] 的 Adapter[{adapter_name}] 的实例"
                )
            select_instance_id = instance_keys[0]
            return adapter_info.adapter(
                adapter_info.instance_configs[select_instance_id], select_instance_id
            )


class InterfaceRegister:
    interfaces: Dict[str, InterfaceInfo] = {}

    @classmethod
    def register(cls, module_name: str):
        try:
            profile = InterfaceProfile.load_by_module_name(module_name)
            interface = profile.load_enter_class()
            cls.interfaces[module_name] = InterfaceInfo(
                module_name=module_name, interface=interface, profile=profile
            )
            logger.info(f"Load Interface [{module_name}] Success")
        except ValidationError as ex:
            logger.warning(
                f"Load Interface [{module_name}] Error: {ex.errors()[0]['ctx']['error']}"
            )
        except Exception as ex:
            logger.warning(f"Load Interface [{module_name}] Error: {ex}")

    @classmethod
    def get_interfaces(cls) -> List[InterfaceInfo]:
        return list(cls.interfaces.values())

    @classmethod
    def get_interface(cls, module: Union[str, Type]) -> InterfaceInfo:
        module_name = module
        if not isinstance(module, str):
            module_name = module.__name__.split(".")[1]
        module_name = (
            module_name
            if len(module_name.split(".")) == 1
            else module_name.split(".")[1]
        )
        return cls.interfaces.get(module_name)
