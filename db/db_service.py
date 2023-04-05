from sqlalchemy import create_engine

from settings import get_config

config = get_config()


class DBService:
    engine = None

    def create_engine(self):
        """
        Creates sqlalchemy db engine
        Returns:
            created engine
        """
        self.engine = create_engine(config.get("DB_URI"))
        return self.engine

    def dispose_engine(self):
        """
        Disposes engine
        """
        self.engine.dispose()


db_service = DBService()
