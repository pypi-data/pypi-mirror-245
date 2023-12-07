# -*- coding: utf-8 -*-
# pylint: disable=C0114,C0116

from typing import Dict, Type
from delpinos.api.core.controllers.api_controller_abstract import ApiControllerAbstract
from delpinos.rabbitmq.api.controllers.enqueue_controller import (
    RabbitmqProducerApiController,
)


controllers: Dict[str, Type[ApiControllerAbstract]] = {
    "enqueue": RabbitmqProducerApiController,
}
