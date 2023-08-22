from helpers.logger import Log


class Model:
    def persist(self):
        from db.database import Database
        Database.insert(self)

    def update(self, updated_record: object, primary_key: str):
        from db.database import Database
        Log.info(f"Updating {self.__table__} record: {updated_record}")
        Log.info(f"\tUpdated model: {updated_record}")
        Database.update(existing_object=self, updated_object=updated_record, primary_key=primary_key)
