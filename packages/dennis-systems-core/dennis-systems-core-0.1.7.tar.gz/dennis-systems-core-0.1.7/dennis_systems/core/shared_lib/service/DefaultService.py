from typing import List, Optional

from django.db.models import Model

from dennis_systems.core.shared_lib.errors.NofFoundException import NotFoundException


class DefaultService:
    def list(self, limit: int, page: int) -> List[Model]:
        pass

    def save(self, item: Model) -> Model:
        return self.save_item(item)
        pass

    def delete(self, item: Model) -> Model:
        self.check_my(item)
        item.__class__.objects.filter(id=id).delete()
        pass

    def get(self, __id: int) -> Optional[Model]:
        res = self.get_class().objects.get(pk=__id)
        if res is None:
            raise NotFoundException()

        return res
        pass

    def save_item(self, item: Model) -> Model:
        item.save()
        return item

    def check_my(self, item: Model):
        return True

    def get_class(self):
        return Model.__class__
