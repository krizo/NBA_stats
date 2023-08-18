from helpers.logger import Log


class Model:
    def persist(self):
        from db.database import Database
        Database.insert(self)

    def update(self, updated_record: object):
        from db.database import Database
        Log.info(f"Updating {self.__table__} record by id: {updated_record.id}")
        Log.info(f"\tUpdated model: {updated_record}")
        Database.update(self, updated_record)
